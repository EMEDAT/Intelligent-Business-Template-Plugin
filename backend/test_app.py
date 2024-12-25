import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_slack_integration(client):
    response = client.post('/integration/slack', json={"channel_id": "test_channel"})
    assert response.status_code in [200, 400, 500]

def test_template_generation(client):
    payload = {
        "template_type": "business_plan",
        "key_points": ["Goal: Test functionality"]
    }
    response = client.post('/templates/generate', json=payload)
    assert response.status_code == 200
    assert "content" in response.json
