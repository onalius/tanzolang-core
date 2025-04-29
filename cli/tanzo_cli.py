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

from clients.python.tanzo_schema.validator import validate_profile, check_registry_references
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
    Also validates and reports on modular typology systems if present.
    """
    try:
        profile = validate_profile(file)
        click.echo(click.style(f"✓ Profile '{profile.profile.name}' is valid", fg='green'))
        
        # Display archetypes information
        click.echo(f"  - {len(profile.profile.archetypes)} archetypes")
        
        for idx, archetype in enumerate(profile.profile.archetypes, 1):
            archetype_name = archetype.name or archetype.type.value
            click.echo(f"  - Archetype {idx}: {archetype_name} ({archetype.type.value})")
            click.echo(f"    - {len(archetype.attributes)} attributes")
            
        # Display parent archetypes if present
        if hasattr(profile.profile, 'parent_archetypes') and profile.profile.parent_archetypes:
            click.echo(f"\n  - {len(profile.profile.parent_archetypes)} parent archetypes")
            for idx, parent in enumerate(profile.profile.parent_archetypes, 1):
                click.echo(f"  - Parent {idx}: {parent.name} (influence: {parent.influence})")
                if parent.reference:
                    click.echo(f"    - Reference: {parent.reference}")
        
        # Display typology information if present
        if hasattr(profile.profile, 'typologies') and profile.profile.typologies:
            click.echo("\n  - Typologies:")
            typologies = profile.profile.typologies
            
            # Check for zodiac typology
            if hasattr(typologies, 'zodiac') and typologies.zodiac:
                click.echo(click.style("    - Zodiac", fg='cyan'))
                click.echo(f"      - Sun: {typologies.zodiac.sun}")
                if typologies.zodiac.moon:
                    click.echo(f"      - Moon: {typologies.zodiac.moon}")
                if typologies.zodiac.rising:
                    click.echo(f"      - Rising: {typologies.zodiac.rising}")
                click.echo(f"      - Registry: {typologies.zodiac.reference}")
            
            # Check for kabbalah typology
            if hasattr(typologies, 'kabbalah') and typologies.kabbalah:
                click.echo(click.style("    - Kabbalah", fg='cyan'))
                click.echo(f"      - Primary Sefira: {typologies.kabbalah.primary_sefira}")
                if typologies.kabbalah.secondary_sefira:
                    click.echo(f"      - Secondary Sefira: {typologies.kabbalah.secondary_sefira}")
                click.echo(f"      - Registry: {typologies.kabbalah.reference}")
            
            # Check for purpose quadrant typology
            if hasattr(typologies, 'purpose_quadrant') and typologies.purpose_quadrant:
                click.echo(click.style("    - Purpose Quadrant", fg='cyan'))
                click.echo(f"      - Passion: {typologies.purpose_quadrant.passion}")
                click.echo(f"      - Expertise: {typologies.purpose_quadrant.expertise}")
                click.echo(f"      - Contribution: {typologies.purpose_quadrant.contribution}")
                click.echo(f"      - Sustainability: {typologies.purpose_quadrant.sustainability}")
                if typologies.purpose_quadrant.reference:
                    click.echo(f"      - Registry: {typologies.purpose_quadrant.reference}")
            
            # Check for any other custom typologies
            for name, typology in typologies.__dict__.items():
                if name not in ['zodiac', 'kabbalah', 'purpose_quadrant'] and typology is not None:
                    click.echo(click.style(f"    - Custom Typology: {name}", fg='cyan'))
                    for key, value in typology.__dict__.items():
                        if value is not None:
                            click.echo(f"      - {key}: {value}")
        else:
            click.echo("\n  - No typologies defined (optional)")
            
        click.echo("\n" + click.style("Profile is valid and contains all required elements.", fg='green'))
        if hasattr(profile.profile, 'typologies') and profile.profile.typologies:
            click.echo(click.style("Modular typology system validation complete.", fg='green'))
            registry_warnings = check_registry_references(profile)
            if registry_warnings:
                for warning in registry_warnings:
                    click.echo(click.style(warning, fg='yellow'))
                click.echo(click.style("\nNote: Missing registry references are warnings only. " 
                                     "The profile is still valid, but some typology references could not be located.", fg='yellow'))
        
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
        
        # Display archetypes and attributes
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
        
        # Display typologies if present
        if 'typologies' in results:
            click.echo("\n" + click.style("Typologies:", fg='cyan'))
            
            # Display zodiac typology if present
            if 'zodiac' in results['typologies']:
                zodiac = results['typologies']['zodiac']
                click.echo("  Zodiac:")
                click.echo(f"    Sun: {zodiac['sun']}")
                if zodiac.get('moon'):
                    click.echo(f"    Moon: {zodiac['moon']}")
                if zodiac.get('rising'):
                    click.echo(f"    Rising: {zodiac['rising']}")
            
            # Display kabbalah typology if present
            if 'kabbalah' in results['typologies']:
                kabbalah = results['typologies']['kabbalah']
                click.echo("  Kabbalah:")
                click.echo(f"    Primary Sefira: {kabbalah['primary_sefira']}")
                if kabbalah.get('secondary_sefira'):
                    click.echo(f"    Secondary Sefira: {kabbalah['secondary_sefira']}")
                if kabbalah.get('path'):
                    click.echo(f"    Path: {kabbalah['path']}")
            
            # Display purpose quadrant typology if present
            if 'purpose_quadrant' in results['typologies']:
                purpose = results['typologies']['purpose_quadrant']
                click.echo("  Purpose Quadrant:")
                click.echo(f"    Passion: {purpose['passion']}")
                click.echo(f"    Expertise: {purpose['expertise']}")
                click.echo(f"    Contribution: {purpose['contribution']}")
                click.echo(f"    Sustainability: {purpose['sustainability']}")
            
            # Display any custom typologies
            for name, typology in results['typologies'].items():
                if name not in ['zodiac', 'kabbalah', 'purpose_quadrant']:
                    click.echo(f"  {name.title()}:")
                    for key, value in typology.items():
                        click.echo(f"    {key}: {value}")
        
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
