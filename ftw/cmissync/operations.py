from logging import getLogger
from zope.component import getUtility
from Products.CMFCore.interfaces import IFolderish
from plone.app.blob.interfaces import IATBlob
from plone.app.blob.utils import openBlob
from ftw.cmissync.interfaces import ICMISRepo
from cmislib.exceptions import ObjectNotFoundException
from Products.CMFCore.utils import getToolByName
from ftw.cmissync.config import TYPE_FIELD_MAPPINGS

logger = getLogger('ftw.cmissync')


class Delete(object):
    """Delete a CMIS object at the given path.
    """
    def __init__(self, path):
        self.path = path

    def __call__(self):
        rtool = getUtility(ICMISRepo)
        repo_obj_path = '%s/%s' % (rtool.docroot_path(), self.path)

        # Try to get the object
        try:
            doc = rtool.repo.getObjectByPath(repo_obj_path)
        except ObjectNotFoundException:
            doc = None
            logger.warning("Delete in CMIS repo failed. No object found at "
                           "'%s'." % repo_obj_path)

        if doc is not None:
            if hasattr(doc, 'deleteTree'):
                doc.deleteTree()
            else:
                doc.delete()


class Update(object):
    """Update or create the given Plone object in the CMIS repo.
    """
    def __init__(self, obj):
        self.obj = obj

    def __call__(self):
        portal_type = self.obj.portal_type
        rtool = getUtility(ICMISRepo)
        portal_url = getToolByName(self.obj, 'portal_url')
        obj_path = '/'.join(portal_url.getRelativeContentPath(self.obj))
        repo_obj_path = '%s/%s' % (rtool.docroot_path(), obj_path)

        # Check if there's already an object at the given path
        try:
            doc = rtool.repo.getObjectByPath(repo_obj_path)
        except ObjectNotFoundException:
            doc = None

        # Content does not exist, create it
        if doc is None:
            parent_path = '/'.join(obj_path.split('/')[:-1])
            repo_parent_path = '%s/%s' % (rtool.docroot_path(), parent_path)
            try:
                repo_parent = rtool.repo.getObjectByPath(repo_parent_path)
            except ObjectNotFoundException:
                # Parent is missing, do nothing
                return

            name = self.obj.getId()
            cmis_type = TYPE_FIELD_MAPPINGS[portal_type][0]

            # Create a folderish object
            if IFolderish.providedBy(self.obj):
                doc = repo_parent.createFolder(name, properties={
                    'cmis:name': name,
                    'cmis:objectTypeId': cmis_type,
                })
            # Create an object with a content stream
            elif IATBlob.providedBy(self.obj):
                blob_wrapper = self.obj.getBlobWrapper()
                doc = repo_parent.createDocument(
                    blob_wrapper.getFilename(),
                    properties={
                        'cmis:name': name,
                        'cmis:objectTypeId': cmis_type,
                    },
                    contentFile=openBlob(blob_wrapper.blob),
                    contentType=blob_wrapper.getContentType(),
                )

            if doc is None:
                return

            # Add aspects
            aspects = TYPE_FIELD_MAPPINGS[portal_type][2]
            for aspect in aspects:
                doc.addAspect(aspect)

        # Update properties
        props = {}
        for fieldname, propname in TYPE_FIELD_MAPPINGS[portal_type][1].items():
            field = self.obj.Schema().getField(fieldname)
            accessor = field.getAccessor(self.obj)
            value = accessor()
            if isinstance(value, str):
                value = value.decode('utf8')
            props[propname] = value
        doc.updateProperties(props)
        import pdb; pdb.set_trace( )


class Move(object):
    """Move an object given by it's path to a new location.
    """
    def __init__(self, obj_path, target_folder_path):
        self.obj_path = obj_path
        self.target_folder_path = target_folder_path

    def __call__(self):
        rtool = getUtility(ICMISRepo)
        o_path = '%s/%s' % (rtool.docroot_path(), self.obj_path)
        t_path = '%s/%s' % (rtool.docroot_path(), self.target_folder_path)

        # Try to get the source object and the target folder
        try:
            obj = rtool.repo.getObjectByPath(o_path)
            target = rtool.repo.getObjectByPath(t_path)
        except ObjectNotFoundException:
            obj = None
            target = None

        if obj is not None and target is not None:
            source = obj.getParent()
            obj.move(source, target)


class Rename(object):
    """Rename an object given by it's path
    """
    def __init__(self, old_path, new_name):
        self.old_path = old_path
        self.new_name = new_name

    def __call__(self):
        rtool = getUtility(ICMISRepo)
        o_path = '%s/%s' % (rtool.docroot_path(), self.old_path)
        # Try to get the source object and the target folder
        try:
            obj = rtool.repo.getObjectByPath(o_path)
        except ObjectNotFoundException:
            obj = None

        if obj is not None:
            obj.updateProperties({'cmis:name': self.new_name})
