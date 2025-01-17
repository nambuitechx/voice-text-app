from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    voice: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)
    query: Mapped[str] = mapped_column(String(), nullable=False)
    answer: Mapped[str] = mapped_column(String(), nullable=True)
    
    def __repr__(self):
        return f"Message(id={self.id!r}, query={self.query!r}, answer={self.answer!r})"
    
    def as_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "answer": self.answer,
        }
