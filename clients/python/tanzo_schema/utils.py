"""
Utility functions for working with TanzoLang profiles.

This module provides helper functions for common tasks such as
exporting profiles to different formats.
"""

import json
from typing import Dict, Any, Union

import yaml
from pydantic import BaseModel

from clients.python.tanzo_schema.models import TanzoProfile


def to_dict(obj: Union[BaseModel, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert a Pydantic model or dictionary to a plain dictionary.
    
    Args:
        obj: The object to convert
        
    Returns:
        Dict[str, Any]: A plain dictionary representation
    """
    if isinstance(obj, BaseModel):
        return obj.model_dump(exclude_none=True)
    return obj


def to_json(obj: Union[BaseModel, Dict[str, Any]], indent: int = 2) -> str:
    """
    Convert a Pydantic model or dictionary to a JSON string.
    
    Args:
        obj: The object to convert
        indent: Number of spaces for indentation
        
    Returns:
        str: A JSON string representation
    """
    return json.dumps(to_dict(obj), indent=indent)


def to_yaml(obj: Union[BaseModel, Dict[str, Any]]) -> str:
    """
    Convert a Pydantic model or dictionary to a YAML string.
    
    Args:
        obj: The object to convert
        
    Returns:
        str: A YAML string representation
    """
    return yaml.dump(to_dict(obj), sort_keys=False)


def save_to_json(obj: Union[BaseModel, Dict[str, Any]], file_path: str, indent: int = 2) -> None:
    """
    Save a Pydantic model or dictionary to a JSON file.
    
    Args:
        obj: The object to save
        file_path: Path to the output file
        indent: Number of spaces for indentation
    """
    with open(file_path, "w") as f:
        json.dump(to_dict(obj), f, indent=indent)


def save_to_yaml(obj: Union[BaseModel, Dict[str, Any]], file_path: str) -> None:
    """
    Save a Pydantic model or dictionary to a YAML file.
    
    Args:
        obj: The object to save
        file_path: Path to the output file
    """
    with open(file_path, "w") as f:
        yaml.dump(to_dict(obj), f, sort_keys=False)


def export_shorthand(profile: TanzoProfile) -> str:
    """
    Export a TanzoLang profile to a concise string representation.
    
    This creates a short summary string that captures the key aspects of the profile.
    
    Args:
        profile: The TanzoProfile to export
        
    Returns:
        str: A shorthand string representation
    """
    archetype = profile.digital_archetype
    identity = archetype.identity
    
    # Start with basic information
    parts = [f"{identity.name}"]
    
    # Add identity information if available
    if identity.age is not None:
        parts.append(f"age:{identity.age}")
    if identity.occupation is not None:
        parts.append(f"job:{identity.occupation}")
    
    # Add top traits (up to 3)
    top_traits = sorted(
        [(name, trait.value) for name, trait in archetype.traits.items()],
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    traits_str = ",".join([f"{name}:{value:.1f}" for name, value in top_traits])
    parts.append(f"traits:[{traits_str}]")
    
    # Add behavioral rules if available (up to 2)
    if profile.behavioral_rules:
        top_rules = sorted(
            [(rule.rule, rule.priority) for rule in profile.behavioral_rules],
            key=lambda x: x[1],
            reverse=True
        )[:2]
        
        rules_str = ";".join([rule for rule, _ in top_rules])
        parts.append(f"rules:[{rules_str}]")
    
    return " | ".join(parts)
