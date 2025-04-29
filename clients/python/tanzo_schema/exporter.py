"""
Exporter module for TanzoLang documents.

This module provides functions to export TanzoLang documents to various formats,
including a shorthand string representation.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from tanzo_schema.models import TanzoDocument
from tanzo_schema.validator import validate_and_parse


def export_to_json(
    document: Union[str, Path, Dict[str, Any], TanzoDocument],
    pretty: bool = True
) -> str:
    """
    Export a TanzoLang document to JSON.
    
    Args:
        document: The document to export. Can be a file path, a dictionary,
                 or a TanzoDocument instance.
        pretty: Whether to pretty-print the JSON.
    
    Returns:
        A JSON string representation of the document.
    """
    # Parse the document if needed
    if not isinstance(document, TanzoDocument):
        document = validate_and_parse(document)
    
    # Convert to dictionary
    doc_dict = document.model_dump(exclude_none=True)
    
    # Convert to JSON
    indent = 2 if pretty else None
    return json.dumps(doc_dict, indent=indent)


def export_to_yaml(
    document: Union[str, Path, Dict[str, Any], TanzoDocument]
) -> str:
    """
    Export a TanzoLang document to YAML.
    
    Args:
        document: The document to export. Can be a file path, a dictionary,
                 or a TanzoDocument instance.
    
    Returns:
        A YAML string representation of the document.
    """
    # Parse the document if needed
    if not isinstance(document, TanzoDocument):
        document = validate_and_parse(document)
    
    # Convert to dictionary
    doc_dict = document.model_dump(exclude_none=True)
    
    # Convert to YAML
    return yaml.dump(doc_dict, sort_keys=False)


def export_shorthand(
    document: Union[str, Path, Dict[str, Any], TanzoDocument]
) -> str:
    """
    Export a TanzoLang document to a shorthand string representation.
    
    The shorthand format is a concise representation of the profile, including
    the profile name and key archetype and trait information.
    
    Args:
        document: The document to export. Can be a file path, a dictionary,
                 or a TanzoDocument instance.
    
    Returns:
        A shorthand string representation of the document.
    """
    # Parse the document if needed
    if not isinstance(document, TanzoDocument):
        document = validate_and_parse(document)
    
    profile = document.profile
    
    # Start with the profile name
    parts = [f"{profile.name}"]
    
    # Add archetypes
    archetype_parts = []
    for archetype in profile.archetypes:
        a_part = f"{archetype.type[:3]}:{archetype.weight:.1f}"
        
        # Add traits if available
        if archetype.traits:
            trait_parts = []
            for trait in archetype.traits:
                t_part = f"{trait.name}:{trait.value:.1f}"
                trait_parts.append(t_part)
            
            if trait_parts:
                a_part += f"({','.join(trait_parts)})"
        
        archetype_parts.append(a_part)
    
    parts.append("|".join(archetype_parts))
    
    return " - ".join(parts)
