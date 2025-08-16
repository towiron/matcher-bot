from aiogram import F, types
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from bot.loader import _

from bot.app.filters.kb_filter import StatsCallback
from bot.app.keyboards.inline.admin import stats_ikb
from bot.app.text import message_text as mt
from bot.app.routers import admin_router
from bot.data.config import GRAPH_FILE_PATH
from bot.database.services.stats import Stats
from bot.utils.graphs import StatsGraph

stats_graph = StatsGraph()


@admin_router.message(StateFilter(None), Command("stats"))
@admin_router.message(StateFilter(None), F.text == "📊 Statistics")
async def _stats_command(message: types.Message, session) -> None:
    """Отправляет администратору меню статистики"""
    await message.answer("Stats sending...")

    data = await Stats.get_registration_data(session)
    stats_graph.create_user_registration_graph(data)
    users_stats = await Stats.user_stats(session)

    text = _(mt.USER_STATS).format(
        users_stats["count"],
        users_stats["banned_count"],
        users_stats["most_popular_language"],
    )

    photo = types.FSInputFile(GRAPH_FILE_PATH)
    await message.answer_photo(photo=photo, caption=text, reply_markup=stats_ikb(_(mt.KB_STAT_PROFILE)))


@admin_router.callback_query(StateFilter(None), StatsCallback.filter())
async def _stats_callback(callback: types.CallbackQuery, callback_data: StatsCallback, session) -> None:
    """Отправляет администратору график и статистику"""

    user_text = _(mt.KB_STAT_USER)
    profile_text = _(mt.KB_STAT_PROFILE)

    if callback_data.type == user_text:
        data = await Stats.get_registration_data(session)
        stats_graph.create_user_registration_graph(data)
        users_stats = await Stats.user_stats(session)

        text = _(mt.USER_STATS).format(
            users_stats["count"],
            users_stats["banned_count"],
            users_stats["most_popular_language"],
        )
        kb_text = profile_text

    elif callback_data.type == profile_text:
        gender_data = await Stats.get_gender_data(session)
        stats_graph.create_gender_pie_chart(gender_data)
        match_stats = await Stats.match_stats(session)
        profile_stats = await Stats.profile_stats(session)

        text = _(mt.PROFILE_STATS).format(
            profile_stats["count"],
            profile_stats["inactive_profile"],
            profile_stats["male_count"],
            profile_stats["female_count"],
            match_stats[0],
            profile_stats["average_age"],
            profile_stats["most_popular_city"],
        )
        kb_text = user_text

    else:
        # Неизвестный тип — просто ответим и выйдем
        await callback.answer(_("Неизвестный тип статистики"))
        return

    media = types.InputMediaPhoto(media=types.FSInputFile(GRAPH_FILE_PATH), caption=text)

    # На случай InaccessibleMessage
    if isinstance(callback.message, types.Message):
        await callback.message.edit_media(media=media, reply_markup=stats_ikb(kb_text))
    else:
        await callback.send_photo(callback.from_user.id, types.FSInputFile(GRAPH_FILE_PATH), caption=text, reply_markup=stats_ikb(kb_text))
