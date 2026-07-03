# DOMAIN MODEL

**Version:** 1.0  
**Status:** Godkänd

---

# Syfte

Domänmodellen beskriver de centrala objekt som Hembygd Verktyg arbetar med.

Den beskriver verksamhetens information – inte hur informationen lagras eller hämtas.

HTML, HTTP, parserimplementationer och filsystem tillhör den tekniska arkitekturen och ingår därför inte i domänmodellen.

Domänmodellen ska vara stabil över tid och oberoende av enskilda webbplatser.

---

# Designprincip

Projektets kärna består av ett litet antal domänobjekt.

Alla tekniska komponenter ska översätta sitt arbete till dessa objekt.

Parsern översätter HTML till domänobjekt.

Downloadern arbetar med domänobjekt.

Exporters arbetar med domänobjekt.

Ingen komponent ska behöva känna till hur en annan komponent fungerar internt.

---

# Domänöversikt

```text
                        Site
                          │
                          │
                 ┌────────┴────────┐
                 │                 │
             Metadata          Entries
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
            Documents                           Assets
                 │                                   │
                 └──────────────┬────────────────────┘
                                │
                            Metadata
```

---

# Site

## Beskrivning

En Site representerar en informationskälla.

Exempel:

- Hembygd.se
- WordPress
- kommunal webbplats
- GitHub Pages
- annan webbplats

En Site beskriver var informationen kommer ifrån.

## Ansvar

En Site innehåller information om:

- namn
- bas-URL
- språk
- beskrivning
- metadata

En Site innehåller ett antal Entries.

---

# Entry

## Beskrivning

Entry är projektets viktigaste domänobjekt.

En Entry representerar en publicerad informationspost.

Exempel:

- årsmöte
- styrelsemöte
- evenemang
- nyhet
- historisk artikel
- publikation
- informationssida

Alla dessa betraktas som samma grundläggande objekt.

Skillnaden beskrivs genom dess typ.

## Ansvar

En Entry beskriver:

- titel
- beskrivning
- typ
- datum
- kategori
- dokument
- resurser
- metadata

---

# EntryType

EntryType beskriver vilken typ av Entry det är.

Exempel:

- Meeting
- Event
- News
- Publication
- Article
- Page
- Other

Projektet ska enkelt kunna utökas med nya typer.

---

# Document

## Beskrivning

Document representerar ett dokument som hör till en Entry.

Exempel:

- PDF
- Word
- Excel
- ZIP
- textfil

## Ansvar

Document beskriver bland annat:

- titel
- URL
- filnamn
- MIME-typ
- filstorlek
- checksumma
- lokal sökväg
- metadata

Document beskriver endast dokumentet.

Det beskriver inte var dokumentet hittades.

---

# Asset

## Beskrivning

Asset representerar andra resurser än dokument.

Exempel:

- bilder
- ljud
- video
- kartor
- illustrationer

Assets hanteras på samma sätt som Documents men representerar andra typer av innehåll.

---

# Metadata

Metadata används genom hela domänmodellen.

Metadata kan beskriva:

- författare
- språk
- licens
- kategori
- taggar
- skapad
- ändrad
- källa

Metadata ska kunna utökas utan att domänobjekten behöver ändras.

---

# Relationer

En Site innehåller många Entries.

En Entry kan innehålla:

- noll eller flera Documents
- noll eller flera Assets

Både Site och Entry kan innehålla Metadata.

Document och Asset kan också innehålla egen Metadata.

---

# Objekt utanför domänen

Följande objekt ingår inte i domänmodellen.

De är tekniska implementationer.

- HTML
- HTTP
- Web Request
- Parser
- Downloader
- Organizer
- Exporter
- Cache
- Logger
- CLI
- Konfiguration

Dessa beskrivs i projektets arkitekturdokument.

---

# Stabilitet

Domänmodellen ska förändras mycket sällan.

När stöd läggs till för en ny webbplats ska parsern anpassas.

Domänmodellen ska normalt inte behöva ändras.

---

# Arkitekturprincip

All information som passerar genom systemet ska representeras av domänobjekt.

Parsern producerar domänobjekt.

Övriga komponenter arbetar enbart mot domänobjekten.

Detta gör systemet:

- enklare att testa
- enklare att underhålla
- enklare att vidareutveckla
- oberoende av enskilda webbplatser

---

# Sammanfattning

Domänmodellen är projektets gemensamma språk.

All funktionalitet i Hembygd Verktyg ska utgå från dessa objekt.

När projektet växer ska nya funktioner i första hand implementeras genom nya parser- eller exportmoduler – inte genom att förändra domänmodellen.