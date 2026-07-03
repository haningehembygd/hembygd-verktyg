# Contributing

Tack för att du vill bidra till Hembygd Verktyg.

Projektet prioriterar korrekthet, tydlighet och långsiktig underhållbarhet. Läs
[AGENTS.md](AGENTS.md) och projektets dokumentation innan du börjar. Instruktionerna
i `AGENTS.md` gäller även när AI-verktyg används i utvecklingen.

## Innan du börjar

1. Läs [visionen](docs/VISION.md), [arkitekturen](docs/ARCHITECTURE.md) och
   [domänmodellen](docs/DOMAIN_MODEL.md).
2. Kontrollera befintliga ADR:er under `docs/adr/`.
3. Avgränsa ändringen till ett tydligt ansvar.
4. Diskutera arkitektur- eller domänändringar innan implementationen påbörjas.

## Utvecklingsmiljö

Projektet kräver Python 3.13 eller senare.

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install --editable ".[dev]"
```

Fullständiga instruktioner finns i [utvecklingsguiden](docs/DEVELOPMENT.md).

## Arbetsflöde

1. Förstå problemet och relevanta krav.
2. Inspektera berörd kod och dokumentation.
3. Beskriv en kort plan före större ändringar.
4. Implementera den minsta sammanhängande lösningen.
5. Lägg till eller uppdatera tester.
6. Uppdatera dokumentation när beteende, arkitektur eller domän ändras.
7. Kör projektets kvalitetskontroller.

Undvik orelaterad refaktorering i samma ändring.

## Kodprinciper

- Använd type hints.
- Föredra tydliga, små moduler och funktioner.
- Använd `pathlib.Path` för sökvägar.
- Håll domänlagret oberoende av infrastructure.
- Placera affärsregler i domain och arbetsflöden i application.
- Introducera inte nya beroenden utan att motivera behov och underhållskostnad.
- Dölj eller ignorera aldrig fel utan en uttrycklig anledning.

## Kvalitetskontroller

Kör följande före en commit:

```bash
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m pytest
```

Om kod behöver formateras:

```bash
.venv/bin/python -m ruff format .
```

Kontrollera även arbetsytan:

```bash
git diff --check
git status --short
```

## Tester

Viktig funktionalitet ska ha tester. Föredra fokuserade enhetstester och använd
integrationstester vid verkliga gränser som filsystem, HTTP eller paketering.

Tester ska ge förtroende för beteendet och inte enbart öka täckningsgraden.

## Dokumentation och ADR

- Uppdatera `docs/ARCHITECTURE.md` vid arkitekturförändringar.
- Uppdatera `docs/DOMAIN_MODEL.md` vid förändringar i domänspråket.
- Skapa en ADR under `docs/adr/` för betydande tekniska beslut.
- Uppdatera `README.md` när publikt beteende eller projektstatus ändras.

## Git

- Gör en logisk ändring per commit.
- Skriv ett kort commit-meddelande som förklarar ändringens syfte.
- Skriv inte om publicerad historik.
- Force-pusha inte.
- Kontrollera den staged diffen före commit.
