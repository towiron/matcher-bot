from aiogram.filters import Filter
from aiogram.types import Message

from utils.geopy import get_coordinates, get_city_name
from app.text import message_text as mt

# ---------------MAPS-----------------

gender_map = {
    mt.KB_GENDER_MALE: "male",
    mt.KB_GENDER_FEMALE: "female",
}

marital_status_map = {
    mt.KB_MARITAL_STATUS_SINGLE: "single",
    mt.KB_MARITAL_STATUS_DIVORCED: "divorced",
    mt.KB_MARITAL_STATUS_WIDOWED: "widowed",
}

yes_no_map = {
    mt.KB_POLYGAMY_YES: True,
    mt.KB_POLYGAMY_NO: False,
    mt.KB_POLYGAMY_UNSURE: None,
}

education_map = {
    mt.KB_EDUCATION_SECONDARY: "secondary",
    mt.KB_EDUCATION_INCOMPLETE_HIGHER: "incomplete_higher",
    mt.KB_EDUCATION_HIGHER: "higher",
}

goal_map = {
    mt.KB_GOAL_MARRIAGE: "marriage",
    mt.KB_GOAL_SERIOUS_RELATIONSHIP: "serious_relationship",
    mt.KB_GOAL_FRIENDSHIP: "friendship",
    mt.KB_GOAL_COMMUNICATION: "communication",
}

religion_map = {
    mt.KB_RELIGION_ISLAM: "islam",
    mt.KB_RELIGION_CHRISTIANITY: "christianity",
    mt.KB_RELIGION_JUDAISM: "judaism",
    mt.KB_RELIGION_BUDDHISM: "buddhism",
    mt.KB_RELIGION_OTHER: "other",
}

religious_level_map = {
    mt.KB_RELIGIOSITY_NONE: None,
    mt.KB_RELIGIOSITY_LOW: "low",
    mt.KB_RELIGIOSITY_MEDIUM: "medium",
    mt.KB_RELIGIOSITY_HIGH: "high",
    mt.KB_RELIGIOSITY_STRICT: "strict",
}

polygamy_map = {
    mt.KB_POLYGAMY_YES: True,
    mt.KB_POLYGAMY_NO: False,
    mt.KB_POLYGAMY_UNSURE: None,
}

ethnicity_map = {
    mt.KB_ETHNICITY_UZBEK: "uzbek",
    mt.KB_ETHNICITY_RUSSIAN: "russian",
}

has_children_map = {
    mt.KB_HAS_CHILDREN_YES: True,
    mt.KB_HAS_CHILDREN_NO: False,
}

leave_previous_tuple = (
    mt.KB_LEAVE_PREVIOUS,
)

start_command_tuple = (
    "/create",
    mt.CREATE_PROFILE,
)

# ---------------FILTERS-----------------

class IsCreate(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text in start_command_tuple

class IsName(Filter):
    async def __call__(self, message: Message) -> bool:
        return len(message.text) < 70

class IsSurname(Filter):
    async def __call__(self, message: Message) -> bool:
        return len(message.text) < 70

class IsGender(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        if message.text in gender_map:
            return {"gender": gender_map[message.text]}
        return None

class IsAge(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and 18 <= int(message.text) <= 99

class IsCity(Filter):
    async def __call__(self, message: Message) -> dict[str, float | str | None] | bool:
        latitude = longitude = None
        city = None

        if message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude
            city = get_city_name(latitude, longitude)
        elif message.text:
            if message.text.isdigit():
                return False
            if message.text in leave_previous_tuple:
                return {"latitude": None, "longitude": None, "city": None}
            elif coordinates := get_coordinates(message.text):
                latitude, longitude = coordinates
                city = message.text
            else:
                return False

        return {"latitude": latitude, "longitude": longitude, "city": city}

class IsEthnicity(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        return {"ethnicity": message.text} if len(message.text) < 70 else None

class IsReligion(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        if message.text in religion_map:
            return {"religion": religion_map[message.text]}
        return None

class IsReligiousLevel(Filter):
    async def __call__(self, message: Message) -> dict[str, str | None] | None:
        if message.text in religious_level_map:
            return {"religious_level": religious_level_map[message.text]}
        return None

class IsHeight(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and 120 < int(message.text) < 250

class IsWeight(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.text.isdigit() and 40 < int(message.text) < 200

class IsMaritalStatus(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        if message.text in marital_status_map:
            return {"marital_status": marital_status_map[message.text]}
        return None

class IsHasChildren(Filter):
    async def __call__(self, message: Message) -> dict[str, bool | None] | None:
        if message.text in yes_no_map:
            return {"has_children": has_children_map[message.text]}
        return None

class IsEducation(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        if message.text in education_map:
            return {"education": education_map[message.text]}
        return None

class IsJob(Filter):
    async def __call__(self, message: Message) -> dict[str, str | None] | None:
        return {"job": message.text} if len(message.text) < 100 else None

class IsPolygamy(Filter):
    async def __call__(self, message: Message) -> dict[str, bool | None] | None:
        if message.text in yes_no_map:
            return {"polygamy": polygamy_map[message.text]}
        return None

class IsGoal(Filter):
    async def __call__(self, message: Message) -> dict[str, str] | None:
        if message.text in goal_map:
            return {"goal": goal_map[message.text]}
        return None

class IsMessageToUser(Filter):
    async def __call__(self, message: Message) -> bool:
        return len(message.text) < 250