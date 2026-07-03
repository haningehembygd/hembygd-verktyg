# API

**Status:** Inte implementerat

Hembygd Verktyg har ännu inget publikt Python-API eller HTTP-API. Projektets
nuvarande publika gränssnitt är det minimala kommandoradskommandot `hembygd`, som
endast verifierar att installationen fungerar.

## Nuvarande gränssnitt

```console
$ hembygd
Hembygd Verktyg
```

Kommandot har ännu inga argument och utför ingen import, bearbetning eller
export.

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
