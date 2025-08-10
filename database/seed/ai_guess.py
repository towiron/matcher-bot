# create_polygamy_candidates_for_anchor.py
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

import random
import argparse
import re
from typing import Optional, Tuple, Iterable

from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from database.models.profile import ProfileModel
from database.models.filter import FilterModel
from database.models.city import CityModel
from database.models.ethnicity import EthnicityModel
from database.models.marital_status import MaritalStatusModel
from database.models import ReligionModel
from database.connect import async_session

fake = Faker("ru_RU")

EDUCATIONS = ["secondary", "higher"]
RELIGIOUS_LEVELS = ["low", "medium", "high"]
LANGUAGES = ["ru"]

# ---------- утилиты ----------
def _around(value: int, low: int, high: int, minv: int, maxv: int) -> tuple[int, int]:
    a = max(minv, value - low)
    b = min(maxv, value + high)
    if a > b:
        a, b = b, a
    return a, b

def _pick_within_filter(low: Optional[int], high: Optional[int], fallback_lo: int, fallback_hi: int) -> int:
    if low is not None and high is not None and low <= high:
        return random.randint(low, high)
    return random.randint(fallback_lo, fallback_hi)

# ---------- словари/шаблоны для разнообразных текстов ----------
F_INTERESTS = [
    "путешествия", "восточная кухня", "история", "конный спорт", "сад и дом",
    "книги и беседы", "благотворительность", "керамика", "вышивка сузане",
    "йога", "походы", "фотография", "выпечка", "чайные церемонии",
    "киновечера", "семейные пикники", "восточная поэзия", "каллиграфия"
]
F_VALUES = [
    "семейные традиции", "взаимная поддержка", "уважение старших", "забота друг о друге",
    "честность и открытость", "тихая гармония дома", "разделение обязанностей",
    "воспитание детей", "бережное отношение к вере", "гостеприимство"
]
F_TRAITS = [
    "спокойный характер", "мягкий юмор", "терпение", "заботливость",
    "практичность", "жизнерадостность", "любовь к уюту", "организованность"
]
F_GOALS_TXT = ["полигамной семье", "большой семье", "традиционной семье"]
F_OPENER = [
    "Семья — приоритет", "Дорожу близкими", "Верю в уважение и заботу",
    "Ценю тёплую домашнюю атмосферу", "Люблю совместные дела"
]

ABOUT_TEMPLATES = [
    "Ценю {value}. Люблю {i1} и {i2}, у меня {trait}.",
    "{opener}. Интересуюсь {i1} и {i2}, близки {value}.",
    "Открыта к {goal}. Радуют {i1}, {i2} и {value}.",
    "Люблю {i1} и {i2}. Для меня важны {value} и {trait}.",
    "Спокойна и уважительна. Ближе всего {value}; увлекаюсь {i1}.",
    "Дома ценю тепло и {value}. Радуют {i1}, а ещё {i2}.",
]

LOOKING_TEMPLATES = [
    "Ищу мужчину для серьёзных отношений в {goal}, важны {v1} и {v2}.",
    "Готова к {goal} при {v1} и {v2}, ценю {v3}.",
    "Хочу строить тёплые отношения в {goal}, где есть {v1} и {v2}.",
    "Открыта к {goal}, если в основе {v1}, {v2} и {v3}.",
    "Ищу человека, который разделяет {v1} и {v2}, ориентирован на {goal}.",
]

def _build_about() -> str:
    tpl = random.choice(ABOUT_TEMPLATES)
    i1, i2 = random.sample(F_INTERESTS, 2)
    value = random.choice(F_VALUES)
    trait = random.choice(F_TRAITS)
    opener = random.choice(F_OPENER)
    goal = random.choice(F_GOALS_TXT)
    text = tpl.format(i1=i1, i2=i2, value=value, trait=trait, opener=opener, goal=goal)
    text = text.replace("  ", " ").strip().rstrip(".") + "."
    return text

def _build_looking_for(anchor_goal: str) -> str:
    tpl = random.choice(LOOKING_TEMPLATES)
    v1, v2, v3 = random.sample(F_VALUES, 3)
    goal_text = "полигамной семье" if (anchor_goal or "marriage") == "marriage" else "семье"
    text = tpl.format(goal=goal_text, v1=v1, v2=v2, v3=v3)
    text = text.replace("  ", " ").strip().rstrip(".") + "."
    return text

def _female_about_and_looking_for(anchor: ProfileModel) -> Tuple[str, str]:
    about = _build_about()
    look = _build_looking_for(anchor.goal or "marriage")
    # небольшие «хвосты» для ещё большей вариативности
    tails = []
    if random.random() < 0.35:
        tails.append("Нравятся семейные пикники по выходным.")
    if random.random() < 0.25:
        tails.append("Люблю готовить для близких.")
    if tails:
        about = (about[:-1] + " " + " ".join(tails)).strip()
    return about, look

# ---------- анти-дубликатор ----------
def _normalize(s: str) -> list[str]:
    s = s.lower()
    s = re.sub(r"[^\w\s\-]+", " ", s)
    tokens = re.findall(r"[a-zа-яё0-9\-]+", s, flags=re.IGNORECASE)
    stop = {"и","в","на","к","по","из","для","о","об","при","если","где","у","с","а","же","но","что","как","то"}
    return [t for t in tokens if t not in stop]

def _jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(1, len(sa | sb))

def _distinct_text(about: str, looking: str, seen: list[tuple[str, str]], thr: float = 0.6) -> bool:
    a1, l1 = _normalize(about), _normalize(looking)
    for a2, l2 in seen:
        if _jaccard(a1, _normalize(a2)) > thr or _jaccard(l1, _normalize(l2)) > thr:
            return False
    return True

# ---------- справочники ----------
async def _load_refs(session: AsyncSession, anchor: ProfileModel):
    city = await session.get(CityModel, anchor.city_id)
    religion = await session.get(ReligionModel, anchor.religion_id)
    ethnicity = await session.get(EthnicityModel, anchor.ethnicity_id)
    marital_statuses = (await session.scalars(select(MaritalStatusModel))).all()

    # подберём «не замужем» / «в разводе»
    ms_single = None
    ms_divorced = None
    for ms in marital_statuses:
        val = (getattr(ms, "en", None) or getattr(ms, "ru", None) or "").lower()
        if "single" in val or "не жен" in val or "не замуж" in val:
            ms_single = ms
        if "divorced" in val or "развод" in val or "в разводе" in val:
            ms_divorced = ms
    default_ms = ms_single or ms_divorced or (marital_statuses[0] if marital_statuses else None)
    return city, religion, ethnicity, default_ms

# ---------- основной генератор ----------
async def create_polygamy_candidates_for_anchor(
    session: AsyncSession,
    anchor_profile_id: int,
    *,
    count: int = 5,   # по умолчанию 5 для тестов
):
    anchor: Optional[ProfileModel] = await session.get(ProfileModel, anchor_profile_id)
    if not anchor:
        print(f"❌ Anchor profile {anchor_profile_id} not found")
        return

    # читаем актуальный фильтр якоря, если есть (поможет точнее подогнать параметры)
    anchor_filter: Optional[FilterModel] = await session.get(FilterModel, anchor.id)

    city, religion, ethnicity, default_ms = await _load_refs(session, anchor)
    if not all([city, religion, ethnicity, default_ms]):
        print("❌ Не найдены справочники (city/religion/ethnicity/marital_status).")
        return

    # ключевые параметры якоря
    anchor_age = anchor.age
    anchor_height = anchor.height
    anchor_weight = anchor.weight
    anchor_has_kids = anchor.has_children
    # если в профиле полигамия не указана — считаем True (для тестов)
    anchor_polygamy = anchor.polygamy if anchor.polygamy is not None else True
    anchor_goal = anchor.goal or "marriage"
    anchor_rel_level = anchor.religious_level or "medium"

    seen_texts: list[tuple[str, str]] = []
    created = 0

    for _ in range(count):
        # --- создаём пользователя ---
        u = UserModel(
            id=fake.unique.random_int(min=10_000_000, max=99_999_999_999),
            username=fake.user_name(),
            language=random.choice(LANGUAGES),
        )
        session.add(u)
        await session.flush()

        # --- профиль кандидатки — стараемся соответствовать фильтру якоря (если он есть) ---
        age = _pick_within_filter(getattr(anchor_filter, "age_from", None),
                                  getattr(anchor_filter, "age_to", None),
                                  max(20, anchor_age - 20), min(45, anchor_age - 5))
        height = _pick_within_filter(getattr(anchor_filter, "height_from", None),
                                     getattr(anchor_filter, "height_to", None),
                                     155, 176)
        weight = _pick_within_filter(getattr(anchor_filter, "weight_from", None),
                                     getattr(anchor_filter, "weight_to", None),
                                     48, 72)
        has_kids = getattr(anchor_filter, "has_children", None)
        if has_kids is None:
            has_kids = random.choice([True, False])

        # тексты с анти-дубликатором
        tries = 0
        about, looking_for = _female_about_and_looking_for(anchor)
        while tries < 10 and not _distinct_text(about, looking_for, seen_texts, thr=0.58):
            about, looking_for = _female_about_and_looking_for(anchor)
            tries += 1
        seen_texts.append((about, looking_for))

        # небольшие хвосты на базе случайных атрибутов — ещё больше вариативности
        tail_bits = []
        if has_kids and random.random() < 0.5:
            tail_bits.append("Люблю время с детьми и совместные занятия.")
        if height > 170 and random.random() < 0.4:
            tail_bits.append("Высокий рост не мешает домашнему уюту :)")
        if random.random() < 0.3:
            tail_bits.append("Иногда организую семейные поездки за город.")
        if tail_bits:
            about = (about[:-1] + " " + " ".join(tail_bits)).strip()

        p = ProfileModel(
            id=u.id,
            name=fake.first_name_female(),
            age=age,
            gender="female",
            city_id=city.id,                         # совпадает с якорем
            height=height,
            weight=weight,
            marital_status_id=default_ms.id,         # чаще «не замужем»/«в разводе»
            has_children=has_kids,
            education=random.choice(EDUCATIONS),
            goal=anchor_goal,                        # якорь ищет «брак» — делаем так же
            polygamy=anchor_polygamy,                # ключевое — открыта к полигамии
            religion_id=religion.id,
            religious_level=anchor_rel_level,
            ethnicity_id=ethnicity.id,
            job=fake.job(),
            about=about[:300],                       # на всякий случай ограничим
            looking_for=looking_for[:300],
            is_active=True,
        )
        session.add(p)

        # --- фильтр девушки — чтобы якорь часто попадал к ней ---
        age_from, age_to = _around(anchor_age, 6, 4, 18, 80)
        h_from, h_to = _around(anchor_height, 8, 8, 140, 210)
        w_from, w_to = _around(anchor_weight, 12, 12, 40, 130)

        f = FilterModel(
            id=u.id,
            city_id=anchor.city_id,                  # тот же город
            age_from=age_from, age_to=age_to,
            height_from=h_from, height_to=h_to,
            weight_from=w_from, weight_to=w_to,
            goal=anchor_goal,
            ethnicity_id=anchor.ethnicity_id,        # можно убрать, если нужен шире охват
            has_children=anchor_has_kids,
        )
        session.add(f)

        created += 1

    await session.commit()
    print(f"✅ Создано {created} кандидаток для anchor={anchor_profile_id} "
          f"(city={city.id}, religion={religion.id}, ethnicity={ethnicity.id}, goal={anchor_goal}, polygamy={anchor_polygamy})")

# ---------- CLI ----------
async def main(anchor: int, count: int):
    async with async_session() as session:
        await create_polygamy_candidates_for_anchor(session, anchor_profile_id=anchor, count=count)

if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="Создание ≥5 кандидаток под конкретный anchor-профиль (полигамия).")
    parser.add_argument("--anchor", type=int, required=True, help="ID анкеты (ProfileModel.id) якорного пользователя")
    parser.add_argument("--count", type=int, default=5, help="Сколько кандидаток создать (по умолчанию 5)")
    args = parser.parse_args()

    asyncio.run(main(args.anchor, args.count))
