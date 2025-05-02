"""
Export functions for Tanzo profiles
"""

import json
from typing import Any, Dict, Optional, Union

import yaml

from clients.python.tanzo_schema.models import TanzoProfile


def export_profile(profile: TanzoProfile, format: str = "shorthand") -> str:
    """
    Export a Tanzo profile to a specific format
    
    Args:
        profile: The profile to export
        format: The format to export to. One of:
                - "shorthand" (default): A compact string representation
                - "json": JSON format
                - "yaml": YAML format
                
    Returns:
        str: The exported profile in the specified format
        
    Raises:
        ValueError: If an unknown format is requested
    """
    if format == "shorthand":
        return _export_shorthand(profile)
    elif format == "json":
        return profile.model_dump_json(indent=2)
    elif format == "yaml":
        # Convert to dict using JSON to ensure enum values are strings
        profile_dict = json.loads(profile.model_dump_json())
        return yaml.dump(profile_dict, sort_keys=False)
    else:
        raise ValueError(f"Unknown export format: {format}")


def _export_shorthand(profile: TanzoProfile) -> str:
    """
    Export a Tanzo profile to a shorthand string representation
    
    Args:
        profile: The profile to export
        
    Returns:
        str: The shorthand string representation
    """
    # Basic profile info
    result = f"{profile.profile.name}@{profile.profile.version}"
    
    # Archetype
    result += f" [{profile.archetype.type.value}"
    
    # Core attributes (take first letter of each)
    core_attr = "".join(attr[0].upper() for attr in profile.archetype.attributes.core)
    result += f":{core_attr}"
    
    # Elements (if present)
    if profile.archetype.affinity and profile.archetype.affinity.elements:
        elements = "".join(element[0].upper() for element in profile.archetype.affinity.elements)
        result += f"|{elements}"
    
    result += "]"
    
    # State
    baseline = profile.properties.state.baseline
    result += f" E{baseline.energy:.0f}/R{baseline.resilience:.0f}/A{baseline.adaptability:.0f}"
    
    # Top capability
    if profile.properties.capabilities:
        # Find capability with highest power
        top_capability = max(profile.properties.capabilities, key=lambda c: c.power)
        result += f" «{top_capability.name}:{top_capability.power:.1f}»"
    
    return result
