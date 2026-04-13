import pytest
from fastapi.testclient import TestClient
from main import app, db_cars  # Předpokládá se, že hlavní kód je v main.py

# Fixture vytvoří testovacího klienta v kontrolovaném prostředí
@pytest.fixture
def client():
    return TestClient(app)

def setup_function():
    """Reset databáze před každým testem, abychom měli jistotu výsledků."""
    db_cars.clear()
    db_cars.update({
        1: {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85},
        2: {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15},
        3: {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60}
    })

def test_reserve_available_car_success(client):
    """Test 1: Úspěšná rezervace volného vozidla."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 1})
    assert response.status_code == 200
    assert db_cars[1]["status"] == "rezervováno"

def test_release_car_to_available(client):
    """Test 2: Uvolnění rezervovaného auta zpět do oběhu."""
    response = client.post(f"/release?car_id=3")
    assert response.status_code == 200
    assert db_cars[3]["status"] == "volné"

def test_send_to_service_and_fix_it(client):
    """Test 3: Poslání auta do servisu a jeho následné opravení."""
    # 1. Pošleme volné auto do servisu
    response = client.post("/service/1?reason=Defekt")
    assert response.status_code == 200
    assert db_cars[1]["status"] == "v servisu"

    # 2. Zkusíme ho rezervovat (mělo by selhat)
    res_fail = client.post("/reserve", json={"user_id": 99, "car_id": 1})
    assert res_fail.status_code == 400

    # 3. Opravíme ho (uvolníme zpět do provozu)
    client.post(f"/release?car_id=1")
    assert db_cars[1]["status"] == "volné"

def test_reserve_nonexistent_car_fails(client):
    """Test 4: Pokus o rezervaci neexistujícího auta."""
    response = client.post("/reserve", json={"user_id": 42, "car_id": 999})
    assert response.status_code == 400

def test_release_nonexistent_car_fails(client):
    """Test 5: Pokus o uvolnění auta, které neexistuje."""
    response = client.post(f"/release?car_id=999")
    assert response.status_code == 404
    assert "nenalezeno" in response.json()["detail"]

if __name__ == "__main__":
    # Spuštění testů přímo ze skriptu
    # Přidáno ignorování varování protože si pytest stěžuje že je modul už importovaný. (Triviální a nedůležité) 
    pytest.main(["-v", "-W", "ignore::pytest.PytestAssertRewriteWarning", __file__])
