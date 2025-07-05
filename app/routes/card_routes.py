from flask import Blueprint, request, Response, jsonify
from flasgger import swag_from
from ..db import db
from ..models.board import Board
from ..models.card import Card
from .helpers import validate_model


bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.get("")
@swag_from("../../docs/cards/get_all_cards.yml")
def get_all_cards():
    query = db.select(Card)
    message_param = request.args.get("message")

    if message_param:
        query = query.where(Card.message.ilike(f"%{message_param}%"))

    cards = db.session.scalars(query.order_by(Card.id))
    cards_response = [card.to_dict() for card in cards]
    return cards_response


@bp.get("/<card_id>")
@swag_from("../../docs/cards/get_one_card.yml")
def get_one_card(card_id):
    card = validate_model(Card, card_id)

    return jsonify({"cards": card.to_dict()})


#updating a single card 
@bp.put("/<card_id>")
@swag_from("../../docs/cards/update_card.yml")
def update_card_on_board(card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()
    card.update_from_dict(request_body)

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<card_id>")
@swag_from("../../docs/cards/delete_card.yml")
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<card_id>/like")
@swag_from("../../docs/cards/like_card.yml")
def like_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict()
