from aiogram.fsm.state import State, StatesGroup


class LikeResponse(StatesGroup):
    response = State()


# class ProfileCreate(StatesGroup):
#     name = State()
#     surname = State()
#     gender = State()
#     age = State()
#     city = State()
#     ethnicity = State()
#     religion = State()
#     religious_level = State()
#     education = State()
#     job = State()
#     height = State()
#     weight = State()
#     marital_status = State()
#     has_children = State()
#     polygamy = State()
#     goal = State()
#
# class ProfileEdit(StatesGroup):
#     name = State()
#     surname = State()
#     gender = State()
#     age = State()
#     city = State()
#     ethnicity = State()
#     religion = State()
#     religious_level = State()
#     education = State()
#     job = State()
#     height = State()
#     weight = State()
#     marital_status = State()
#     has_children = State()
#     polygamy = State()
#     goal = State()


class Search(StatesGroup):
    search = State()
    message = State()
