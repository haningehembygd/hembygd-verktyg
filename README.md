# Hembygd Verktyg

[![CI](https://github.com/haningehembygd/hembygd-verktyg/actions/workflows/ci.yml/badge.svg)](https://github.com/haningehembygd/hembygd-verktyg/actions/workflows/ci.yml)

Hembygd Verktyg är ett open source-projekt från Haninge Hembygdsgille.

Projektets mål är att utveckla moderna verktyg för digitalisering, import,
organisering och publicering av kulturhistoriskt material.

## Status

Projektet är i en tidig utvecklingsfas. Den tekniska grunden, domänmodellen och
den första importfunktionen finns på plats. Verktyget kan läsa en lokalt sparad
föreningsdokumentsida från Hembygd.se och omvandla innehållet till domänobjekt.
Nedladdning, organisering och publicering är ännu inte implementerade.

Det nuvarande kommandot verifierar installationen:

```console
$ hembygd
Hembygd Verktyg
```

En sparad Hembygd.se-sida kan analyseras med:

```bash
hembygd import-html foreningsdokument.html
```

Kommandot använder för närvarande Haninge Hembygdsgilles föreningsdokumentsida
som standardkälla. `--source-url` och `--site-name` kan användas för att ange
andra värden.

## Planerade funktioner

- hämtning av sidor och dokument från Hembygd.se och andra informationskällor
- automatisk organisering av digitala arkiv
- generering av README-filer och index
- export till JSON och andra öppna format
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
