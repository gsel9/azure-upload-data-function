# NOTE:
- Fails due to no storage account
- Should prolly configure access to storage account via Functions by assigning a role to the Function resource

https://learn.microsoft.com/en-gb/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python

https://learn.microsoft.com/en-us/azure/azure-functions/scenario-scheduled-tasks?pivots=programming-language-python&tabs=linux

1. Create a resource group, a Function App and a Storage Account
2. Connect the function app tp a storage account
    - Enable system assigned identity in your function app (App > Identity) and save it.
    - Give storage access to your function app by assigning Storage Blob Data Owner, Storage Queue Data Contributor, and Storage Account Contributor roles via Managed Identity in Storage account IAM.
    - See [link](https://techcommunity.microsoft.com/blog/appsonazureblog/use-managed-identity-instead-of-azurewebjobsstorage-to-connect-a-function-app-to/3657606) for additional details 
3. Set Storage account credentials as env variables (Function App > Settings > Env variables)
    - Add AzureWebJobsStorage__accountName + name of storage account
    - Add AzureWebJobsStorage__credential + managedidentity
4. Pull .github/workflow into code repo and push to trigger GitHub actions for deployment
5. Test function in portal/programmatic
