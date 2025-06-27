import json

# checks POST /boards creates a new board
def test_create_board(client):
    # Arrange
    board_data = {"title": "Gratitude", "owner": "Mikaela"}

    # Act
    response = client.post("/boards", json=board_data)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Gratitude"
    assert data["owner"] == "Mikaela"

# checks GET /boards returns all boards
def test_get_all_boards(client, one_board):
    # Arrange
    # (one_board fixture creates a board already)

    # Act
    response = client.get("/boards")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(board["title"] == one_board.title for board in data)

# checks GET /boards/<board_id> returns the correct board
def test_get_one_board(client, one_board):
    # Arrange
    board_id = one_board.id

    # Act
    response = client.get(f"/boards/{board_id}")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["board"]["title"] == one_board.title

# checks PUT /boards/<board_id> updates the board
def test_put_board(client, one_board):
    # Arrange
    board_id = one_board.id
    update_data = {"title": "New Title", "owner": "Someone Else"}

    # Act
    response = client.put(f"/boards/{board_id}", json=update_data)

    # Assert
    assert response.status_code == 204

# checks DELETE /boards/<board_id> deletes the board
def test_delete_board(client, one_board):
    # Arrange
    board_id = one_board.id

    # Act
    response = client.delete(f"/boards/{board_id}")

    # Assert
    assert response.status_code == 204

# checks GET /boards/<board_id>/cards returns all cards for board
def test_get_cards_for_board(client, one_board_one_card):
    # Arrange
    board_id = one_board_one_card["board_id"]

    # Act
    response = client.get(f"/boards/{board_id}/cards")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert "cards" in data
    assert isinstance(data["cards"], list)

# checks POST /boards/<board_id>/cards creates a card on board
def test_post_card_on_board(client, one_board):
    # Arrange
    board_id = one_board.id
    card_data = {"message": "Be positive!"}

    # Act
    response = client.post(f"/boards/{board_id}/cards", json=card_data)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Be positive!"