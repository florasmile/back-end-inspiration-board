import json

# getting all cards from a real board returns a list of card dicts (status 200)
def test_get_cards_for_board(client, one_board_one_card):
    # Arrange
    board_id = one_board_one_card["board_id"]

    # Act
    response = client.get(f"/cards/boards/{board_id}/cards")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert type(data) is list
    assert data[0]["message"] == "Sample Card"



# using a fake board id to make sure it returns 404 not found
def test_get_cards_board_not_found(client):
    # Arrange
    fake_board_id = 9999

    # Act
    response = client.get(f"/cards/boards/{fake_board_id}/cards")

    # Assert
    assert response.status_code == 404



# successfully creating a card on a real board returns 201 and card data
def test_post_card_success(client, one_board):
    # Arrange
    board_id = one_board["board_id"]
    data = {"message": "New Test Card"}

    # Act
    response = client.post(
        f"/cards/boards/{board_id}/cards",
        json=data
    )

    # Assert
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data["message"] == "New Test Card"



# creating a card with a message over 40 chars returns 400 error
def test_post_card_message_too_long(client, one_board):
    # Arrange
    board_id = one_board["board_id"]
    data = {"message": "A" * 41}

    # Act
    response = client.post(
        f"/cards/boards/{board_id}/cards",
        json=data
    )

    # Assert
    assert response.status_code == 400



# posting a card to a fake board id returns 404
def test_post_card_board_not_found(client):
    # Arrange
    fake_board_id = 8888
    data = {"message": "test"}

    # Act
    response = client.post(
        f"/cards/boards/{fake_board_id}/cards",
        json=data
    )

    # Assert
    assert response.status_code == 404



# deleting an existing card returns 204 No Content
def test_delete_card_success(client, one_card):
    # Arrange
    card_id = one_card["card_id"]

    # Act
    response = client.delete(f"/cards/{card_id}")

    # Assert
    assert response.status_code == 204



# trying to delete a fake card id returns 404
def test_delete_card_not_found(client):
    # Arrange
    fake_card_id = 8888

    # Act
    response = client.delete(f"/cards/{fake_card_id}")

    # Assert
    assert response.status_code == 404



# liking a card increments likes_count and returns 200
def test_patch_like_card_success(client, one_card):
    # Arrange
    card_id = one_card["card_id"]

    # Act
    response = client.patch(f"/cards/{card_id}/like")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["likes_count"] == 1



# trying to like a fake card id returns 404
def test_patch_like_card_not_found(client):
    # Arrange
    fake_card_id = 8888

    # Act
    response = client.patch(f"/cards/{fake_card_id}/like")

    # Assert
    assert response.status_code == 404