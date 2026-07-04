from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime

app = FastAPI(title="EV Sharing API")

#   DATABÁZE
db_cars = {
    1: {"id": 1, "model": "Škoda Enyaq", "status": "volné", "battery": 85, "userid": None},
    2: {"id": 2, "model": "Tesla Model 3", "status": "v servisu", "battery": 15, "userid": None},
    3: {"id": 3, "model": "Hyundai Ioniq 5", "status": "rezervováno", "battery": 60, "userid": "4"}
}

class ReservationRequest(BaseModel):
    user_id: int
    car_id: int

#   KOMPONENTA: Rezervační služba (Úkol 3) 
class ReservationService:
    @staticmethod
    def create_reservation(user_id: int, car_id: int) -> dict:
        print(f"\n[START] Rezervace auta {car_id} pro uživatele {user_id}")
        car = db_cars.get(car_id)
        
        if not car:
            print(f"[ERROR] Auto {car_id} neexistuje.")
            raise ValueError("Vozidlo nenalezeno.")
        
        if car["status"] != "volné":
            raise ValueError("Vozidlo není k dispozici.")

        # Simulace procesu
        car["status"] = "v procesu platby"
        print(f"[LOG - Platební brána] Autorizace platby...")
        
        # Success
        car["status"] = "rezervováno"
        car["userid"] = f"{user_id}" 
        print(f"[LOG - Databáze] SUCCESS: Auto {car_id} rezervováno.")
        
        return {"status": "ok", "message": "Rezervace vytvořena", "car": car}

    @staticmethod
    def release_car(car_id: int) -> dict:
        print(f"\n[START] Uvolnění auta {car_id} do oběhu")
        car = db_cars.get(car_id)
        
        if not car:
            print(f"[ERROR] Auto {car_id} neexistuje.")
            raise ValueError("Vozidlo nenalezeno.")
        
        if car["status"] == "volné":
            raise ValueError("Vozidlo už je volné.")

        # Jednoduchá změna stavu
        puvodni_stav = car["status"]
        car["status"] = "volné"
        car["userid"] = None 
        
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
        
        if car["status"] != "volné":
            raise ValueError("Vozidlo není k dispozici.")



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

#  REST API Controller

@app.post("/reserve")
async def reserve_car(user_id: int, car_id: int):
    try:
        # Tady už nepíšeme request.user_id, ale rovnou user_id
        return ReservationService.create_reservation(user_id, car_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    



@app.post("/service")
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
    
@app.get("/cars")
async def get_all_cars():
    return db_cars

if __name__ == "__main__":
    import uvicorn
   # uvicorn.run(app, host="0.0.0.0", port=8000) # TOTO PAK ODKOMENTOVAT!!  Komentováne pro Ukázku "konzole" 
## Připomínka použít http://0.0.0.0:8000/docs    



#     Ukázka konzole


# 1. Úspěšná rezervace volného vozidla

    ReservationService.create_reservation(user_id=42, car_id=1)
    assert db_cars[1]["status"] == "rezervováno", "Test 1 selhal: Auto 1 by mělo být rezervováno!"
    print("Test 1 OK: Auto zarezervováno.")

    # 2. Pokus o rezervaci vozidla, které je v servisu (selhání)
    try:
        ReservationService.create_reservation(user_id=99, car_id=2)
        assert False, "Test 2 selhal: Rezervace auta v servisu MĚLA vyhodit chybu, ale prošla!"
    except ValueError as e:
        assert str(e) == "Vozidlo není k dispozici.", f"Test 2 selhal: Vyhozena špatná hláška ({e})"
        print("Test 2 OK: Systém správně zablokoval rezervaci auta v servisu.")

        # 3. Uvolnění auta 1

    ReservationService.release_car(car_id=1)
    assert db_cars[1]["status"] == "volné", "Test 3 selhal: Auto 1 se po uvolnění nezměnilo na volné!"
    print("Test 3 OK: Auto uvolněno z rezervace.")



    # 4. Odeslání vozidla do servisu z důvodu poruchy

    ReservationService.set_to_service(car_id=1, reason="Nízký tlak v pneumatikách")
    assert db_cars[1]["status"] == "v servisu", "Test 4 selhal: Auto 1 nebylo odesláno do servisu!"
    print("Test 4 OK: Auto odesláno do servisu.")

    # 5. Krok 4 ale auto není volné protože je v servisu
    try:
        ReservationService.set_to_service(car_id=1, reason="Nízký tlak v pneumatikách")
        assert False, "Test 5 selhal: Auto už v servisu je, mělo to vyhodit chybu!"
    except ValueError as e:
        print("Test 5 OK: Systém zabránil duplicitnímu odeslání do servisu.")

    # 6. Uvolnění vozidla ze servisu zpět do oběhu

    ReservationService.release_car(car_id=1)
    assert db_cars[1]["status"] == "volné", "Test 6 selhal: Auto 1 nezměnilo stav ze servisu na volné!"
    print("Test 6 OK: Auto uvolněno ze servisu zpět do provozu.")

    print("--- Konec jednotkových testů ---")

