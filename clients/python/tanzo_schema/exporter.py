"""
Exporter module for TanzoLang profiles.

This module provides functions to export TanzoLang profiles in various formats,
including a shorthand string representation.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from tanzo_schema.validator import load_profile


def _get_trait_shorthand(trait_data: Dict[str, Any]) -> str:
    """
    Convert a trait to shorthand notation.
    
    Args:
        trait_data (Dict[str, Any]): The trait data.
        
    Returns:
        str: Shorthand notation for the trait.
    """
    value = trait_data.get("value", 50)
    variance = trait_data.get("variance")
    
    if variance is not None:
        return f"{value}±{variance}"
    else:
        return str(value)


def _get_trait_summary(
    traits: Dict[str, Dict[str, Any]]
) -> str:
    """
    Generate a trait summary string.
    
    Args:
        traits (Dict[str, Dict[str, Any]]): Dictionary of traits.
        
    Returns:
        str: Trait summary string.
    """
    trait_codes = {
        "openness": "O",
        "conscientiousness": "C",
        "extraversion": "E",
        "agreeableness": "A",
        "neuroticism": "N"
    }
    
    parts = []
    for trait_name, trait_code in trait_codes.items():
        if trait_name in traits:
            trait_data = traits[trait_name]
            shorthand = _get_trait_shorthand(trait_data)
            parts.append(f"{trait_code}:{shorthand}")
    
    return " ".join(parts)


def generate_shorthand(profile_data: Dict[str, Any]) -> str:
    """
    Generate a shorthand string representation of a profile.
    
    Args:
        profile_data (Dict[str, Any]): The profile data.
        
    Returns:
        str: Shorthand representation.
    """
    # Extract profile name
    name = profile_data.get("metadata", {}).get("name", "Unnamed")
    
    # Extract traits
    traits = profile_data.get("digital_archetype", {}).get("traits", {})
    trait_summary = _get_trait_summary(traits)
    
    # Combine into shorthand
    return f"{name} [{trait_summary}]"


def export_profile(
    profile_path: Union[str, Path], 
    output_format: str = "shorthand"
) -> Union[str, Dict[str, Any]]:
    """
    Export a profile in the specified format.
    
    Args:
        profile_path (Union[str, Path]): Path to the profile file.
        output_format (str, optional): Output format - "shorthand", "json", or "dict". Defaults to "shorthand".
        
    Returns:
        Union[str, Dict[str, Any]]: Exported profile in requested format.
        
    Raises:
        ValueError: If the file format is not supported or output_format is invalid.
    """
    profile_data = load_profile(profile_path)
    
    if output_format == "shorthand":
        return generate_shorthand(profile_data)
    elif output_format == "json":
        return json.dumps(profile_data, indent=2)
    elif output_format == "dict":
        return profile_data
    else:
        raise ValueError(f"Unsupported output format: {output_format}")
