from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import endpoints
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=None)

app.include_router(endpoints.router)

@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)