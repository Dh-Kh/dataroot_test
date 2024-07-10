from typing import Any, Sequence, Union
import redis
import json

class RedisConnector(object):
    
    def __init__(self):
        self._redis_instance = redis.Redis(host='localhost', 
                                           port=6379, 
                                           password=12345)

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
        