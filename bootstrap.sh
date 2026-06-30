#!/bin/bash

set -e

echo
echo "=============================================="
echo " Initialiserar Hembygd Verktyg"
echo "=============================================="
echo

#
# Katalogstruktur
#

mkdir -p docs
mkdir -p examples
mkdir -p output
mkdir -p samples
mkdir -p scripts
mkdir -p templates
mkdir -p tests

mkdir -p hembygd/core
mkdir -p hembygd/models
mkdir -p hembygd/parsers

#
# Python-filer
#

touch hembygd/__init__.py
touch hembygd/__main__.py
touch hembygd/cli.py

touch hembygd/core/__init__.py
touch hembygd/core/config.py
touch hembygd/core/crawler.py
touch hembygd/core/downloader.py
touch hembygd/core/logger.py
touch hembygd/core/organizer.py
touch hembygd/core/utils.py

touch hembygd/models/__init__.py
touch hembygd/models/document.py
touch hembygd/models/meeting.py
touch hembygd/models/page.py
touch hembygd/models/site.py

touch hembygd/parsers/__init__.py
touch hembygd/parsers/base.py
touch hembygd/parsers/hembygd.py

#
# README-filer
#

cat > README.md << EOF
# Hembygd Verktyg

Hembygd Verktyg är ett open source-projekt från Haninge Hembygdsgille.

Projektets mål är att utveckla moderna verktyg för digitalisering, import, organisering och publicering av kulturhistoriskt material.

## Funktioner

- Import av dokument från Hembygd.se
- Automatisk organisering av arkiv
- Generering av README-filer
- Export till JSON
- Publicering till GitHub
- Stöd för framtida API:er

## Status

🚧 Under utveckling
EOF

cat > docs/README.md << EOF
# Dokumentation

Projektets dokumentation.

Här samlas:

- Arkitektur
- Designbeslut
- API-beskrivningar
- UML-diagram
- Framtida funktioner
EOF

cat > examples/README.md << EOF
# Exempel

Exempel på hur verktyget används.
EOF

cat > samples/README.md << EOF
# Testdata

HTML, PDF, JSON och annan testdata används här för utveckling och tester.
EOF

cat > scripts/README.md << EOF
# Scripts

Hjälpskript för utveckling.

Exempel:

- bootstrap
- release
- format
- lint
- test
EOF

cat > templates/README.md << EOF
# Templates

Mallar som används när filer genereras.
EOF

cat > tests/README.md << EOF
# Tester

Projektets enhets- och integrationstester.
EOF

cat > output/README.md << EOF
# Output

Genererade filer sparas här.

Denna katalog versioneras normalt inte, förutom denna README.
EOF

#
# .gitignore
#

cat > .gitignore << EOF
# macOS
.DS_Store

# Python
__pycache__/
*.py[cod]
*.so

# Virtual environment
.venv/

# IDE
.vscode/
.idea/

# pytest
.pytest_cache/

# Ruff
.ruff_cache/

# Coverage
.coverage
htmlcov/

# Output
output/*
!output/README.md
EOF

#
# Startkod
#

cat > hembygd/__main__.py << EOF
from hembygd.cli import main

if __name__ == "__main__":
    main()
EOF

cat > hembygd/cli.py << EOF
def main():
    print("Hembygd Verktyg")
EOF

echo
echo "=============================================="
echo " Projektet är klart!"
echo "=============================================="
echo

find . | sort
