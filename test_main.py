import unittest
import json
from unittest.mock import MagicMock, patch
from main import MockAPIHandler

class TestMockAPIHandler(unittest.TestCase):
    """
    Unit-Tests für die MockAPIHandler-Klasse.
    Wir testen die do_GET- und do_POST-Methoden sowie die Helper-Funktionen.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert einen Mock-Anfrage-Handler.
        """
        # Erstelle einen Mock-Request und Client-Adresse für den Handler
        self.mock_request = MagicMock() # Simuliert eine Socket-Verbindung
        self.mock_client_address = ('127.0.0.1', 12345) # Simuliert die Client-Adresse
        self.mock_server = MagicMock() # Simuliert den HTTP-Server

        # Erstelle eine Instanz des Handlers mit Mocks
        self.handler = MockAPIHandler(self.mock_request, self.mock_client_address, self.mock_server)

        # Mocke die Methoden, die HTTP-Antworten senden
        self.handler.send_response = MagicMock() # Simuliert das Senden des Statuscodes
        self.handler.send_header = MagicMock() # Simuliert das Senden von Headern
        self.handler.end_headers = MagicMock() # Simuliert das Beenden der Header

        # Mocke wfile zum Schreiben der Antwortdaten
        self.handler.wfile = MagicMock() # Simuliert die Ausgabedatei für die Antwort

    def test_set_headers(self):
        """
        Testet die interne _set_headers-Methode.
        """
        self.handler._set_headers(200, "text/plain") # Ruft die Methode auf
        self.handler.send_response.assert_called_once_with(200) # Überprüft den Statuscode
        self.handler.send_header.assert_called_once_with("Content-type", "text/plain") # Überprüft den Content-Type
        self.handler.end_headers.assert_called_once() # Überprüft, ob end_headers aufgerufen wurde

    def test_do_GET_existing_path(self):
        """
        Testet eine GET-Anfrage an einen existierenden Pfad.
        """
        self.handler.path = "/api/users" # Setzt den angefragten Pfad
        self.handler.do_GET() # Ruft die do_GET-Methode auf

        self.handler.send_response.assert_called_once_with(200) # Erwartet Status 200
        self.handler.send_header.assert_called_once_with("Content-type", "application/json") # Erwartet JSON Content-Type
        self.handler.end_headers.assert_called_once() # Erwartet, dass Header beendet werden
        
        # Überprüft den geschriebenen Antwortkörper
        expected_body = json.dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body) # Überprüft den Antwortkörper

    def test_do_GET_non_existing_path(self):
        """
        Testet eine GET-Anfrage an einen nicht-existierenden Pfad.
        """
        self.handler.path = "/api/nonexistent" # Setzt einen nicht-existierenden Pfad
        self.handler.do_GET() # Ruft die do_GET-Methode auf

        self.handler.send_response.assert_called_once_with(404) # Erwartet Status 404
        self.handler.send_header.assert_called_once_with("Content-type", "application/json") # Erwartet JSON Content-Type
        self.handler.end_headers.assert_called_once() # Erwartet, dass Header beendet werden

        expected_body = json.dumps({"error": "Not Found"}).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body) # Überprüft den Fehler-Antwortkörper

    def test_do_POST_existing_path(self):
        """
        Testet eine POST-Anfrage an einen existierenden Pfad mit Daten.
        """
        self.handler.path = "/api/users" # Setzt den angefragten Pfad
        post_data = b'{"name": "Charlie"}' # Beispiel-POST-Daten
        
        # Mocke die Header und rfile für POST-Anfragen
        self.handler.headers = {'Content-Length': str(len(post_data))} # Simuliert den Content-Length Header
        self.handler.rfile = MagicMock() # Simuliert die Eingabedatei für den Anfragekörper
        self.handler.rfile.read.return_value = post_data # Simuliert das Lesen der POST-Daten

        self.handler.do_POST() # Ruft die do_POST-Methode auf

        self.handler.send_response.assert_called_once_with(201) # Erwartet Status 201
        self.handler.send_header.assert_called_once_with("Content-type", "application/json") # Erwartet JSON Content-Type
        self.handler.end_headers.assert_called_once() # Erwartet, dass Header beendet werden

        expected_body = json.dumps({"message": "User created successfully", "id": 3}).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body) # Überprüft den Antwortkörper

    def test_do_POST_non_existing_path(self):
        """
        Testet eine POST-Anfrage an einen nicht-existierenden Pfad.
        """
        self.handler.path = "/api/nonexistent" # Setzt einen nicht-existierenden Pfad
        post_data = b'{"name": "David"}' # Beispiel-POST-Daten

        self.handler.headers = {'Content-Length': str(len(post_data))}
        self.handler.rfile = MagicMock()
        self.handler.rfile.read.return_value = post_data

        self.handler.do_POST() # Ruft die do_POST-Methode auf

        self.handler.send_response.assert_called_once_with(404) # Erwartet Status 404
        expected_body = json.dumps({"error": "Not Found"}).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body) # Überprüft den Fehler-Antwortkörper

    def test_do_POST_unsupported_method(self):
        """
        Testet eine POST-Anfrage an einen Pfad, der nur GET unterstützt (z.B. /api/products).
        """
        self.handler.path = "/api/products" # Pfad, der nur GET unterstützt
        post_data = b'{"item": "New Product"}'

        self.handler.headers = {'Content-Length': str(len(post_data))}
        self.handler.rfile = MagicMock()
        self.handler.rfile.read.return_value = post_data

        self.handler.do_POST() # Ruft die do_POST-Methode auf

        self.handler.send_response.assert_called_once_with(405) # Erwartet Status 405 (Method Not Allowed)
        expected_body = json.dumps({"error": "Method Not Allowed"}).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body) # Überprüft den Fehler-Antwortkörper

    def test_do_POST_invalid_json(self):
        """
        Testet eine POST-Anfrage mit ungültigem JSON-Körper.
        """
        self.handler.path = "/api/users"
        post_data = b'not a json string' # Ungültige JSON-Daten

        self.handler.headers = {'Content-Length': str(len(post_data))}
        self.handler.rfile = MagicMock()
        self.handler.rfile.read.return_value = post_data

        self.handler.do_POST() # Ruft die do_POST-Methode auf

        self.handler.send_response.assert_called_once_with(201) # Erwartet Status 201, da der Pfad existiert
        # Der Körper sollte die Standard-POST-Antwort für /api/users sein, da der Input ignoriert wird
        expected_body = json.dumps({"message": "User created successfully", "id": 3}).encode("utf-8")
        self.handler.wfile.write.assert_called_once_with(expected_body)


if __name__ == '__main__':
    unittest.main()
