from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from loader import _

import app.filters.create_profile_filtres as filters
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileCreate
from database.models.user import UserModel
from database.services import Profile

from .profile import profile_command

from app.text import message_text as mt


# CREATE PROFILE
@dating_router.message(StateFilter(None), F.text == _(mt.KB_FILL_PROFILE_AGAIN))
@dating_router.message(StateFilter(None), filters.IsCreate())
async def _create_profile_command(message: types.Message, state: FSMContext, user: UserModel):
    kb = RegistrationFormKb.name(user)
    await message.answer(_(mt.ASK_NAME), reply_markup=kb)
    await state.set_state(ProfileCreate.name)


# NAME
@dating_router.message(StateFilter(ProfileCreate.name), F.text, filters.IsName())
async def _name(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(name=message.text)
    kb = RegistrationFormKb.surname(user)
    await message.answer(_(mt.ASK_SURNAME), reply_markup=kb)
    await state.set_state(ProfileCreate.surname)


# SURNAME
@dating_router.message(StateFilter(ProfileCreate.surname), F.text, filters.IsSurname())
async def _surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    kb = RegistrationFormKb.gender()
    await message.answer(_(mt.ASK_GENDER), reply_markup=kb)
    await state.set_state(ProfileCreate.gender)


# GENDER
@dating_router.message(StateFilter(ProfileCreate.gender), F.text, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(gender=message.text)
    kb = RegistrationFormKb.age(user)
    await message.answer(_(mt.ASK_AGE), reply_markup=kb)
    await state.set_state(ProfileCreate.age)


# AGE
@dating_router.message(StateFilter(ProfileCreate.age), F.text, filters.IsAge())
async def _age(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(age=message.text)
    kb = RegistrationFormKb.location(user)
    await message.answer(_(mt.ASK_CITY), reply_markup=kb)
    await state.set_state(ProfileCreate.city)


# CITY
@dating_router.message(StateFilter(ProfileCreate.city), F.text | F.location, filters.IsCity())
async def _city(
    message: types.Message,
    state: FSMContext,
    latitude: float | None,
    longitude: float | None,
    city: str | None,
    user: UserModel,
):
    if not (latitude or longitude):
        city = user.profile.city
        latitude = user.profile.latitude
        longitude = user.profile.longitude

    await state.update_data(
        city=city,
        latitude=latitude,
        longitude=longitude,
    )

    kb = RegistrationFormKb.ethnicity()
    await message.answer(_(mt.ASK_ETHNICITY), reply_markup=kb)
    await state.set_state(ProfileCreate.ethnicity)


# ETHNICITY
@dating_router.message(StateFilter(ProfileCreate.ethnicity), F.text, filters.IsEthnicity())
async def ethnicity(message: types.Message, state: FSMContext):
    await state.update_data(ethnicity=message.text)
    kb = RegistrationFormKb.religion()
    await message.answer(_(mt.ASK_RELIGION), reply_markup=kb)
    await state.set_state(ProfileCreate.religion)


# RELIGION
@dating_router.message(StateFilter(ProfileCreate.religion), F.text, filters.IsReligion())
async def _religion(message: types.Message, state: FSMContext):
    await state.update_data(religion=message.text)

    kb = RegistrationFormKb.religious_level()
    await message.answer(_(mt.ASK_RELIGIOUS_LEVEL), reply_markup=kb)
    await state.set_state(ProfileCreate.religious_level)


# RELIGIOUS LEVEL
@dating_router.message(StateFilter(ProfileCreate.religious_level), F.text, filters.IsReligiousLevel())
async def _religious_level(message: types.Message, state: FSMContext):
    await state.update_data(religious_level=message.text)

    kb = RegistrationFormKb.education()
    await message.answer(_(mt.ASK_EDUCATION), reply_markup=kb)
    await state.set_state(ProfileCreate.education)


# EDUCATION
@dating_router.message(StateFilter(ProfileCreate.education), F.text, filters.IsEducation())
async def _education(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(education=message.text)
    kb = RegistrationFormKb.job(user)
    await message.answer(_(mt.ASK_JOB), reply_markup=kb)
    await state.set_state(ProfileCreate.job)


# JOB
@dating_router.message(StateFilter(ProfileCreate.job), F.text, filters.IsJob())
async def _job(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(job=message.text)
    kb = RegistrationFormKb.height(user)
    await message.answer(_(mt.ASK_HEIGHT), reply_markup=kb)
    await state.set_state(ProfileCreate.height)


# HEIGHT
@dating_router.message(StateFilter(ProfileCreate.height), F.text, filters.IsHeight())
async def _height(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(height=message.text)
    kb = RegistrationFormKb.weight(user)
    await message.answer(_(mt.ASK_WEIGHT), reply_markup=kb)
    await state.set_state(ProfileCreate.weight)


# WEIGHT
@dating_router.message(StateFilter(ProfileCreate.weight), F.text, filters.IsWeight())
async def _weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    kb = RegistrationFormKb.marital_status()
    await message.answer(_(mt.ASK_MARITAL_STATUS), reply_markup=kb)
    await state.set_state(ProfileCreate.marital_status)


# MARITAL STATUS
@dating_router.message(StateFilter(ProfileCreate.marital_status), F.text, filters.IsMaritalStatus())
async def _marital_status(message: types.Message, state: FSMContext):
    await state.update_data(marital_status=message.text)
    kb = RegistrationFormKb.has_children()
    await message.answer(_(mt.ASK_HAS_CHILDREN), reply_markup=kb)
    await state.set_state(ProfileCreate.has_children)


# HAS CHILDREN
@dating_router.message(StateFilter(ProfileCreate.has_children), F.text, filters.IsHasChildren())
async def _has_children(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(has_children=message.text)
    kb = RegistrationFormKb.polygamy()
    await message.answer(_(mt.ASK_POLYGAMY), reply_markup=kb)
    await state.set_state(ProfileCreate.polygamy)


# POLYGAMY
@dating_router.message(StateFilter(ProfileCreate.polygamy), F.text, filters.IsPolygamy())
async def _polygamy(message: types.Message, state: FSMContext):
    await state.update_data(polygamy=message.text)
    kb = RegistrationFormKb.goal()
    await message.answer(_(mt.ASK_GOAL), reply_markup=kb)
    await state.set_state(ProfileCreate.goal)


# GOAL
@dating_router.message(StateFilter(ProfileCreate.goal), F.text, filters.IsGoal())
async def _goal(message: types.Message, state: FSMContext, session, user: UserModel):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    profile = normalize_profile_data(data)
    await Profile.create_or_update(
        session=session,
        id=user.id,
        **profile,
    )

    await session.refresh(user)
    await state.clear()

    await message.answer(_(mt.PRFILE_SUCCESSFULLY_CREATED), reply_markup=ReplyKeyboardRemove())
    await profile_command(message, user)


def normalize_profile_data(data: dict) -> dict:
    return {
        "gender": filters.gender_map.get(data.get("gender"), data.get("gender")),
        "marital_status": filters.marital_status_map.get(data.get("marital_status"), data.get("marital_status")),
        "education": filters.education_map.get(data.get("education"), data.get("education")),
        "goal": filters.goal_map.get(data.get("goal"), data.get("goal")),
        "religion": filters.religion_map.get(data.get("religion"), data.get("religion")),
        "religious_level": filters.religious_level_map.get(data.get("religious_level"), data.get("religious_level")),
        "has_children": filters.yes_no_map.get(data.get("has_children"), data.get("has_children")),
        "polygamy": filters.yes_no_map.get(data.get("polygamy"), data.get("polygamy")),
        "name": data.get("name"),
        "surname": data.get("surname"),
        "age": int(data.get("age")),
        "city": data.get("city"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "height": int(data.get("height")),
        "weight": int(data.get("weight")),
        "ethnicity": data.get("ethnicity"),
        "job": data.get("job"),
    }