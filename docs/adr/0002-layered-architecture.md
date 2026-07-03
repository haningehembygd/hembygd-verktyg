# ADR-0002 – Lagerindelad arkitektur

**Status:** Accepterad
**Datum:** 2026-07-03

---

# Bakgrund

Projektets första struktur grupperade kod i generella kataloger för `core`,
`models` och `parsers`. Samtidigt definierar den godkända domänmodellen `Entry`
som det centrala informationsobjektet, medan äldre arkitekturdokument och
exempel använder separata modeller som `Page` och `Meeting`.

Skillnaden skapar två konkurrerande vokabulärer och gör det oklart var
affärsregler, arbetsflöden och tekniska adaptrar ska placeras.

---

# Beslut

Projektet delas in i fyra lager:

1. Presentation
2. Application
3. Domain
4. Infrastructure

Domänlagret följer `docs/DOMAIN_MODEL.md` och använder följande centrala objekt:

- `Site`
- `Entry`
- `EntryType`
- `Document`
- `Asset`
- `Metadata`

Möten, evenemang, artiklar och sidor representeras av `Entry` tillsammans med
`EntryType`. De äldre exemplen `Page` och `Meeting` i ADR-0001 ska inte tolkas som
separata centrala modeller.

Paketstrukturen speglar lagren:

```text
hembygd/
├── presentation/
├── application/
├── domain/
└── infrastructure/
```

Generella paket som `core` och generella `utils`-moduler används inte. Nya
undermoduler skapas först när de har ett konkret ansvar.

---

# Beroenderegler

- Domain importerar inte från andra projektlager.
- Application får bero på domain.
- Presentation får bero på application och domäntyper som behövs för visning.
- Infrastructure får bero på application och domain.
- Konkreta infrastructure-adaptrar kopplas till application vid programmets
  sammansättningspunkt.

---

# Konsekvenser

Fördelar:

- dokumentation och kod använder samma domänspråk
- affärsregler hålls oberoende av tekniska integrationer
- nya parsers och exporters kan läggas till utan ändringar i domänen
- paketens ansvar blir tydligare för nya utvecklare

Nackdelar:

- fler tydliga paket behövs än i den ursprungliga minimala strukturen
- gränssnitt mellan application och infrastructure måste utformas uttryckligt
- enkla funktioner kan kräva sammansättning över flera lager

---

# Ersätter

Detta beslut ersätter ADR-0001:s modell-exempel i de delar där `Page` och
`Meeting` framställs som centrala domänmodeller. ADR-0001:s övriga principer
gäller fortsatt.
