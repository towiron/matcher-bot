from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from utils.logging import logger

app = FastAPI()

# Mount static files directory (for your CSS/JS files)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

allow_origins=["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,  # или ["*"] — для всех источников
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/profile", response_class=HTMLResponse)
async def index():
    with open("frontend/profile_page.html", "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        return content

@app.get("/filter", response_class=HTMLResponse)
async def index():
    with open("frontend/filter_page.html", "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        return content

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)