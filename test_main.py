import unittest
import json
import os
import time
import tempfile
import threading
import http.client
from unittest.mock import MagicMock, patch
from main import MockAPIHandler, load_config, create_server

class TestMockAPIHandler(unittest.TestCase):
    """
    Unit-Tests für die MockAPIHandler-Klasse.
    Wir testen die do_GET- und do_POST-Methoden sowie die Helper-Funktionen.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert einen Mock-Anfrage-Handler.
        """
        # BaseHTTPRequestHandler.__init__ würde beim normalen Konstruktor sofort die
        # Request-Maschinerie (setup/handle) starten und aus dem gemockten Socket lesen,
        # was zu "decoding to str: need a bytes-like object, MagicMock found" führt.
        # Daher erzeugen wir die Instanz ohne __init__ und statten sie mit echten Stubs aus,
        # sodass die Dispatch-Logik von MockAPIHandler echt geprüft wird.
        self.handler = MockAPIHandler.__new__(MockAPIHandler)

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


CONFIG_TEST_HOST = '127.0.0.1'
CONFIG_TEST_PORT = 8020


class TestConfigFileSupport(unittest.TestCase):
    """
    Tests für das Laden von Mock-Definitionen aus einer JSON-Konfigurationsdatei.

    Es wird eine echte temporäre Datei geschrieben, mit `load_config` geladen und
    sowohl auf Handler-Ebene als auch über einen echten laufenden Server geprüft.
    """

    config_content = {
        "/api/config-endpoint": {
            "GET": {"status": 200, "body": {"source": "config-file", "value": 42}},
            "POST": {"status": 201, "body": {"created": True}}
        }
    }

    @classmethod
    def setUpClass(cls) -> None:
        # Sichert die eingebauten Mocks, um sie nach den Tests wiederherzustellen.
        cls._original_mocks = MockAPIHandler.MOCK_RESPONSES

        fd, cls.config_path = tempfile.mkstemp(suffix=".json", prefix="config_")
        with os.fdopen(fd, "w", encoding="utf-8") as config_file:
            json.dump(cls.config_content, config_file)

    @classmethod
    def tearDownClass(cls) -> None:
        # Stellt die eingebauten Mocks wieder her, damit andere Testklassen nicht beeinflusst werden.
        MockAPIHandler.MOCK_RESPONSES = cls._original_mocks
        if os.path.exists(cls.config_path):
            os.remove(cls.config_path)

    def test_load_config_returns_expected_dict(self) -> None:
        """`load_config` liest die JSON-Datei korrekt ein."""
        loaded = load_config(self.config_path)
        self.assertEqual(loaded, self.config_content)

    def test_load_config_rejects_non_object(self) -> None:
        """Eine Top-Level-Liste statt Objekt wird abgelehnt."""
        fd, path = tempfile.mkstemp(suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as bad_file:
                json.dump([1, 2, 3], bad_file)
            with self.assertRaises(ValueError):
                load_config(path)
        finally:
            os.remove(path)

    def test_handler_serves_config_defined_route(self) -> None:
        """
        Ein Handler, der mit den geladenen Config-Mocks bestückt ist, liefert die
        in der Datei definierte Route mit dem konfigurierten Status und Body aus.
        """
        loaded = load_config(self.config_path)
        handler = MockAPIHandler.__new__(MockAPIHandler)
        # Instanz-Attribut überschreibt das Klassen-Attribut, ohne andere Tests zu beeinflussen.
        handler.MOCK_RESPONSES = loaded
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.wfile = MagicMock()

        handler.path = "/api/config-endpoint"
        handler.do_GET()

        handler.send_response.assert_called_once_with(200)
        expected_body = json.dumps({"source": "config-file", "value": 42}).encode("utf-8")
        handler.wfile.write.assert_called_once_with(expected_body)

    def test_running_server_uses_config(self) -> None:
        """
        Ein echter Server, der über `create_server` mit den Config-Mocks gestartet
        wird, beantwortet HTTP-Anfragen anhand der Config-Datei.
        """
        loaded = load_config(self.config_path)
        httpd = create_server(CONFIG_TEST_PORT, mocks=loaded)
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        time.sleep(0.3)
        try:
            conn = http.client.HTTPConnection(CONFIG_TEST_HOST, CONFIG_TEST_PORT)
            conn.request("GET", "/api/config-endpoint")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data, {"source": "config-file", "value": 42})
            conn.close()

            # Eine nur im eingebauten Default vorhandene Route ist nun nicht mehr definiert.
            conn = http.client.HTTPConnection(CONFIG_TEST_HOST, CONFIG_TEST_PORT)
            conn.request("GET", "/api/status")
            response = conn.getresponse()
            self.assertEqual(response.status, 404)
            conn.close()
        finally:
            httpd.shutdown()
            httpd.server_close()
            server_thread.join(timeout=1)


if __name__ == '__main__':
    unittest.main()
