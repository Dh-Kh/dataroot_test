from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from ..dependencies import (verifier, backend, SessionData, cookie)
from uuid import uuid4, UUID
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

router = APIRouter()

"""write docs for each endpoint"""

@router.post("/api/v1/create_session/{session_data}")
async def create_session(session_data: str, response: Response):
    
    session = uuid4()
    
    data = SessionData(session_data=session_data)
    
    await backend.create(session, data)
    
    cookie.attach_to_response(response, session)
    
    return JSONResponse(content={
        "user session": data
        }, status_code=200)
    
@router.post("/api/v1/delete_session")
async def delete_session(response: Response, session_uuid: UUID = Depends(cookie)):
    
    await backend.delete(session_uuid)
    
    cookie.delete_from_response(response)
    
    return JSONResponse(content={
        "result": "Session has been deleted!"
        }, status_code=204)

@router.post("/api/v1/chat")
async def chat(text: str, session_data: SessionData = Depends(verifier)):
    
    """
    The API route to communicate with the ChatGPT. The chat history for different session IDs must be stored in the
    Redis database.

    :param session_id: str
        Session identifier to keep track of the conversation.
    :param text: str
        User input text

    :return: bot response
    """

    return {"bot_text": ...}, 200


@router.post("/api/v1/write_to_doc")
def write_to_doc(session_id: str):
    """
    Accepts request and launches a task to write the conversation history with the given identifier to the Google Docs.

    :return: task_id of the background task that was started
    """

    return {"task_id": ...}, 200


@router.get("/api/v1/status/<task_id>")
def status(task_id: str):
    """
    Check the status of the background task. It should receive a task_id and return the status of the task. The task
    can have four possible statuses: pending, running, finished, or failed.

    :param task_id: str

    :return: status of the background task (pending, running, finished, or failed)
    """

    return {"status": ...}, 200


@router.get("/-/healthy/")
def healthy():
    return {}, 200
