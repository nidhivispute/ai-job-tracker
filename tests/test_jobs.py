def test_create_job(client, auth_headers):
    response = client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company_name"] == "ExampleTech"
    assert data["status"] == "saved"


def test_list_jobs(client, auth_headers):
    client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    response = client.get("/api/jobs/", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_job_status(client, auth_headers):
    create_response = client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    job_id = create_response.json()["id"]

    update_response = client.patch(
        f"/api/jobs/{job_id}",
        headers=auth_headers,
        json={
            "status": "applied"
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "applied"


def test_invalid_job_status_fails(client, auth_headers):
    create_response = client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    job_id = create_response.json()["id"]

    response = client.patch(
        f"/api/jobs/{job_id}",
        headers=auth_headers,
        json={
            "status": "random"
        },
    )

    assert response.status_code == 422


def test_delete_job(client, auth_headers):
    create_response = client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    job_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/jobs/{job_id}", headers=auth_headers)

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Job deleted successfully"

    get_response = client.get(f"/api/jobs/{job_id}", headers=auth_headers)

    assert get_response.status_code == 404