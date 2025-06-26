from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from ..db import db

if TYPE_CHECKING:
    from .board import Board

class Card(db.Model):
    # So SQLAlchemy handle the table vs. manually
    __tablename__ = "card"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(40), nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"), nullable=False)
    board: Mapped["Board"] = relationship(back_populates="cards")

    @validates("message")
    def message(self, key, message):
        if len(message) > 40:
            raise ValueError("The message fild shoudn't be grater than 40 characters")
        return message

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }

    @classmethod
    def from_dict(cls, dict_data_card):
        return cls(
            message=dict_data_card["message"],
            board_id=dict_data_card["board_id"],
            likes_count=dict_data_card["likes_count"] if "likes_count" in dict_data_card else 0
        )

    def update_from_dict(self, dict_data_card):
        if "message" in dict_data_card:
            self.message = dict_data_card["message"]
        if "likes_count" in dict_data_card:
            self.likes_count = dict_data_card["likes_count"]
