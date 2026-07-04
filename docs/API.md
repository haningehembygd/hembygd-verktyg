# API

**Status:** Tidig CLI

Hembygd Verktyg har ännu inget stabilt publikt Python-API eller HTTP-API.
Projektets nuvarande publika gränssnitt är kommandoradsverktyget `hembygd`.

## Nuvarande gränssnitt

```console
$ hembygd
Hembygd Verktyg
```

Utan argument verifierar kommandot installationen. En lokalt sparad
föreningsdokumentsida kan importeras med:

```console
$ hembygd import-html foreningsdokument.html
Imported N entries and M documents from Haninge Hembygdsgille
```

Tillgängliga alternativ:

- `--source-url` anger originalsidans URL
- `--site-name` anger informationskällans namn

Kommandot läser endast HTML-filen. Det hämtar eller laddar inte ned innehåll från
internet.

## Framtida API

Ett framtida API ska byggas ovanpå application-lagrets användningsfall och
använda den godkända domänmodellen. API-lagret får inte innehålla affärslogik
eller exponera källspecifik HTML och infrastructure-detaljer.

Innan ett publikt API introduceras ska projektet besluta och dokumentera:

- målgrupp och användningsfall
- stabilitets- och versionspolicy
- serialisering av domänobjekt
- felmodell
- autentisering och behörighet, om relevant
- bakåtkompatibilitet

Ett sådant beslut ska dokumenteras i en separat ADR.
