import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json'):
        creds = Credentials.from_authorized_user_file(
            r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\Drive_Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(r'C:\Users\huzai\PycharmProjects\Python-projects-1\Google\token3.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        response = service.files().list(q="name='Hexzdrivefolder' and mimeType='application/vnd.google-apps.folder'",
                                        spaces='drive').execute()

        if not response['files']:
            file_metadata = {
                "name": "Hexzdrivefolder",
                "mimeType": "application/vnd.google-apps.folder",
            }

            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']

        file_metadata = {
            "name": "Passwords.txt",
            "parents": [folder_id]
        }

        file_path = r"C:\Users\huzai\PycharmProjects\Python-projects-1\NewPasswords.txt"
        media = MediaFileUpload(file_path)
        upload_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file ID: {upload_file.get('id')} & name {file_metadata.get('name')}")

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == "__main__":
    main()
