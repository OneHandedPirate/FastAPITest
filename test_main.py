from fastapi.testclient import TestClient
from app import main
from random import choice
from string import ascii_letters, digits

ALPHANUM = ascii_letters + digits

client = TestClient(main.app)


test_account = {"username": ''.join(choice(ALPHANUM) for _ in "123456"),
                "password": ''.join(choice(ALPHANUM) for _ in range(9))}
token = None


def test_create_account():
    response = client.post("/create_account", json=test_account)

    assert response.status_code == 201
    assert response.json()["username"] == test_account["username"]


def test_create_account_duplicate():
    response = client.post("/create_account", json=test_account)

    assert response.status_code == 400
    assert response.json()["detail"] == f"The user {test_account['username']} " \
                                         f"is already registered"


def test_create_account_short_username():
    short_name_info = {"username": "test", "password": "helloworld"}

    response = client.post("/create_account", json=short_name_info)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value has at least 5 characters"
    assert response.json()["detail"][0]["loc"][1] == "username"


def test_create_account_short_password():
    short_pass_info = {"username": "test_account", "password": "hell"}

    response = client.post("/create_account", json=short_pass_info)

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value has at least 8 characters"
    assert response.json()["detail"][0]["loc"][1] == "password"


def test_login():
    response = client.post("/login", data=test_account)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == 'bearer'

    global token
    token = response.json()["access_token"]


def test_login_bad_creds():
    wrong_creds = {"username": "sfgsdfsdgdfdgdfgdfgdfgd", "password": "gdfgdfgdfgd"}

    response = client.post("/login", data=wrong_creds)

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credentials"}


def test_get_info():
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/get_info", headers=headers)

    assert response.status_code == 200
    assert "salary" in response.json() and "promotion_date" in response.json()


def test_get_info_wrongs_token():
    header_wrong_token = {"Authorization": f"Bearer {token[:-1]}"}

    response = client.get("/get_info", headers=header_wrong_token)

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_account():
    response = client.delete(f"delete_account/{test_account['username']}")
    assert response.status_code == 204


def test_delete_non_existent_account():
    response = client.delete(f"delete_account/{test_account['username']}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"User {test_account['username']} does not exist"}