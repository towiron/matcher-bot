from database.services.base import BaseService
from ..models.city import CityModel


class City(BaseService):
    model = CityModel