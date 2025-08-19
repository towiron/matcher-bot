
from app.text import message_text as mt

# ---------------MAPS-----------------

gender_map = {
    mt.KB_GENDER_MALE: "male",
    mt.KB_GENDER_FEMALE: "female",
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

religious_level_map = {
    mt.KB_RELIGIOSITY_NONE: None,
    mt.KB_RELIGIOSITY_LOW: "low",
    mt.KB_RELIGIOSITY_MEDIUM: "medium",
    mt.KB_RELIGIOSITY_HIGH: "high",
    mt.KB_RELIGIOSITY_STRICT: "strict",
}

start_command_tuple = (
    "/create",
    mt.CREATE_PROFILE,
)
