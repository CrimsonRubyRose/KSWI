# 5. Testování softwaru

## 5.1 Implementované testy
Pro vytvořenou komponentu a API bylo napsáno 5 testů pomocí frameworku `pytest`. Testy pokrývají jak happy-path (úspěšná rezervace), tak chybové stavy (rezervace obsazeného nebo neexistujícího vozidla). Zdrojový kód testů je součástí odevzdaného repozitáře v souboru `test_main.py`.

**Výstup z úspěšného spuštění testů:**

test_main.py::test_reserve_available_car_success PASSED                                                                                                                              [ 20%]
test_main.py::test_release_car_to_available PASSED                                                                                                                                   [ 40%] 
test_main.py::test_send_to_service_and_fix_it PASSED                                                                                                                                 [ 60%]
test_main.py::test_reserve_nonexistent_car_fails PASSED                                                                                                                              [ 80%] 
test_main.py::test_release_nonexistent_car_fails PASSED                                                                                                                              [100%] 

==================================================================================== 5 passed in 0.04s ==================================================================================== 

## 5.2 Plán testování celého systému

Pro zajištění kvality (QA) celého produkčního systému je navržen následující plán:

### Typy testů
* **Jednotkové testy (Unit Testing):** Budou testovat izolované funkce (např. matematický výpočet ceny za minutu jízdy). Metoda návrhu: **Whitebox** (vývojář vidí do kódu a testuje všechny větve podmínek).
* **Integrační testy:** Budou ověřovat komunikaci mezi Rezervační službou a Databází, nebo mezi API a platební bránou.
* **End-to-End (E2E) testy:** Simulace reálného uživatele proklikávajícího mobilní aplikaci od přihlášení až po ukončení jízdy. Metoda návrhu: **Blackbox** (tester nezná vnitřní kód, zná jen vstupy a očekávané výstupy).
* **Akceptační testování (UAT):** Finální testování se vzorkem reálných uživatelů před nasazením na produkci.

### Strategie a kvalita kódu
* **Shift-left přístup:** Testování začíná už ve fázi návrhu požadavků. Vývojáři píší testy dříve než kód (TDD - Test Driven Development), aby se odhalily chyby co nejdříve.
* **Statická analýza kódu:** Nasazení nástrojů (např. SonarQube) pro automatickou kontrolu zranitelností a dodržování štábní kultury kódu.
* **CI/CD datovod (Pipeline):** Každý commit do větve `main` v Gitu automaticky spustí build aplikace, linter (statickou analýzu) a všechny testy. Pokud nějaký test selže, nasazení na produkci se automaticky zablokuje.

---

# 6. Evoluce softwaru

Systém je navržen tak, aby umožňoval budoucí rozšiřování. Pro další iteraci vývoje (v2.0) jsou navrženy následující tři změny:

## 1. Integrace s MHD (Městská hromadná doprava)
* **Popis:** Uživatel si bude moci koupit kombinovaný lístek, který ho nechá dojet tramvají k nejbližšímu volnému autu.
* **Dopad na architekturu a kód:** Bude nutné přidat novou komponentu `TransitIntegrationService`, která bude přes externí API komunikovat s dopravním podnikem. V databázi přibude nová entita `KombinovanaRezervace`. Logika naší komponenty `ReservationService` se bude muset rozšířit o schopnost rezervovat auto s odloženým startem (než uživatel dojede tramvají).

## 2. Dynamická cenotvorba (Surge Pricing)
* **Popis:** V době dopravní špičky nebo deště se cena za minutu jízdy automaticky zvýší. Pokud má auto málo baterie a uživatel ho zapojí do nabíječky, dostane naopak slevu.
* **Dopad na architekturu a kód:** Neovlivní to samotnou architekturu (vrstvy zůstanou stejné), ale výrazně to zasáhne `BillingService` (Fakturační službu) a `ReservationService`. V `ReservationService` se bude muset při vytvoření rezervace zafixovat aktuálně vypočítaná cena. 

## 3. Zavedení firemních účtů (B2B Fleet)
* **Popis:** Identifikace nového typu uživatele: **Firemní manažer**. Ten může rezervovat auta pro své zaměstnance na sdílený firemní účet.
* **Dopad na architekturu a kód:** Bude nutné masivně upravit datové modely. Do tabulky uživatelů přibude vazba na `CompanyAccount`. Změní se autentizační a autorizační API. V UI přibude zcela nový dashboard pro firemní manažery. Naše komponenta `ReservationService` bude muset před vytvořením rezervace ověřit nejen to, zda je uživatel platný, ale zda má jeho firma dostatečný kredit na fakturu.
