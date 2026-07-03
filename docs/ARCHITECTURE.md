# ARCHITECTURE

**Version:** 0.2
**Status:** Godkänd

---

# Syfte

Hembygd Verktyg använder en lagerindelad arkitektur med domänmodellen som
systemets stabila kärna.

Arkitekturen ska göra det möjligt att lägga till nya informationskällor,
arbetsflöden och exportformat utan att domänmodellen kopplas till HTML, HTTP,
filsystem eller andra tekniska detaljer.

---

# Arkitekturöversikt

```text
                    Presentation
                        CLI
                         │
                         ▼
                    Application
                     Workflows
                         │
                         ▼
                       Domain
        Site ──► Entry ──┬──► Document
                         └──► Asset
                              Metadata
                         ▲
                         │
                  Infrastructure
          Parsers · Downloaders · Exporters
```

Pilar nedåt visar hur ett användningsfall anropas. Infrastructure ansluter till
de gränssnitt som arbetsflödena behöver och översätter teknisk information till
och från domänobjekt.

Domänlagret importerar aldrig från något annat projektlager.

---

# Lager

## Presentation

Presentation är systemets gränssnitt mot användaren.

Ansvar:

- läsa kommandoradsargument
- validera indata på gränssnittsnivå
- starta rätt application-arbetsflöde
- presentera resultat och felmeddelanden

Presentation innehåller ingen affärslogik och arbetar inte direkt med
infrastruktur.

---

## Application

Application beskriver och samordnar systemets användningsfall.

Ansvar:

- koordinera import, nedladdning, organisering och export
- definiera de gränssnitt som externa komponenter behöver uppfylla
- hantera transaktions- och arbetsflödesgränser
- returnera tydliga resultat till presentation

Application använder domänobjekt men innehåller inga regler för HTML, HTTP eller
specifika filformat.

---

## Domain

Domain innehåller projektets verksamhetsbegrepp och regler.

De centrala objekten är:

- `Site`
- `Entry`
- `EntryType`
- `Document`
- `Asset`
- `Metadata`

`Entry` är den gemensamma representationen för exempelvis möten, evenemang,
nyheter, publikationer, artiklar och informationssidor. Skillnaden uttrycks med
`EntryType`; separata domänmodeller som `Meeting` och `Page` används därför inte.

Den fullständiga modellen definieras i `docs/DOMAIN_MODEL.md`.

---

## Infrastructure

Infrastructure innehåller tekniska adaptrar.

Exempel:

- webbplatsspecifika parsers
- HTTP-klienter och nedladdare
- filsystemslagring
- JSON-, Markdown- och CSV-exporters
- integrationer med GitHub och externa API:er

Infrastructure får bero på application och domain. Lagret innehåller inga
affärsregler.

---

# Komponentansvar

## Parser

En parser översätter data från en extern informationskälla till domänobjekt.

En parser får:

- läsa och analysera källans representation
- tolka källspecifik metadata
- skapa `Site`, `Entry`, `Document` och `Asset`

En parser får inte:

- skriva filer
- organisera kataloger
- ladda ned dokument
- exponera HTML eller källspecifika datastrukturer till andra lager

---

## Downloader

En downloader hämtar innehåll som beskrivs av domänobjekt.

Den får hantera HTTP, filstorlek och kontrollsummor men får inte analysera HTML
eller besluta hur material ska kategoriseras.

---

## Organizer

En organizer bygger den önskade katalogstrukturen utifrån domänobjekt.

Den får skapa kataloger, placera filer och generera index, men hämtar inte data
från externa källor.

---

## Exporter

En exporter omvandlar domänobjekt till ett publiceringsformat, exempelvis JSON,
Markdown, CSV eller GitHub Pages-innehåll.

En exporter känner inte till hur informationen ursprungligen hämtades.

---

# Paketstruktur

```text
hembygd/
├── presentation/     # CLI och framtida användargränssnitt
├── application/      # Användningsfall och komponentgränssnitt
├── domain/           # Domänobjekt och affärsregler
└── infrastructure/   # Parsers, nedladdare, lagring och exporters
```

Nya undermoduler skapas först när ett konkret användningsfall behöver dem.
Generella kataloger som `core` och generella `utils`-moduler undviks eftersom de
saknar en tydlig arkitektonisk gräns.

---

# Beroenderegler

- Domain har inga beroenden till övriga projektlager.
- Application får bero på domain.
- Presentation får bero på application och på domäntyper som behövs för visning.
- Infrastructure får bero på application och domain.
- Presentation och application får inte importera konkreta infrastructure-adaptrar
  annat än i en avgränsad sammansättningspunkt.
- Kommunikation mellan komponenter sker med domänobjekt och uttryckliga
  gränssnitt, inte med HTML eller godtyckliga dictionaries.

---

# Sammansättning

Programmets startpunkt ansvarar för att skapa konkreta infrastructure-adaptrar
och koppla dem till application-arbetsflöden. Denna sammansättning hålls nära
presentationens startpunkt och innehåller ingen affärslogik.

---

# Felhantering

Fel hanteras där de kan beskrivas meningsfullt:

- Infrastructure översätter tekniska fel till tydliga komponentfel.
- Application avgör om ett arbetsflöde kan fortsätta eller måste avbrytas.
- Presentation visar ett begripligt meddelande och en korrekt slutstatus.

Fel får aldrig ignoreras utan loggning eller förklaring.

---

# Teststrategi

- Domain testas med snabba enhetstester utan externa resurser.
- Application testas mot enkla testimplementationer av sina gränssnitt.
- Infrastructure testas med avgränsad testdata och integrationstester.
- Presentation testas genom CLI-anrop och verifiering av slutstatus och utdata.

Varje lager ska kunna testas utan att hela systemet behöver startas.

---

# Arkitekturprincip

Externa representationer översätts vid systemets gräns. När information har
kommit in i systemet representeras den av de objekt som definieras i
domänmodellen.

Detta håller kärnan stabil, gör adaptrar utbytbara och låter projektet växa utan
att webbplatsspecifika detaljer sprids genom koden.
