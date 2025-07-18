import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.board import Board
from app.models.card import Card
from datetime import datetime

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# One board
@pytest.fixture
def one_board(app):
    new_board = Board(title="Inspiration", owner="Ada")
    db.session.add(new_board)
    db.session.commit()
    return new_board


# One card (unlinked)
@pytest.fixture
def one_card(app, one_board):
    new_card = Card(message="Believe in yourself", board_id=one_board.id)
    db.session.add(new_card)
    db.session.commit()
    return new_card


# Three cards on same board
@pytest.fixture
def three_cards(app, one_board):
    db.session.add_all([
        Card(message="Keep going", likes_count=0, board_id=one_board.id),
        Card(message="You matter", likes_count=2, board_id=one_board.id),
        Card(message="Stay curious", likes_count=1, board_id=one_board.id)
    ])
    db.session.commit()


# One card with created_at set (for date tests)
@pytest.fixture
def dated_card(app, one_board):
    card = Card(message="Timestamp test", board_id=one_board.id, created_at=datetime(2025, 6, 24, 12, 0, 0))
    db.session.add(card)
    db.session.commit()
    return card

# One card belongs to one board (link manually)
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    one_board.cards.append(one_card)
    db.session.commit()
    return (one_board, one_card)


@pytest.fixture
def one_board_one_card(app):
    board = Board(title="Test", owner="Tester")
    db.session.add(board)
    db.session.commit()

    card = Card(message="Sample Card", board_id=board.id)
    db.session.add(card)
    db.session.commit()

    return {"board_id": board.id, "card_id": card.id}