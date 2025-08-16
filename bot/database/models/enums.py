from enum import IntEnum, StrEnum

class UserStatus(IntEnum):
    Banned = 0
    User = 1
    Sponsor = 2
    Moderator = 3
    Admin = 4
    Owner = 5

class EntryKind(StrEnum):
    TOP_UP = "top_up"        # платёж от провайдера
    BONUS = "bonus"          # любой бонус (ежедневный, стартовый, стрик)
    USAGE = "usage"          # списание за действие (просмотр и т.п.)
    ADJUST = "adjust"        # ручная корректировка/возврат/исправление

class Source(StrEnum):
    Click = "click"
    Payme = "payme"
    Uzum  = "uzum"
    Initial = "initial"      # стартовые шансы при регистрации
    Internal = "internal"    # системные бонусы, вручную и т.п.
