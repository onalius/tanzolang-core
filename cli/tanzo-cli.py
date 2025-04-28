#!/usr/bin/env python3
"""
Tanzo CLI - Command-line interface for TanzoLang

This CLI provides utilities for validating, simulating, and exporting TanzoLang profiles.

Usage:
    tanzo-cli.py validate <file>
    tanzo-cli.py simulate <file> [--iterations=<n>]
    tanzo-cli.py export <file> [--format=<fmt>]
    tanzo-cli.py --help
"""

import os
import sys
import json
import click
from pathlib import Path

# Add parent directory to sys.path to import tanzo_schema
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from clients.python.tanzo_schema import (
        validate_tanzo_profile, load_profile_from_yaml,
        export_profile_shorthand, simulate_profile
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent / "clients" / "python"))
    from tanzo_schema import (
        validate_tanzo_profile, load_profile_from_yaml,
        export_profile_shorthand, simulate_profile
    )


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Tanzo CLI - Command-line interface for TanzoLang profiles."""
    pass


@cli.command("validate")
@click.argument("file", type=click.Path(exists=True, readable=True, path_type=Path))
def validate_cmd(file: Path):
    """Validate a TanzoLang profile against the schema."""
    try:
        profile = load_profile_from_yaml(file)
        click.echo(f"✅ Profile '{profile.profile.name}' is valid!")
        return 0
    except ValueError as e:
        click.echo(f"❌ Validation error: {str(e)}", err=True)
        return 1
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        return 1


@cli.command("simulate")
@click.argument("file", type=click.Path(exists=True, readable=True, path_type=Path))
@click.option(
    "--iterations", "-i", type=int, default=100,
    help="Number of Monte Carlo iterations to run (default: 100)"
)
def simulate_cmd(file: Path, iterations: int):
    """Run a Monte Carlo simulation on a TanzoLang profile."""
    try:
        profile = load_profile_from_yaml(file)
        result = simulate_profile(profile, iterations=iterations)
        click.echo(result.summary)
        return 0
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        return 1


@cli.command("export")
@click.argument("file", type=click.Path(exists=True, readable=True, path_type=Path))
@click.option(
    "--format", "-f", type=click.Choice(["short", "json", "yaml"]), default="short",
    help="Export format (default: short)"
)
def export_cmd(file: Path, format: str):
    """Export a TanzoLang profile in various formats."""
    try:
        profile = load_profile_from_yaml(file)
        
        if format == "short":
            result = export_profile_shorthand(profile)
            click.echo(result)
        elif format == "json":
            from tanzo_schema.exporters import export_profile_json
            result = export_profile_json(profile)
            click.echo(result)
        elif format == "yaml":
            from tanzo_schema.exporters import export_profile_yaml
            result = export_profile_yaml(profile)
            click.echo(result)
        
        return 0
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        return 1


if __name__ == "__main__":
    sys.exit(cli())
