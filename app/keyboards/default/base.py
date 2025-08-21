from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from .kb_generator import simple_kb_generator as kb_gen
from app.text import message_text as mt

del_kb = ReplyKeyboardRemove()


cancel_kb: ReplyKeyboardMarkup = kb_gen(
    ["/cancel"],
)

start_kb: ReplyKeyboardMarkup = kb_gen(
    ["/start"],
)

def menu_kb() -> ReplyKeyboardMarkup:
    return kb_gen(
        [mt.KB_FIND_MATCH],
        [mt.KB_MY_PROFILE, mt.KB_BUY_CHANCES],
        [mt.KB_DISABLE_PROFILE],
    )

def search_kb() -> ReplyKeyboardMarkup:
    return kb_gen(
        [mt.KB_GIVE_CHANCE, mt.KB_NEXT],
        [mt.KB_BACK_TO_SEARCH],
    )

def payment_kb() -> ReplyKeyboardMarkup:
    return kb_gen(
        [mt.KB_BUY_CHANCES],
        [mt.KB_BACK],
    )

def search_kb_after_chance() -> ReplyKeyboardMarkup:
    return kb_gen(
        [mt.KB_NEXT],
        [mt.KB_BACK_TO_SEARCH],
    )

match_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "👎"],
    ["💤"],
)

cancel_mailing_to_user_kb: ReplyKeyboardMarkup = kb_gen(
    ["↩️"],
)
