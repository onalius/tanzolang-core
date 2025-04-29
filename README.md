# TanzoLang Core

[![CI](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml/badge.svg)](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/onalius/tanzo-lang-core/branch/main/graph/badge.svg)](https://codecov.io/gh/onalius/tanzo-lang-core)
[![PyPI version](https://badge.fury.io/py/tanzo-schema.svg)](https://badge.fury.io/py/tanzo-schema)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://onalius.github.io/tanzo-lang-core/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/onalius/tanzo-lang-core/blob/main/CONTRIBUTING.md)

**TanzoLang is an open-source language for giving soul to AI.**

TanzoLang provides a structured framework for encoding AI personality blueprints using archetypal and typological systems. It enables symbolic, archetypal personality definition across platforms, allowing for the creation of rich, nuanced AI personas with depth and meaning.

Visit [TomoTanzo.com](https://tomotanzo.com) for the official UI and marketplace for AI personas.

## 📚 Documentation

- [TANZOLANG.md](./TANZOLANG.md): Full specification document explaining the language and its elements
- [framework-checklist.md](./framework-checklist.md): Implementation roadmap for the framework
- [Registry of Archetypes](./registry/archetypes/): Canonical archetype definitions

## 🌟 Features

- **JSON-Schema Specification**: Define archetypes and their attributes with strong validation
- **Probability Distributions**: Support for normal, uniform, and discrete distributions for simulation
- **Python SDK**: Pydantic-based models for type-safe manipulation
- **TypeScript SDK**: Zod-powered schema validation and type inference
- **CLI Tools**: Command-line utilities for validation, simulation, and export

## 📦 Installation

### Python

#### Using pip

```bash
pip install tanzo-schema
```

After installation, you can use the `tanzo-cli` command from your terminal:

```bash
# Show help
tanzo-cli --help

# Validate a profile
tanzo-cli validate profile.yaml

# Run a simulation
tanzo-cli simulate profile.yaml

# Export a profile
tanzo-cli export profile.yaml
```

#### Using Poetry (recommended for development)

```bash
# Clone the repository
git clone https://github.com/onalius/tanzo-lang-core.git
cd tanzo-lang-core

# Install with Poetry
poetry install

# Use the CLI through Poetry
poetry run tanzo-cli --help
```

### 🐍 Manual Installation (if Poetry fails)

If Poetry isn't working or you're encountering compiler errors (like with NumPy), you can install manually with pip:

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
pip install -U pip
pip install numpy==1.26.4 --only-binary=:all:
pip install -e .[dev]
```

Alternatively, you can use the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

Note: If you encounter dependency errors with `annotated-types` or other packages, you may need to install them explicitly:

```bash
pip install annotated-types pydantic click jsonschema pyyaml
```

This approach ensures NumPy is installed as a binary wheel, avoiding compiler issues on systems without native build tools.
