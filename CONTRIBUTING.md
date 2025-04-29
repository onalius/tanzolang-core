# Contributing to TanzoLang Core

Thank you for considering contributing to TanzoLang! This document outlines the process for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Development Workflow

### Branch Naming

We use the following branch naming convention:

- `feature/short-description` - For new features
- `fix/short-description` - For bug fixes
- `docs/short-description` - For documentation changes
- `refactor/short-description` - For code refactoring
- `test/short-description` - For adding or updating tests

### Conventional Commits

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This enables automatic versioning and changelog generation.

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Development Setup

1. Clone the repository

```bash
git clone https://github.com/onalius/tanzo-lang-core.git
cd tanzo-lang-core
```

2. Set up the development environment

**Using Poetry (recommended):**

```bash
# Install Poetry if you don't have it
pip install poetry

# Install dependencies
poetry install
```

**Using Pip with requirements file (alternative):**

If you're experiencing compilation issues with NumPy or other binary dependencies:

```bash
# First rename the template file
mv requirements_template.txt requirements.txt

# Install using pip with binary wheels
pip install -r requirements.txt
```

3. Run the tests

```bash
pytest
```

