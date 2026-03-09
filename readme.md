On your Storage Account:

Go to Access Control (IAM)
Click Add role assignment
Assign your Function App’s managed identity one of:

Storage Blob Data Contributor (upload/write)
Storage Blob Data Reader (read-only)


Scope: Storage Account or container


# TODO:
Any key–value pair you add under: 
Azure Portal → Function App → Configuration → Application settings 
is injected into your Function App’s environment at runtime.