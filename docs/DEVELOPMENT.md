# Development

Den här guiden beskriver projektets nuvarande utvecklingsmiljö och
kvalitetskontroller.

## Förutsättningar

- Python 3.13 eller senare
- Git
- valfritt: VS Code

Projektets Python-version anges i `.python-version` och paketkravet i
`pyproject.toml`.

## Installation

Skapa en lokal virtuell miljö:

```bash
python3.13 -m venv .venv
```

Installera projektet och utvecklingsverktygen i redigerbart läge:

```bash
.venv/bin/python -m pip install --editable ".[dev]"
```

Kommandona ovan använder sökvägar för macOS och Linux. På Windows används
`.venv\Scripts\python.exe` i stället.

Verifiera installationen:

```bash
.venv/bin/hembygd
.venv/bin/python -m hembygd
```

Båda kommandona ska för närvarande skriva `Hembygd Verktyg`.

## Testa HTML-import

Parsern kan köras mot en lokalt sparad Hembygd.se-sida:

```bash
.venv/bin/hembygd import-html foreningsdokument.html
```

Använd `--source-url` och `--site-name` om filen kommer från en annan sida eller
förening. Parsern utför inga nätverksanrop; HTML-hämtning är ett separat framtida
ansvar.

HTML tolkas med Beautiful Soup. Beroendet valdes framför standardbibliotekets
lägre nivå eftersom sidans redigerade HTML innehåller varierande nästling,
icke-brytande blanksteg och historiska markupskillnader. Beroendet hålls inom
huvudversion 4 för att undvika oväntade kompatibilitetsbrott.

## Projektstruktur

```text
hembygd/
├── presentation/     # CLI och framtida användargränssnitt
├── application/      # Användningsfall och komponentgränssnitt
├── domain/           # Domänobjekt och affärsregler
└── infrastructure/   # Tekniska adaptrar, inklusive Hembygd-parsern
```

Skapa inte nya generella `core`- eller `utils`-moduler. Placera kod i det lager
som motsvarar dess ansvar och skapa undermoduler först när ett konkret behov
finns.

## Ruff

Kontrollera koden:

```bash
.venv/bin/python -m ruff check .
```

Kontrollera formateringen:

```bash
.venv/bin/python -m ruff format --check .
```

Formatera Python-koden:

```bash
.venv/bin/python -m ruff format .
```

Ruff-konfigurationen finns i `pyproject.toml`.

## Tester

Kör alla tester:

```bash
.venv/bin/python -m pytest
```

Kör med täckningsrapport:

```bash
.venv/bin/python -m pytest --cov=hembygd --cov-report=term-missing
```

Testerna ligger under `tests/`.

## VS Code

Projektets `.vscode/`-katalog innehåller:

- rekommenderade tillägg för Python, Ruff, Prettier och YAML
- Ruff som Python-formatterare
- Prettier för Markdown, JSON, JSONC och YAML
- pytest-discovery
- debugkonfigurationer för CLI och tester
- uppgifter för miljöinstallation, lintning, formatering, tester och täckning

Välj `.venv/bin/python` som interpreter. Uppgifterna använder för närvarande
macOS/Linux-sökvägar; Windows-användare kan köra motsvarande kommandon från en
terminal tills uppgifterna har gjorts plattformsoberoende.

## Dokumentation

Prettier används för Markdown, JSON och YAML via VS Code. Kontrollera dessutom
att filer inte innehåller oavsiktlig avslutande whitespace:

```bash
git diff --check
```

Dokumentationen är en del av projektets specifikation. Läsordningen och kraven
finns i `AGENTS.md`.

## Före commit

1. Kör Ruff-kontrollen.
2. Kontrollera Ruff-formatering.
3. Kör pytest.
4. Kör `git diff --check`.
5. Granska `git status --short` och staged diff.
6. Säkerställ att dokumentationen beskriver det implementerade beteendet.
