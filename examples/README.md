# Exempel

## Importera standardsidan

Hämta och analysera Haninge Hembygdsgilles föreningsdokumentsida:

```bash
hembygd import-url
```

Spara resultatet för vidare användning:

```bash
hembygd import-url --output output/archive.json
```

## Importera en annan URL

```bash
hembygd import-url https://www.hembygd.se/example/foreningsdokument \
  --site-name "Exempelföreningen"
```

Sidan måste använda den dokumentstruktur som Hembygd-parsern stöder.

## Importera sparad HTML

Analysera en lokal fil utan nätverksanrop:

```bash
hembygd import-html foreningsdokument.html
```

Ange originalkällan när filen inte kommer från standardsidan:

```bash
hembygd import-html sida.html \
  --source-url https://www.hembygd.se/example/foreningsdokument \
  --site-name "Exempelföreningen"
```

Kommandona visar hur många poster och dokument som hittades. Alternativet
`--output` kan användas med både `import-url` och `import-html`. De länkade
dokumentfilerna laddas ännu inte ned.
