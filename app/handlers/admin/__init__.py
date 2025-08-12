from .admin import admin_router # noqa: F811
from .ban import admin_router # noqa: F811
from .logs import admin_router # noqa: F811
from .mailing import admin_router # noqa: F811
from .stats import admin_router # noqa: F811

__all__ = ["admin_router"]
