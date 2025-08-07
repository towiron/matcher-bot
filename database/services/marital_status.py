from database.services.base import BaseService
from ..models.marital_status import MaritalStatusModel


class MaritalStatus(BaseService):
    model = MaritalStatusModel