from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import _

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
    [_(mt.KB_FIND_MATCH)],
    [_(mt.KB_MY_PROFILE), _(mt.KB_BUY_CHANCES)],
    [_(mt.KB_DISABLE_PROFILE)],
)

search_kb: ReplyKeyboardMarkup = kb_gen(
    [_(mt.KB_NEXT), _(mt.KB_GIVE_CHANCE)],
    [_(mt.KB_BACK_TO_SEARCH)],
)

payment_kb: ReplyKeyboardMarkup = kb_gen(
    [_(mt.KB_BUY_CHANCES)],
    [_(mt.KB_BACK)],
)

search_kb_after_chance: ReplyKeyboardMarkup = kb_gen(
    [_(mt.KB_NEXT)],
    [_(mt.KB_BACK_TO_SEARCH)],
)

match_kb: ReplyKeyboardMarkup = kb_gen(
    ["❤️", "👎"],
    ["💤"],
)

cancel_mailing_to_user_kb: ReplyKeyboardMarkup = kb_gen(
    ["↩️"],
)
