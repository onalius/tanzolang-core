# TanzoLang Core

[![CI](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml/badge.svg)](https://github.com/onalius/tanzo-lang-core/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/onalius/tanzo-lang-core/branch/main/graph/badge.svg)](https://codecov.io/gh/onalius/tanzo-lang-core)
[![PyPI version](https://badge.fury.io/py/tanzo-schema.svg)](https://badge.fury.io/py/tanzo-schema)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://onalius.github.io/tanzo-lang-core/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Core schema and tools for the TanzoLang ecosystem - a specification for modeling digital, physical, social, emotional, and cognitive archetypes in the Tomodaichi Tanzo ecosystem.

## Overview

TanzoLang is a schema specification for defining profiles with archetypes and traits. This repository provides:

- The canonical JSON Schema specification 📜
- Python and TypeScript SDKs for working with TanzoLang profiles 🧰
- CLI tools for validating, simulating, and exporting profiles 🛠️
- Comprehensive documentation and examples 📚

## 🚀 Quick Start

### Python SDK and CLI

```bash
# Install using pip
pip install tanzo-schema

# Validate a profile
tanzo-cli validate examples/Kai_profile.yaml

# Run a simulation
tanzo-cli simulate examples/Kai_profile.yaml

# Export to shorthand format
tanzo-cli export examples/Kai_profile.yaml
