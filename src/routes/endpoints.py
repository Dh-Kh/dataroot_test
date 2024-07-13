from fastapi import APIRouter, Response, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI  
from utils.sessions import (verifier, backend, SessionData, cookie)
from utils.writer import Writer
from uuid import uuid4, UUID
from connectors.redis_connector import RedisConnector
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

router = APIRouter()

@router.post("/api/v1/create_session/{session_data}")
async def create_session(data: str, response: Response):
    
    session = uuid4()
    
    data = SessionData(data=data)
    
    await backend.create(session, data)
    
    cookie.attach_to_response(response, session)
    
    return JSONResponse(content={"user session": jsonable_encoder(data)}, status_code=200)

@router.post("/api/v1/delete_session")
async def delete_session(response: Response, session_uuid: UUID = Depends(cookie)):
    
    await backend.delete(session_uuid)
    
    cookie.delete_from_response(response)
    
    return JSONResponse(content={"result": "Session has been deleted!"}, status_code=204)

@router.get("/api/v1/user_info", dependencies=[Depends(cookie)])
async def user_info(session_data: SessionData = Depends(verifier)):
    
    return JSONResponse(
        content={"user_info": jsonable_encoder(session_data)}, 
        status_code=200
    )


@router.post("/api/v1/chat")
async def chat(text: str, session_data: SessionData = Depends(verifier)):

    """
    A temperature between 0.5 and 1.0 is a good balance between randomness and predictability.
    """
    
    redis_connector = RedisConnector()
        
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.5
    )
    
    prompt_template = PromptTemplate(
        input_variables=["history", "text"],
        template="""You are a helpful assistant. The following is the conversation history:
            {history}
            Human: {text}
            Assistant:"""
    )
        
        
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    
    chat_history = redis_connector.get_from_redis(session_data) or []
    
    chat_history.append({"role": "user", "data": text})
    
    model_answer = llm_chain.invoke({"history": chat_history, "text": text})["text"]
    
    chat_history.append({"role": "AI", "data": model_answer})
    
    redis_connector.insert_into_redis(session_data, chat_history)
    

    return JSONResponse(content={
        "AI TEXT": model_answer
        }, status_code=200)


@router.post("/api/v1/write_to_doc")
async def write_to_doc(session_data: str, background_task: BackgroundTasks):
    
    redis_connector = RedisConnector()
        
    writer = Writer(session_data=session_data)

    redis_connector.set_task_status(session_data, "pending")
    
    try:
        
        redis_connector.set_task_status(session_data, "running")

        background_task.add_task(writer.write_to_doc, redis_connector)
        
    except Exception as e:
        
        print(e)
        
        redis_connector.set_task_status(session_data, "failed")
        
        return JSONResponse(content={
            "task_id": "Not executed"
            }, status_code=500
        )
    
    redis_connector.set_task_status(session_data, "finished")
    
    return JSONResponse(content={
        "task_id": session_data
        }, status_code=200)



@router.get("/api/v1/status/<task_id>")
async def status(task_id: str):
    
    redis_connector = RedisConnector()

    status = redis_connector.get_task_status(task_id)
   
    return JSONResponse(content={
        "status": status
    }, status_code=200)



