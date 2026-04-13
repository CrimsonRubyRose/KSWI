# 1. Inženýrství požadavků

## 1.1 Diagram případů užití (Use Case)
Tento diagram definuje interakce mezi jednotlivými rolemi uživatelů a systémem pro správu elektromobilů.

```mermaid
graph LR
    subgraph Role
        U[Běžný uživatel]
        T[Servisní technik]
        A[Administrátor]
    end

    subgraph "Systém sdílení aut"
        U --- UC1(Vyhledat auto na mapě)
        U --- UC1b(Zobrazit informace a stav auta)
        U --- UC2(Rezervovat auto)
        U --- UC3(Zobrazit historii jízd)

        T --- UC4(Zaevidovat nabití baterie)
        T --- UC5(Odebrat auto z mapy k servisu)
        T --- UC6(Zobrazit vybitá a rozbitá auta)

        A --- UC7(Zablokovat nebo odblokovat uživatele)
        A --- UC8(Vyřešit reklamace a faktury)
        A --- UC9(Změnit cenu za minutu jízdy)
    end
```

## 1.2 Diagramy aktivit
Níže jsou rozkresleny jednotlivé případy užití krok za krokem z pohledu jednotlivých rolí v systému.

### Role: Běžný uživatel

**UC1: Vyhledat auto na mapě**
```mermaid
flowchart TD
    Start((Start)) --> Open[Otevření mobilní aplikace]
    Open --> GPS[Načtení aktuální GPS polohy]
    GPS --> Fetch[Dotaz na server pro volná auta v okolí]
    Fetch --> Display[Vykreslení bodů na mapě]
    Display --> End((Konec))
```

**UC1b: Zobrazit informace a stav auta**
```mermaid
flowchart TD
    Start((Start)) --> Click[Kliknutí na ikonu auta na mapě]
    Click --> FetchData[Načtení detailů z databáze]
    FetchData --> Show[Zobrazení SPZ, dojezdu a % baterie]
    Show --> End((Konec))
```

**UC2: Rezervovat auto**
```mermaid
flowchart TD
    Start((Start)) --> Select[Uživatel klikne na Rezervovat]
    Select --> Check{Je auto stále volné?}
    Check -- Ne --> Error[Zobrazení chyby: Auto je obsazené]
    Check -- Ano --> Lock[Dočasná blokace vozidla v DB]
    Lock --> Pay{Ověření platební karty}
    Pay -- Zamítnuto --> Cancel[Zrušení blokace]
    Pay -- Schváleno --> Confirm[Potvrzení rezervace a spuštění odpočtu]
    Confirm --> End((Konec))
    Error --> End
    Cancel --> End
```

**UC3: Zobrazit historii jízd**
```mermaid
flowchart TD
    Start((Start)) --> Profile[Otevření profilu uživatele]
    Profile --> ClickHistory[Kliknutí na 'Moje jízdy']
    ClickHistory --> FetchDB[Systém načte data z databáze]
    FetchDB --> DisplayList[Zobrazení seznamu s cenami a trasami]
    DisplayList --> End((Konec))
```

### Role: Servisní technik

**UC4: Zaevidovat nabití baterie**
```mermaid
flowchart TD
    Start((Start)) --> Plug[Technik připojí auto do nabíječky]
    Plug --> Scan[Naskenuje QR kód auta v servisní aplikaci]
    Scan --> Confirm[Potvrdí zahájení nabíjení]
    Confirm --> UpdateStatus[Systém změní stav na 'Nabíjí se']
    UpdateStatus --> End((Konec))
```

**UC5: Odebrat auto z mapy k servisu**
```mermaid
flowchart TD
    Start((Start)) --> FindCar[Nalezení poškozeného auta v aplikaci]
    FindCar --> ClickService[Kliknutí na 'Přepnout do servisu']
    ClickService --> Reason[Zadání důvodu odstávky]
    Reason --> UpdateDB[Auto se v DB přepne na 'Mimo provoz']
    UpdateDB --> Hide[Auto zmizí z mapy běžným uživatelům]
    Hide --> End((Konec))
```

**UC6: Zobrazit vybitá a rozbitá auta**
```mermaid
flowchart TD
    Start((Start)) --> OpenApp[Otevření servisního panelu]
    OpenApp --> Filter[Zapnutí filtru 'Kritický stav']
    Filter --> Query[Systém vyhledá auta s baterií pod 15 % nebo nahlášenou závadou]
    Query --> ShowList[Zobrazení seznamu vozidel k řešení]
    ShowList --> End((Konec))
```

### Role: Administrátor

**UC7: Zablokovat nebo odblokovat uživatele**
```mermaid
flowchart TD
    Start((Start)) --> SearchUser[Vyhledání uživatele podle jména/ID]
    SearchUser --> SelectAction[Zvolení akce: Blokovat/Odblokovat]
    SelectAction --> Confirm[Potvrzení administrátorem]
    Confirm --> UpdateAcc[Aktualizace stavu účtu v databázi]
    UpdateAcc --> End((Konec))
```

**UC8: Vyřešit reklamace a faktury**
```mermaid
flowchart TD
    Start((Start)) --> OpenTicket[Otevření podané reklamace]
    OpenTicket --> CheckRide[Kontrola GPS logů a času jízdy]
    CheckRide --> Decision{Uznat reklamaci?}
    Decision -- Ne --> Reject[Zamítnutí s odůvodněním]
    Decision -- Ano --> Refund[Vrácení peněz na kartu uživatele]
    Refund --> CloseTicket[Uzavření případu]
    Reject --> CloseTicket
    CloseTicket --> End((Konec))
```

**UC9: Změnit cenu za minutu jízdy**
```mermaid
flowchart TD
    Start((Start)) --> OpenSettings[Otevření globálního nastavení cen]
    OpenSettings --> InputPrice[Zadání nové ceny za minutu]
    InputPrice --> Save[Uložení změn]
    Save --> UpdateSystem[Propagace nové ceny do systému pro další jízdy]
    UpdateSystem --> End((Konec))
```

## 1.3 Specifikace funkčních požadavků

| ID | Požadavek | Popis | Priorita | Zdroj | Rizika | Závislosti |
|:---|:---|:---|:---:|:---|:---|:---|
| **F01** | Rezervace vozidla | Uživatel si může zablokovat auto pro sebe skrze aplikaci. | High | Zákazník | Race condition (duplicitní rezervace) | F02 |
| **F02** | Sledování stavu | Systém eviduje stavy: volné, rezervované, v servisu. | High | Provoz | Nekoherentní data v databázi | - |
| **F03** | Správa uživatelů | Administrátor může měnit role a oprávnění uživatelů. | Medium | Zadání | Neoprávněné zvýšení privilegií | - |
| **F04** | Integrace map | Zobrazení polohy a dostupnosti aut na mapovém podkladu. | Medium | UX | Výpadek externí mapové služby (API) | F02 |
| **F05** | Fakturace jízdy | Automatický výpočet ceny a vystavení faktury po jízdě. | High | Business | Chyba ve výpočtu času/vzdálenosti | F06 |
| **F06** | Historie jízd | Uživatel má přístup k seznamu svých minulých výpůjček. | Low | Zákazník | Únik citlivých osobních údajů | - |
| **F07** | Stav baterie | Systém v reálném čase monitoruje a zobrazuje % nabití. | High | Technik | Zpoždění telemetrických dat z vozidla | - |
| **F08** | Ukončení jízdy | Bezpečné ukončení pronájmu a uzamčení vozidla. | High | Zákazník | Auto zůstane fyzicky odemčené | F01 |
| **F09** | Blokace neplatičů | Automatické zamezení rezervace při neuhrazených dluzích. | Medium | Fakturace | Chybná blokace platícího zákazníka | F05 |
| **F10** | Servisní režim | Možnost technika vyřadit vozidlo z nabídky pro veřejnost. | Medium | Technik | Nechtěné vyřazení funkčního vozu | F02 |

## 1.4 Mimofunkční požadavky

1. **Bezpečnost (N01):** Komunikace mezi aplikací klienta a serverem probíhá výhradně přes šifrovaný protokol TLS (Transport Layer Security). (Priorita: High)
2. **Dostupnost (N02):** Systém musí být pro uživatele dostupný v režimu 24/7 s garantovanou dostupností 99,9 % času (minimalizace neplánovaných výpadků). (Priorita: Medium)
3. **Robustnost (N03):** Systém je odolný proti hardwarovým chybám a plánované údržbě, při lokálním výpadku primárního serveru plynule přebírají provoz záložní (backup) servery. (Priorita: Medium)
4. **Ochrana dat (N04):** Systém plně splňuje požadavky GDPR; citlivá osobní data (např. hesla, platební údaje) jsou v databázi šifrována pomocí standardu SHA-256. (Priorita: High)
5. **Logování (N05):** Veškeré změny stavů vozidla (např. rezervace, servisní odstávka) jsou logovány/uložené s přímou vazbou na ID uživatele. (Priorita: Low)

## 1.5 Konfliktní požadavky a nejasnosti během analýzy

**Identifikovaná nejasnost:**
Během analýzy byl zjištěn konflikt mezi požadavkem na **Zobrazení historie jízd (F06)** a striktní **Ochranou dat podle GDPR (N04)**. Systém musí na jednu stranu zaznamenávat trasu, ale dlouhodobé uchovávání přesných GPS bodů pohybu konkrétní osoby je z hlediska ochrany soukromí problematické.

**Navržené řešení:**
Systém bude uchovávat detailní GPS trasu na mapě pouze po dobu 30 dnů od ukončení jízdy (kvůli bodu UC8 - Vyřešení případných reklamací). Poté se detailní souřadnice z databáze automaticky nevratně smažou a v historii uživatele (F06) zůstane pouze agregovaný záznam: Datum, celkový čas, start, cíl, ujetá vzdálenost a cena.
