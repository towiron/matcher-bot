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

@app.get("/fill_profile", response_class=HTMLResponse)
async def index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        content = content.replace('src="script.js"', 'src="/static/script.js"')
        return content

@app.post("/api/profile/create")
async def submit_profile(request: Request):
    data = await request.json()
    print("Получена анкета:", data)
    return {"success": True}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)