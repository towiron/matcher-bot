from bot.database.services.base import BaseService
from ..models.ethnicity import EthnicityModel


class Ethnicity(BaseService):
    model = EthnicityModel