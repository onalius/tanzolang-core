# Contributing to TanzoLang Core

Thank you for your interest in contributing to TanzoLang Core! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Getting Started

1. Fork the repository
2. Clone your forked repository
3. Install development dependencies with Poetry: `poetry install`
4. Install pre-commit hooks: `poetry run pre-commit install`

## Development Workflow

### Branch Naming Convention

Use the following format for branch names:

- `feature/short-description` - For new features
- `fix/issue-short-description` - For bug fixes
- `docs/short-description` - For documentation updates
- `refactor/short-description` - For code refactoring
- `test/short-description` - For adding or updating tests

Example: `feature/add-new-archetype-validator`

### Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages. This enables automatic versioning and changelog generation.

Format: `<type>(<scope>): <description>`

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `chore`: Build process or auxiliary tool changes

Examples:
- `feat(schema): add new communication style options`
- `fix(cli): resolve validation error handling issue`
- `docs(readme): update installation instructions`

### Pre-commit Hooks

We use pre-commit hooks to enforce code quality. The hooks run:

- Black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting
- Commitizen for commit message validation

If a pre-commit hook fails, the commit will be aborted. You can run the checks manually:

```bash
poetry run pre-commit run --all-files
