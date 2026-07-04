# ADR-0003 – Versionshanterad JSON-export

**Status:** Accepterad
**Datum:** 2026-07-04

---

# Bakgrund

Importerad information behöver kunna granskas och återanvändas utanför
programprocessen. Ett exportformat blir ett publikt kontrakt och måste därför
vara stabilt även när den interna implementationen förändras.

---

# Beslut

Projektets första exportformat är läsbar UTF-8 JSON med följande egenskaper:

- dokumentets toppnivå innehåller `schema_version`
- den första schemaversionen är `1`
- domänobjekt mappas uttryckligt till JSON-fält
- datum och tidsstämplar använder ISO 8601
- enumvärden använder sina stabila strängvärden
- sökvägar representeras som strängar
- tuples representeras som JSON-arrayer
- metadata-attribut representeras som JSON-objekt
- valfria fält behålls och representeras som `null`
- Unicode skrivs direkt och ersätts inte med escape-sekvenser
- filer skrivs atomiskt via en temporär fil i destinationskatalogen

Exportimplementationen får inte förlita sig på automatisk serialisering av
dataklasser. Varje fält mappas uttryckligt för att interna modelländringar inte
oavsiktligt ska ändra exportformatet.

---

# Konsekvenser

Fördelar:

- konsumenter kan kontrollera schemaversionen
- exporter blir läsbara för både människor och program
- förändringar i formatet blir medvetna designbeslut
- en avbruten skrivning lämnar inte en halvfärdig målfil

Nackdelar:

- nya domänfält måste läggas till uttryckligt i exportern
- framtida inkompatibla formatändringar kräver en ny schemaversion
- JSON-filer innehåller även valfria fält som saknar värde

---

# Framtida förändringar

Bakåtkompatibla tillägg kan göras inom samma schemaversion när befintliga
konsumenter inte påverkas. Inkompatibla ändringar kräver höjd `schema_version`
och dokumenterad migreringsstrategi.
