from app.models.card import Card
from app.models.board import Board
from app.db import db

def test_create_card_from_dict(app):
    # Arrange: create a board to satisfy FK constraint
    board = Board(title="Quotes", owner="Jane")
    db.session.add(board)
    db.session.commit()

    card_data = {
        "message": "Be kind to yourself",
        "board_id": board.board_id,
        "likes_count": 2
    }

    # Act
    card = Card.from_dict(card_data)
    db.session.add(card)
    db.session.commit()

    # Assert
    assert card.card_id is not None
    assert card.message == "Be kind to yourself"
    assert card.board_id == board.board_id
    assert card.likes_count == 2

def test_card_to_dict(app):
    # Arrange
    board = Board(title="Motivation", owner="Dev")
    db.session.add(board)
    db.session.commit()

    card = Card(message="Keep going", board_id=board.board_id, likes_count=1)
    db.session.add(card)
    db.session.commit()

    # Act
    card_dict = card.to_dict()

    # Assert
    assert card_dict == {
        "card_id": card.card_id,
        "message": "Keep going",
        "likes_count": 1,
        "board_id": board.board_id
    }

def test_update_card_from_dict(app):
    # Arrange
    board = Board(title="Tips", owner="Dev")
    db.session.add(board)
    db.session.commit()

    card = Card(message="Old message", board_id=board.board_id)
    db.session.add(card)
    db.session.commit()

    # Act
    update_data = {"message": "New message", "likes_count": 5}
    card.update_from_dict(update_data)
    db.session.commit()

    # Assert
    assert card.message == "New message"
    assert card.likes_count == 5
