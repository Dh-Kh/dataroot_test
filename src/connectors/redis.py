from typing import Any, Sequence, Union
from dotenv import load_dotenv
import redis
import json
import os

load_dotenv()

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_HOST = os.getenv("REDIS_HOST")

class RedisConnector(object):
    
    def __init__(self):
        
        self._redis_instance = redis.Redis(host=REDIS_HOST, 
                                           port=REDIS_PORT, 
                                           password=REDIS_PASSWORD)

    def insert_into_redis(self, session_data: str, stored_data: Union[Sequence, Any]) -> None:
        if self._redis_instance.exists(session_data):
            
            existing_data = json.loads(self._redis_instance.get(session_data).decode())

            if not isinstance(existing_data, list):
                existing_data = [existing_data]
            else:
                existing_data.extend(stored_data)
            
            self._redis_instance.set(session_data, json.dumps(existing_data))
            
        else:
            self._redis_instance.mset({
                session_data: json.dumps(stored_data)
            })
    
    def get_from_redis(self, session_data: str) -> Union[Sequence, Any]:
        data = self._redis_instance.get(session_data)
        
        if not data:
            return 
        
        return json.loads(data.decode())
    
    def get_task_status(self, task_id: str) -> Union[str, Any]:
        
        data = self._redis_instance.get(task_id)
        
        if not data:
            return
        
        return json.loads(data.decode())

    def set_task_status(self, task_id: str, status: str) -> None:
        self._redis_instance.set(task_id, status)
        
        
        