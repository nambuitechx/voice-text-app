import uuid

from typing import Any
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self):
        serialized = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            serialized[c.name] = value
        return serialized