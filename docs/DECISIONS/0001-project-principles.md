# ADR-0001 – Projektprinciper

**Status:** Accepterad  
**Datum:** 2026-06-30

---

# Bakgrund

Hembygd Verktyg är tänkt att utvecklas under många år och kunna användas av flera olika hembygdsföreningar och kulturarvsorganisationer.

Projektet ska därför prioritera långsiktig kvalitet framför kortsiktig utvecklingshastighet.

Detta dokument beskriver de grundprinciper som hela projektet ska följa.

---

# Beslut

## 1. Python

Projektet utvecklas i modern Python.

- Minsta version: Python 3.12
- Type hints används överallt.
- Modern Python-syntax används konsekvent.

---

## 2. Datamodeller

Projektets centrala objekt implementeras som dataklasser.

Exempel:

- Site
- Page
- Meeting
- Document

Dataklasser ska använda:

- `@dataclass`
- `slots=True`

när det är lämpligt.

---

## 3. pathlib används överallt

Alla sökvägar representeras av `pathlib.Path`.

Vanliga strängar används inte för fil- och kataloghantering.

Detta ger bättre läsbarhet och plattformsoberoende.

---

## 4. En komponent – ett ansvar

Varje modul ska ha ett tydligt ansvar.

Exempel:

Parser:

- analyserar HTML
- skapar objekt

Downloader:

- hämtar filer

Organizer:

- bygger katalogstruktur

Exporter:

- producerar utdata

Ingen modul ska utföra flera av dessa uppgifter.

---

## 5. Parsern returnerar objekt

Parsern ska aldrig:

- skriva filer
- skapa kataloger
- ladda ned dokument

Parsern returnerar endast datamodeller.

---

## 6. Downloadern känner inte till HTML

Downloadern ska endast arbeta med Document-objekt.

Den ska aldrig analysera HTML eller webbplatser.

---

## 7. Datamodeller är projektets gemensamma språk

All kommunikation mellan moduler sker genom datamodeller.

Ingen modul ska utbyta information genom egna datastrukturer.

---

## 8. Ingen hårdkodning

Projektet ska undvika:

- hårdkodade sökvägar
- hårdkodade URL:er
- hårdkodade filnamn

Konfiguration ska samlas på ett ställe.

---

## 9. Små, testbara moduler

Kod ska delas upp i små komponenter.

Varje komponent ska kunna testas separat.

---

## 10. Läsbarhet framför kort kod

Kod ska vara enkel att förstå.

Det är bättre med tydlig kod än kort kod.

Projektet prioriterar underhållbarhet framför minimal kodmängd.

---

## 11. Dokumentation är en del av koden

Ny funktionalitet ska dokumenteras.

Arkitekturförändringar ska dokumenteras genom nya ADR-dokument.

Dokumentationen är en del av projektet och inte något som skrivs i efterhand.

---

## 12. Öppen arkitektur

Projektet ska kunna utökas med nya parsermoduler.

Exempel:

- Hembygd.se
- WordPress
- kommunala webbplatser
- andra kulturarvsplattformar

Kärnan ska inte behöva ändras när stöd för en ny webbplats läggs till.

---

## Konsekvenser

Genom dessa principer blir projektet:

- lättare att förstå
- lättare att testa
- lättare att vidareutveckla
- enklare för nya utvecklare att bidra till
- mindre beroende av enskilda personer

Projektet får en tydlig och långsiktigt hållbar arkitektur.

---

# Framtida beslut

Alla större tekniska beslut ska dokumenteras som egna ADR-dokument.

Exempel:

- ADR-0002 – Konfigurationshantering
- ADR-0003 – Parserarkitektur
- ADR-0004 – Plugin-system
- ADR-0005 – Loggningsstrategi
- ADR-0006 – Caching
- ADR-0007 – Exportformat