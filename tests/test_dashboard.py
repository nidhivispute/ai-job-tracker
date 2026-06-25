import fitz


def make_pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def test_dashboard_stats(client, auth_headers, tmp_path, monkeypatch):
    import app.services.resume_service as resume_service

    monkeypatch.setattr(resume_service, "UPLOAD_DIR", tmp_path / "resumes")

    client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS Git",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "AnotherTech",
            "job_title": "Software Intern",
            "job_description": "React TypeScript CSS HTML Git",
            "job_url": "https://example.com/job2",
            "location": "Remote",
            "status": "applied",
        },
    )

    pdf_bytes = make_pdf_bytes("Python FastAPI PostgreSQL Git backend development.")

    upload_response = client.post(
        "/api/resumes/upload",
        headers=auth_headers,
        files={
            "file": ("resume.pdf", pdf_bytes, "application/pdf")
        },
        data={
            "title": "Backend Resume"
        },
    )

    resume_id = upload_response.json()["id"]

    jobs_response = client.get("/api/jobs/", headers=auth_headers)
    job_id = jobs_response.json()[0]["id"]

    client.post(
        "/api/analysis/resume-match",
        headers=auth_headers,
        json={
            "resume_id": resume_id,
            "job_id": job_id,
        },
    )

    response = client.get("/api/dashboard/stats", headers=auth_headers)

    assert response.status_code == 200

    data = response.json()

    assert data["total_jobs"] == 2
    assert data["jobs_by_status"]["saved"] == 1
    assert data["jobs_by_status"]["applied"] == 1
    assert data["total_resumes"] == 1
    assert data["total_analyses"] == 1
    assert data["average_match_score"] is not None

