from fastapi import APIRouter,  Request, Response
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from utils.writer import Writer
from connectors.redis_connector import RedisConnector
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter()

@router.post("/api/v1/create_session/{session_id}")
async def create_session(request: Request, session_id: str):
    
    request.session["session_id"] = session_id
    
    return JSONResponse(content={"user session": session_id}, status_code=200)

@router.post("/api/v1/delete_session")
async def delete_session(request: Request, response: Response):
    
    if "session_id" in request.session:

        del request.session["session_id"]
        
        response.status_code = 204
        
        return response
    
    else:
        
        return JSONResponse(content={"session_id": "Not found"}, status_code=404)
        

@router.get("/api/v1/session_info")
async def user_info(request: Request):
    
    session_id = request.session.get("session_id")

    if session_id:
    
        return JSONResponse(
            content={"session_info": session_id},
            status_code=200
        )
    
    else:
        
        return JSONResponse(
            content={"session_info": "Not found"},
            status_code=404
            )
    

@router.post("/api/v1/chat")
async def chat(user_text: str, request: Request):

    """
    A temperature between 0.5 and 1.0 is a good balance between randomness and predictability.
    """
    
    redis_connector = RedisConnector()
        
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
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
    
    session_id = request.session.get("session_id")
        
    if session_id:
        
        session_info = f"{session_id}_chat"

    
        chat_history = redis_connector.get_from_redis(session_info) or []
    
        chat_history.append({"role": "user", "data": user_text})
    
        model_answer = llm_chain.invoke({"history": chat_history, "text": user_text})["text"]
    
        chat_history.append({"role": "AI", "data": model_answer})
    
        redis_connector.insert_into_redis(session_info, chat_history)
    
        if model_answer:
            return JSONResponse(content={
                "bot_text": model_answer
            }, status_code=200)
   
    else:
        
        return JSONResponse(
            content={"session_info": "Not found"},
            status_code=404
        )



@router.get("/api/v1/write_to_doc")
async def write_to_doc(request: Request):
    
    session_id = request.session.get("session_id")
        
    if session_id:
        
        session_info = f"{session_id}_status"
        
        redis_connector = RedisConnector()
        
        writer = Writer(session_data=f"{session_id}_chat")

        redis_connector.set_task_status(session_info, "pending")
    
        try:
        
            redis_connector.set_task_status(session_info, "running")

            writer.write_to_doc(redis_connector)
        
        except Exception as e:
        
            print(e)
        
            redis_connector.set_task_status(session_info, "failed")
        
            return JSONResponse(content={
                "task_id": "Not executed"
            }, status_code=400)
                
    
        redis_connector.set_task_status(session_info, "finished")
    
        return JSONResponse(content={
            "task_id": session_info
        }, status_code=200)
    
    else:
        
        return JSONResponse(
            content={"session_info": "Not found"},
            status_code=404
        )



@router.get("/api/v1/status/<task_id>")
async def status(task_id: str):
    
    redis_connector = RedisConnector()

    status = redis_connector.get_task_status(task_id)
   
    if not status:
        return JSONResponse(
            content={"status": "Not found"},
            status_code=404
        )

    return JSONResponse(content={
        "status": status
    }, status_code=200)

