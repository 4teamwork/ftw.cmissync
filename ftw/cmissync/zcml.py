from zope.interface import Interface
from zope import schema
from zope.component.zcml import utility
from ftw.cmissync.interfaces import ICMISRepo
from ftw.cmissync.repo import CMISRepo


class IRepoDirective(Interface):
    """Directive which registers a CMIS Repository"""

    url = schema.URI(
        title=u"CMIS Provider URL",
        description=u"e.g. 'http://cmis.alfresco.com/cmisatom'.",
        required=True,
    )

    user = schema.TextLine(
        title=u"User",
        description=u"The username used to authenticate with the repository.",
        required=True,
    )

    password = schema.TextLine(
        title=u"Password",
        description=u"The password for the user used to authenticate with the "
                     "repository.",
        required=True,
    )

    repository_id = schema.ASCIILine(
        title=u"Repository ID",
        description=u"The id of the repository if multiple repositories are "
            "provided by the service. If no id is specified, the first "
            "repository will be used.",
        required=False,
        default=None,
    )

    document_root = schema.ASCIILine(
        title=u"Document Root",
        description=u"The path of the object in the repository corresponding "
                     "with the Plone site root",
        required=False,
        default='/'
    )


def repoDirective(_context, url, user, password, repository_id=None, 
                  document_root='/'):

    utility(_context,
            provides=ICMISRepo,
            component=CMISRepo(url, user, password,
                               repository_id=repository_id,
                               document_root=document_root),)
