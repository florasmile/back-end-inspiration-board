from flask import Blueprint, request, Response, jsonify
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

    return jsonify({"board": board.to_dict()})


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


@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)

    return board.to_dict_with_cards()

# get all boards with their cards for debugging. DO NOT USE IN PRODUCTION
@bp.get("/with-cards")
def get_all_boards_with_cards():
    query = db.select(Board).order_by(Board.id)
    boards = db.session.scalars(query).all()

    boards_with_cards = [board.to_dict_with_cards() for board in boards]

    return boards_with_cards, 200


@bp.post("/<board_id>/cards")
def create_card_for_board(board_id):
    validate_model(Board, board_id)
    request_body = request.get_json()
    request_body["board_id"] = int(board_id)

    return create_model(Card, request_body)


#reassign a card from one board to another
@bp.post("/<board_id>/cards/assign")
def reassign_cards_to_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    card_ids = request_body.get("card_ids", [])

    if not card_ids:
        return {"message": "Request must include a list of card_ids"}, 400

    updated_cards = []
    for card_id in card_ids:
        card = validate_model(Card, card_id)
        previous_board = card.board_id
        card.board_id = board.id 
        updated_cards.append({
            "card_id": card.id,
            "from_board": previous_board,
            "to_board": board.id
        })

    db.session.commit()

    return {
        "message": f"Moved {len(updated_cards)} card(s) to board {board.id}",
        "reassigned_cards": updated_cards
    }, 200
