#!/usr/bin/env python3

"""
TanzoLang CLI tool

A command-line interface for working with TanzoLang profiles.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click

# Add the parent directory to the Python path to import the tanzo_schema package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from clients.python.tanzo_schema import validate_document, run_simulation, export_shorthand


@click.group()
def cli():
    """TanzoLang CLI - Tools for working with TanzoLang profiles."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True, readable=True))
def validate(file: str):
    """Validate a TanzoLang profile against the schema."""
    try:
        errors = validate_document(file)
        
        if not errors:
            click.echo(click.style("Validation passed!", fg="green", bold=True))
            return 0
        else:
            click.echo(click.style("Validation failed!", fg="red", bold=True))
            for error in errors:
                click.echo(click.style(f"  - {error}", fg="red"))
            return 1
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red", bold=True))
        return 1


@cli.command()
@click.argument('file', type=click.Path(exists=True, readable=True))
@click.option('--iterations', '-i', type=int, default=100, help='Number of simulation iterations to run')
def simulate(file: str, iterations: int):
    """Run a Monte Carlo simulation on a TanzoLang profile."""
    try:
        # Validate the document first
        errors = validate_document(file)
        if errors:
            click.echo(click.style("Validation failed!", fg="red", bold=True))
            for error in errors:
                click.echo(click.style(f"  - {error}", fg="red"))
            return 1
        
        # Run the simulation
        click.echo(f"Running simulation with {iterations} iterations...")
        results = run_simulation(file, iterations=iterations)
        
        # Display the results
        click.echo(results)
        return 0
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red", bold=True))
        return 1


@cli.command()
@click.argument('file', type=click.Path(exists=True, readable=True))
def export(file: str):
    """Export a TanzoLang profile to a shorthand string."""
    try:
        # Validate the document first
        errors = validate_document(file)
        if errors:
            click.echo(click.style("Validation failed!", fg="red", bold=True))
            for error in errors:
                click.echo(click.style(f"  - {error}", fg="red"))
            return 1
        
        # Generate the shorthand
        shorthand = export_shorthand(file)
        
        # Display the result
        click.echo(shorthand)
        return 0
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red", bold=True))
        return 1


def main():
    """Entry point for the CLI."""
    return cli()


if __name__ == "__main__":
    sys.exit(main())
