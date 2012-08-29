# Plone type to CMIS type mapping
# Maps a Plone type to a 3-tuple (CMIS type, field mapping, Alfresco aspects)

TYPE_FIELD_MAPPINGS = {

    'Folder': ('cmis:folder',
               {
        'title': 'cm:title',
        'description': 'cm:description',
    },
    [u'P:cm:titled',]),

    'Image': ('cmis:document',{
        'title': 'cm:title',
        'description': 'cm:description',
    },
    [u'P:cm:titled']),
    
}
