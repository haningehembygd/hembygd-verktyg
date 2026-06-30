# VISION

# Hembygd Verktyg

**Version:** 0.1  
**Status:** Utkast  
**Projekt:** Hembygd Verktyg  
**Organisation:** Haninge Hembygdsgille

---

# Vision

Hembygd Verktyg är ett öppet programvaruprojekt vars mål är att hjälpa hembygdsföreningar och andra kulturarvsorganisationer att digitalisera, organisera och publicera sitt kulturhistoriska material.

Projektet ska minska det manuella arbetet kring dokumenthantering, webbpublicering och öppna data genom att erbjuda moderna, automatiserade och återanvändbara verktyg.

Den långsiktiga ambitionen är att skapa ett ramverk som kan användas av många föreningar, oavsett teknisk kunskapsnivå eller vilken webbplattform de använder.

---

# Syfte

Projektets syfte är att:

- automatisera repetitiva arbetsuppgifter
- förenkla publicering av kulturhistoriskt material
- skapa välstrukturerade digitala arkiv
- underlätta skapandet av öppna data
- minska beroendet av manuellt arbete
- bevara föreningars digitala information för framtiden

---

# Mål

Projektet ska göra det möjligt att:

- importera dokument från webbplatser
- organisera dokument automatiskt
- generera katalogstrukturer
- skapa README-filer och index
- skapa JSON-filer och andra öppna dataformat
- publicera material till GitHub
- publicera material till webbplatser
- integrera med Google Sheets
- skapa API:er för evenemang och annan föreningsinformation
- återanvända samma verktyg för många olika föreningar

---

# Grundprinciper

Projektet ska följa följande principer.

## Öppen källkod

Programvaran utvecklas som öppen källkod.

Kod ska vara enkel att förstå, enkel att bidra till och enkel att återanvända.

---

## Modulär arkitektur

Projektet byggs av fristående komponenter.

Exempel:

- parser
- crawler
- downloader
- organizer
- exporter

Varje komponent ska ha ett tydligt ansvar.

---

## Automatisering

Allt som kan automatiseras bör automatiseras.

Målet är att minimera manuellt arbete.

---

## Återanvändbarhet

Projektet ska inte vara beroende av en specifik webbplats.

Nya webbplatser ska kunna stödjas genom att skapa nya parsermoduler utan att ändra övriga delar av systemet.

---

## Långsiktighet

Projektet ska kunna underhållas under många år.

Kod ska därför prioritera:

- tydlighet
- läsbarhet
- testbarhet
- dokumentation

framför kortast möjliga implementation.

---

# Målgrupper

Projektet riktar sig främst till:

- hembygdsföreningar
- kulturhistoriska föreningar
- museer
- ideella organisationer
- arkiv
- lokalhistoriska projekt

---

# Exempel på användningsområden

Projektet ska bland annat kunna användas för att:

- importera årsmöteshandlingar
- skapa digitala dokumentarkiv
- publicera föreningsprotokoll
- skapa evenemangs-API:er
- exportera data till JSON
- generera GitHub Pages-innehåll
- skapa öppna data för andra system
- leverera data till Home Assistant
- skapa historiska kartlager
- synkronisera information mellan olika webbplatser

---

# Vad projektet inte är

Projektet är inte:

- ett CMS
- ett dokumenthanteringssystem
- ett webbhotell
- en databas
- en ersättning för GitHub

Projektets uppgift är att automatisera och strukturera information mellan olika system.

---

# Kvalitetsmål

Projektet ska hålla hög teknisk kvalitet.

Det innebär bland annat:

- modern Python
- tydlig arkitektur
- konsekvent kodstil
- omfattande dokumentation
- automatiserade tester
- versionshantering
- reproducerbara byggprocesser

---

# Långsiktig vision

På sikt ska Hembygd Verktyg utvecklas till ett generellt ramverk för digitalisering av kulturarv.

Målet är att samma verktyg ska kunna användas av många olika organisationer genom att endast byta parser eller konfiguration.

Projektet ska vara ett exempel på hur modern öppen programvara kan bidra till att bevara och tillgängliggöra lokalt kulturarv.

---

# Motto

> **Bevara historien. Automatisera arbetet. Dela kunskapen.**