from flask import Blueprint, request, Response, jsonify
from app.models.board import Board
from app.models.card import Card
from app.routes.helpers import validate_model, create_model
from ..db import db
from flasgger import swag_from

bp = Blueprint("board_bp", __name__, url_prefix="/boards")

@bp.post("")
@swag_from({
    "tags": ["Boards"],
    "summary": "Create a new board",
    "consumes": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "owner": {"type": "string"}
                },
                "required": ["title", "owner"]
            }
        }
    ],
    "responses": {
        201: {"description": "Board created successfully"},
        400: {"description": "Missing or invalid fields"}
    }
})
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)


@bp.get("")
@swag_from({
    "tags": ["Boards"],
    "summary": "Get all boards",
    "parameters": [
        {
            "name": "title",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Filter boards by title"
        }
    ],
    "responses": {
        200: {
            "description": "List of boards",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "board_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "owner": {"type": "string"}
                    }
                }
            }
        }
    }
})
def get_all_boards():
    query = db.select(Board)
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Board.title.ilike(f"%{title_param}%"))

    boards = db.session.scalars(query.order_by(Board.id))
    boards_response = [board.to_dict() for board in boards]
    return boards_response


@bp.get("/<board_id>")
@swag_from({
    "tags": ["Boards"],
    "summary": "Get one board",
    "parameters": [
        {
            "name": "board_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {
            "description": "Board data",
            "schema": {
                "type": "object",
                "properties": {
                    "board": {
                        "type": "object",
                        "properties": {
                            "board_id": {"type": "integer"},
                            "title": {"type": "string"},
                            "owner": {"type": "string"}
                        }
                    }
                }
            }
        },
        404: {"description": "Board not found"}
    }
})
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return jsonify({"board": board.to_dict()})


@bp.put("/<board_id>")
@swag_from({
    "tags": ["Boards"],
    "summary": "Update a board",
    "parameters": [
        {"name": "board_id", "in": "path", "type": "integer", "required": True},
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "owner": {"type": "string"}
                }
            }
        }
    ],
    "responses": {
        204: {"description": "Board updated"},
        400: {"description": "Invalid data"},
        404: {"description": "Board not found"}
    }
})
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    board.update_from_dict(request_body)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<board_id>")
@swag_from({
    "tags": ["Boards"],
    "summary": "Delete a board",
    "parameters": [
        {"name": "board_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        204: {"description": "Board deleted"},
        404: {"description": "Board not found"}
    }
})
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.get("/<board_id>/cards")
@swag_from({
    "tags": ["Boards"],
    "summary": "Get all cards for a board",
    "parameters": [
        {"name": "board_id", "in": "path", "type": "integer", "required": True}
    ],
    "responses": {
        200: {
            "description": "Board and its cards",
            "schema": {
                "type": "object",
                "properties": {
                    "board_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "owner": {"type": "string"},
                    "cards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "message": {"type": "string"},
                                "likes_count": {"type": "integer"}
                            }
                        }
                    }
                }
            }
        },
        404: {"description": "Board not found"}
    }
})
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)

    return board.to_dict_with_cards()


@bp.get("/with-cards")
@swag_from({
    "tags": ["Boards"],
    "summary": "⚠️ [DEBUG ONLY] Get all boards with their cards",
    "description": "⚠️ This endpoint is for debugging only. **Do not use in production.**",
    "deprecated": True,
    "responses": {
        200: {
            "description": "Boards and cards",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "board_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "owner": {"type": "string"},
                        "cards": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "message": {"type": "string"},
                                    "likes_count": {"type": "integer"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_all_boards_with_cards():
    query = db.select(Board).order_by(Board.id)
    boards = db.session.scalars(query).all()

    boards_with_cards = [board.to_dict_with_cards() for board in boards]

    return boards_with_cards, 200


@bp.post("/<board_id>/cards")
@swag_from({
    "tags": ["Boards"],
    "summary": "Create card for board",
    "parameters": [
        {"name": "board_id", "in": "path", "type": "integer", "required": True},
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        }
    ],
    "responses": {
        201: {"description": "Card created"},
        400: {"description": "Invalid request"},
        404: {"description": "Board not found"}
    }
})
def create_card_for_board(board_id):
    validate_model(Board, board_id)
    request_body = request.get_json()
    request_body["board_id"] = int(board_id)

    return create_model(Card, request_body)


@bp.post("/<board_id>/cards/assign")
@swag_from({
    "tags": ["Boards"],
    "summary": "Reassign cards to board",
    "parameters": [
        {"name": "board_id", "in": "path", "type": "integer", "required": True},
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "card_ids": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                },
                "required": ["card_ids"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "Cards reassigned",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "reassigned_cards": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "card_id": {"type": "integer"},
                                "from_board": {"type": "integer"},
                                "to_board": {"type": "integer"}
                            }
                        }
                    }
                }
            }
        },
        400: {"description": "No card_ids provided"},
        404: {"description": "Board or card not found"}
    }
})
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
