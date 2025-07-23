from aiogram import F, types
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

import app.filters.create_profile_filtres as filters
from app.keyboards.default.registration_form import RegistrationFormKb
from app.routers import dating_router
from app.states.default import ProfileCreate
from app.text import message_text as mt
from database.models.user import UserModel
from database.services import Profile

from .profile import profile_command


# ---< Create profile >---
@dating_router.message(StateFilter(None), F.text == "🔄")
@dating_router.message(StateFilter(None), filters.IsCreate())
async def _create_profile_command(message: types.Message, state: FSMContext):
    """Запускает процесс создания профиля пользователя.
    Также используется для пересоздания анкеты"""
    kb = RegistrationFormKb.gender()
    await message.answer(mt.GENDER, reply_markup=kb)
    await state.set_state(ProfileCreate.gender)


# ---< Gender >---
@dating_router.message(StateFilter(ProfileCreate.gender), F.text, filters.IsGender())
async def _gender(message: types.Message, state: FSMContext, gender: str):
    await state.update_data(gender=gender)

    kb = RegistrationFormKb.find_gender()
    await message.reply(
        text=mt.FIND_GENDER,
        reply_markup=kb,
    )

    await state.set_state(ProfileCreate.find_gender)


# ---< Find gender >---
@dating_router.message(StateFilter(ProfileCreate.find_gender), F.text, filters.IsFindGender())
async def _find_gender(
    message: types.Message, state: FSMContext, find_gender: str, user: UserModel
):
    await state.update_data(find_gender=find_gender)

    kb = RegistrationFormKb.photo(user)
    await message.reply(
        text=mt.PHOTO,
        reply_markup=kb,
    )

    await state.set_state(ProfileCreate.photo)


# ---< Photo >---
@dating_router.message(StateFilter(ProfileCreate.photo), filters.IsPhoto())
async def _photo(message: types.Message, state: FSMContext, user: UserModel):
    photo = (
        user.profile.photo
        if message.text in filters.leave_previous_tuple
        else message.photo[0].file_id
    )
    await state.update_data(photo=photo)

    kb = RegistrationFormKb.name(user)
    await message.reply(
        text=mt.NAME,
        reply_markup=kb,
    )
    await state.set_state(ProfileCreate.name)


# ---< Name >---
@dating_router.message(StateFilter(ProfileCreate.name), F.text, filters.IsName())
async def _name(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(name=message.text)

    kb = RegistrationFormKb.age(user)
    await message.reply(
        text=mt.AGE,
        reply_markup=kb,
    )
    await state.set_state(ProfileCreate.age)


# ---< Age >---
@dating_router.message(StateFilter(ProfileCreate.age), F.text, filters.IsAge())
async def _age(message: types.Message, state: FSMContext, user: UserModel):
    await state.update_data(age=message.text)

    kb = RegistrationFormKb.location(user)
    await message.reply(
        text=mt.CITY,
        reply_markup=kb,
    )

    await state.set_state(ProfileCreate.city)


# ---< City >---
@dating_router.message(StateFilter(ProfileCreate.city), F.text | F.location, filters.IsCity())
async def _city(
    message: types.Message, state: FSMContext, latitude: str, longitude: str, user: UserModel
):
    if not (latitude or longitude):
        city = user.profile.city
        latitude = user.profile.latitude
        longitude = user.profile.longitude
    else:
        city = message.text if message.text else "📍"

    await state.update_data(
        city=city,
        latitude=latitude,
        longitude=longitude,
    )

    kb = RegistrationFormKb.description(user)
    await message.reply(
        text=mt.DESCRIPTION,
        reply_markup=kb,
    )
    await state.set_state(ProfileCreate.description)


# ---< Description >---
@dating_router.message(StateFilter(ProfileCreate.description), F.text, filters.IsDescription())
async def _description(message: types.Message, state: FSMContext, user: UserModel, session):
    data = await state.get_data()
    description = (
        user.profile.description if message.text in filters.leave_previous_tuple else message.text
    )

    await Profile.create_or_update(
        session=session,
        id=message.from_user.id,
        gender=data["gender"],
        find_gender=data["find_gender"],
        photo=data["photo"],
        name=data["name"],
        age=int(data["age"]),
        city=data["city"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        description=description,
    )

    await state.clear()
    await session.refresh(user)
    await profile_command(message, user)
