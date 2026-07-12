import os
import json
import io

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import (
    MediaIoBaseUpload,
    MediaIoBaseDownload
)

SCOPES = ["https://www.googleapis.com/auth/drive"]


# --------------------------------------------------
# Google Drive Service
# --------------------------------------------------
def get_drive_service():

    credentials_json = os.environ.get("GOOGLE_CREDENTIALS")

    if not credentials_json:
        raise Exception(
            "GOOGLE_CREDENTIALS environment variable is not set."
        )

    try:
        credentials_info = json.loads(credentials_json)
    except json.JSONDecodeError:
        raise Exception(
            "GOOGLE_CREDENTIALS is not valid JSON."
        )

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


# --------------------------------------------------
# Get Google Drive Folder ID
# --------------------------------------------------
def get_folder_id():

    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")

    if not folder_id:
        raise Exception(
            "GOOGLE_DRIVE_FOLDER_ID environment variable is not set."
        )

    return folder_id


# --------------------------------------------------
# List Templates
# --------------------------------------------------
def list_templates():

    service = get_drive_service()

    folder_id = get_folder_id()

    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed=false",
        fields="files(id,name,mimeType,modifiedTime)"
    ).execute()

    return results.get("files", [])


# --------------------------------------------------
# Upload Template
# --------------------------------------------------
def upload_template(file_stream, filename):

    service = get_drive_service()

    folder_id = get_folder_id()

    media = MediaIoBaseUpload(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        resumable=True
    )

    metadata = {
        "name": filename,
        "parents": [folder_id]
    }

    file = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name"
    ).execute()

    return file


# --------------------------------------------------
# Download Template
# --------------------------------------------------
def download_template(file_id, output_path):

    service = get_drive_service()

    request = service.files().get_media(fileId=file_id)

    with open(output_path, "wb") as file:

        downloader = MediaIoBaseDownload(file, request)

        done = False

        while not done:
            status, done = downloader.next_chunk()

    return output_path


# --------------------------------------------------
# Delete Template
# --------------------------------------------------
def delete_template(file_id):

    service = get_drive_service()

    service.files().delete(
        fileId=file_id
    ).execute()

    return True


# --------------------------------------------------
# Get Single File Details
# --------------------------------------------------
def get_template(file_id):

    service = get_drive_service()

    file = service.files().get(
        fileId=file_id,
        fields="id,name,mimeType,modifiedTime"
    ).execute()

    return file


# --------------------------------------------------
# Test Connection
# --------------------------------------------------
def test_connection():

    try:
        files = list_templates()

        return {
            "status": "success",
            "template_count": len(files),
            "templates": files
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }