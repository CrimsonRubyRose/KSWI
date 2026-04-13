import pytest
from fastapi.testclient import TestClient
from main import app, db_cars # Předpokládám, že se tvůj soubor jmenuje main.py

client = TestClient(app)

def setup_function():
    """Reset databáze před každým testem, abychom měli jistotu výsledků."""
    db_cars.clear()
    db_cars.update({
        1: {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85},
        2: {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15},
        3: {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60}
    })

def test_reserve_available_car_success():
    """Test: Úspěšná rezervace volného vozidla."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 1})
    assert response.status_code == 200
    assert db_cars[1]["status"] == "rezervováno"

def test_release_car_to_available():
    """Test: Uvolnění rezervovaného auta zpět do oběhu."""
    # Nejdřív uvolníme auto 3, které je v DB jako rezervované
    response = client.post("/release?car_id=3")
    assert response.status_code == 200
    assert db_cars[3]["status"] == "volné"

def test_send_to_service_and_fix_it():
    """Test: Poslání auta do servisu a jeho následné opravení (uvolnění)."""
    # 1. Pošleme volné auto do servisu
    response = client.post("/service/1?reason=Defekt")
    assert response.status_code == 200
    assert db_cars[1]["status"] == "v servisu"

    # 2. Zkusíme ho rezervovat (mělo by selhat)
    res_fail = client.post("/reserve", json={"user_id": 99, "car_id": 1})
    assert res_fail.status_code == 400

    # 3. Opravíme ho (release)
    client.post("/release?car_id=1")
    assert db_cars[1]["status"] == "volné"

def test_reserve_nonexistent_car_fails():
    """Test: Pokus o rezervaci neexistujícího auta."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 999})
    assert response.status_code == 400 # Tvůj kód vrací 400 ValueError

def test_release_nonexistent_car_fails():
    """Test: Pokus o uvolnění auta, které neexistuje (ID 999)."""
    response = client.post("/release?car_id=999")
    assert response.status_code == 404
    assert "nenalezeno" in response.json()["detail"]

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
