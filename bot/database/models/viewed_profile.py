from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel

class ViewedProfileModel(BaseModel):
    __tablename__ = "viewed_profiles"
    __table_args__ = (
        UniqueConstraint("viewer_id", "viewed_user_id", name="uq_viewed_profiles"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    viewer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    viewed_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
