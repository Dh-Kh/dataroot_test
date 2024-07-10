from fastapi import APIRouter
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
import os

load_dotenv()

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

router = APIRouter()

@router.post("/api/v1/chat")
def chat(session_id: str, text: str):
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
