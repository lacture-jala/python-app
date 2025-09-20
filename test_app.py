import app

client = app.app.test_client()

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the Home Route"}

def test_greet_user():
    response = client.get("/api/greet/Alex")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, Alex!"}

def test_calculate_square():
    response = client.get("/api/square/5")
    assert response.status_code == 200
    assert response.get_json() == {
        "input": 5,
        "operation": "square",
        "result": 25
    }

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

def test_404_handler():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Resource not found"}
