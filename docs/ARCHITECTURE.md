# ARCHITECTURE

**Version:** 0.1  
**Status:** Utkast

---

# Översikt

Hembygd Verktyg är byggt som ett modulärt ramverk där varje komponent har ett tydligt och avgränsat ansvar.

Grundprincipen är:

> **En komponent ska göra en sak – och göra den väl.**

Systemet består av en kärna ("Core") och ett antal fristående moduler.

---

# Övergripande arkitektur

```text
                 CLI
                  │
                  ▼
            Application
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
 Parser       Downloader   Organizer
      │                       │
      ▼                       ▼
  Models                Exporters
      │                       │
      └──────────────┬────────┘
                     ▼
                 Output
```

Varje modul ansvarar endast för sin egen uppgift.

Ingen modul ska känna till hur andra moduler är implementerade.

---

# Designprinciper

Projektet bygger på följande principer:

- Single Responsibility Principle
- Separation of Concerns
- Modulär design
- Hög testbarhet
- Låg koppling mellan moduler
- Tydliga datamodeller
- Utbyggbarhet genom nya parsermoduler

---

# Komponenter

## CLI

CLI är programmets användargränssnitt.

Ansvar:

- läsa kommandoradsargument
- starta rätt arbetsflöde
- visa status
- visa felmeddelanden

CLI innehåller ingen affärslogik.

---

## Application

Application samordnar programmets arbetsflöde.

Ansvar:

- skapa objekt
- starta rätt parser
- koordinera nedladdning
- koordinera export

Application ska inte känna till HTML eller filformat.

---

## Parser

Parsern analyserar en webbplats.

Ansvar:

- läsa HTML
- identifiera objekt
- skapa datamodeller

Parsern laddar aldrig ned dokument.

Parsern skriver aldrig filer.

Parsern returnerar endast objekt.

---

## Downloader

Downloader ansvarar endast för filhämtning.

Ansvar:

- ladda ned filer
- verifiera filstorlek
- verifiera checksumma
- spara filer

Downloader analyserar aldrig HTML.

---

## Organizer

Organizer ansvarar för katalogstrukturen.

Ansvar:

- skapa mappar
- flytta filer
- skapa README.md
- skapa index

Organizer hämtar aldrig information från internet.

---

## Exporters

Exporters omvandlar data till olika format.

Exempel:

- JSON
- Markdown
- CSV
- GitHub Pages
- API-data

Exporters känner inte till hur informationen hämtades.

---

# Datamodeller

Projektets datamodeller utgör kärnan i systemet.

Till en början används följande modeller:

- Site
- Page
- Meeting
- Document

Alla övriga komponenter arbetar mot dessa modeller.

---

## Site

Beskriver en informationskälla.

Exempel:

- Hembygd.se
- WordPress
- Kommunwebbplats

---

## Page

Representerar en hämtad HTML-sida.

Innehåller:

- URL
- titel
- HTML
- metadata

---

## Meeting

Representerar ett möte eller en aktivitet.

Exempel:

- årsmöte
- styrelsemöte
- evenemang

Ett Meeting innehåller ett antal Document.

---

## Document

Representerar ett dokument.

Exempel:

- PDF
- Word
- Excel

Document innehåller metadata och eventuell lokal fil.

---

# Arbetsflöde

Normalt arbetsflöde:

1. CLI startas.
2. Application skapas.
3. Parser väljs.
4. Parser analyserar webbplatsen.
5. Datamodeller skapas.
6. Downloader hämtar dokument.
7. Organizer bygger katalogstruktur.
8. Exporters genererar önskat resultat.

---

# Parserarkitektur

Varje webbplats implementeras som en egen parser.

Exempel:

- HembygdParser
- WordpressParser
- HaningeParser

Alla parserklasser ska implementera samma gemensamma gränssnitt.

Det gör att nya webbplatser kan stödjas utan att övriga delar av systemet behöver ändras.

---

# Felhantering

Fel ska hanteras så nära källan som möjligt.

Programmet ska:

- fortsätta när det är möjligt
- logga alla fel
- ge tydliga felmeddelanden
- aldrig avsluta utan förklaring

---

# Testbarhet

Alla komponenter ska kunna testas separat.

Det ska vara möjligt att testa:

- parsern
- downloadern
- organizern
- exporters

utan att behöva köra hela programmet.

---

# Framtida utbyggnad

Arkitekturen är avsedd att kunna växa.

Planerade utbyggnader inkluderar:

- stöd för flera webbplatser
- GitHub-publicering
- Google Sheets
- öppna API:er
- GIS- och kartdata
- bildhantering
- OCR
- AI-baserad metadataanalys
- Home Assistant-integration

---

# Arkitekturprincip

All information ska passera genom datamodellerna.

Ingen komponent får kommunicera direkt med en annan genom HTML, filer eller egna datastrukturer.

Detta gör systemet enklare att testa, underhålla och vidareutveckla.