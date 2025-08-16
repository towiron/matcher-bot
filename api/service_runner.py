from typing import AsyncGenerator, Annotated

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import Depends

from bot.database.connect import async_session
from bot.database.services import City, Ethnicity, Religion
from bot.database.services import MaritalStatus
from sqlalchemy.ext.asyncio import AsyncSession


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

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@app.get("/profile", response_class=HTMLResponse)
async def profile_page():
    with open("frontend/profile_page.html", "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        return content

@app.get("/cities")
async def cities_list(session: Annotated[AsyncSession, Depends(get_session)]):
    cities = await City.get_all(session)
    return [
        {
            "id": city.id,
            "uz": city.uz,
            "ru": city.ru,
            "en": city.en,
        }
        for city in cities
    ]

@app.get("/ethnicities")
async def ethnicities_list(session: Annotated[AsyncSession, Depends(get_session)]):
    ethnicities = await Ethnicity.get_all(session)
    return [
        {
            "id": ethnicity.id,
            "uz_male": ethnicity.uz_male,
            "uz_female": ethnicity.uz_female,
            "ru_male": ethnicity.ru_male,
            "ru_female": ethnicity.ru_female,
            "en_male": ethnicity.en_male,
            "en_female": ethnicity.en_female,
        }
        for ethnicity in ethnicities
    ]

@app.get("/religions")
async def religions_list(session: Annotated[AsyncSession, Depends(get_session)]):
    religions = await Religion.get_all(session)
    return [
        {
            "id": religion.id,
            "uz": religion.uz,
            "ru": religion.ru,
            "en": religion.en,
        }
        for religion in religions
    ]

@app.get("/marital_statuses")
async def marital_statuses_list(session: Annotated[AsyncSession, Depends(get_session)]):
    statuses = await MaritalStatus.get_all(session)
    return [
        {
            "id": status.id,
            "uz_male": status.uz_male,
            "uz_female": status.uz_female,
            "ru_male": status.ru_male,
            "ru_female": status.ru_female,
            "en_male": status.en_male,
            "en_female": status.en_female,
        }
        for status in statuses
    ]


@app.get("/filter", response_class=HTMLResponse)
async def filter_page():
    with open("frontend/filter_page.html", "r", encoding="utf-8") as f:
        content = f.read()
        content = content.replace('href="styles.css"', 'href="/static/styles.css"')
        return content