# Local Language Assistant

A conversational AI assistant designed to help underserved communities access government scheme information through multi-language support and low-bandwidth optimization.

## Features

- **Multi-language Support**: Hindi, Tamil, Telugu, Bengali, and Marathi
- **Low-bandwidth Optimized**: Works on 2G networks with minimal data usage
- **Actionable Responses**: Clear, step-by-step guidance for accessing government schemes
- **Simple Language**: 5th-grade reading level for accessibility
- **Session Context**: Maintains conversation context for natural interactions

## Project Structure

```
local-language-assistant/
├── src/                    # Source code
│   ├── config.py          # Configuration module
│   └── __init__.py
├── tests/                  # Test suite
│   └── __init__.py
├── data/                   # Data files (schemes, etc.)
├── pyproject.toml         # Project dependencies and configuration
└── README.md
```

## Installation

1. Ensure you have Python 3.9 or higher installed
2. Install dependencies:

```bash
pip install -e .
```

For development dependencies:

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Development

This project uses:
- **FastAPI** for the backend API
- **Pydantic** for data validation
- **Hypothesis** for property-based testing
- **pytest** for unit and integration testing

## Requirements

See `.kiro/specs/local-language-assistant/requirements.md` for detailed requirements.

## Design

See `.kiro/specs/local-language-assistant/design.md` for technical design documentation.

## License

[To be determined]
