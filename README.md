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

### For Developers

If you're developing TanzoLang Core or experiencing issues with binary dependencies (like NumPy), use the provided requirements template:

```bash
# Rename the template first
mv requirements_template.txt requirements.txt

# Install using pip with binary packages
pip install -r requirements.txt
```

This approach ensures NumPy is installed as a binary wheel, avoiding compiler issues on systems without native build tools.
