from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

def upload_basic(folder_id :str,fileName : str,mimeType : str):
    credentials = service_account.Credentials.from_service_account_file('service_account_key.json')

    scopes = ['https://www.googleapis.com/auth/drive.readonly','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.appdata','https://www.googleapis.com/auth/drive.metadata','https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.photos.readonly']

    credentials = credentials.with_scopes(scopes)
    try:
        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {
            "name": fileName,
            "parents": [folder_id]
            }
        media = MediaFileUpload(fileName, mimetype=mimeType)
        file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
        )
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
    return file.get("id")

if __name__ == "__main__":
    folder_id = '1J8AiSCoskkOP6GXAPi1lgV-oPnhgfSHv'
    fileName="requirements.txt"
    mimeType='text/plain'
    upload_basic(folder_id,fileName,mimeType)