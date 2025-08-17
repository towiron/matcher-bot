import json
import re

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.filter import FilterModel
from database.models.profile import ProfileModel
from database.models.viewed_profile import ViewedProfileModel
from database.models.match import MatchModel
from typing import Optional, List, Tuple, Dict
from utils.logging import logger
from openai import OpenAI
from data.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


async def search_profiles(session: AsyncSession, profile: ProfileModel) -> list[int]:
    # Получаем фильтр пользователя
    filter_obj: Optional[FilterModel] = await session.get(FilterModel, profile.id)
    if not filter_obj:
        return []

    target_gender = "female" if profile.gender == "male" else "male"

    viewed_subq = select(ViewedProfileModel.viewed_user_id).where(
        ViewedProfileModel.viewer_id == profile.id
    )
    matched_subq = select(MatchModel.receiver_id).where(
        MatchModel.sender_id == profile.id
    )

    filters = [
        ProfileModel.is_active,
        ProfileModel.id != profile.id,
        ProfileModel.gender == target_gender,
        ~ProfileModel.id.in_(viewed_subq),
        ~ProfileModel.id.in_(matched_subq),
    ]

    if filter_obj.city_id is not None:
        filters.append(ProfileModel.city_id == filter_obj.city_id)

    if filter_obj.age_from is not None:
        filters.append(ProfileModel.age >= filter_obj.age_from)
    if filter_obj.age_to is not None:
        filters.append(ProfileModel.age <= filter_obj.age_to)

    if filter_obj.height_from is not None:
        filters.append(ProfileModel.height >= filter_obj.height_from)
    if filter_obj.height_to is not None:
        filters.append(ProfileModel.height <= filter_obj.height_to)

    if filter_obj.weight_from is not None:
        filters.append(ProfileModel.weight >= filter_obj.weight_from)
    if filter_obj.weight_to is not None:
        filters.append(ProfileModel.weight <= filter_obj.weight_to)

    if filter_obj.goal:
        filters.append(ProfileModel.goal == filter_obj.goal)

    if filter_obj.ethnicity_id is not None:
        filters.append(ProfileModel.ethnicity_id == filter_obj.ethnicity_id)

    if filter_obj.has_children is not None:
        filters.append(ProfileModel.has_children == filter_obj.has_children)

    if profile.polygamy is not None:
        filters.append(ProfileModel.polygamy == profile.polygamy)

    if profile.religion_id is not None:
        filters.append(ProfileModel.religion_id == profile.religion_id)

    stmt = (
        select(ProfileModel.id)
        .where(and_(*filters))
        .order_by(ProfileModel.created_at.desc())
    )
    result = await session.execute(stmt)
    profile_ids = [row[0] for row in result.fetchall()]

    logger.log("DATABASE", f"{profile.id} поиск анкет по фильтру, найдено: {profile_ids}")
    return profile_ids

# ---------- helpers ----------

def _clean(s: Optional[str]) -> str:
    if not s:
        return ""
    # убираем лишние пробелы и ограничиваем длину
    s = re.sub(r"\s+", " ", s).strip()
    # если страшные символы встречаются, можно раскомментировать:
    # s = s.encode("utf-8", "ignore").decode()
    return s[:500]

async def _load_user_and_candidates(
    session: AsyncSession, user_profile_id: int, profile_ids: List[int]
):
    """Возвращает профиль пользователя и список кандидатов (id, about, looking_for)."""
    user = await session.get(ProfileModel, user_profile_id)
    if not profile_ids:
        return user, []

    rows = (await session.execute(
        select(ProfileModel.id, ProfileModel.about, ProfileModel.looking_for)
        .where(ProfileModel.id.in_(profile_ids))
    )).all()

    cands = []
    for pid, about, looking_for in rows:
        cands.append((pid, _clean(about), _clean(looking_for)))
    return user, cands


def _build_prompt_with_reasons(user_about, user_looking_for, cands, lang: str = "ru") -> str:
    lang_clause = {
        "ru": (
            "Отвечай ТОЛЬКО на русском языке. "
            "Поле reason — должно быть информативным (максимум 150 символов) "
            "и содержать ТОЛЬКО позитивные совпадения. "
            "Объясни конкретно, почему кандидат подходит: общие интересы, цели, ценности, образ жизни. "
            "Каждый ответ должен быть УНИКАЛЬНЫМ и отражать конкретные детали из профиля кандидата. "
            "Избегай общих фраз типа 'общие интересы' - будь конкретным."
        ),
        "en": (
            "Answer ONLY in English. "
            "The 'reason' must be informative (max 150 characters) "
            "and contain ONLY positive matches. "
            "Explain specifically why the candidate is a good match: shared interests, goals, values, lifestyle. "
            "Each answer must be UNIQUE and reflect specific details from the candidate's profile. "
            "Avoid generic phrases like 'shared interests' - be specific."
        ),
    }.get(lang, f"Answer ONLY in {lang}. The 'reason' must be informative and contain only positive matches.")

    head = (
        "You are a matching assistant for a dating app.\n"
        "Given USER (about, looking_for) and CANDIDATES, rank candidates by MUTUAL fit "
        "based on shared values, goals, lifestyle, and interests.\n"
        f"{lang_clause}\n\n"
        "CRITICAL REQUIREMENTS:\n"
        "1. Each reason must be UNIQUE and specific to that candidate\n"
        "2. Mention specific hobbies, activities, or traits from their profile\n"
        "3. Avoid generic phrases - be concrete and detailed\n"
        "4. Maximum 150 characters for reason field\n"
        "5. Focus on what makes THIS candidate special\n\n"
        "Return STRICT JSON ONLY in this exact shape:\n"
        "{\n"
        '  "results": [\n'
        '    {"id": <int>, "score": <0..100>, "reason": "<unique specific reason for this candidate>"}\n'
        "  ]\n"
        "}\n"
        "No extra text. No quotes in reason field. Each reason must be different."
    )

    user_block = f'\nUSER:\nabout: {user_about}\nlooking_for: {user_looking_for}\n'
    cand_block = "CANDIDATES:\n" + "\n".join(
        f"- id: {pid}\n  about: {about}\n  looking_for: {lf}" for pid, about, lf in cands
    )
    return head + user_block + cand_block


# Универсальный вызов через Chat Completions — стабильно работает даже на старых SDK
client = OpenAI(api_key=OPENAI_API_KEY)

# --- замените вашу версию на эту ---
def _chat_call_get_json(
    prompt: str,
    *,
    retries: int = 2,
    temp: float = 0.1,
    max_tokens: int = 1500,
    lang: str = "ru"
) -> str:
    """
    Никогда не бросает исключений. На любые проблемы логирует и возвращает '{"results": []}'.
    """
    import time
    import random
    import json as _json

    delay = 0.6
    safe_empty = '{"results": []}'

    system_text = {
        "ru": "You are a helpful assistant. Reply strictly in Russian. Provide detailed but concise responses.",
        "en": "You are a helpful assistant. Reply strictly in English. Provide detailed but concise responses.",
    }.get(lang, f"You are a helpful assistant. Reply strictly in {lang}. Provide detailed but concise responses.")

    for attempt in range(retries + 1):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_text},
                    {"role": "user", "content": prompt},
                ],
                temperature=temp,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )

            text = (resp.choices[0].message.content or "").strip()
            if not text:
                raise ValueError("empty_content")

            # проверка JSON
            try:
                _json.loads(text)
            except _json.JSONDecodeError as e:
                raise ValueError(f"json_decode_error_primary: {e}") from e

            if len(text) > 3000:
                logger.log("AI_MATCH_WARNING", f"Response too long ({len(text)} chars) on attempt={attempt}")
                # попробуем еще раз, без исключения
                if attempt < retries:
                    time.sleep(delay + random.random() * 0.2)
                    delay *= 2
                    continue
                else:
                    return safe_empty

            return text

        except Exception as e:
            logger.log("AI_MATCH_TRY_ERROR", f"attempt={attempt} err={e!r}")

            # вторая попытка без response_format
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_text},
                        {"role": "user", "content": prompt + "\n\nReturn STRICT JSON only. No extra text."},
                    ],
                    temperature=temp,
                    max_tokens=max_tokens,
                )
                text = (resp.choices[0].message.content or "").strip()
                if not text:
                    raise ValueError("empty_content_fallback")

                try:
                    _json.loads(text)
                except _json.JSONDecodeError as e2:
                    raise ValueError(f"json_decode_error_fallback: {e2}") from e2

                if len(text) > 3000:
                    logger.log("AI_MATCH_WARNING", f"Response too long ({len(text)} chars) on fallback attempt={attempt}")
                    if attempt < retries:
                        time.sleep(delay + random.random() * 0.2)
                        delay *= 2
                        continue
                    else:
                        return safe_empty

                return text

            except Exception as e2:
                logger.log("AI_MATCH_TRY_ERROR_FALLBACK", f"attempt={attempt} err={e2!r}")
                if attempt < retries:
                    time.sleep(delay + random.random() * 0.2)
                    delay *= 2
                    continue
                else:
                    # последняя точка — не бросаем исключение
                    logger.log("AI_MATCH_GIVE_UP", f"give up after {attempt+1} attempts")
                    return safe_empty

    # теоретически недостижимо, но пусть будет
    return safe_empty


# ---------- main function ----------

async def search_profiles_by_ai_with_reasons(
    session: AsyncSession,
    user_profile_id: int,
    profile_ids: List[int],
    *,
    max_results: int = 5,
    language: str = "ru"
) -> Tuple[List[int], Dict[int, str]]:
    """
    Возвращает (ids, reasons), где ids — до 5 лучших кандидатов,
    reasons — словарь {id: краткое обоснование}.
    """
    user, cands = await _load_user_and_candidates(session, user_profile_id, profile_ids)
    if not user or not cands:
        return [], {}

    ua, ulf = _clean(user.about), _clean(user.looking_for)

    # Если у пользователя нет текста — просто вернём первых из списка
    if not (ua or ulf):
        ids = [pid for pid, _, _ in cands][:max_results]
        reasons = {
            pid: "Нет текстов у пользователя — возвращены первые кандидаты после БД-фильтра."
            for pid in ids
        }
        return ids, reasons

    # Не раздуваем промпт - ограничиваем до 5 кандидатов для стабильности
    if len(cands) > 10:
        cands = cands[:10]

    prompt = _build_prompt_with_reasons(ua, ulf, cands, language)

    try:
        raw = _chat_call_get_json(
            prompt,
            retries=2,
            temp=0.7,  # увеличиваем температуру для большей креативности
            max_tokens=1500,
            lang=language
        )

        logger.log("AI_MATCH", f"raw[:1500]={raw[:1500]!r}")

        # осторожный парс без рейза наружу
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as json_err:
            logger.log("AI_MATCH_JSON_ERROR", f"user={user_profile_id} JSON decode error: {json_err}")
            logger.log("AI_MATCH_FULL_RESPONSE", f"user={user_profile_id} full response: {raw}")
            data = {"results": []}  # мягкий фолбэк

        results = data.get("results", [])
        logger.log("AI_MATCH_DEBUG", f"user={user_profile_id} parsed {len(results)} results")

        allowed_ids = {pid for pid, _, _ in cands}
        cleaned: List[Tuple[float, int, str]] = []
        for item in results:
            try:
                pid = int(item.get("id"))
                if pid not in allowed_ids:
                    continue
                score = float(item.get("score", 0))
                reason = str(item.get("reason", "")).strip()[:400]
                cleaned.append((score, pid, reason))
            except Exception as item_err:
                logger.log("AI_MATCH_ITEM_SKIP", f"user={user_profile_id} err={item_err!r} item={item!r}")
                continue

        cleaned.sort(reverse=True)
        top = cleaned[:max_results]
        ids = [pid for _, pid, _ in top]
        reasons = {pid: reason for _, pid, reason in top}

        if not ids:
            # мягкий фолбэк, без исключений
            ids = [pid for pid, _, _ in cands][:max_results]
            reasons = {pid: "Фолбэк: модель вернула пустой список." for pid in ids}
            logger.log("AI_MATCH_EMPTY", f"user={user_profile_id} fallback ids={ids}")

        logger.log("AI_MATCH_REASONS", f"user={user_profile_id} top={ids} reasons={reasons}")
        return ids, reasons

    except Exception as e:
        ids = [pid for pid, _, _ in cands][:max_results]
        reasons = {pid: f"Фолбэк из-за непредвиденной ошибки: {e!s}"}
        logger.log("AI_MATCH_ERROR", f"user={user_profile_id} error: {e}")
        return ids, reasons
