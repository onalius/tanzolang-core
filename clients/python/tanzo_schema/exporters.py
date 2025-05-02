"""
Export utilities for TanzoLang profiles.
"""

from typing import Optional, Dict, Any, List, Union
import json
import yaml
from pathlib import Path

from clients.python.tanzo_schema.models import TanzoProfile, Archetype


def export_profile_shorthand(profile: TanzoProfile) -> str:
    """
    Export a profile as a shorthand string representation.
    
    Args:
        profile (TanzoProfile): The profile to export
        
    Returns:
        str: A shorthand string representation of the profile
    """
    p = profile.profile
    archetype = p.archetype
    
    # Start with name and primary archetype
    shorthand = f"{p.name} [{archetype.primary.value}"
    
    # Add secondary archetype if present
    if archetype.secondary:
        shorthand += f"/{archetype.secondary.value}"
    
    shorthand += "]"
    
    # Add personality traits if present
    if p.personality and p.personality.traits:
        traits = p.personality.traits
        shorthand += f" | O:{traits.openness:.1f} C:{traits.conscientiousness:.1f} "
        shorthand += f"E:{traits.extraversion:.1f} A:{traits.agreeableness:.1f} N:{traits.neuroticism:.1f}"
    
    # Add communication style if present
    if p.communication and p.communication.style:
        shorthand += f" | {p.communication.style.value}"
        
        if p.communication.tone:
            shorthand += f", {p.communication.tone.value}"
    
    return shorthand


def export_profile_json(profile: TanzoProfile, path: Optional[Union[str, Path]] = None) -> str:
    """
    Export a profile as a JSON string or to a JSON file.
    
    Args:
        profile (TanzoProfile): The profile to export
        path (Optional[Union[str, Path]]): If provided, write the JSON to this file path
        
    Returns:
        str: The JSON string representation of the profile
    """
    json_str = profile.model_dump_json(indent=2)
    
    if path:
        with open(path, "w") as f:
            f.write(json_str)
    
    return json_str


def export_profile_yaml(profile: TanzoProfile, path: Optional[Union[str, Path]] = None) -> str:
    """
    Export a profile as a YAML string or to a YAML file.
    
    Args:
        profile (TanzoProfile): The profile to export
        path (Optional[Union[str, Path]]): If provided, write the YAML to this file path
        
    Returns:
        str: The YAML string representation of the profile
    """
    # Convert to dict first and ensure enum values are converted to strings
    profile_dict = json.loads(profile.model_dump_json())
    
    # Convert to YAML
    yaml_str = yaml.dump(profile_dict, sort_keys=False, default_flow_style=False)
    
    if path:
        with open(path, "w") as f:
            f.write(yaml_str)
    
    return yaml_str
