from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    voice: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    
    def __repr__(self):
        return f"Message(id={self.id!r})"
    
    def as_dict(self):
        return {
            "id": self.id,
        }
