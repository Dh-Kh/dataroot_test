from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import endpoints

app = FastAPI()

app.include_router(endpoints.router)

@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)