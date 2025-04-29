"""
Export utilities for TanzoLang profiles
"""

from typing import Dict, Any, Optional, Union, List
from pathlib import Path

from tanzo_schema.models import (
    TanzoProfile,
    Attribute,
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
)
from tanzo_schema.validator import validate_profile


def format_distribution(distribution: Union[NormalDistribution, UniformDistribution, DiscreteDistribution]) -> str:
    """
    Format a probability distribution as a concise string
    
    Args:
        distribution: The distribution to format
        
    Returns:
        str: A formatted string representation
    """
    if isinstance(distribution, NormalDistribution):
        return f"N({distribution.mean:.2f}, {distribution.stdDev:.2f})"
    
    elif isinstance(distribution, UniformDistribution):
        return f"U({distribution.min:.2f}, {distribution.max:.2f})"
    
    elif isinstance(distribution, DiscreteDistribution):
        # Format discrete values and weights
        pairs = []
        for val, weight in zip(distribution.values, distribution.weights):
            # Format the value based on its type
            if isinstance(val, str):
                formatted_val = f'"{val}"'
            elif isinstance(val, bool):
                formatted_val = str(val).lower()
            else:
                formatted_val = str(val)
            
            pairs.append(f"{formatted_val}:{weight:.2f}")
        
        return f"D({', '.join(pairs)})"
    
    else:
        raise ValueError(f"Unknown distribution type: {type(distribution)}")


def format_attribute(attribute: Attribute) -> str:
    """
    Format an attribute as a concise string
    
    Args:
        attribute: The attribute to format
        
    Returns:
        str: A formatted string representation
    """
    value = attribute.value
    
    # Format based on value type
    if isinstance(value, (NormalDistribution, UniformDistribution, DiscreteDistribution)):
        formatted_value = format_distribution(value)
    elif isinstance(value, str):
        formatted_value = f'"{value}"'
    elif isinstance(value, bool):
        formatted_value = str(value).lower()
    else:
        formatted_value = str(value)
    
    # Include unit if available
    if attribute.unit:
        return f"{attribute.name}={formatted_value} {attribute.unit}"
    else:
        return f"{attribute.name}={formatted_value}"


def export_profile(profile_path: Union[str, Path]) -> str:
    """
    Export a TanzoLang profile as a concise string representation
    
    Args:
        profile_path: Path to the profile file
        
    Returns:
        str: A formatted string representation of the profile
    """
    # Validate the profile first
    profile = validate_profile(profile_path)
    
    # Format the profile
    lines = [f"TanzoProfile: {profile.profile.name} (v{profile.version})"]
    
    # Format each archetype
    for archetype in profile.profile.archetypes:
        archetype_name = archetype.name or archetype.type.value
        archetype_line = f"  {archetype.type.value.upper()}:{archetype_name}"
        lines.append(archetype_line)
        
        # Format attributes for this archetype
        for attribute in archetype.attributes:
            attribute_line = f"    {format_attribute(attribute)}"
            lines.append(attribute_line)
    
    return "\n".join(lines)
