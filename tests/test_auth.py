user_data = {
    "username": "qwerty",
    "password": "Abg%sad12@s"
}


def test_auth(client, reset_db):
    client.post('/users', json=user_data)

    response = client.post('/login', json=user_data)
    assert response.status_code == 200

    token = response.json()['token']
    response = client.get('/items', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200


def test_no_auth(client):
    response = client.get('/items')
    assert response.status_code == 401


def test_auth_fail(client, reset_db):
    client.post('/users', json=user_data)

    response = client.post('/login', json=user_data)
    assert response.status_code == 200

    token = response.json()['token'][:-1]
    response = client.get('/items', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 401
