from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

app = FastAPI(title="EV Sharing API")

# In-memory databáze (Simulace Datové vrstvy)
db_cars = {
    1: {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85},
    2: {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15},
    3: {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60}
}

# Datový model požadavku
class ReservationRequest(BaseModel):
    user_id: int
    car_id: int

# --- KOMPONENTA: Rezervační služba (Úkol 3) ---
class ReservationService:
    @staticmethod
    def create_reservation(user_id: int, car_id: int) -> dict:
        # Simulace komunikace s ostatními komponentami pomocí tisku do konzole (dle zadání)
        print(f"[LOG - Controller] Předávám požadavek Rezervační službě pro auto ID: {car_id}")
        
        car = db_cars.get(car_id)
        if not car:
            print(f"[ERROR - Databáze] Auto ID: {car_id} nenalezeno.")
            raise ValueError("Vozidlo neexistuje.")
        
        if car["status"] != "volné":
            print(f"[ERROR - Logika] Auto ID: {car_id} není dostupné (Stav: {car['status']}).")
            raise ValueError("Vozidlo není aktuálně k dispozici.")

        # Aktualizace stavu
        car["status"] = "rezervováno"
        print(f"[LOG - Databáze] Zápis: Stav auta ID: {car_id} změněn na 'rezervováno'.")
        print(f"[LOG - Platební brána] Asynchronní autorizace platby pro uživatele {user_id} zahájena.")
        
        return {
            "message": "Rezervace úspěšně vytvořena",
            "timestamp": str(datetime.datetime.now()),
            "car": car
        }

# --- WEBOVÉ SLUŽBY / REST API (Úkol 4) ---

@app.get("/cars")
def get_available_cars():
    """Vrátí seznam všech vozidel."""
    return list(db_cars.values())

@app.post("/reserve")
def reserve_car(request: ReservationRequest):
    """Endpoint pro vytvoření rezervace."""
    try:
        # Volání naší implementované komponenty
        result = ReservationService.create_reservation(request.user_id, request.car_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("[SYSTÉM] Startuji API server na http://127.0.0.0:8000 ...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
