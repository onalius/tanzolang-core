#!/usr/bin/env python3

# Re-export the CLI for easier importing in tests
from cli.tanzo_cli import cli

if __name__ == "__main__":
    cli()