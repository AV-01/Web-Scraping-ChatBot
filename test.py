from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/documents']

# Add your service account file path
SERVICE_ACCOUNT_FILE = 'google-creds.json'

# Authenticate and construct service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=credentials)

# Replace 'DOCUMENT_ID' with the actual ID of your Google Doc
DOCUMENT_ID = '1VmGf6cu_DeplgjwzSiVuakIIkajq6H1i-p89ClGcqFU'

# Retrieve the document
document = service.documents().get(documentId=DOCUMENT_ID).execute()
print('The title of the document is: {}'.format(document.get('title')))

# Example: Insert text at the beginning of the document
requests = [
    {
        'insertText': {
            'location': {
                'index': 1,
            },
            'text': 'Hello, this is a test!\n'
        }
    }
]

result = service.documents().batchUpdate(
    documentId=DOCUMENT_ID, body={'requests': requests}).execute()
