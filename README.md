# Hembygd Verktyg

[![CI](https://github.com/haningehembygd/hembygd-verktyg/actions/workflows/ci.yml/badge.svg)](https://github.com/haningehembygd/hembygd-verktyg/actions/workflows/ci.yml)

Hembygd Verktyg är ett open source-projekt från Haninge Hembygdsgille.

Projektets mål är att utveckla moderna verktyg för digitalisering, import,
organisering och publicering av kulturhistoriskt material.

## Status

Projektet är i en tidig utvecklingsfas. Den tekniska grunden, domänmodellen och
den första importfunktionen finns på plats. Verktyget kan läsa en lokalt sparad
föreningsdokumentsida från Hembygd.se eller hämta sidan direkt från webben och
omvandla innehållet till domänobjekt. Dokumentnedladdning, organisering och
publicering är ännu inte implementerade.

Det nuvarande kommandot verifierar installationen:

```console
$ hembygd
Hembygd Verktyg
```

Haninge Hembygdsgilles föreningsdokumentsida kan hämtas och analyseras med:

```bash
hembygd import-url
```

Spara samtidigt hela resultatet som versionshanterad JSON:

```bash
hembygd import-url --output output/archive.json
```

En redan sparad Hembygd.se-sida kan analyseras utan nätverksanrop med:

```bash
hembygd import-html foreningsdokument.html
```

Kommandona använder Haninge Hembygdsgilles föreningsdokumentsida som
standardkälla. En annan URL kan skickas till `import-url`. `--source-url` och
`--site-name` kan användas med lokal HTML.

## Planerade funktioner

- nedladdning av dokument från Hembygd.se och andra informationskällor
- automatisk organisering av digitala arkiv
- generering av README-filer och index
- export till ytterligare öppna format
- publicering till GitHub och webbplatser
- stöd för framtida API:er och integrationer

## Teknisk grund

- Python 3.13 eller senare
- lagerindelad arkitektur
- Ruff för lintning och Python-formatering
- pytest för automatiserade tester
- Prettier för Markdown, JSON och YAML i VS Code

Projektets centrala domänobjekt är `Site`, `Entry`, `EntryType`, `Document`,
`Asset` och `Metadata`. Se [domänmodellen](docs/DOMAIN_MODEL.md) och
[arkitekturen](docs/ARCHITECTURE.md) för detaljer.

## Kom igång

Skapa en virtuell miljö och installera projektets utvecklingsverktyg:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install --editable ".[dev]"
```

Kör kvalitetskontrollerna:

```bash
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest
```

VS Code-användare kan också använda projektets rekommenderade tillägg och
uppgifter i `.vscode/`.

Mer information finns i [utvecklingsguiden](docs/DEVELOPMENT.md).

## Bidra

Läs [CONTRIBUTING.md](CONTRIBUTING.md) innan du föreslår en ändring.

## Licens

Projektet distribueras under [Apache License 2.0](LICENSE).
