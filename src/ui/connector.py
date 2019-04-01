from __future__ import print_function
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import messageSender

# If modifying these scopes, delete the file config/token.pickle.
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

class GmailConnector:
    def __init__(self, messageSender):
        self._mailFrom = None
        self.sender = messageSender
        self.send_messages = []

        creds = None
        # The file config/token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('configs/token.pickle'):
            with open('configs/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'configs/credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('configs/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.gmail = build('gmail', 'v1', credentials=creds)

    @property
    def mailFrom(self):
        return self._mailFrom

    @mailFrom.setter
    def mailFrom(self, value):
        self._mailFrom = value
    
    async def get_labels(self, label):
        results = self.gmail.users().labels().list(userId='me', labelIds=label).execute()
        labels = results.get('labels', [])
        return labels

    async def get_message(self, msg_id):
        message = self.gmail.users().messages().get(userId='me', id=msg_id).execute()
        # messages = response.get('messages', [])
        return json.dumps(message)

    async def get_list_messages(self, count, label):
        response = self.gmail.users().messages().list(userId='me', maxResults=count, labelIds=label).execute()
        messages = response.get('messages', [])
        return messages

    def delete_msg(self, id):
        self.gmail.users().messages().delete(userId='me', id=id).execute()

    def send_message(self, userId, message):
        self.send_messages.append(message)
        self.sender.sendMessage(self.gmail, userId, message)

if __name__ == '__main__':
    connector = GmailConnector(messageSender=messageSender)
    connector.mailfFrom = 'bogdanovsi884@gmail.com'
    mailTo = 'freekerrr@gmail.com'
    msg = messageSender.CreateMessageWithAttachment(connector.mailfFrom, mailTo, 'Python', "hello man Как дела", '', filename='README.md')
    connector.send_message('me', msg)