from flask import Blueprint, request, Response, jsonify
from ..db import db
from ..models.board import Board
from ..models.card import Card
from .helpers import validate_model, create_model


bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.get("/<card_id>")
def get_one_card(card_id):
    card = validate_model(Card, card_id)

    return jsonify({"cards": card.to_dict()})

#get all cards assign for board from the cards site
@bp.get("/boards/<board_id>/cards")
def get_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict_with_cards()["cards"]


@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict()
