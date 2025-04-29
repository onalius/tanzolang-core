#!/usr/bin/env python3
"""
Tanzo CLI - Command-line interface for working with TanzoLang profiles.

This CLI provides commands for validating, simulating, and exporting TanzoLang profiles.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import click
import yaml

# Add parent directory to path to allow importing the tanzo_schema package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from tanzo_schema import (
        export_profile,
        simulate_profile,
        summarize_simulations,
        validate_profile,
    )
except ImportError:
    # If the package is not installed, try to import from clients/python
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "clients" / "python"))
    from tanzo_schema import (
        export_profile,
        simulate_profile,
        summarize_simulations,
        validate_profile,
    )


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Tanzo CLI - Command-line interface for working with TanzoLang profiles.
    
    This CLI provides commands for validating, simulating, and exporting TanzoLang profiles.
    """
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show detailed validation output")
def validate(file: str, verbose: bool):
    """
    Validate a TanzoLang profile file.
    
    Checks the provided file against the TanzoLang schema and reports any validation errors.
    
    Example:
        tanzo-cli validate examples/Kai_profile.yaml
    """
    errors = validate_profile(file)
    
    if not errors:
        click.echo(click.style("✓ Profile is valid", fg="green"))
        return 0
    else:
        click.echo(click.style("✗ Profile validation failed:", fg="red"))
        for error in errors:
            click.echo(click.style(f"  - {error}", fg="red"))
        return 1


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--iterations", "-i", default=100, help="Number of simulation iterations")
@click.option("--variance", "-v", type=float, help="Global variance factor (0-1)")
@click.option("--output", "-o", type=click.Path(), help="Output file for detailed results")
def simulate(file: str, iterations: int, variance: Optional[float], output: Optional[str]):
    """
    Run Monte-Carlo simulation on a TanzoLang profile.
    
    Generates multiple variations of the profile based on trait and attribute variances
    and produces statistical summaries.
    
    Example:
        tanzo-cli simulate examples/Kai_profile.yaml --iterations 100
    """
    # First validate the profile
    errors = validate_profile(file)
    if errors:
        click.echo(click.style("✗ Profile validation failed:", fg="red"))
        for error in errors:
            click.echo(click.style(f"  - {error}", fg="red"))
        return 1
    
    # Run simulations
    click.echo(f"Running {iterations} simulation iterations...")
    
    simulations = simulate_profile(file, iterations, variance)
    summary = summarize_simulations(simulations)
    
    # Display summary
    click.echo("\nSimulation Summary:")
    click.echo("===================")
    
    # Output traits
    click.echo("\nPersonality Traits:")
    click.echo("-----------------")
    for trait in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
        if trait in summary:
            stats = summary[trait]
            click.echo(f"{trait.capitalize()}: {stats['mean']:.1f} (±{stats['std_dev']:.1f}), range: {stats['min']:.1f}-{stats['max']:.1f}")
    
    # Output other statistics
    for key, stats in summary.items():
        if key not in ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]:
            category = key.replace(".", " > ")
            click.echo(f"\n{category.capitalize()}:")
            click.echo(f"  Mean: {stats['mean']:.1f}")
            click.echo(f"  Std Dev: {stats['std_dev']:.1f}")
            click.echo(f"  Range: {stats['min']:.1f} - {stats['max']:.1f}")
    
    # Save detailed results if output path provided
    if output:
        output_path = Path(output)
        with open(output_path, "w") as f:
            if output_path.suffix.lower() == ".json":
                json.dump({"summary": summary, "simulations": simulations}, f, indent=2)
            else:
                yaml.dump({"summary": summary, "simulations": simulations}, f)
        click.echo(f"\nDetailed results saved to {output}")
    
    return 0


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--format", "-f", type=click.Choice(["shorthand", "json", "yaml"]), default="shorthand", help="Output format")
@click.option("--output", "-o", type=click.Path(), help="Output file (defaults to stdout)")
def export(file: str, format: str, output: Optional[str]):
    """
    Export a TanzoLang profile in various formats.
    
    Converts a TanzoLang profile to different formats:
    - shorthand: A compact string representation
    - json: Formatted JSON
    - yaml: Formatted YAML
    
    Example:
        tanzo-cli export examples/Kai_profile.yaml --format shorthand
    """
    # First validate the profile
    errors = validate_profile(file)
    if errors:
        click.echo(click.style("✗ Profile validation failed:", fg="red"))
        for error in errors:
            click.echo(click.style(f"  - {error}", fg="red"))
        return 1
    
    # Generate export based on format
    if format == "shorthand":
        result = export_profile(file, "shorthand")
    elif format == "json":
        result = export_profile(file, "json")
    elif format == "yaml":
        profile_dict = export_profile(file, "dict")
        result = yaml.dump(profile_dict, sort_keys=False)
    
    # Output result
    if output:
        with open(output, "w") as f:
            f.write(result)
        click.echo(f"Exported profile to {output}")
    else:
        click.echo(result)
    
    return 0


if __name__ == "__main__":
    cli()
