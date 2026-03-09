import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")

    if not name:
        try:
            body = req.get_json()
            name = body.get("name")
        except:
            pass

    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Hello! Pass a name in the query string.",
            status_code=200
        )


def main():
    storage_key = require_env(STORAGE_CONNECTION)
    container_name = "data"
    container_dir = "pdf"

    data_dir = Path("./data/pdf")

    blob_service = BlobServiceClient.from_connection_string(storage_key)
    container_client = blob_service.get_container_client(container_name)

    for filename in os.listdir(data_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        # Blob name includes the directory prefix
        blob_client = container_client.get_blob_client(f"{container_dir}/{filename}")

        file_path = data_dir / filename   # Full path to the PDF file

        with open(file_path, "rb") as data:
            # NOTE: Will create `container_dir` is not exists
            blob_client.upload_blob(data, overwrite=True)
    
        print("Upload complete.")
