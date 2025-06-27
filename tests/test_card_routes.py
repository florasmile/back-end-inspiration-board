import json

# checks GET /cards/<card_id> returns the correct card
def test_get_one_card(client, one_card):
    # Arrange
    card_id = one_card.id

    # Act
    response = client.get(f"/cards/{card_id}")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["cards"]["message"] == one_card.message

# checks PUT /cards/<card_id> updates the card
def test_put_card(client, one_card):
    # Arrange
    card_id = one_card.id
    update_data = {"message": "Updated Message", "likes_count": 5}

    # Act
    response = client.put(f"/cards/{card_id}", json=update_data)

    # Assert
    assert response.status_code == 204

# checks DELETE /cards/<card_id> deletes the card
def test_delete_card(client, one_card):
    # Arrange
    card_id = one_card.id

    # Act
    response = client.delete(f"/cards/{card_id}")

    # Assert
    assert response.status_code == 204

# checks PATCH /cards/<card_id>/like increases likes_count
def test_patch_like_card(client, one_card):
    # Arrange
    card_id = one_card.id

    # Act
    response = client.patch(f"/cards/{card_id}/like")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["likes_count"] == 1
