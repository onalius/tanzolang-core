# Contributing to TanzoLang Core

Thank you for your interest in contributing to TanzoLang Core! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
  - [Branch Naming](#branch-naming)
  - [Commit Messages](#commit-messages)
  - [Pull Requests](#pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.11+
- Poetry (for Python dependency management)
- Node.js 16+ (for TypeScript development)
- Git

### Setting Up the Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/tanzo-lang-core.git
   cd tanzo-lang-core
   ```

2. Set up Python environment with Poetry:
   ```bash
   poetry install
   ```

3. Set up TypeScript environment:
   ```bash
   cd clients/typescript
   npm install
   ```

4. Install pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## Making Changes

### Branch Naming

Use the following conventions for branch names:

- `feature/short-description` - For new features
- `fix/issue-description` - For bug fixes
- `docs/what-changed` - For documentation updates
- `refactor/what-changed` - For code refactoring
- `test/what-changed` - For test-related changes

Include the issue number if applicable: `fix/issue-42-description`

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification, which provides a standardized format for commit messages:

