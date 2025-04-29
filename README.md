# TanzoLang Core

[![CI](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml/badge.svg)](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/onalius/tanzo-lang-core/branch/main/graph/badge.svg)](https://codecov.io/gh/onalius/tanzo-lang-core)
[![PyPI version](https://badge.fury.io/py/tanzo-schema.svg)](https://badge.fury.io/py/tanzo-schema)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://onalius.github.io/tanzo-lang-core/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

TanzoLang is the open schema specification for defining digital archetypes and their attributes in the Tomodaichi Tanzo ecosystem.

## 🌟 Features

- **JSON-Schema Specification**: Define archetypes and their attributes with strong validation
- **Probability Distributions**: Support for normal, uniform, and discrete distributions for simulation
- **Python SDK**: Pydantic-based models for type-safe manipulation
- **TypeScript SDK**: Zod-powered schema validation and type inference
- **CLI Tools**: Command-line utilities for validation, simulation, and export

## 📦 Installation

### Python

```bash
pip install tanzo-schema
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

This approach ensures NumPy is installed as a binary wheel, avoiding compiler issues on systems without native build tools.
