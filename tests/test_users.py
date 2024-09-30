user_data1 = {
    "username": "qwerty",
    "password": "Abg%sad12@s"
}


user_data2 = {
    "username": "qwerty123",
    "password": "aJ7Nb(*a"
}


def test_create(client, reset_db, no_auth):

    response = client.post('/users', json=user_data1)
    assert response.status_code == 201

    result = response.json()
    del result['id']
    expected = {
        **user_data1,
    }
    del expected['password']
    assert result == expected

    response = client.post('/users', json=user_data1)
    assert response.status_code == 409


def test_create_duplicate(client, reset_db):
    client.post('/users', json=user_data1)
    response = client.post('/users', json=user_data1)
    assert response.status_code == 409


def test_get(client, reset_db, no_auth):

    response = client.get('/users/1')
    assert response.status_code == 404

    response = client.post('/users', json=user_data1)
    id = response.json()['id']
    response = client.get(f'/users/{id}')
    assert response.status_code == 200

    result = response.json()
    del result['id']
    expected = {
        **user_data1,
    }
    del expected['password']
    assert result == expected


def test_get_not_found(client, reset_db, no_auth):
    response = client.get('/users/1')
    assert response.status_code == 404


def test_get_all(client, reset_db, no_auth):

    client.post('/users', json=user_data1)
    client.post('/users', json=user_data2)
    response = client.get('/users')
    assert response.status_code == 200

    result = response.json()
    assert len(result) == 2


def test_update(client, reset_db, no_auth):

    response = client.post('/users', json=user_data1)
    id = response.json()['id']
    response = client.put(f'/users/{id}', json=user_data2)
    assert response.status_code == 200

    result = response.json()
    expected = {
        'id': id,
        **user_data2,
    }
    del expected['password']
    assert result == expected


def test_update_not_found(client, reset_db, no_auth):
    response = client.put('/users/1', json=user_data2)
    assert response.status_code == 404


def test_delete(client, reset_db, no_auth):

    response = client.delete('/users/1')
    assert response.status_code == 404

    response = client.post('/users', json=user_data1)
    id = response.json()['id']
    response = client.delete(f'/users/{id}')
    assert response.status_code == 204

    response = client.get(f'/users')
    result = response.json()
    expected = []
    assert result == expected


def test_delete_not_found(client, reset_db, no_auth):
    response = client.delete('/users/1')
    assert response.status_code == 404
