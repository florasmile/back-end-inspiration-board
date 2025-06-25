from flask import Blueprint, request, Response
from ..db import db
from ..models.board import Board
from ..models.card import Card

# GET /boards/<board_id>/cards
# POST /boards/<board_id>/cards
# DELETE /cards/<card_id>
# PUT /cards/<card_id>/like
# validate_model refactor 

# all routes end with /cards
bp = Blueprint("cards_bp", __name__, url_prefix="/cards")


# GET /cards/boards/1/cards
# get all cards for a specific board
@bp.get("/boards/<int:board_id>/cards")
def get_cards_for_board(board_id):
    # fetch board by id, return 404 if missing
    board = Board.query.get(board_id)
    if not board:
        return {"error": "Board not found"}, 404

    # get all cards with matching board_id in route
    cards = Card.query.filter_by(board_id=board_id).all()
    # return list of card dicts
    return [card.to_dict() for card in cards]


# POST /cards/boards/1/cards
# create a card for a specific board
@bp.post("/boards/<int:board_id>/cards")
def create_card_for_board(board_id):
    # confirm board exists
    board = Board.query.get(board_id)
    if not board:
        return {"error": "Board not found"}, 404

    # get json data from request
    request_body = request.get_json()

    # create new card using Card model
    new_card = Card(
        # get message value sent from fronted json
        message=request_body["message"],
        board_id=board.board_id
    )

    # stage & commit the new card to db
    db.session.add(new_card)
    db.session.commit()

    # return the new card as dict with 201 (created)
    return new_card.to_dict(), 201


# DELETE /cards/1 
# delete a card by id
@bp.delete("/<int:card_id>")
def delete_card(card_id):
    # find and delete the card by id
    card = Card.query.get(card_id)
    if not card:
        return {"error": "Card not found"}, 404

    # stage & commit deletion to db
    db.session.delete(card)
    db.session.commit()

    # successful delete
    return Response(status=204, mimetype="application/json")


# PATCH /cards/1/like
# like a card by id (increment likes_count)
@bp.patch("/<int:card_id>/like")
def like_card(card_id):
    # get the card by id
    card = Card.query.get(card_id)
    if not card:
        return {"error": "Card not found"}, 404

    # add 1 to likes count
    card.likes_count += 1
    db.session.commit()

    # return updated card as dict
    return card.to_dict()
