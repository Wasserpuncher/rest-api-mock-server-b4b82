# Architektur Deep Dive: REST API Mock Server

Dieses Dokument bietet einen detaillierten Einblick in das architektonische Design des REST API Mock Servers, wobei der Schwerpunkt auf seinen Kernkomponenten, Designentscheidungen und Erweiterbarkeit liegt.

## Kernkomponenten

Der Mock-Server basiert auf zwei primären Modulen der Python-Standardbibliothek:

1.  **`http.server`**: Dieses Modul ist die Grundlage für die Erstellung einfacher HTTP-Server. Es stellt die Klasse `BaseHTTPRequestHandler` bereit, die wir erweitern, um eine benutzerdefinierte Anfragebearbeitungslogik zu definieren.
2.  **`socketserver`**: Dieses Modul bietet generische Basisklassen für die Implementierung von Netzwerkservern. `http.server` verwendet `socketserver` intern, um eingehende Verbindungen zu verwalten und an den entsprechenden Anfrage-Handler weiterzuleiten. `socketserver.TCPServer` wird verwendet, um einen TCP-Server zu erstellen, der auf HTTP-Anfragen lauscht.

### `main.py` - Die Server-Anwendung

`main.py` enthält die zentrale Logik für den Mock-Server:

*   **`MockAPIHandler(http.server.BaseHTTPRequestHandler)`**: Dies ist das Herzstück des Servers. Es erbt von `BaseHTTPRequestHandler` und überschreibt Schlüsselmethoden, um unsere Mock-API-Funktionalität zu implementieren:
    *   **`MOCK_RESPONSES`**: Ein klassenweites Wörterbuch, das die vordefinierten Mock-Daten speichert. Dieses Wörterbuch ordnet URL-Pfade HTTP-Methoden zu, und jede Methode ordnet dann einem Wörterbuch zu, das den `status`-Code und den `body` der Mock-Antwort enthält. Dies ist derzeit zur Vereinfachung fest codiert, ist aber ein Hauptkandidat für eine externe Konfiguration.
    *   **`_set_headers(self, status_code, content_type)`**: Eine Hilfsmethode, um das Senden von HTTP-Statuscodes und Content-Type-Headern zu optimieren. Sie gewährleistet eine konsistente Header-Einstellung für alle Antworten.
    *   **`_send_response(self, path, method)`**: Die Kernlogik zum Bestimmen und Senden der Mock-Antwort. Sie sucht den angeforderten `path` und die `method` in `MOCK_RESPONSES`. Wenn eine Übereinstimmung gefunden wird, sendet sie den entsprechenden Status und Body. Wenn der Pfad existiert, aber die Methode nicht, wird `405 Method Not Allowed` zurückgegeben. Wenn der Pfad nicht gefunden wird, wird `404 Not Found` zurückgegeben.
    *   **`do_GET(self)`**: Überschreibt die Basismethoden der Klasse, um `GET`-Anfragen zu verarbeiten. Es protokolliert die eingehende Anfrage und ruft `_send_response` mit dem Pfad und der Methode "GET" auf.
    *   **`do_POST(self)`**: Überschreibt die Basismethoden der Klasse, um `POST`-Anfragen zu verarbeiten. Es liest den Anfragetext (angenommen als JSON), protokolliert ihn und ruft dann `_send_response` mit dem Pfad und der Methode "POST" auf. Die tatsächlichen POST-Daten werden protokolliert, aber derzeit nicht verwendet, um die Mock-Antwort zu ändern, da die Antworten statisch sind.
*   **`run_server(port)`**: Diese Funktion initialisiert und startet den `socketserver.TCPServer`. Sie bindet an einen angegebenen Port (Standard 8000) und verwendet `MockAPIHandler`, um eingehende Anfragen zu verarbeiten. Sie enthält eine grundlegende Fehlerbehandlung für `KeyboardInterrupt`, um ein ordnungsgemäßes Herunterfahren des Servers zu ermöglichen.

## Design-Entscheidungen

1.  **Fokus auf Standardbibliothek**: Das Hauptziel war es, einen leichtgewichtigen Mock-Server mit minimalen externen Abhängigkeiten zu erstellen. Die Verwendung von `http.server` und `socketserver` erreicht dies und macht das Projekt für Python-Entwickler einfach einzurichten und zu verstehen.
2.  **Objektorientierte Programmierung (OOP)**: Die Verwendung von Klassen wie `MockAPIHandler` fördert Modularität und Wiederverwendbarkeit. Sie trennt die Belange der Anfragebearbeitung klar von der Lebenszyklusverwaltung des Servers.
3.  **Fest codierte Mocks (Anfangsphase)**: Für die Erstversion sind Mock-Antworten innerhalb von `MOCK_RESPONSES` fest codiert. Dies vereinfacht die erste Implementierung und ermöglicht eine schnelle Demonstration. Dies ist explizit als Ausgangspunkt konzipiert, mit zukünftigen Plänen zur Externalisierung der Konfiguration.
4.  **Zweisprachige Dokumentation**: Das Projekt betont die Zugänglichkeit durch die Bereitstellung umfassender Dokumentation in Englisch und Deutsch, einschließlich Inline-Kommentaren in Deutsch, um Anfängern in Python in deutschsprachigen Regionen zu helfen.
5.  **Protokollierung**: Eine grundlegende Protokollierung ist integriert, um Einblick in Serveroperationen, eingehende Anfragen und Antworten zu geben, was für die Fehlersuche und Überwachung entscheidend ist.

## Erweiterbarkeit und zukünftige Verbesserungen

Obwohl einfach, ist die aktuelle Architektur auf Erweiterbarkeit ausgelegt:

1.  **Externe Konfiguration (Hohe Priorität)**: Die unmittelbarste Verbesserung besteht darin, `MOCK_RESPONSES` von einem fest codierten Wörterbuch in eine externe Konfigurationsdatei (z. B. `config.json` oder `config.yaml`) zu verschieben. Dies würde es Benutzern ermöglichen, Mock-Endpunkte und -Antworten zu definieren und zu ändern, ohne den Python-Code zu berühren, was die Flexibilität erheblich erhöht. Der `initial_issue_title` spiegelt dies wider.
    *   **Implementierungsidee**: Eine `ConfigLoader`-Klasse könnte eingeführt werden, um die Konfigurationsdatei zu parsen und das `MOCK_RESPONSES`-Wörterbuch (oder eine ähnliche Struktur) dynamisch beim Serverstart zu füllen.
2.  **Dynamische Antworten**: Derzeit sind die Antworten statisch. Zukünftige Versionen könnten Logik einführen, um dynamische Antworten basierend auf Anforderungsparametern, Headern oder sogar simuliertem Status zu generieren (z. B. inkrementelle IDs für POST-Anfragen, Fehlerantworten nach einer bestimmten Anzahl von Anfragen).
    *   **Implementierungsidee**: Die `MOCK_RESPONSES` könnten nicht nur statische Bodies, sondern Funktionen oder Vorlagen speichern, die zur Generierung der Antwort ausgeführt werden.
3.  **Middleware/Plugins**: Für komplexere Szenarien könnte ein Middleware-Muster eingeführt werden, um die Ausführung benutzerdefinierter Logik vor oder nach der Hauptgenerierung der Mock-Antwort zu ermöglichen (z. B. Authentifizierung, Protokollierung, Anforderungsänderung).
4.  **Unterstützung für andere HTTP-Methoden**: `MockAPIHandler` kann einfach erweitert werden, um `do_PUT`, `do_DELETE`, `do_PATCH` usw. nach dem bestehenden Muster aufzunehmen.
5.  **HTTPS-Unterstützung**: Für das Testen sicherer Endpunkte würde das Hinzufügen eines `ssl`-Kontexts zum `TCPServer` HTTPS ermöglichen.
6.  **CLI-Argumente**: `run_server` kann erweitert werden, um Befehlszeilenargumente für Port, Konfigurationsdateipfad usw. mithilfe von `argparse` zu akzeptieren.

## Sicherheitsüberlegungen

Als Mock-Server ist die Sicherheit im Allgemeinen weniger besorgniserregend, da er für lokale Entwicklungs- und Testumgebungen gedacht ist. Einige grundlegende Punkte sind jedoch relevant:

*   **Exposition**: Dieser Server sollte **nicht** ohne entsprechende Sicherheitsmaßnahmen (z. B. Firewalls, Zugriffskontrolle) dem öffentlichen Internet ausgesetzt werden. Er ist für die Verwendung im internen Netzwerk oder auf dem Localhost konzipiert.
*   **Eingabevalidierung**: Obwohl der aktuelle POST-Handler versucht, JSON zu parsen, würde ein produktionsreifer Server eine robuste Eingabevalidierung erfordern, um verschiedene Angriffsvektoren (z. B. Injection-Angriffe, fehlerhafte Anfragen) zu verhindern.
*   **Ressourcenbeschränkungen**: Der `http.server` ist nicht für Hochleistungs- oder hohe Last ausgelegt. Für produktionsähnliche Lasttests wären robustere Lösungen erforderlich. Dieser Mock-Server eignet sich am besten für Funktionstests und schnelles Prototyping.

Durch die Einhaltung dieser architektonischen Prinzipien und die Planung zukünftiger Verbesserungen soll der REST API Mock Server ein robustes und anpassungsfähiges Werkzeug für Entwickler sein.
