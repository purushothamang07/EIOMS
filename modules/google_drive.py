import os
import json
import io

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_drive_service():

    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")

    if not credentials_json:
        raise Exception("GOOGLE_CREDENTIALS variable not found")

    credentials_info = json.loads(credentials_json)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=SCOPES
    )

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return service


def list_templates():

    service = get_drive_service()

    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id,name)"
    ).execute()

    return results.get("files", [])


def upload_template(file_stream, filename):

    service = get_drive_service()

    folder_id = os.environ["GOOGLE_DRIVE_FOLDER_ID"]

    media = MediaIoBaseUpload(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    metadata = {
        "name": filename,
        "parents": [folder_id]
    }

    service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()


def delete_template(file_id):

    service = get_drive_service()

    service.files().delete(
        fileId=file_id
    ).execute()