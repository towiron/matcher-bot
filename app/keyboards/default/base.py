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

menu_kb: ReplyKeyboardMarkup = kb_gen(
    [mt.KB_FIND_MATCH],
    [mt.KB_MY_PROFILE, mt.KB_BUY_CHANCES],
    [mt.KB_DISABLE_PROFILE],
)

search_kb: ReplyKeyboardMarkup = kb_gen(
    [mt.KB_GIVE_CHANCE, mt.KB_NEXT],
    [mt.KB_BACK_TO_SEARCH],
)

payment_kb: ReplyKeyboardMarkup = kb_gen(
    [mt.KB_BUY_CHANCES],
    [mt.KB_BACK],
)

search_kb_after_chance: ReplyKeyboardMarkup = kb_gen(
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
