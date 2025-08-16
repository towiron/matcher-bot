
from bot.app.text import message_text as mt

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
