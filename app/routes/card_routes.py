from flask import Blueprint, request, Response, jsonify
from flasgger import swag_from
from ..db import db
from ..models.board import Board
from ..models.card import Card
from .helpers import validate_model


bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.get("")
@swag_from({
    "tags": ["Cards"],
    "responses": {
        200: {
            "description": "A list of all cards",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "message": {"type": "string"},
                        "likes_count": {"type": "integer"},
                        "board_id": {"type": "integer"},
                    }
                }
            }
        }
    },
    "parameters": [
        {
            "name": "message",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Filter cards by message substring"
        }
    ]
})
def get_all_cards():
    query = db.select(Card)
    message_param = request.args.get("message")

    if message_param:
        query = query.where(Card.message.ilike(f"%{message_param}%"))

    cards = db.session.scalars(query.order_by(Card.id))
    cards_response = [card.to_dict() for card in cards]
    return cards_response


@bp.get("/<card_id>")
@swag_from({
    "tags": ["Cards"],
    "parameters": [
        {
            "name": "card_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the card to retrieve"
        }
    ],
    "responses": {
        200: {
            "description": "Card data",
            "schema": {
                "type": "object",
                "properties": {
                    "cards": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "message": {"type": "string"},
                            "likes_count": {"type": "integer"},
                            "board_id": {"type": "integer"},
                        }
                    }
                }
            }
        },
        404: {
            "description": "Card not found"
        }
    }
})
def get_one_card(card_id):
    card = validate_model(Card, card_id)

    return jsonify({"cards": card.to_dict()})


#updating a single card 
@bp.put("/<card_id>")
@swag_from({
    "tags": ["Cards"],
    "parameters": [
        {
            "name": "card_id",
            "in": "path",
            "type": "integer",
            "required": True
        },
        {
            "in": "body",
            "name": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "likes_count": {"type": "integer"}
                }
            }
        }
    ],
    "responses": {
        204: {"description": "Card updated"},
        400: {"description": "Invalid request body"},
        404: {"description": "Card not found"}
    }
})
def update_card_on_board(card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()
    card.update_from_dict(request_body)

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@bp.delete("/<card_id>")
@swag_from({
    "tags": ["Cards"],
    "parameters": [
        {
            "name": "card_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        204: {"description": "Card deleted"},
        404: {"description": "Card not found"}
    }
})
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<card_id>/like")
@swag_from({
    "tags": ["Cards"],
    "parameters": [
        {
            "name": "card_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the card to like"
        }
    ],
    "responses": {
        200: {
            "description": "Card liked",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "message": {"type": "string"},
                    "likes_count": {"type": "integer"},
                    "board_id": {"type": "integer"},
                }
            }
        },
        404: {
            "description": "Card not found"
        }
    }
})
def like_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()

    return card.to_dict()
