import os
from datetime import datetime
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import json

API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_PATH = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH, scopes=SCOPES
)

drive_service = build(API_NAME, API_VERSION, credentials=credentials)

today_date = datetime.today().strftime('%d-%m-%Y')
folder_name = f'backup_{today_date}'

folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
folder = drive_service.files().create(body=folder_metadata, fields='id').execute()

current_folder = os.getcwd()
files = [f for f in os.listdir(current_folder) if os.path.isfile(os.path.join(current_folder, f))]

for file_name in files:
    file_metadata = {'name': file_name, 'parents': [folder['id']]}
    media = MediaFileUpload(os.path.join(current_folder, file_name), resumable=True)

    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Successfully uploaded: {file_name} (File ID: {file["id"]})')
    except HttpError as e:
        print(f'Error uploading {file_name}: {e}')

print(f'Upload completo! Os arquivos foram salvos na pasta: {folder_name} (ID: {folder["id"]})')