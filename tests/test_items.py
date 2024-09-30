item_data1 = {
    "id": 1234,
    "position": 1,
    "author": "John Doe",
    "title": "Understanding SQLAlchemy",
    "views": 100
}

item_data2 = {
    "id": 5678,
    "position": 2,
    "author": "Jane Smith",
    "title": "Advanced SQLAlchemy Techniques",
    "views": 250
}


def test_create(client, reset_db, no_auth):
    response = client.post('/items', json=item_data1)
    assert response.status_code == 201

    result = response.json()
    assert result == item_data1


def test_create_duplicate(client, reset_db, no_auth):
    client.post('/items', json=item_data1)
    response = client.post('/items', json=item_data1)
    assert response.status_code == 409


def test_get(client, reset_db, no_auth):
    item_id = client.post('/items', json=item_data1).json()['id']
    response = client.get(f'/items/{item_id}')
    assert response.status_code == 200

    result = response.json()
    assert result == item_data1


def test_get_not_found(client, reset_db, no_auth):
    response = client.get(f'/items/9999')
    assert response.status_code == 404


def test_get_list(client, reset_db, no_auth):
    client.post('/items', json=item_data1)
    client.post('/items', json=item_data2)

    response = client.get('/items')
    assert response.status_code == 200

    result = response.json()
    assert result == [item_data1, item_data2]


def test_put(client, reset_db, no_auth):
    item_id = client.post('/items', json=item_data1).json()['id']
    item_data_put = {
        **item_data2,
        "id": item_id,
    }
    response = client.put(f'/items/{item_id}', json=item_data_put)
    assert response.status_code == 200

    result = response.json()
    assert result == item_data_put


def test_put_not_found(client, reset_db, no_auth):
    response = client.put('/items/9999', json=item_data1)
    assert response.status_code == 404


def test_delete(client, reset_db, no_auth):
    item_id = client.post('/items', json=item_data1).json()['id']
    response = client.delete(f'/items/{item_id}')
    assert response.status_code == 204


def test_delete_not_found(client, reset_db, no_auth):
    response = client.delete('/items/9999')
    assert response.status_code == 404
