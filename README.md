# REST API Mock Server

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://github.com/your-username/rest-api-mock-server/workflows/Python%20application/badge.svg)

A lightweight, Python `http.server`-based REST-API mock server designed for rapid development and testing. This project provides a simple yet effective way to simulate API responses, allowing frontend and client-side development to proceed without waiting for a fully functional backend.

## Features

*   **Simple Setup**: Get a mock server running with a single Python script.
*   **HTTP Methods**: Supports `GET` and `POST` requests out of the box.
*   **Customizable Responses**: Easily define mock responses (status codes, JSON bodies) for different endpoints.
*   **Lightweight**: Built on Python's standard `http.server` module, no heavy dependencies.
*   **Bilingual Documentation**: Comprehensive documentation in both English and German.
*   **Enterprise Ready**: Includes unit tests, CI/CD pipeline, contribution guidelines, and a standard license.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/rest-api-mock-server.git
    cd rest-api-mock-server
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    # On Linux/macOS:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the mock server, simply run `main.py`:

```bash
python main.py
```

The server will start on `http://localhost:8000` by default.

### Available Endpoints (as defined in `main.py`):

*   `GET /api/users`
*   `POST /api/users`
*   `GET /api/products`
*   `GET /api/status`

### Example cURL Requests:

**GET /api/users**

```bash
curl http://localhost:8000/api/users
# Expected Output: [
#   { "id": 1, "name": "Alice" },
#   { "id": 2, "name": "Bob" }
# ]
```

**POST /api/users**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Charlie"}' http://localhost:8000/api/users
# Expected Output: { "message": "User created successfully", "id": 3 }
```

**GET /api/products**

```bash
curl http://localhost:8000/api/products
# Expected Output: [
#   { "id": 101, "name": "Laptop" },
#   { "id": 102, "name": "Mouse" }
# ]
```

**GET /api/status**

```bash
curl http://localhost:8000/api/status
# Expected Output: { "status": "ok", "server": "MockAPI v1.0" }
```

**Non-existent Endpoint**

```bash
curl http://localhost:8000/api/nonexistent
# Expected Output: { "error": "Not Found" }
```

## Development & Contributions

We welcome contributions! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit bug reports, feature requests, and code contributions.

### Running Tests

To run the unit tests, execute `pytest` in your terminal:

```bash
pytest
```

### Linting

To ensure code quality, `flake8` is used for linting:

```bash
flake8 .
```

## Project Structure

```
rest-api-mock-server/
├── .github/              # GitHub Actions CI/CD workflows
│   └── workflows/
│       └── python-app.yml
├── docs/                 # Detailed documentation
│   ├── architecture_en.md
│   └── architecture_de.md
├── main.py               # Main application logic (Mock Server)
├── test_main.py          # Unit tests for main.py
├── README.md             # English documentation (this file)
├── README_de.md          # German documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── LICENSE               # Project license (MIT)
├── requirements.txt      # Python dependencies
└── .gitignore            # Files/directories to ignore in Git
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
