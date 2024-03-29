import os
from time import sleep,localtime
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from collections import namedtuple
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

CLIENT_FILE = os.path.join("api_tokens\\client.json")
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ['https://mail.google.com/']
rpi_email = ""
aero_email = ""
gps_data_path = "\\gps_data\\"
circuit_data_path = "\\circuit_data\\"

def main():
    print("Email being drafted...")
    message,subject = draft()
    print("Email successfully created, attempting to send...",end="")

    send(message,subject)
    print(" Sent.")

def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    creds = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    token_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)
        # with open(os.path.join(working_dir, token_dir, token_file), 'rb') as token:
        #   cred = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

def draft():
    now = datetime.date.today()
    now = now.strftime("%m/%d/%y")
    subject = "Daily Report for " + now
    message = ""

    return message,subject

def send(body=None,subject=None):

    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

    try:
        
        message = EmailMessage()

        message.set_content(body)

        message['To'] = aero_email,"camgilrein@gmail.com"
        message['From'] = rpi_email
        message['Subject'] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message

if __name__ == "__main__":
    main()