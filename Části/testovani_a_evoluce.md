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

#### 1. FUNCTIONAL TESTING (Funkční testování)
Zaměřuje se na to, **co** ten systém dělá a zda správně plní zadané požadavky.

* **Unit tests (Jednotkové testy):** Testují izolované funkce (např. matematický výpočet ceny za jízdu nebo test na sčítání) pomocí metody **Whitebox**.
* **Integration tests (Integrační testy):** Ověřují vzájemnou komunikaci mezi komponentami (např. propojení funkce a databáze nebo API a platební brány). V této fázi se často používají testovací dvojníci (test doubles) – v naší implementaci je to slovník `db_cars` v paměti fungující jako **Fake**.
* **End to end tests (E2E / Systémový test):** Simuluje průchod celým systémem z pohledu uživatele pomocí metody **Blackbox**. Testuje se kompletní scénář, například zda lze vybrat auto, provést rezervaci a zkusit, zda vše funguje od začátku do konce (obdoba vložení věci do nákupního košíku v e-shopech).
* **Alpha / Beta / Acceptance test (Akceptační testování):** Závěrečný test, kdy zákazník testuje software. Pokud ho potvrdí, software je nasazen (deploynutý). Má tyto fáze:
    * **Alpha test:** Testování, jak systém běží interně na firemním hardwaru (HW).
    * **Beta test:** Testování koncovými uživateli přímo na jejich vlastním (user) HW.

#### 2. NON-FUNCTIONAL TESTING (Mimo-funkční testy)
Zaměřuje se na to, **jak** ty funkce systém vykonává (vlastnosti jako výkon, stabilita a bezpečnost).

* **Load / Stress / Endurance testing:** Testování zátěže na systém a celkového výkonu:
    * *Load test:* Testování při standardním, očekávaném zatížení.
    * *Stress test:* Krátkodobé vystavení systému extrémní, maximální zátěži (short term).
    * *Endurance test:* Dlouhodobé testování systému pod vysokou zátěží (max long).
* **Scalability test (Testování škálovatelnosti):** Ověřuje, jak je systém schopen růst a zvládat navyšování kapacity hardwaru nebo počtu uživatelů.
* **Pen testy (Penetrační testování):** Simulované kybernetické útoky, které testují zabezpečení systému a hledají potenciální zranitelnosti.
  

### Testovací dvojníci (Test Doubles)
V plánu testování využíváme tyto typy testovacích dvojníků pro izolaci komponent:

* **Test Dummy:** Prázdný objekt předávaný výhradně jako parametr funkce (jako figurína při crash testech). Neobsahuje žádná reálná data a slouží jen k úspěšnému vyvolání funkce.
* **Test Stub:** Náhrada, která vrací natvrdo zadané (hard-coded) statické hodnoty. Používá se k podstrčení fixních dat (např. pevná cena za minutu), aby test nezávisel na externích službách.
* **Test Fake:** Funkční náhrada systému s jednodušší implementací, která není vhodná pro ostrý provoz. V našem projektu je to slovník `db_cars` simulující databázi v paměti.
* **Test Mock:** Dvojník s předem definovaným chováním. Používá se ke zjednodušení procesů, například pro okamžité vracení platného autorizačního tokenu bez nutnosti reálného přihlašování.
* **Test Spy:** Dvojník podobný Stubu, který navíc aktivně monitoruje a zaznamenává informace o tom, jak s ním systém komunikoval (např. počítá množství zavolání).

### Strategie a kvalita kódu

* **Shift-left přístup:** Strategie, kdy se testování a kontrola kvality posouvají na úplný začátek vývojového cyklu. Testování tak nezačíná až u hotového kódu, ale již ve fázi analýzy a návrhu zadání. Hlavní technikou tohoto přístupu je:
    * **Validace (Kontrola kvality požadavků):** Před samotným kódováním se požadavky kontrolují podle 5 základních kritérií, aby se předešlo drahým chybám v implementaci:
        1. *Validita (Správnost):* Ověřuje se, zda je požadavek opravdu zapotřebí a zda jeho roli už neplní jiná existující funkce.
        2. *Konzistence (Bezrozpornost):* Kontroluje se, zda je požadavek ve shodě s ostatními a zda nejdou proti sobě.
        3. *Úplnost:* Ověřuje se, zda požadavek obsahuje všechny informace, které vývojáři potřebují k implementaci.
        4. *Realismus (Realizovatelnost):* Zkoumá se, zda je požadavek technicky, finančně a časově realizovatelný.
        5. *Ověřitelnost:* Požadavek musí být měřitelný (obsahovat konkrétní čas nebo hodnotu), aby se dalo exaktně ověřit jeho splnění.

* **TDD (Test Driven Development):** Vývojová praxe, při které programátoři píší automatizované testy dříve než samotný produkční kód, což je vede k čistšímu návrhu a okamžitému odhalení chyb. Podporuje to myšlenku včasného odhalování defektů.

* **BDD (Behavior-Driven Development):** Rozšíření metodiky TDD, které se zaměřuje na chování systému z pohledu uživatele. Scénáře se píší v lidsky čitelném jazyce (často pomocí šablony *Given-When-Then* / *Pokud-Když-Pak*). To umožňuje, aby na kvalitu a správnost požadavků dohlíželi společně vývojáři, testeři i byznys analytici ještě před začátkem vývoje.

* **Statická analýza kódu:** Nasazení nástrojů (např. SonarQube) pro automatickou kontrolu zranitelností, bezpečnostních chyb a dodržování jednotné štábní kultury kódu bez nutnosti jeho spuštění.

* **CI/CD datovod (Pipeline):** Každý commit do větve `main` v Gitu automaticky spustí build aplikace, linter (statickou analýzu) a všechny testy. Pokud jakýkoliv test nebo kontrola kvality selže, nasazení na produkční servery se automaticky zablokuje.

---


# 6. Evoluce softwaru

Systém je navržen tak, aby umožňoval budoucí rozšiřování. Pro další iteraci vývoje (v2.0) jsou navrženy následující tři změny:

### 1. Integrace s MHD (Městská hromadná doprava)
* **Popis:** Uživatel si bude moci zakoupit kombinovaný lístek, který mu umožní dojet tramvají či autobusem k nejbližšímu volnému elektromobilu.
* **Dopad na architekturu a kód:** Bude nutné přidat novou komponentu `TransitIntegrationService`, která bude přes externí API komunikovat s dopravním podnikem. V databázi přibude nová entita `KombinovanaRezervace`. Logika naší komponenty `ReservationService` se bude muset rozšířit o schopnost rezervovat vozidlo s odloženým startem (po dobu, než uživatel k autu dojede hromadnou dopravou).

### 2. Dynamická cenotvorba (Surge Pricing)
* **Popis:** V době dopravní špičky nebo nepříznivého počasí (deště) se cena za minutu jízdy automaticky zvýší. Pokud má auto nízký stav baterie a uživatel ho po ukončení jízdy zapojí do nabíječky, dostane naopak slevu.
* **Dopad na architekturu a kód:** Tato změna neovlivní samotnou architekturu (vrstvy zůstanou stejné), ale výrazně zasáhne do vnitřního kódu `BillingService` (Fakturační služby) a `ReservationService`. V `ReservationService` se bude muset při vytvoření rezervace zafixovat aktuálně vypočítaná cena, aby se během jízdy už neměnila.

### 3. Zavedení firemních účtů (B2B Fleet)
* **Popis:** Identifikace nového typu uživatele: Firemní manažer. Tento uživatel může rezervovat auta pro své zaměstnance a platby se strhávají ze sdíleného firemního účtu.
* **Dopad na architekturu a kód:** Bude nutné masivně upravit datové modely. Do databázové tabulky uživatelů přibude vazba na `CompanyAccount`. Změní se autentizační a autorizační API a v uživatelském rozhraní (UI) přibude zcela nový dashboard pro správu firemní flotily. Naše komponenta `ReservationService` bude muset před schválením rezervace ověřit nejen platnost uživatele, ale také zda má jeho firma na svém účtu dostatečný kredit.
