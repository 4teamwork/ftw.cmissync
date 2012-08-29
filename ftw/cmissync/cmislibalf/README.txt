cmislibalf 0.3.1
http://code.google.com/p/cmislib-alfresco-extension/

Aspects are an essential tool to model metadata in Alfresco. The CMIS 
specification does not define aspects or something similar, but it defines 
several extension points. Alfresco uses these extensions point to send aspect 
data back and forth between a CMIS client and the server.

CMIS extensions are XML fragments placed in different parts of a CMIS object. 
The Alfresco aspect fragments are documented on the Alfresco Wiki. So, 
theoretically, they are available to all CMIS clients out there including 
cmislib.

In reality, dealing with CMIS extensions isn't fun and can require quite a lot 
of code. cmislib does all the XML parsing for you but, since it doesn't know 
anything about aspects, it can't provide pretty interfaces.

That's where the "Alfresco cmislib Extension" steps in. It seamlessly merges 
aspect properties with object properties and provides interfaces to get, add 
and remove aspects.
