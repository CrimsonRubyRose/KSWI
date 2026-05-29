# 5. Testování softwaru

## 5.1 Implementované testy
Pro vytvořenou komponentu a API bylo napsáno 5 testů pomocí frameworku `pytest`. Testy pokrývají jak happy-path (úspěšná rezervace), tak chybové stavy (rezervace obsazeného nebo neexistujícího vozidla). Zdrojový kód testů je součástí odevzdaného repozitáře v souboru `test_main.py`.

**Výstup z úspěšného spuštění testů:**
### Výsledek testování komponenty ReservationService

```text
============================= test session starts =============================
platform win32 -- Python 3.13.0, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\Admin\Desktop\Schule\KSWI-main
plugins: anyio-4.13.0
collected 5 items          

test_main.py::test_reserve_available_car_success PASSED          [ 20%]
test_main.py::test_release_car_to_available PASSED               [ 40%]
test_main.py::test_send_to_service_and_fix_it PASSED             [ 60%]
test_main.py::test_reserve_nonexistent_car_fails PASSED          [ 80%]
test_main.py::test_release_nonexistent_car_fails PASSED          [100%]

============================== 5 passed in 0.04s ============================== 
```

## 5.2 Plán testování celého systému

Pro zajištění kvality (QA) celého produkčního systému je navržen následující plán:

### Metody návrhu testů (Test Design Techniques)
Při návrhu testovacích případů kombinujeme dvě základní metodiky testování:
* **Whitebox testing (Testování černé skříňky zevnitř):** Technika, při které tester/vývojář zná vnitřní strukturu, logiku a zdrojový kód aplikace. Testy se navrhují tak, aby prošly všechny podmínky, cykly a větve v kódu. Typicky se využívá u jednotkových testů.
* **Blackbox testing (Testování černé skříňky):** Technika, kdy se na systém nahlíží jako na uzavřenou schránku bez znalosti vnitřního kódu. Testuje se čistě funkčnost systému na základě definovaných vstupů a očekávaných výstupů přes uživatelské rozhraní nebo API. Typicky se využívá u E2E a akceptačních testů.

### Typy testů
* **Jednotkové testy (Unit Testing):** Budou testovat izolované funkce (např. matematický výpočet ceny za minutu jízdy) pomocí metody **Whitebox**. Pro izolaci byznys logiky od vnějších systémů (mapy, platební brána) se využívají testovací dvojníci (**Test Doubles**), konkrétně typy **Dummy** (pro prázdné objekty v parametrech) a **Stub** (pro fixní podstrčené odpovědi z externích API).
* **Integrační testy:** Budou ověřovat komunikaci mezi Rezervační službou a Databází, nebo mezi API a platební bránou. V rámci naší minimální implementace je databáze simulována přímo v paměti (slovník `db_cars`), což v architektuře testování reprezentuje testovacího dvojníka typu **Fake**.
* **End-to-End (E2E) testy:** Simulace reálného uživatele proklikávajícího mobilní aplikaci od přihlášení až po ukončení jízdy pomocí metody **Blackbox**.
* **Akceptační testování (UAT):** Finální testování se vzorkem reálných uživatelů před nasazením na produkci, které ověřuje splnění zadání z pohledu zákazníka (Blackbox přístup).

### Testovací dvojníci (Test Doubles)
V plánu testování využíváme tyto typy testovacích dvojníků pro izolaci komponent:

* **Test Dummy:** Prázdný objekt předávaný výhradně jako parametr funkce (jako figurína při crash testech). Neobsahuje žádná reálná data a slouží jen k úspěšnému vyvolání funkce.
* **Test Stub:** Náhrada, která vrací natvrdo zadané (hard-coded) statické hodnoty. Používá se k podstrčení fixních dat (např. pevná cena za minutu), aby test nezávisel na externích službách.
* **Test Fake:** Funkční náhrada systému s jednodušší implementací, která není vhodná pro ostrý provoz. V našem projektu je to slovník `db_cars` simulující databázi v paměti.
* **Test Mock:** Dvojník s předem definovaným chováním. Používá se ke zjednodušení procesů, například pro okamžité vracení platného autorizačního tokenu bez nutnosti reálného přihlašování.
* **Test Spy:** Dvojník podobný Stubu, který navíc aktivně monitoruje a zaznamenává informace o tom, jak s ním systém komunikoval (např. počítá množství zavolání).
* 
### Strategie a kvalita kódu
* **Shift-left přístup:** Testování začíná už ve fázi návrhu požadavků. Vývojáři píší testy dříve než samotný kód v rámci metodiky **TDD** (Test Driven Development), aby se odhalily chyby co nejdříve.
* **Statická analýza kódu:** Nasazení nástrojů (např. SonarQube) pro automatickou kontrolu zranitelností, bezpečnostních chyb a dodržování jednotné štábní kultury kódu bez nutnosti jeho spuštění.
* **CI/CD datovod (Pipeline):** Každý commit do větve main v Gitu automaticky spustí build aplikace,

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
* **Dopad na architekturu a kód:** Bude nutné masivně upravit datové modely. Do tabulky uživatelů přibude vazba na `CompanyAccount`. Změní se autentizační a autorizační API. V UI přibude zcela nový dashboard pro firemní manažery. Naše komponenta `ReservationService` bude muset před vytvořením rezervace ověřit nejen to, zda je uživatel platný, ale zda má jeho firma dostatečný kredit na kreditní kartě.
