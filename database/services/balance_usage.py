from database.services.base import BaseService
from ..models.balance_usage import BalanceUsageModel


class BalanceUsage(BaseService):
    model = BalanceUsageModel
