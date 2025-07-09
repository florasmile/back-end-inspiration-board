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

# checks likes_count cannot be changed by PUT /cards/<card_id>
def test_put_card_does_not_update_likes_count(client, one_card):
    # Arrange
    card_id = one_card.id
    original_likes = one_card.likes_count

    # Act
    # Ignores likes_count update attempt
    update_data = {"message": "Updated Message", "likes_count": 99}
    response = client.put(f"/cards/{card_id}", json=update_data)
    assert response.status_code == 204

    # Assert
    # Refetch and check likes_count to original number
    response = client.get(f"/cards/{card_id}")
    data = response.get_json()
    assert data["cards"]["likes_count"] == original_likes


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
