import pytest
from fastapi.testclient import TestClient
from main import app, db_cars

client = TestClient(app)

def setup_function():
    """Před každým testem resetujeme databázi do výchozího stavu."""
    db_cars[1] = {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85}
    db_cars[2] = {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15}
    db_cars[3] = {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60}

def test_get_cars_returns_200():
    """Test: Získání seznamu aut funguje (Integrační)."""
    response = client.get("/cars")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_reserve_available_car_success():
    """Test: Úspěšná rezervace volného vozidla (Integrační)."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Rezervace úspěšně vytvořena"

def test_reserve_unavailable_car_fails():
    """Test: Pokus o rezervaci auta v servisu (Jednotkový/Logika)."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 2})
    assert response.status_code == 400
    assert "není aktuálně k dispozici" in response.json()["detail"]

def test_reserve_nonexistent_car_fails():
    """Test: Pokus o rezervaci neexistujícího auta (Jednotkový/Logika)."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 999})
    assert response.status_code == 400
    assert "neexistuje" in response.json()["detail"]

def test_database_state_changes_after_reservation():
    """Test: Ověření změny stavu v databázi po rezervaci (Jednotkový/Stavový)."""
    assert db_cars[1]["status"] == "volné"
    client.post("/reserve", json={"user_id": 42, "car_id": 1})
    assert db_cars[1]["status"] == "rezervováno"
