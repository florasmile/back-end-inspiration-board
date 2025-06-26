from flask import Blueprint, request, Response
from ..db import db
from ..models.board import Board
from ..models.card import Card
from .helpers import validate_model, create_model


bp = Blueprint("cards_bp", __name__)


# GET /boards/1/cards
# get all cards for a specific board
@bp.get("/boards/<int:board_id>/cards")
def get_cards_for_board(board_id):
    # helper func
    board = validate_model(Board, board_id)

    # get all cards with matching board_id in route
    cards = Card.query.filter_by(board_id=board_id).all()

    # return list of card dicts
    return [card.to_dict() for card in cards]


# POST /boards/1/cards
# create a card for a specific board
@bp.post("/boards/<int:board_id>/cards")
def create_card_for_board(board_id):
    # helper func
    board = validate_model(Board, board_id)

    # get json data from request
    request_body = request.get_json()

    # insert the board_id into the request data so Card gets it
    request_body["board_id"] = board_id

    # helper func
    return create_model(Card, request_body)


# DELETE /cards/1 
# delete a card by id
@bp.delete("/cards/<int:card_id>")
def delete_card(card_id):
    # helper func
    card = validate_model(Card, card_id)

    # stage & commit deletion to db
    db.session.delete(card)
    db.session.commit()

    # successful delete
    return Response(status=204, mimetype="application/json")


# PATCH /cards/1/like
# like a card by id (increment likes_count)
@bp.patch("/cards/<int:card_id>/like")
def like_card(card_id):
    # helper func
    card = validate_model(Card, card_id)

    # add 1 to likes count
    card.likes_count += 1
    db.session.commit()

    # return updated card as dict
    return card.to_dict()