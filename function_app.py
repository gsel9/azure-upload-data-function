import azure.functions as func
from upload_pdf import app as fastapi_app

# Wrap FastAPI with Azure Functions
app = func.AsgiFunctionApp(
    app=fastapi_app,
    http_auth_level=func.AuthLevel.FUNCTION,  # Requires a function key to be sent with the request
)
