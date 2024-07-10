from fastapi import Depends, FastAPI
from .routes import endpoints

app = FastAPI()

app.include_router(endpoints.router)