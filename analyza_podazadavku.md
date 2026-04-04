## 1.3 Specifikace funkčních požadavků

| ID | Požadavek | Popis | Priorita | Zdroj | Rizika | Závislosti |
|:---|:---|:---|:---:|:---|:---|:---|
| **F01** | Rezervace vozidla | Uživatel si může zablokovat auto pro sebe. | High | Zákazník | Race condition (2 lidi naráz) | F02 |
| **F02** | Sledování stavu | Systém eviduje: volné, rezervované, v servisu. | High | Provoz | Špatná synchronizace dat | - |
| **F03** | Správa uživatelů | Admin může měnit role (Admin/User). | Medium | Zadání | Neoprávněná změna práv | - |
| **F04** | Integrace map | Zobrazení polohy všech volných aut na mapě. | Medium | UX | Výpadek API mapové služby | F02 |
| **F05** | Fakturace jízdy | Automatický výpočet ceny po ukončení jízdy. | High | Business | Chyba v GPS (špatné km) | F06 |
| **F06** | Historie jízd | Uživatel vidí své minulé cesty a výdaje. | Low | Zákazník | Únik osobních dat | - |
| **F07** | Stav baterie | Systém v reálném čase hlásí % nabití. | High | Technik | Zpoždění dat z vozu | - |
| **F08** | Ukončení jízdy | Možnost zamknout auto a ukončit pronájem. | High | Zákazník | Auto zůstane odemčené | F01 |
| **F09** | Blokace neplatičů | Systém zakáže rezervaci při dluhu. | Medium | Fakturace | Falešná pozitivita | F05 |
| **F10** | Servisní režim | Technik může auto vyřadit z nabídky. | Medium | Technik | Auto "zmizí" pod rukama | F02 |

## 1.4 Mimofunkční požadavky

1. **Bezpečnost (N01):** Veškerá komunikace mezi aplikací a serverem musí být šifrována pomocí TLS 1.3. (Priorita: High)
2. **Dostupnost (N02):** Systém musí být dostupný 99,5 % času (SLA). (Priorita: Medium)
3. **Odezva (N03):** API musí odpovědět na požadavek na rezervaci do 500 ms. (Priorita: Medium)
4. **GDPR (N04):** Osobní údaje (OP, jméno) musí být uloženy v šifrované databázi. (Priorita: High)
5. **Auditovatelnost (N05):** Každá změna stavu vozidla musí být logována s časovou značkou a ID uživatele. (Priorita: Low)

## 1.5 Konfliktní požadavky a nejasnosti

**Identifikovaná nejasnost:**
Během analýzy vznikl rozpor mezi požadavkem na **maximální rychlost rezervace** (uživatel chce auto jedním kliknutím) a **požadavkem na platební jistotu** (ověření solventnosti uživatele a platnosti karty trvá několik sekund).

**Navržené řešení:**
Systém zavede stav **"Optimistická rezervace"**. Auto se uživateli zablokuje okamžitě v UI, zatímco na pozadí běží asynchronní validace platby. Pokud validace selže do 30 sekund, rezervace se zruší a uživatel je informován. Tím zajistíme plynulé UX bez rizika pro firmu.
