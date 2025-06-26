from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .card import Card

class Board(db.Model):
# So SQLAlchemy handle the table vs. manually
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(nullable=False)
    cards: Mapped[List["Card"]] = relationship(back_populates="board", cascade="all, delete")

    def to_dict(self):
        return { 
            "id" : self.id,
            "title": self.title,
            "owner": self.owner
        }
    
    def to_dict_with_cards(self):
        board_dict = self.to_dict()
        board_dict["cards"] = [card.to_dict() for card in self.cards]
        return board_dict 

    @classmethod
    def from_dict(cls, dict_data_board):
        return cls(
            title=dict_data_board["title"],
            owner=dict_data_board["owner"]
        )

    def update_from_dict(self, dict_data_board):
        if "title" in dict_data_board:
            self.title = dict_data_board["title"]
        if "owner" in dict_data_board:
            self.owner = dict_data_board["owner"]