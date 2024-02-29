from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import os
import io


def upload_basic(folder_id: str, file_content: bytes, file_name: str, mime_type: str):
    # Load service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        "service_account_key.json"
    )

    # Define required scopes
    scopes = ["https://www.googleapis.com/auth/drive"]

    # Assign required scopes to credentials
    credentials = credentials.with_scopes(scopes)

    try:
        # Build Drive API service
        service = build("drive", "v3", credentials=credentials)

        # Prepare file metadata
        file_metadata = {"name": file_name, "parents": [folder_id]}

        # Create a media object for file upload
        media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type)

        # Upload file to Google Drive
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
