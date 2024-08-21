from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(chat_router)


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()
