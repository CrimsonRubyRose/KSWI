# 1. Inženýrství požadavků

## Diagramy případů užití (Use Case)
```mermaid
useCaseDiagram
    actor "Běžný uživatel" as U
    actor "Servisní technik" as T
    actor "Administrátor" as A

    U --> (Vyhledat auto)
    U --> (Rezervovat auto)
    U --> (Historie jízd)

    T --> (Změnit stav nabití)
    T --> (Servisní odstávka)
    T --> (Seznam aut k údržbě)

    A --> (Správa uživatelů)
    A --> (Fakturace)
    A --> (Reporty systému)

stateDiagram-v2
    [*] --> VyhledatAuto
    VyhledatAuto --> VybratAuto
    VybratAuto --> KontrolaDostupnosti
    if (Je volné?) then
        --> Rezervovat
        Rezervovat --> [*]
    else
        --> VyhledatAuto
    endif
