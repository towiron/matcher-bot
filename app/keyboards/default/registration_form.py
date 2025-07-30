from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardMarkup

from data.config import WEB_APP_URL
from database.models.profile import ProfileModel
from database.models.user import UserModel
from loader import _

from .base import del_kb
from .kb_generator import simple_kb_generator as kb_gen
from app.text import message_text as mt

def create_profile_kb(language: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_(mt.CREATE_PROFILE),
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/profile?language={language}")
                )
            ]
        ],
        resize_keyboard=True
    )
    return kb

def profile_menu_kb(language: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=_(mt.KB_FILL_PROFILE_AGAIN),
                    web_app=WebAppInfo(url=f"{WEB_APP_URL}/profile?language={language}")
                ),
                KeyboardButton(
                    text=_(mt.KB_BACK),
                )
            ]
        ],
        resize_keyboard=True
    )
    return kb


class RegistrationFormKb:
    @staticmethod
    def name(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.name])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def surname(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.surname])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def gender() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_GENDER_MALE)), KeyboardButton(text=_(mt.KB_GENDER_FEMALE))],
            ],
        )
        return kb

    @staticmethod
    def age(user) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([str(user.profile.age)])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def location(user: UserModel | None):
        builder = ReplyKeyboardBuilder()
        if user.profile and user.profile.city != "📍":
            builder.button(text=_(mt.KB_LEAVE_PREVIOUS))
        builder.button(
            text=_(mt.KB_LOCATION),
            request_location=True,
        )
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def ethnicity() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_ETHNICITY_UZBEK)), KeyboardButton(text=_(mt.KB_ETHNICITY_RUSSIAN))]
            ],
        )
        return kb

    @staticmethod
    def religion() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_RELIGION_ISLAM)), KeyboardButton(text=_(mt.KB_RELIGION_CHRISTIANITY))],
                [KeyboardButton(text=_(mt.KB_RELIGION_JUDAISM)), KeyboardButton(text=_(mt.KB_RELIGION_BUDDHISM))],
                [KeyboardButton(text=_(mt.KB_RELIGION_OTHER))],
                ],
        )
        return kb

    @staticmethod
    def religious_level() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_RELIGIOSITY_NONE)), KeyboardButton(text=_(mt.KB_RELIGIOSITY_LOW))],
                [KeyboardButton(text=_(mt.KB_RELIGIOSITY_MEDIUM)), KeyboardButton(text=_(mt.KB_RELIGIOSITY_HIGH))],
                [KeyboardButton(text=_(mt.KB_RELIGIOSITY_STRICT))]
            ],
        )
        return kb

    @staticmethod
    def job(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.job])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def height(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.height])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def weight(user: UserModel) -> ReplyKeyboardMarkup:
        try:
            kb = kb_gen([user.profile.weight])
        except:
            kb = del_kb
        return kb

    @staticmethod
    def education() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_EDUCATION_SECONDARY)), KeyboardButton(text=_(mt.KB_EDUCATION_INCOMPLETE_HIGHER))],
                [KeyboardButton(text=_(mt.KB_EDUCATION_HIGHER))],
            ],
        )
        return kb

    @staticmethod
    def marital_status() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_MARITAL_STATUS_SINGLE))],
                [KeyboardButton(text=_(mt.KB_MARITAL_STATUS_DIVORCED)), KeyboardButton(text=_(mt.KB_MARITAL_STATUS_WIDOWED))],
            ],
        )
        return kb

    @staticmethod
    def has_children() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_HAS_CHILDREN_YES)), KeyboardButton(text=_(mt.KB_HAS_CHILDREN_NO))],
            ],
        )
        return kb

    @staticmethod
    def polygamy() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_POLYGAMY_YES)), KeyboardButton(text=_(mt.KB_POLYGAMY_NO))],
                [KeyboardButton(text=_(mt.KB_POLYGAMY_UNSURE))]
            ],
        )
        return kb

    @staticmethod
    def goal() -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton(text=_(mt.KB_GOAL_MARRIAGE)), KeyboardButton(text=_(mt.KB_GOAL_SERIOUS_RELATIONSHIP))],
                [KeyboardButton(text=_(mt.KB_GOAL_FRIENDSHIP)), KeyboardButton(text=_(mt.KB_GOAL_COMMUNICATION))],
            ],
        )
        return kb

    @staticmethod
    def leave_previous(profile: ProfileModel) -> ReplyKeyboardMarkup:
        if profile:
            kb = ReplyKeyboardMarkup(
                resize_keyboard=True,
                one_time_keyboard=True,
                keyboard=[
                    [KeyboardButton(text=_(mt.KB_LEAVE_PREVIOUS))],
                ],
            )
        else:
            kb = del_kb
        return kb