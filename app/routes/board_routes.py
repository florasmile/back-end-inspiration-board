from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from app.routes.helpers import validate_model, create_model

from ..db import db

bp = Blueprint("board_bp", __name__, url_prefix="/boards")


@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)


@bp.get("")
def get_all_boards():
    query = db.select(Board)
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Board.title.ilike(f"%{title_param}%"))

    boards = db.session.scalars(query.order_by(Board.id))
    boards_response = [board.to_dict() for board in boards]
    return boards_response


@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return {"board": board.to_dict()}


@bp.put("/<board_id>")
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    board.update_from_dict(request_body)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#? need to figure out : should it update exist card or create a new one 
@bp.post("/<board_id>/cards")
def create_card_for_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    card_ids = request_body.get("card_ids")

    cards = []
    for card_id in card_ids:
        card = validate_model(Card, card_id)
        cards.append(card)
    board.cards = cards
    db.session.commit()

    return {"id": board.id, "task_ids": card_ids}


@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict_with_cards()
