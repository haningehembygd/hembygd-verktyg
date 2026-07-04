# API

**Status:** Tidig CLI

Hembygd Verktyg har ännu inget stabilt publikt Python-API eller HTTP-API.
Projektets nuvarande publika gränssnitt är kommandoradsverktyget `hembygd`.

## Nuvarande gränssnitt

```console
$ hembygd
Hembygd Verktyg
```

Utan argument verifierar kommandot installationen. Standardsidan kan hämtas och
importeras direkt med:

```console
$ hembygd import-url
Imported N entries and M documents from Haninge Hembygdsgille
```

En annan sida kan anges som argument:

```bash
hembygd import-url https://www.hembygd.se/example/foreningsdokument
```

En lokalt sparad föreningsdokumentsida kan importeras utan nätverksanrop med:

```console
$ hembygd import-html foreningsdokument.html
Imported N entries and M documents from Haninge Hembygdsgille
```

Tillgängliga alternativ:

- `--source-url` anger originalsidans URL
- `--site-name` anger informationskällans namn

`import-url` hämtar endast HTML-sidan. Länkade dokument laddas ännu inte ned.
`import-html` gör inga nätverksanrop.

## JSON-export

Båda importkommandona accepterar `--output`:

```bash
hembygd import-url --output output/archive.json
hembygd import-html foreningsdokument.html --output output/archive.json
```

JSON-dokumentets toppnivå är:

```json
{
  "schema_version": 1,
  "site": {
    "name": "Haninge Hembygdsgille",
    "entries": []
  }
}
```

Det verkliga `site`-objektet innehåller webbplatsfält, metadata och alla entries.
Varje entry innehåller metadata, dokument och assets. Datum använder ISO 8601,
enumvärden skrivs som strängar och valfria värden representeras som `null`.

Schemakontraktet definieras i
[ADR-0003](adr/0003-versioned-json-export.md).

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
