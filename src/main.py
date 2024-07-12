from fastapi import FastAPI
from .routes import endpoints

app = FastAPI()

app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)