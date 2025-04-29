#!/usr/bin/env python3
"""
TanzoLang CLI Tool

A command-line interface for working with TanzoLang profiles.
"""

import sys
import os
from pathlib import Path
import json
import click

# Add parent directory to import path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from clients.python.tanzo_schema.validator import validate_profile
from clients.python.tanzo_schema.simulator import simulate_profile
from clients.python.tanzo_schema.exporter import export_profile


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    TanzoLang CLI - Tools for working with TanzoLang profiles.
    
    This CLI provides utilities for validating, simulating, and exporting
    TanzoLang profiles that describe digital archetypes and attributes.
    """
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False, readable=True))
def validate(file):
    """
    Validate a TanzoLang profile file.
    
    Checks if the file conforms to the TanzoLang schema and reports any errors.
    """
    try:
        profile = validate_profile(file)
        click.echo(click.style(f"✓ Profile '{profile.profile.name}' is valid", fg='green'))
        click.echo(f"  - {len(profile.profile.archetypes)} archetypes")
        
        for idx, archetype in enumerate(profile.profile.archetypes, 1):
            archetype_name = archetype.name or archetype.type.value
            click.echo(f"  - Archetype {idx}: {archetype_name} ({archetype.type.value})")
            click.echo(f"    - {len(archetype.attributes)} attributes")
        
        return 0
    
    except Exception as e:
        click.echo(click.style(f"✗ Validation failed: {str(e)}", fg='red'))
        return 1


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--iterations', '-i', default=100, type=int, help='Number of simulation iterations')
@click.option('--output', '-o', type=click.Path(dir_okay=False, writable=True), 
              help='Output file for simulation results (JSON format)')
def simulate(file, iterations, output):
    """
    Run a Monte-Carlo simulation on a TanzoLang profile.
    
    Performs multiple iterations and reports statistical results.
    """
    try:
        # Run simulation
        click.echo(f"Running simulation with {iterations} iterations...")
        results = simulate_profile(file, iterations)
        
        # Display summary
        click.echo(click.style(f"✓ Simulation completed for '{results['profile_name']}'", fg='green'))
        
        for archetype_name, attributes in results['archetypes'].items():
            click.echo(f"\nArchetype: {archetype_name}")
            
            for attr_name, stats in attributes.items():
                click.echo(f"  Attribute: {attr_name}")
                
                if 'fixed_value' in stats:
                    # Fixed value, no statistics
                    click.echo(f"    Fixed value: {stats['fixed_value']}")
                    
                elif 'frequencies' in stats:
                    # Categorical data
                    click.echo("    Value frequencies:")
                    for value, freq in stats['frequencies'].items():
                        percentage = freq * 100
                        click.echo(f"      {value}: {percentage:.2f}%")
                        
                else:
                    # Numeric data
                    click.echo(f"    Mean: {stats['mean']:.4f}")
                    click.echo(f"    Median: {stats['median']:.4f}")
                    click.echo(f"    Min: {stats['min']:.4f}")
                    click.echo(f"    Max: {stats['max']:.4f}")
                    click.echo(f"    Std Dev: {stats['std_dev']:.4f}")
        
        # Write to output file if specified
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults written to {output}")
            
        return 0
        
    except Exception as e:
        click.echo(click.style(f"✗ Simulation failed: {str(e)}", fg='red'))
        return 1


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option('--output', '-o', type=click.Path(dir_okay=False, writable=True), 
              help='Output file for exported format')
def export(file, output):
    """
    Export a TanzoLang profile to a concise string format.
    
    Creates a human-readable string representation of the profile.
    """
    try:
        # Generate export format
        export_text = export_profile(file)
        
        # Display or write to file
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(export_text)
            click.echo(f"Profile exported to {output}")
        else:
            click.echo("\n" + export_text)
            
        return 0
        
    except Exception as e:
        click.echo(click.style(f"✗ Export failed: {str(e)}", fg='red'))
        return 1


if __name__ == '__main__':
    cli()
