
### Description

The task is to create an application with an API (like Flask or FastAPI) that contains three endpoints and a background task processor.    
The application must allow users to converse with ChatGPT. The conversation history should be saved into the Redis database using the `session_id` key. When the user ends the conversation, he should be able to run a background task using a separate endpoint. The background task must save the dialog into a Google Doc. The user should also be able to get the status of the initiated task.   

### Deliverables

The main deliverable is a repository with the docker-compose file describing how to deploy the system locally (i.e., with `docker compose up`). 

The docker-compose must include the following services:

- Service with an API with endpoints described in the section below;
- Redis;

### **Background Task**

When the user posts a request with a session_id, the background processor must extract the corresponding dialog from the Redis database, create a new Google document (named by `session_id`), move it to the folder with dialogs, and write the prettified dialog into the document.
Please remember that it must be possible to send any number of tasks to the processing route at any time. You should manage them, not miss any, and have valid statuses for each task. You decide on the tools and architecture of the background processing approaches, status storage, API framework, libraries, and LLM.    

### API Endpoints

1. **Chatting – `/api/v1/chat`**    
    The POST endpoint aims to accept textual requests, query the OpenAI API (ChatGPT) using custom predesigned prompt to generate a response, save the utterance pair to redis and return the response.    

    Body Format:  
    `{"session_id": str, "user_text": str}`
    
    Response format:   
    `{"bot_text": str}`

2. **Write to Doc – `/api/v1/write_to_doc`**  
    The POST endpoint is aimed at accepting session identifiers and writing the corresponding dialog history to Google Docs.    

    Body Format:  
    `{"session_id": str}`

    Response format:  
    `{"task_id": str}`
    
3. **Status – `/api/v1/status/<task_id>`**  
    GET endpoint, which will accept the task ID and return its status. The task can have four possible statuses: pending, running, finished, or failed.    

    Response format:   
    `{"status": str}`

