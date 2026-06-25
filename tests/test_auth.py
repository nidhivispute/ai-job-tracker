def test_signup_success(client, unique_email):
    response = client.post(
        "/api/auth/signup",
        json={
            "email": unique_email,
            "password": "password123",
            "full_name": "Test User",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == unique_email
    assert data["full_name"] == "Test User"
    assert "hashed_password" not in data


def test_duplicate_signup_fails(client, unique_email):
    payload = {
        "email": unique_email,
        "password": "password123",
        "full_name": "Test User",
    }

    first_response = client.post("/api/auth/signup", json=payload)
    second_response = client.post("/api/auth/signup", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email is already registered"


def test_login_success(client, unique_email):
    password = "password123"

    client.post(
        "/api/auth/signup",
        json={
            "email": unique_email,
            "password": password,
            "full_name": "Test User",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": unique_email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert data["email"]
    assert data["full_name"] == "Test User"


def test_get_current_user_without_token_fails(client):
    response = client.get("/api/auth/me")

    assert response.status_code in [401, 403]