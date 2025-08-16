from bot.database.services.base import BaseService
from ..models.religion import ReligionModel


class Religion(BaseService):
    model = ReligionModel