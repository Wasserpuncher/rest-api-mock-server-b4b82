import http.server
import socketserver
import json
import logging
from typing import Dict, Any

# Konfiguriere das Logging für bessere Sichtbarkeit
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MockAPIHandler(http.server.BaseHTTPRequestHandler):
    """
    Ein benutzerdefinierter HTTP-Anfrage-Handler, der als Mock-API-Server fungiert.
    Es verarbeitet GET- und POST-Anfragen und liefert vordefinierte Antworten.
    """
    # Beispiel für Mock-Daten. In zukünftigen Versionen könnte dies aus einer Konfigurationsdatei geladen werden.
    MOCK_RESPONSES: Dict[str, Dict[str, Any]] = {
        "/api/users": {
            "GET": {"status": 200, "body": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]},
            "POST": {"status": 201, "body": {"message": "User created successfully", "id": 3}}
        },
        "/api/products": {
            "GET": {"status": 200, "body": [{"id": 101, "name": "Laptop"}, {"id": 102, "name": "Mouse"}]},
        },
        "/api/status": {
            "GET": {"status": 200, "body": {"status": "ok", "server": "MockAPI v1.0"}}
        }
    }

    def _set_headers(self, status_code: int = 200, content_type: str = "application/json") -> None:
        """
        Setzt die Standard-HTTP-Header für die Antwort.

        Args:
            status_code (int): Der HTTP-Statuscode, der gesetzt werden soll.
            content_type (str): Der Content-Type-Header der Antwort.
        """
        self.send_response(status_code) # Sendet den HTTP-Statuscode
        self.send_header("Content-type", content_type) # Setzt den Content-Type-Header
        self.end_headers() # Beendet die Header-Sektion

    def _send_response(self, path: str, method: str) -> None:
        """
        Sendet eine Mock-Antwort basierend auf dem Pfad und der HTTP-Methode.

        Args:
            path (str): Der angefragte URL-Pfad.
            method (str): Die HTTP-Methode (z.B. "GET", "POST").
        """
        # Überprüfe, ob der Pfad in den Mock-Antworten existiert
        if path in self.MOCK_RESPONSES:
            # Überprüfe, ob die Methode für diesen Pfad definiert ist
            if method in self.MOCK_RESPONSES[path]:
                response_data = self.MOCK_RESPONSES[path][method] # Holt die definierte Antwort
                status = response_data.get("status", 200) # Holt den Statuscode, Standard ist 200
                body = response_data.get("body", {}) # Holt den Antwortkörper, Standard ist ein leeres Dictionary
                
                self._set_headers(status) # Setzt die Header mit dem entsprechenden Statuscode
                self.wfile.write(json.dumps(body).encode("utf-8")) # Schreibt den JSON-Antwortkörper
                logging.info(f"Mock-Antwort gesendet für {method} {path} mit Status {status}") # Loggt die gesendete Antwort
            else:
                # Wenn die Methode nicht definiert ist, antworte mit 405 Method Not Allowed
                self._set_headers(405) # Setzt den Statuscode auf 405
                self.wfile.write(json.dumps({"error": "Method Not Allowed"}).encode("utf-8")) # Sendet eine Fehlermeldung
                logging.warning(f"Methode {method} nicht erlaubt für Pfad {path}") # Loggt die Warnung
        else:
            # Wenn der Pfad nicht gefunden wird, antworte mit 404 Not Found
            self._set_headers(404) # Setzt den Statuscode auf 404
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8")) # Sendet eine Fehlermeldung
            logging.warning(f"Pfad {path} nicht gefunden") # Loggt die Warnung

    def do_GET(self) -> None:
        """
        Verarbeitet HTTP GET-Anfragen.
        """
        logging.info(f"GET-Anfrage empfangen für: {self.path}") # Loggt die empfangene GET-Anfrage
        self._send_response(self.path, "GET") # Sendet die entsprechende Mock-Antwort

    def do_POST(self) -> None:
        """
        Verarbeitet HTTP POST-Anfragen.
        Liest den Anfragekörper, falls vorhanden, und gibt eine Mock-Antwort zurück.
        """
        content_length = int(self.headers.get('Content-Length', 0)) # Holt die Länge des Anfragekörpers
        post_data = self.rfile.read(content_length) # Liest den Anfragekörper
        
        try:
            json_data = json.loads(post_data.decode('utf-8')) # Versucht, den Anfragekörper als JSON zu parsen
            logging.info(f"POST-Anfrage empfangen für: {self.path}, Daten: {json_data}") # Loggt die empfangenen POST-Daten
        except json.JSONDecodeError:
            logging.warning(f"POST-Anfrage für {self.path} enthielt ungültiges JSON oder keine Daten.") # Loggt den JSON-Parsing-Fehler
            json_data = {}

        self._send_response(self.path, "POST") # Sendet die entsprechende Mock-Antwort

def run_server(port: int = 8000) -> None:
    """
    Startet den Mock-API-Server auf dem angegebenen Port.

    Args:
        port (int): Der Port, auf dem der Server lauschen soll.
    """
    # Erstellt einen TCP-Server, der unseren MockAPIHandler verwendet
    handler = MockAPIHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        logging.info(f"Mock-API-Server gestartet auf Port {port}") # Loggt den Serverstart
        logging.info("Verfügbare Endpunkte:")
        for path, methods in MockAPIHandler.MOCK_RESPONSES.items():
            for method in methods.keys():
                logging.info(f"  - {method} {path}") # Listet die verfügbaren Endpunkte auf
        
        try:
            httpd.serve_forever() # Startet den Server, der unendlich Anfragen verarbeitet
        except KeyboardInterrupt:
            logging.info("Server wird heruntergefahren...") # Loggt das Herunterfahren durch Benutzer
            httpd.shutdown() # Fährt den Server ordentlich herunter
            logging.info("Server heruntergefahren.") # Bestätigt das Herunterfahren

if __name__ == "__main__":
    run_server()
