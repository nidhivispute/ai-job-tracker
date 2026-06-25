import fitz


def make_pdf_bytes(text: str) -> bytes:
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)

    pdf_bytes = document.tobytes()
    document.close()

    return pdf_bytes


def test_resume_upload_and_match_analysis(client, auth_headers, tmp_path, monkeypatch):
    import app.services.resume_service as resume_service

    monkeypatch.setattr(resume_service, "UPLOAD_DIR", tmp_path / "resumes")

    pdf_bytes = make_pdf_bytes(
        "Python FastAPI PostgreSQL Git REST API backend development."
    )

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

    assert upload_response.status_code == 201

    resume_id = upload_response.json()["id"]

    job_response = client.post(
        "/api/jobs/",
        headers=auth_headers,
        json={
            "company_name": "ExampleTech",
            "job_title": "Backend Intern",
            "job_description": "Python FastAPI PostgreSQL Docker AWS Git REST API",
            "job_url": "https://example.com/job",
            "location": "Remote",
            "status": "saved",
        },
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    analysis_response = client.post(
        "/api/analysis/resume-match",
        headers=auth_headers,
        json={
            "resume_id": resume_id,
            "job_id": job_id,
        },
    )

    assert analysis_response.status_code == 201

    data = analysis_response.json()

    assert data["resume_id"] == resume_id
    assert data["job_id"] == job_id
    assert data["match_score"] > 0
    assert "python" in data["strong_matches"]
    assert "docker" in data["missing_skills"] or "aws" in data["missing_skills"]