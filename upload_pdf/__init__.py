import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = FastAPI()


class InputArgs(BaseModel):
    container_name: str
    container_dir: str
    data_dir: str  # e.g. "./data/pdf"


def get_blob_service_client() -> BlobServiceClient:
    """
    Uses Managed Identity when deployed to Azure Functions.
    Uses developer credentials (Azure CLI login) when running locally.
    """
    # Reads env variables from Azure Functions portal
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    if not account_name:
        raise RuntimeError("STORAGE_ACCOUNT_NAME environment variable is not set")

    account_url = f"https://{account_name}.blob.core.windows.net"

    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=account_url, credential=credential)


@app.post("/upload_pdf")
async def upload_pdf(args: InputArgs):
    blob_service = get_blob_service_client()
    container = blob_service.get_container_client(args.container_name)
    filenames = [blob.name for blob in container.list_blobs()]
    return {"files": filenames}
    """
    try:
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            raise HTTPException(
                status_code=400, 
                detail=f"Local directory not found: {data_dir}"
            )

        blob_service = get_blob_service_client()
        container = blob_service.get_container_client(args.container_name)
        filenames = [blob.name for blob in container.list_blobs()]
        return {"files": filenames}

        # Ensure container exists
        try:
            container.create_container()
        except Exception:
            pass

        uploaded = []

        for filename in os.listdir(data_dir):
            if not filename.lower().endswith(".pdf"):
                continue

            blob_name = f"{args.container_dir}/{filename}"
            blob_client = container.get_blob_client(blob_name)

            with open(data_dir / filename, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)

            uploaded.append(blob_name)
        """
        return {"status": "ok", "uploaded": uploaded}

    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
