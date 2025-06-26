from app.models.board import Board
from app.db import db

def test_create_board_from_dict(app):
    # Arrange
    board_data = {"title": "Inspiration Board", "owner": "Ada"}

    # Act
    board = Board.from_dict(board_data)
    db.session.add(board)
    db.session.commit()

    # Assert
    assert board.id is not None
    assert board.title == "Inspiration Board"
    assert board.owner == "Ada"

def test_board_to_dict(app):
    # Arrange
    board = Board(title="Dev Board", owner="Tatyana")
    db.session.add(board)
    db.session.commit()

    # Act
    board_dict = board.to_dict()

    # Assert
    assert board_dict == {
        "id": board.id,
        "title": "Dev Board",
        "owner": "Tatyana"
    }

def test_update_board_from_dict(app):
    # Arrange
    board = Board(title="Old Title", owner="Old Owner")
    db.session.add(board)
    db.session.commit()

    # Act
    update_data = {"title": "New Title", "owner": "New Owner"}
    board.update_from_dict(update_data)
    db.session.commit()

    # Assert
    assert board.title == "New Title"
    assert board.owner == "New Owner"
