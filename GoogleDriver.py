from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import io,os

def upload_basic(folder_id: str, file_content: bytes, file_name: str, mime_type: str):
    path_service_account_file = os.path.dirname(os.path.abspath(__file__)) +'/service_account_key.json'
    credentials = service_account.Credentials.from_service_account_file(path_service_account_file)

    scopes = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.photos.readonly'
    ]

    credentials = credentials.with_scopes(scopes)
    try:
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=mime_type)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    except HttpError as error:
        print(f'An error occurred: {error}')
        file = None
    return file.get('id')
