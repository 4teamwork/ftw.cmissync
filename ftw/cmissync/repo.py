from ftw.cmissync import cmislibalf
from cmislib import CmisClient
from ftw.cmissync.interfaces import ICMISRepo
from zope.interface import implements


class CMISRepo(object):
    implements(ICMISRepo)
    
    def __init__(self, url, user, password, repository_id=None,
                 document_root='/'):

        self.client = CmisClient(url, user, password)
        if not repository_id:
            self.repo = self.client.getDefaultRepository()
        else:
            self.repo = self.client.getRepository(repository_id)
        self.docroot = self.repo.getObjectByPath(document_root)

    def docroot_path(self):
        paths = self.docroot.getPaths()
        if paths:
            return paths[0]
        return None
