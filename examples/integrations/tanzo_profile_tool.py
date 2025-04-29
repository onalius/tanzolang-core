#!/usr/bin/env python
"""
TanzoLang Profile Tool

A simple command-line tool that loads a TanzoLang profile and provides various
exports and simulations.

Usage:
    python tanzo_profile_tool.py export <profile_path> [--format=<format>]
    python tanzo_profile_tool.py emojitype <profile_path>
    python tanzo_profile_tool.py simulate <profile_path> [--iterations=<n>]
    python tanzo_profile_tool.py prompt <profile_path> [--template=<template>]

Options:
    -h --help               Show this help message
    --format=<format>       Export format: json, yaml, shorthand [default: shorthand]
    --iterations=<n>        Number of simulation iterations [default: 10]
    --template=<template>   Prompt template to use [default: langchain]
"""

import json
import os
import random
import sys
from pathlib import Path

import yaml
from docopt import docopt


def load_profile(profile_path):
    """
    Load a TanzoLang profile from a YAML or JSON file.
    
    Args:
        profile_path: Path to the profile file
        
    Returns:
        The loaded profile as a dictionary
    """
    path = Path(profile_path)
    if not path.exists():
        print(f"Error: Profile file {profile_path} not found")
        sys.exit(1)
        
    try:
        with open(path, 'r') as f:
            if path.suffix.lower() in ('.yaml', '.yml'):
                return yaml.safe_load(f)
            elif path.suffix.lower() == '.json':
                return json.load(f)
            else:
                print(f"Error: Unsupported file format: {path.suffix}")
                sys.exit(1)
    except Exception as e:
        print(f"Error loading profile: {e}")
        sys.exit(1)


def export_profile(profile, format='shorthand'):
    """
    Export a TanzoLang profile in the specified format.
    
    Args:
        profile: The profile to export
        format: The export format (json, yaml, shorthand)
        
    Returns:
        The exported profile as a string
    """
    if format == 'json':
        return json.dumps(profile, indent=2)
    elif format == 'yaml':
        return yaml.dump(profile, sort_keys=False)
    elif format == 'shorthand':
        return generate_shorthand(profile)
    else:
        print(f"Error: Unsupported export format: {format}")
        sys.exit(1)


def generate_shorthand(profile):
    """
    Generate a shorthand string representation of a TanzoLang profile.
    
    Args:
        profile: The profile to convert
        
    Returns:
        A concise string representation
    """
    result = []
    
    # Get the profile section
    prof = profile.get('profile', {})
    name = prof.get('name', 'Unnamed Profile')
    result.append(f"Profile: {name}")
    
    # Add archetypes
    archetypes = prof.get('archetypes', [])
    if archetypes:
        result.append("\nArchetypes:")
        for arch in archetypes:
            arch_type = arch.get('type', 'unknown')
            arch_name = arch.get('name', 'Unnamed')
            result.append(f"- {arch_name} ({arch_type})")
            
            # Add key attributes
            attributes = arch.get('attributes', [])
            for attr in attributes:
                attr_name = attr.get('name', 'unnamed')
                attr_value = attr.get('value', '')
                
                # Handle different value types
                if isinstance(attr_value, dict):
                    if 'distribution' in attr_value:
                        dist_type = attr_value.get('distribution')
                        if dist_type == 'normal':
                            mean = attr_value.get('mean', 0)
                            std = attr_value.get('stdDev', 0)
                            attr_str = f"{mean}±{std}"
                        elif dist_type == 'uniform':
                            min_val = attr_value.get('min', 0)
                            max_val = attr_value.get('max', 0)
                            attr_str = f"{min_val}..{max_val}"
                        elif dist_type == 'discrete':
                            values = attr_value.get('values', [])
                            weights = attr_value.get('weights', [])
                            attr_str = f"{'/'.join(str(v) for v in values)}"
                        else:
                            attr_str = str(attr_value)
                    else:
                        attr_str = str(attr_value)
                else:
                    attr_str = str(attr_value)
                    
                result.append(f"  • {attr_name}: {attr_str}")
    
    # Add symbolic fields if present
    for field in ['lineage', 'ikigai', 'scars', 'symbolism']:
        if field in prof:
            result.append(f"\n{field.capitalize()}:")
            if isinstance(prof[field], list):
                for item in prof[field]:
                    if isinstance(item, dict) and 'name' in item:
                        result.append(f"- {item['name']}")
            elif isinstance(prof[field], dict):
                for key, value in prof[field].items():
                    if isinstance(value, dict) or isinstance(value, list):
                        result.append(f"- {key}: <complex>")
                    else:
                        result.append(f"- {key}: {value}")
    
    return '\n'.join(result)


def generate_emojitype(profile):
    """
    Generate an emoji representation of a TanzoLang profile.
    
    Args:
        profile: The profile to convert
        
    Returns:
        A string of emojis representing the profile's key aspects
    """
    emojis = []
    prof = profile.get('profile', {})
    
    # Map archetype types to emojis
    type_emoji = {
        'digital': '💻',
        'physical': '💪',
        'hybrid': '🧬',
        'social': '👥',
        'emotional': '❤️',
        'cognitive': '🧠'
    }
    
    # Map common attributes to emojis
    attr_emoji = {
        'wisdom': '🦉',
        'strength': '🏋️',
        'creativity': '🎨',
        'intelligence': '🧠',
        'charisma': '✨',
        'empathy': '🤗',
        'courage': '🦁',
        'agility': '🏃',
        'curiosity': '🔍',
        'patience': '⏳',
        'loyalty': '🐕',
        'leadership': '👑',
        'analysis': '📊',
        'passion': '🔥',
        'precision': '🎯',
        'speed': '⚡',
        'intuition': '🔮',
        'spirituality': '🕉️'
    }
    
    # Add profile type emoji
    archetypes = prof.get('archetypes', [])
    for arch in archetypes:
        arch_type = arch.get('type', 'unknown')
        if arch_type in type_emoji:
            emojis.append(type_emoji[arch_type])
    
    # Add attribute emojis
    seen_attrs = set()
    for arch in archetypes:
        attributes = arch.get('attributes', [])
        for attr in attributes:
            attr_name = attr.get('name', '').lower()
            if attr_name in attr_emoji and attr_name not in seen_attrs:
                emojis.append(attr_emoji[attr_name])
                seen_attrs.add(attr_name)
    
    # Add symbolism emojis if available
    symbolism = prof.get('symbolism', {})
    symbolism_map = {
        'primary_element': {
            'fire': '🔥',
            'water': '💧',
            'earth': '🌎',
            'air': '💨',
            'metal': '⚙️',
            'wood': '🌳'
        },
        'animal': {
            'owl': '🦉',
            'wolf': '🐺',
            'lion': '🦁',
            'eagle': '🦅',
            'snake': '🐍',
            'dolphin': '🐬',
            'fox': '🦊',
            'butterfly': '🦋'
        },
        'season': {
            'spring': '🌱',
            'summer': '☀️',
            'autumn': '🍂',
            'winter': '❄️'
        }
    }
    
    for sym_key, sym_map in symbolism_map.items():
        if sym_key in symbolism:
            sym_value = symbolism.get(sym_key)
            if sym_value in sym_map:
                emojis.append(sym_map[sym_value])
    
    # Ensure we have at least 3 emojis
    while len(emojis) < 3:
        emojis.append(random.choice(['🌟', '✨', '💫', '⭐']))
    
    # Limit to a maximum of 7 emojis
    return ' '.join(emojis[:7])


def simulate_profile(profile, iterations=10):
    """
    Run a simple Monte-Carlo simulation on a TanzoLang profile.
    
    Args:
        profile: The profile to simulate
        iterations: Number of simulation iterations
        
    Returns:
        A dictionary with simulation results
    """
    results = {
        'iterations': iterations,
        'attributes': {}
    }
    
    prof = profile.get('profile', {})
    archetypes = prof.get('archetypes', [])
    
    # Collect all attributes with distributions
    for arch in archetypes:
        attributes = arch.get('attributes', [])
        for attr in attributes:
            attr_name = attr.get('name')
            attr_value = attr.get('value')
            
            if isinstance(attr_value, dict) and 'distribution' in attr_value:
                results['attributes'][attr_name] = {
                    'samples': [],
                    'description': attr.get('description', ''),
                    'unit': attr.get('unit', '')
                }
                
                # Generate samples based on distribution type
                dist_type = attr_value.get('distribution')
                if dist_type == 'normal':
                    mean = attr_value.get('mean', 0)
                    std = attr_value.get('stdDev', 0)
                    for _ in range(iterations):
                        sample = random.normalvariate(mean, std)
                        results['attributes'][attr_name]['samples'].append(sample)
                        
                elif dist_type == 'uniform':
                    min_val = attr_value.get('min', 0)
                    max_val = attr_value.get('max', 0)
                    for _ in range(iterations):
                        sample = random.uniform(min_val, max_val)
                        results['attributes'][attr_name]['samples'].append(sample)
                        
                elif dist_type == 'discrete':
                    values = attr_value.get('values', [])
                    weights = attr_value.get('weights', [1] * len(values))
                    for _ in range(iterations):
                        sample = random.choices(values, weights=weights, k=1)[0]
                        results['attributes'][attr_name]['samples'].append(sample)
    
    # Calculate statistics for each attribute
    for attr_name, attr_data in results['attributes'].items():
        samples = attr_data['samples']
        if all(isinstance(s, (int, float)) for s in samples):
            attr_data['mean'] = sum(samples) / len(samples)
            attr_data['min'] = min(samples)
            attr_data['max'] = max(samples)
            sorted_samples = sorted(samples)
            attr_data['median'] = sorted_samples[len(sorted_samples) // 2]
    
    return results


def format_simulation_results(results):
    """
    Format simulation results as a human-readable string.
    
    Args:
        results: Simulation results dictionary
        
    Returns:
        A formatted string with simulation statistics
    """
    lines = [f"Simulation Results ({results['iterations']} iterations)\n"]
    
    for attr_name, attr_data in results['attributes'].items():
        lines.append(f"Attribute: {attr_name}")
        if 'description' in attr_data and attr_data['description']:
            lines.append(f"Description: {attr_data['description']}")
            
        if 'mean' in attr_data:
            lines.append(f"  Mean: {attr_data['mean']:.2f}")
            lines.append(f"  Min: {attr_data['min']:.2f}")
            lines.append(f"  Max: {attr_data['max']:.2f}")
            lines.append(f"  Median: {attr_data['median']:.2f}")
        else:
            # Handle non-numeric samples (like discrete string values)
            samples = attr_data['samples']
            value_counts = {}
            for s in samples:
                value_counts[s] = value_counts.get(s, 0) + 1
                
            lines.append("  Value distribution:")
            for value, count in value_counts.items():
                percentage = (count / len(samples)) * 100
                lines.append(f"    {value}: {percentage:.1f}%")
                
        lines.append("")
    
    return '\n'.join(lines)


def generate_langchain_prompt(profile):
    """
    Generate a LangChain-compatible prompt from a TanzoLang profile.
    
    Args:
        profile: The profile to convert
        
    Returns:
        A string with a LangChain prompt template
    """
    prof = profile.get('profile', {})
    name = prof.get('name', 'AI Assistant')
    description = prof.get('description', 'An AI assistant')
    
    # Gather archetype information
    archetype_strings = []
    for arch in prof.get('archetypes', []):
        arch_type = arch.get('type', 'unknown')
        arch_name = arch.get('name', 'Unnamed')
        arch_desc = arch.get('description', '')
        archetype_strings.append(f"- {arch_name} ({arch_type}): {arch_desc}")
    
    # Gather attribute information
    attribute_strings = []
    for arch in prof.get('archetypes', []):
        for attr in arch.get('attributes', []):
            attr_name = attr.get('name', 'unnamed')
            attr_desc = attr.get('description', '')
            attribute_strings.append(f"- {attr_name}: {attr_desc}")
    
    # Gather symbolic elements
    symbol_strings = []
    for field in ['lineage', 'ikigai', 'memory', 'scars', 'symbolism']:
        if field in prof:
            if isinstance(prof[field], list):
                for item in prof[field]:
                    if isinstance(item, dict) and 'name' in item and 'description' in item:
                        symbol_strings.append(f"- {item['name']}: {item['description']}")
            elif isinstance(prof[field], dict):
                # For simplicity, we'll just include the main top-level items
                for key, value in prof[field].items():
                    if isinstance(value, str):
                        symbol_strings.append(f"- {key}: {value}")
    
    # Build the prompt template
    template = [
        """I want you to act as {name}, {description}.

Your personality is based on the following archetypes:
{archetypes}

Your key attributes and traits are:
{attributes}

{symbols}

Respond to the following as {name}: {input}"""     
    ]
    
    # Build example mappings
    mappings = {
        'name': name,
        'description': description,
        'archetypes': '\n'.join(archetype_strings),
        'attributes': '\n'.join(attribute_strings),
        'symbols': '\n'.join(['Your symbolic elements include:'] + symbol_strings) if symbol_strings else '',
        'input': '{input}'
    }
    
    # Return the template and mappings
    return {
        'template': template[0],
        'mappings': mappings,
        'example': template[0].format(**{k: v for k, v in mappings.items() if k != 'input'}, input="Tell me about yourself.")
    }


def main():
    args = docopt(__doc__)
    profile_path = args['<profile_path>']
    profile = load_profile(profile_path)
    
    if args['export']:
        format = args['--format']
        result = export_profile(profile, format)
        print(result)
        
    elif args['emojitype']:
        result = generate_emojitype(profile)
        print(result)
        
    elif args['simulate']:
        iterations = int(args['--iterations'])
        results = simulate_profile(profile, iterations)
        formatted_results = format_simulation_results(results)
        print(formatted_results)
        
    elif args['prompt']:
        template = args['--template']
        if template == 'langchain':
            result = generate_langchain_prompt(profile)
            print("# LangChain Prompt Template\n")
            print("## Template")
            print("```")
            print(result['template'])
            print("```\n")
            print("## Example Output\n")
            print("```")
            print(result['example'])
            print("```")
        else:
            print(f"Error: Unsupported template type: {template}")
            sys.exit(1)


if __name__ == '__main__':
    main()
