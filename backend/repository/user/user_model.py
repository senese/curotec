from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import List

from ..order.order_model import OrderModel
from ..db_handler import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    orders: Mapped[List[OrderModel]] = relationship(cascade="all, delete")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
