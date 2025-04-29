#!/usr/bin/env python3
"""
Tanzo CLI - Command-line interface for working with TanzoLang files.

This CLI provides utilities for validating, simulating, and exporting Tanzo profiles.
"""

import json
import os
import random
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
import yaml

# Add parent directory to path to import tanzo_schema
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from clients.python.tanzo_schema import (
        SchemaValidationError,
        TanzoProfile,
        validate_profile,
    )
except ImportError:
    click.echo("Error: Could not import tanzo_schema package. Please ensure it's installed.")
    sys.exit(1)


def load_profile(profile_path: str) -> TanzoProfile:
    """
    Load and validate a profile from the specified path.
    
    Args:
        profile_path: Path to the profile file
        
    Returns:
        TanzoProfile: Validated profile
        
    Raises:
        click.ClickException: If validation fails
    """
    try:
        return validate_profile(profile_path)
    except SchemaValidationError as e:
        error_msg = f"Validation failed: {e.message}"
        if e.details:
            error_msg += "\nDetails:"
            for detail in e.details:
                error_msg += f"\n  - {detail['path']}: {detail['message']}"
        raise click.ClickException(error_msg)
    except FileNotFoundError:
        raise click.ClickException(f"File not found: {profile_path}")
    except Exception as e:
        raise click.ClickException(f"Error processing profile: {str(e)}")


def run_simulation(
    profile: TanzoProfile, iterations: int, environment: Optional[str] = None
) -> Dict:
    """
    Run a Monte Carlo simulation on the profile.
    
    Args:
        profile: The validated profile to simulate
        iterations: Number of simulation iterations
        environment: Optional specific environment to simulate
        
    Returns:
        Dict: Simulation results
    """
    results = {
        "traits": {},
        "skills": {},
        "environments": {},
    }
    
    # Setup random seed if provided in simulation parameters
    if profile.simulation_parameters and profile.simulation_parameters.seed is not None:
        random.seed(profile.simulation_parameters.seed)
    
    # Extract variation factor
    variation_factor = (
        profile.simulation_parameters.variation_factor
        if profile.simulation_parameters and profile.simulation_parameters.variation_factor is not None
        else 0.2
    )
    
    # Get simulation environments
    environments = []
    if environment:
        environments = [environment]
    elif profile.simulation_parameters and profile.simulation_parameters.environments:
        environments = profile.simulation_parameters.environments
    else:
        environments = ["default"]
    
    # Store all simulation runs for statistical analysis
    trait_values = {trait: [] for trait in profile.archetype.core_traits}
    skill_values = {skill.name: [] for skill in profile.archetype.skills}
    env_scores = {env: [] for env in environments}
    
    # Run simulations
    for _ in range(iterations):
        # Simulate traits
        trait_results = {}
        for trait_name, trait in profile.archetype.core_traits.items():
            base = trait.base
            range_min, range_max = (None, None)
            
            if trait.range:
                range_min, range_max = trait.range
            else:
                # Default range if not specified
                range_min = max(0, base - base * variation_factor)
                range_max = min(10, base + base * variation_factor)
            
            # Select distribution method
            if trait.distribution == "normal":
                # Normal distribution centered at base with stddev proportional to range
                std_dev = (range_max - range_min) / 4  # 95% within range
                value = random.gauss(base, std_dev)
                # Clamp to valid range
                value = max(range_min, min(range_max, value))
            elif trait.distribution == "uniform":
                # Uniform distribution within range
                value = random.uniform(range_min, range_max)
            elif trait.distribution == "exponential":
                # Exponential distribution anchored at range_min
                scale = (range_max - range_min) / 3  # Most values within range
                value = range_min + random.expovariate(1 / scale)
                # Clamp to valid range
                value = min(range_max, value)
            else:
                # Default to triangular distribution
                value = random.triangular(range_min, range_max, base)
            
            trait_results[trait_name] = value
            trait_values[trait_name].append(value)
        
        # Simulate skills
        skill_results = {}
        for skill in profile.archetype.skills:
            base = skill.proficiency.base
            range_min, range_max = (None, None)
            
            if skill.proficiency.range:
                range_min, range_max = skill.proficiency.range
            else:
                # Default range if not specified
                range_min = max(0, base - base * variation_factor)
                range_max = min(10, base + base * variation_factor)
            
            # Select distribution method similar to traits
            if skill.proficiency.distribution == "normal":
                std_dev = (range_max - range_min) / 4
                value = random.gauss(base, std_dev)
                value = max(range_min, min(range_max, value))
            elif skill.proficiency.distribution == "uniform":
                value = random.uniform(range_min, range_max)
            elif skill.proficiency.distribution == "exponential":
                scale = (range_max - range_min) / 3
                value = range_min + random.expovariate(1 / scale)
                value = min(range_max, value)
            else:
                value = random.triangular(range_min, range_max, base)
            
            skill_results[skill.name] = value
            skill_values[skill.name].append(value)
        
        # Simulate performance in each environment
        for env in environments:
            # Simple model: weighted average of relevant traits and skills
            # In a real implementation, this would be more sophisticated
            # and environment-specific
            env_score = 0
            weights = 0
            
            # Add trait contributions (simplified)
            for trait_name, value in trait_results.items():
                weight = 1.0  # Equal weights for simplicity
                env_score += value * weight
                weights += weight
            
            # Add skill contributions (simplified)
            for skill_name, value in skill_results.items():
                weight = 1.5  # Skills weighted more than traits
                env_score += value * weight
                weights += weight
            
            # Normalize score
            if weights > 0:
                env_score /= weights
            
            # Add random variation based on environment
            env_variation = variation_factor * 2  # More variation in environments
            env_score *= random.uniform(1 - env_variation, 1 + env_variation)
            
            # Clamp to valid range
            env_score = max(0, min(10, env_score))
            env_scores[env].append(env_score)
    
    # Calculate statistics
    for trait_name, values in trait_values.items():
        results["traits"][trait_name] = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stddev": statistics.stdev(values) if len(values) > 1 else 0,
        }
    
    for skill_name, values in skill_values.items():
        results["skills"][skill_name] = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stddev": statistics.stdev(values) if len(values) > 1 else 0,
        }
    
    for env, values in env_scores.items():
        results["environments"][env] = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stddev": statistics.stdev(values) if len(values) > 1 else 0,
        }
    
    return results


def generate_shorthand(profile: TanzoProfile) -> str:
    """
    Generate a shorthand string representation of the profile.
    
    Args:
        profile: The validated profile
        
    Returns:
        str: Shorthand representation
    """
    # Format: Name[T:intel/creat/social S:skill1/skill2]
    archetype = profile.archetype
    
    # Get core traits
    core_traits = []
    for trait_name in ["intelligence", "creativity", "sociability"]:
        if trait_name in archetype.core_traits:
            trait = archetype.core_traits[trait_name]
            core_traits.append(f"{trait_name[:5]}:{trait.base:.1f}")
    
    traits_str = "/".join(core_traits)
    
    # Get top skills (up to 3)
    skills = sorted(
        archetype.skills,
        key=lambda s: s.proficiency.base,
        reverse=True
    )[:3]
    skills_str = "/".join([f"{s.name}:{s.proficiency.base:.1f}" for s in skills])
    
    # Generate shorthand
    result = f"{archetype.name}[T:{traits_str} S:{skills_str}]"
    
    # Add profile type indicator
    type_indicators = {
        "full": "F",
        "archetype_only": "A",
        "simulation": "S"
    }
    result = f"{type_indicators.get(profile.profile_type.value, '?')}:{result}"
    
    return result


@click.group()
@click.version_option("0.1.0")
def cli():
    """
    Tanzo CLI - Tools for working with TanzoLang files.
    
    This CLI provides utilities for validating, simulating, and exporting Tanzo profiles.
    """
    pass


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def validate(file):
    """
    Validate a Tanzo profile file against the schema.
    
    FILE: Path to the Tanzo profile YAML or JSON file.
    """
    try:
        profile = load_profile(file)
        click.echo(click.style("Validation successful! ✓", fg="green"))
        click.echo(f"Profile type: {profile.profile_type.value}")
        click.echo(f"Archetype: {profile.archetype.name}")
    except click.ClickException as e:
        click.echo(click.style(str(e), fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--iterations", "-n", type=int, default=100,
    help="Number of simulation iterations (default: 100)"
)
@click.option(
    "--environment", "-e", type=str,
    help="Specific environment to simulate"
)
@click.option(
    "--output", "-o", type=click.Path(),
    help="Save results to file (JSON format)"
)
def simulate(file, iterations, environment, output):
    """
    Run a Monte Carlo simulation on a Tanzo profile.
    
    FILE: Path to the Tanzo profile YAML or JSON file.
    """
    try:
        profile = load_profile(file)
        
        click.echo(f"Running simulation with {iterations} iterations...")
        results = run_simulation(profile, iterations, environment)
        
        # Print summary to console
        click.echo("\nSimulation Results:")
        click.echo("===================")
        
        click.echo("\nCore Traits:")
        for trait, stats in results["traits"].items():
            click.echo(f"  {trait}:")
            click.echo(f"    Mean: {stats['mean']:.2f}")
            click.echo(f"    Range: {stats['min']:.2f} - {stats['max']:.2f}")
            click.echo(f"    StdDev: {stats['stddev']:.2f}")
        
        click.echo("\nSkills:")
        for skill, stats in results["skills"].items():
            click.echo(f"  {skill}:")
            click.echo(f"    Mean: {stats['mean']:.2f}")
            click.echo(f"    Range: {stats['min']:.2f} - {stats['max']:.2f}")
            click.echo(f"    StdDev: {stats['stddev']:.2f}")
        
        click.echo("\nEnvironments:")
        for env, stats in results["environments"].items():
            click.echo(f"  {env}:")
            click.echo(f"    Mean: {stats['mean']:.2f}")
            click.echo(f"    Range: {stats['min']:.2f} - {stats['max']:.2f}")
            click.echo(f"    StdDev: {stats['stddev']:.2f}")
        
        # Save to file if output specified
        if output:
            with open(output, "w") as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to {output}")
        
    except click.ClickException as e:
        click.echo(click.style(str(e), fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("file", type=click.Path(exists=True))
def export(file):
    """
    Export a Tanzo profile as a shorthand string.
    
    FILE: Path to the Tanzo profile YAML or JSON file.
    """
    try:
        profile = load_profile(file)
        shorthand = generate_shorthand(profile)
        click.echo(shorthand)
    except click.ClickException as e:
        click.echo(click.style(str(e), fg="red"))
        sys.exit(1)


if __name__ == "__main__":
    cli()
