# Contributing to REST API Mock Server

We welcome contributions from the community! Whether you're reporting a bug, suggesting a feature, or submitting code, your help is valuable. Please take a moment to review this document to ensure a smooth contribution process.

## Table of Contents

1.  [Code of Conduct](#code-of-conduct)
2.  [How to Contribute](#how-to-contribute)
    *   [Bug Reports](#bug-reports)
    *   [Feature Requests](#feature-requests)
    *   [Code Contributions](#code-contributions)
3.  [Development Setup](#development-setup)
4.  [Code Style](#code-style)
5.  [Testing](#testing)
6.  [Commit Messages](#commit-messages)
7.  [License](#license)

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md) (not yet created but implied). By participating in this project, you agree to abide by its terms.

## How to Contribute

### Bug Reports

If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/your-username/rest-api-mock-server/issues). When reporting a bug, please include:

*   A clear and concise description of the bug.
*   Steps to reproduce the behavior.
*   Expected behavior.
*   Actual behavior.
*   Screenshots or error messages, if applicable.
*   Your operating system and Python version.

### Feature Requests

We love to hear your ideas for new features! Please open an issue on the [GitHub Issues page](https://github.com/your-username/rest-api-mock-server/issues) with the label `enhancement`.

*   Clearly describe the feature you'd like to see.
*   Explain why this feature would be useful.
*   Provide any examples or mockups if possible.

### Code Contributions

If you'd like to contribute code, please follow these steps:

1.  **Fork the repository** to your own GitHub account.
2.  **Clone your forked repository** to your local machine:
    ```bash
    git clone https://github.com/your-username/rest-api-mock-server.git
    cd rest-api-mock-server
    ```
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    # or for a bug fix:
    git checkout -b bugfix/issue-number-short-description
    ```
4.  **Make your changes.** Ensure you adhere to the [Code Style](#code-style) and write [Tests](#testing) for your changes.
5.  **Run tests and linting** to ensure everything is working correctly and adheres to standards.
6.  **Commit your changes** with a clear and descriptive [Commit Message](#commit-messages).
7.  **Push your branch** to your forked repository:
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request** from your branch to the `main` branch of the original repository. Provide a clear description of your changes and reference any related issues.

## Development Setup

To set up your development environment, follow the [Installation](#installation) steps in `README.md` and ensure you install the development dependencies:

```bash
pip install -r requirements.txt
```

## Code Style

We follow common Python style guidelines:

*   **PEP 8**: Adhere to PEP 8 for code formatting.
*   **Type Hinting**: Use type hints for function arguments and return values.
*   **Docstrings**: All public classes, methods, and functions should have clear docstrings (using reStructuredText or Google style).
*   **Variable Names**: Use clear, descriptive English variable names.
*   **Inline Comments**: Use inline comments to explain complex logic, especially in German for beginner-friendliness.

We use `flake8` for linting. You can run it locally:

```bash
flake8 .
```

## Testing

All new features and bug fixes should be accompanied by appropriate unit tests. Tests are written using `unittest` (or `pytest` runner).

*   **Location**: Tests reside in `test_main.py` for `main.py`.
*   **Running Tests**: To run all tests, navigate to the project root and execute:
    ```bash
    pytest
    ```

## Commit Messages

Please use clear and concise commit messages. A good commit message explains *what* was changed and *why*. We generally follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification, but a simpler `type: subject` format is also acceptable (e.g., `feat: Add config file support`, `fix: Handle invalid JSON in POST`).

## License

By contributing to the REST API Mock Server, you agree that your contributions will be licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
