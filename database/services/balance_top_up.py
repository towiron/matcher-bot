from database.services.base import BaseService
from ..models.balance_top_up import BalanceTopUpModel


class BalanceTopUp(BaseService):
    model = BalanceTopUpModel
