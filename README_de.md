# REST API Mock Server

![Python-Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Lizenz](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://github.com/your-username/rest-api-mock-server/workflows/Python%20application/badge.svg)

Ein leichter, auf Pythons `http.server` basierender REST-API Mock-Server, der für schnelle Entwicklung und Tests konzipiert wurde. Dieses Projekt bietet eine einfache und effektive Möglichkeit, API-Antworten zu simulieren, wodurch die Frontend- und Client-seitige Entwicklung fortgesetzt werden kann, ohne auf ein voll funktionsfähiges Backend warten zu müssen.

## Funktionen

*   **Einfache Einrichtung**: Ein Mock-Server läuft mit einem einzigen Python-Skript.
*   **HTTP-Methoden**: Unterstützt `GET`- und `POST`-Anfragen sofort.
*   **Anpassbare Antworten**: Einfache Definition von Mock-Antworten (Statuscodes, JSON-Bodies) für verschiedene Endpunkte.
*   **Leichtgewicht**: Basiert auf Pythons Standardmodul `http.server`, keine schweren Abhängigkeiten.
*   **Zweisprachige Dokumentation**: Umfassende Dokumentation in Englisch und Deutsch.
*   **Enterprise-Ready**: Enthält Unit-Tests, CI/CD-Pipeline, Richtlinien für Beiträge und eine Standardlizenz.

## Installation

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/your-username/rest-api-mock-server.git
    cd rest-api-mock-server
    ```

2.  **Virtuelle Umgebung erstellen und aktivieren (empfohlen):**
    ```bash
    python -m venv .venv
    # Unter Linux/macOS:
    source .venv/bin/activate
    # Unter Windows:
    .venv\Scripts\activate
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```

## Verwendung

Um den Mock-Server zu starten, führen Sie einfach `main.py` aus:

```bash
python main.py
```

Der Server wird standardmäßig auf `http://localhost:8000` gestartet.

### Verfügbare Endpunkte (wie in `main.py` definiert):

*   `GET /api/users`
*   `POST /api/users`
*   `GET /api/products`
*   `GET /api/status`

### Beispiel cURL-Anfragen:

**GET /api/users**

```bash
curl http://localhost:8000/api/users
# Erwartete Ausgabe: [
#   { "id": 1, "name": "Alice" },
#   { "id": 2, "name": "Bob" }
# ]
```

**POST /api/users**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Charlie"}' http://localhost:8000/api/users
# Erwartete Ausgabe: { "message": "User created successfully", "id": 3 }
```

**GET /api/products**

```bash
curl http://localhost:8000/api/products
# Erwartete Ausgabe: [
#   { "id": 101, "name": "Laptop" },
#   { "id": 102, "name": "Mouse" }
# ]
```

**GET /api/status**

```bash
curl http://localhost:8000/api/status
# Erwartete Ausgabe: { "status": "ok", "server": "MockAPI v1.0" }
```

**Nicht existierender Endpunkt**

```bash
curl http://localhost:8000/api/nonexistent
# Erwartete Ausgabe: { "error": "Not Found" }
```

## Entwicklung & Beiträge

Wir freuen uns über Beiträge! Bitte beachten Sie die [CONTRIBUTING.md](CONTRIBUTING.md) für Richtlinien zum Einreichen von Fehlerberichten, Funktionsanfragen und Code-Beiträgen.

### Tests ausführen

Um die Unit-Tests auszuführen, geben Sie `pytest` in Ihrem Terminal ein:

```bash
pytest
```

### Linting

Um die Codequalität sicherzustellen, wird `flake8` für das Linting verwendet:

```bash
flake8 .
```

## Projektstruktur

```
rest-api-mock-server/
├── .github/              # GitHub Actions CI/CD-Workflows
│   └── workflows/
│       └── python-app.yml
├── docs/                 # Detaillierte Dokumentation
│   ├── architecture_en.md
│   └── architecture_de.md
├── main.py               # Hauptanwendungslogik (Mock Server)
├── test_main.py          # Unit-Tests für main.py
├── README.md             # Englische Dokumentation (diese Datei)
├── README_de.md          # Deutsche Dokumentation
├── CONTRIBUTING.md       # Richtlinien für Beiträge
├── LICENSE               # Projektlizenz (MIT)
├── requirements.txt      # Python-Abhängigkeiten
└── .gitignore            # Dateien/Verzeichnisse, die in Git ignoriert werden sollen
```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – weitere Details finden Sie in der Datei [LICENSE](LICENSE).
