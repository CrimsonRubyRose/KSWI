from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

app = FastAPI(title="EV Sharing API")

# --- DATOVÁ VRSTVA (In-memory simulace) ---
db_cars = {
    1: {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85},
    2: {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15},
    3: {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60}
}

class ReservationRequest(BaseModel):
    user_id: int
    car_id: int

# --- KOMPONENTA: Rezervační služba (Úkol 3) ---
class ReservationService:
    @staticmethod
    def create_reservation(user_id: int, car_id: int) -> dict:
        print(f"\n[START] Rezervace auta {car_id} pro uživatele {user_id}")
        car = db_cars.get(car_id)
        
        if not car or car["status"] != "volné":
            print(f"[ERROR] Auto {car_id} není dostupné.")
            raise ValueError("Vozidlo není k dispozici.")

        # Simulace procesu
        car["status"] = "v procesu platby"
        print(f"[LOG - Platební brána] Autorizace platby...")
        
        # Success
        car["status"] = "rezervováno"
        print(f"[LOG - Databáze] SUCCESS: Auto {car_id} rezervováno.")
        
        return {"status": "ok", "message": "Rezervace vytvořena", "car": car}

    @staticmethod
    def release_car(car_id: int) -> dict:
        print(f"\n[START] Uvolnění auta {car_id} do oběhu")
        car = db_cars.get(car_id)
        
        if not car:
            print(f"[ERROR] Auto {car_id} neexistuje.")
            raise ValueError("Vozidlo nenalezeno.")

        # Jednoduchá změna stavu
        puvodni_stav = car["status"]
        car["status"] = "volné"
        
        print(f"[LOG - Databáze] Změna stavu z '{puvodni_stav}' na 'volné'.")
        print(f"[LOG - Fakturační služba] Jízda uzavřena, záznam uložen.")
        
        return {
            "status": "ok", 
            "message": f"Vozidlo bylo úspěšně uvolněno (původní stav: {puvodni_stav})",
            "car": car
        }
    
    @staticmethod
    def set_to_service(car_id: int, reason: str = "Nespecifikováno") -> dict:
        print(f"\n[START] Odeslání auta {car_id} do servisu")
        car = db_cars.get(car_id)
        
        if not car:
            print(f"[ERROR] Auto {car_id} neexistuje.")
            raise ValueError("Vozidlo nenalezeno.")

        # Změna stavu na servis
        stary_stav = car["status"]
        car["status"] = "v servisu"
        
        print(f"[LOG - Databáze] ZÁPIS: Stav auta {car_id} změněn z '{stary_stav}' na 'v servisu'.")
        print(f"[LOG - Správa vozidel] Notifikace technikovi: Auto {car_id} vyžaduje kontrolu. Důvod: {reason}")
        
        return {
            "status": "ok",
            "message": f"Auto {car_id} bylo vyřazeno z oběhu a nahlášeno servisu.",
            "details": car
        }

# --- ENDPOINTY (REST API Controller) ---

@app.post("/reserve")
async def reserve_car(request: ReservationRequest):
    try:
        return ReservationService.create_reservation(request.user_id, request.car_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/service/{car_id}")
async def send_to_service(car_id: int, reason: str = "Hlášena porucha uživatelem"):
    try:
        return ReservationService.set_to_service(car_id, reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/release")
async def release_car(car_id: int):
    try:
        return ReservationService.release_car(car_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
