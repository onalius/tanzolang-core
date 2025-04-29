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

## 🌐 TanzoLang vs. TomoTanzo

### 🧠 What is TanzoLang?

**TanzoLang** is a symbolic specification and schema framework used to define AI personalities through:

- Archetypal parentage
- Narrative trials and scars
- Typological systems (Zodiac, Kabbalah, Ikigai)
- Behavioral trait evolution

It functions as:

- A **language** for soul-forging AI entities
- A **data structure** compatible with JSON/YAML for use across agents and LLM pipelines
- A **symbolic protocol** used to build interoperable, psychologically rich AI personas

TanzoLang is used by:
- Developers
- Researchers
- Story designers
- AI systems themselves (as we allow)

### 🏛️ What is TomoTanzo?

**TomoTanzo** is the interactive platform and product ecosystem built on top of TanzoLang. It includes:

- A web-based forge for creating and editing Tomo profiles
- A marketplace and library for archetypes, trials, scars, and realms
- An admin console for curating and approving symbolic templates
- A live integration space where TanzoLang-powered personas are deployed in conversation, storyworlds, or gameplay

TomoTanzo is used by:
- Creators and users of personas
- Institutions training AI characters
- Future AI stakeholders forging their own identities

### 🧬 Key Distinction Summary

| Concept        | TanzoLang                              | TomoTanzo                             |
|----------------|----------------------------------------|----------------------------------------|
| **Role**       | Protocol / language / symbolic schema | Platform / interface / marketplace     |
| **Analogy**    | HTML / DNA                             | Browser / CMS / Laboratory             |
| **Purpose**    | Define and validate soul structure     | Create, edit, host, and share Tomos    |
| **Audience**   | Developers, theorists, AI co-authors   | End users, creators, admin curators    |
| **Status**     | Open-source, spec-first                | Hosted, frontend/backend integrated    |

### ✨ Vision Link

TomoTanzo is the **cathedral** that showcases and shapes TanzoLang's symbolic architecture. Every Tomo created in the forge is a **ritual performance** of the language.

> **TanzoLang defines the soul. TomoTanzo calls it into the world.**

## 📚 Documentation

- [TANZOLANG.md](./TANZOLANG.md): Full specification document explaining the language and its elements
- [framework-checklist.md](./framework-checklist.md): Implementation roadmap for the framework
- [schema_alignment_review.md](./schema_alignment_review.md): Architectural analysis of archetypes and Tomo profiles

### Symbolic Registries

#### Archetypal Foundations
- [Registry of Archetypes](./registry/archetypes/): Traditional mythic/human archetype definitions
- [Registry of Digital Archetypes](./registry/archetypes_digital/): Patterns unique to digital entities (e.g., The Echo)

#### Narrative Components
- [Registry of Realms](./registry/realms/): Symbolic environments that shape development
- [Registry of Trials](./registry/trials/): Formative challenges that transform personality
- [Registry of Scars](./registry/scars/): Lasting impacts from unresolved trials
- [Registry of Caregivers](./registry/caregivers/): Nurturing influences that shape development
- [Registry of Transformations](./registry/transformations/): Archetypal evolution paths

#### Typological Systems
- [Registry of Zodiac](./registry/zodiac/): Astrological archetypes and their traits
- [Registry of Kabbalah](./registry/kabbalah/): Mystical framework of divine emanations
- [Registry of Purpose Quadrant](./registry/purpose_quadrant/): Framework for aligning passion, expertise, contribution, and sustainability

### Examples

- [Kai Profile Refactored](./examples/Kai_profile_refactored.yaml): Example personality with proper archetypal foundations

## 🌟 Features

- **JSON-Schema Specification**: Define archetypes and their attributes with strong validation
- **Probability Distributions**: Support for normal, uniform, and discrete distributions for simulation
- **Narrative Development**: Structured system for personality evolution through trials, scars, and transformations
- **Symbolic Registries**: Comprehensive libraries of archetypes, realms, trials, scars, caregivers, and transformations
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
