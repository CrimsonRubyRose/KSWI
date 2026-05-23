# 3. Vývoj komponent a API

Pro implementaci klíčové komponenty byl zvolen jazyk **Python** s využitím moderního webového frameworku **FastAPI**. Zvolená komponenta je **Rezervační služba (ReservationService)**, která řeší ověření dostupnosti vozidla a změnu jeho stavu.

## 3.1 Komunikace komponent
Zadání vyžaduje ukázku komunikace komponent. Protože se jedná o konzolovou aplikaci bez napojení na reálnou produkční databázi a externí služby, je meziprocesová komunikace simulována výpisem do standardního výstupu (konzole) v reálném čase.

**Příklad výstupu v konzoli při úspěšné rezervaci:**
```text
[LOG - Controller] Předávám požadavek Rezervační službě pro auto ID: 1
[LOG - Databáze] Zápis: Stav auta ID: 1 změněn na 'rezervováno'.
[LOG - Platební brána] Asynchronní autorizace platby pro uživatele 99 zahájena.
```

# 4. Webové služby

Nad vytvořenou komponentou bylo vystaveno REST API pro komunikaci s frontendem (mobilní aplikací).

## 4.1 Seznam endpointů
* `GET /cars` - Vrací aktuální stav celé flotily (pro vykreslení do mapy).
* `POST /reserve` - Přijímá JSON s ID uživatele a ID vozidla a vytváří rezervaci.

## 4.2 Ukázka volání API pomocí nástroje cURL

**0. List informací o všech aut v databázi:**
```bash
curl -X GET "http://127.0.0.1:8000/cars" -H "accept: application/json"
```
Výsledek: {"1":{"id":1,"model":"Škoda Enyaq","status":"volné","battery":85},"2":{"id":2,"model":"Tesla Model 3","status":"v servisu","battery":15},"3":{"id":3,"model":"Hyundai Ioniq 5","status":"rezervováno","battery":60}}

**1. Rezervace:**
```bash
curl -X POST "http://127.0.0.1:8000/reserve" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"user_id\": 42, \"car_id\": 1}"
```
Výsledek: {"status":"ok","message":"Rezervace vytvořena","car":{"id":1,"model":"Škoda Enyaq","status":"rezervováno","battery":85}}

**2. Odeslání auta do servisu:**
```bash
curl -X POST "http://127.0.0.1:8000/service/1?reason=Defekt" -H "accept: application/json"
```
Výsledek: {"status":"ok","message":"Auto 1 bylo vyřazeno z oběhu a nahlášeno servisu.","details":{"id":1,"model":"Škoda Enyaq","status":"v servisu","battery":85}}

**3. Uvolnění auta z servisu:**
```bash
curl -X POST "http://127.0.0.1:8000/release?car_id=1" -H "accept: application/json"
```
Výsledek: {"status":"ok","message":"Vozidlo bylo úspěšně uvolněno (původní stav: volné)","car":{"id":1,"model":"Škoda Enyaq","status":"volné","battery":85}}

**4. Neúspěšná rezervace (auto v servisu):**
Očekávaný výsledek: Chybová hláška vozidlo není k dispozici
```bash
curl -X POST "http://127.0.0.1:8000/reserve" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"user_id\": 99, \"car_id\": 2}"
```
{"detail":"Vozidlo není k dispozici."}
Výsledek: {"status":"ok","message":"Rezervace vytvořena","car":{"id":1,"model":"Škoda Enyaq","status":"rezervováno","battery":85}}

**5. Neúspěšné odeslání auta do servisu (neexistující auto):**
Očekávaný výsledek: Chybová hláška vozidlo nenalezeno
```bash
curl -X POST "http://127.0.0.1:8000/service/1?reason=Defekt" -H "accept: application/json"
```
Výsledek: {"detail":"Vozidlo nenalezeno."}

**6. Neúspěšné uvolnění auta z servisu (neexistující auto):**
Očekávaný výsledek: Chybová hláška vozidlo nenalezeno
```bash
curl -X POST "http://127.0.0.1:8000/release?car_id=999" -H "accept: application/json"
```
Výsledek: {"detail":"Vozidlo nenalezeno."}
