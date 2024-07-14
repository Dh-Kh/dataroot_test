from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from connectors.redis_connector import RedisConnector
from typing import Type
from pathlib import Path
import os
import pickle

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

GOOGLE_SCOPES = os.getenv("GOOGLE_SCOPES")



class Writer(object):
    
    def __init__(self, session_data: str):
        self.session_data = session_data
     
    def write_to_doc(self, redis_instance: Type[RedisConnector]) -> None:
        
        creds = None 
        
        file_path = Path(__file__).parent.parent / "token.pickle"
        
        if os.path.exists(file_path):
        
            with open(file_path, 'rb') as token:
                creds = pickle.load(token)
                
        else:
            
            cred_path = Path(__file__).parent.parent / "credentials.json"
            
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, GOOGLE_SCOPES)
            
            creds = flow.run_local_server(port=0)
            
            with open(file_path, 'wb') as token:
                pickle.dump(creds, token)
        
        try:
            
            service = build("docs", "v1", credentials=creds)
            
            chat_history = redis_instance.get_from_redis(self.session_data)

            if not chat_history:
                raise ValueError("Chat history is empty")
            
            doc = service.documents().create(body={
                'title': f"Chat History for {self.session_data}"
            }).execute()
            
            document_id = doc['documentId']

            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,  
                        },
                        'text': str(chat_history)  
                    }
                }
            ]

            service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
            
        except HttpError as e:
            print(e)
            
