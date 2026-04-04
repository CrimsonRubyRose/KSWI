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

**1. Získání seznamu vozidel:**
```bash
curl -X GET "http://localhost:8000/cars" -H "accept: application/json"
```

**2. Vytvoření úspěšné rezervace (Auto ID 1 je volné):**
```bash
curl -X POST "http://localhost:8000/reserve" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 99, "car_id": 1}'
```

**3. Pokus o rezervaci obsazeného vozidla (Auto ID 2 je v servisu):**
Očekávaný výsledek je HTTP Status 400 (Bad Request).
```bash
curl -X POST "http://localhost:8000/reserve" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 99, "car_id": 2}'
```
