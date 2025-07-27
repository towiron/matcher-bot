from aiogram import types
from aiogram.filters.state import StateFilter

from app.routers import dating_router
from app.states.default import ProfileCreate
from app.text import message_text as mt

@dating_router.message(StateFilter(ProfileCreate.name))
async def _incorrect_name(message: types.Message):
    """Ошибка фильтра имени"""
    await message.answer(mt.INVALID_LONG_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.surname))
async def _incorrect_surname(message: types.Message):
    """Ошибка фильтра фамилии"""
    await message.answer(mt.INVALID_LONG_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.gender))
async def _incorrect_gender(message: types.Message):
    """Ошибка фильтра гендера"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.age))
async def _incorrect_age(message: types.Message):
    """Ошибка фильтра возраста"""
    await message.answer(mt.INVALID_AGE)


@dating_router.message(StateFilter(ProfileCreate.city))
async def _incorrect_city(message: types.Message):
    """Ошибка фильтра города"""
    await message.answer(mt.INVALID_CITY_RESPONSE)


@dating_router.message(StateFilter(ProfileCreate.ethnicity))
async def _incorrect_ethnicity(message: types.Message):
    """Ошибка фильтра национальности"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.religion))
async def _incorrect_religion(message: types.Message):
    """Ошибка фильтра религии"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.religious_level))
async def _incorrect_religious_level(message: types.Message):
    """Ошибка фильтра религии"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.education))
async def _incorrect_education(message: types.Message):
    """Ошибка фильтра образование"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.job))
async def _incorrect_job(message: types.Message):
    """Ошибка фильтра работа"""
    await message.answer(mt.INVALID_LONG_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.height))
async def _incorrect_height(message: types.Message):
    """Ошибка фильтра рост"""
    await message.answer(mt.INVALID_HEIGHT)

@dating_router.message(StateFilter(ProfileCreate.weight))
async def _incorrect_weight(message: types.Message):
    """Ошибка фильтра вес"""
    await message.answer(mt.INVALID_WEIGHT)

@dating_router.message(StateFilter(ProfileCreate.marital_status))
async def _incorrect_marital_status(message: types.Message):
    """Ошибка фильтра национальности"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.has_children))
async def _incorrect_has_children(message: types.Message):
    """Ошибка фильтра о наличии детей"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.polygamy))
async def _incorrect_polygamy(message: types.Message):
    """Ошибка фильтра полигамности"""
    await message.answer(mt.INVALID_RESPONSE)

@dating_router.message(StateFilter(ProfileCreate.goal))
async def _incorrect_goal(message: types.Message):
    """Ошибка фильтра цели"""
    await message.answer(mt.INVALID_RESPONSE)