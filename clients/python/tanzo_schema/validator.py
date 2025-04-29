"""
Validator module for TanzoLang profiles.

This module provides functions to validate TanzoLang profiles against the schema.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jsonschema
import yaml
from jsonschema import Draft7Validator

from tanzo_schema.models import TanzoProfile


def _load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON schema.
    
    Returns:
        Dict[str, Any]: The loaded schema as a dictionary.
    """
    # Try to find the schema in various locations
    possible_paths = [
        # Relative to the current file (in package)
        Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json",
        # In a standard install location
        Path("/") / "spec" / "tanzo-schema.json",
        # In the current directory
        Path.cwd() / "spec" / "tanzo-schema.json",
    ]
    
    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
    
    # If schema not found in filesystem, use embedded minimal schema
    # This ensures the validator can work even if the schema file is not available
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["metadata", "digital_archetype"],
        "properties": {
            "metadata": {
                "type": "object",
                "required": ["version", "name"],
            },
            "digital_archetype": {
                "type": "object",
                "required": ["traits", "attributes"],
                "properties": {
                    "traits": {
                        "type": "object",
                        "required": ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"],
                    }
                }
            }
        }
    }


def validate_profile_against_schema(profile_data: Dict[str, Any]) -> List[str]:
    """
    Validate a profile against the TanzoLang JSON schema.
    
    Args:
        profile_data (Dict[str, Any]): Profile data as a dictionary.
        
    Returns:
        List[str]: List of validation errors, empty if valid.
    """
    schema = _load_schema()
    validator = Draft7Validator(schema)
    
    errors = []
    for error in validator.iter_errors(profile_data):
        errors.append(f"{' -> '.join([str(p) for p in error.path])}: {error.message}")
    
    return errors


def validate_profile_with_pydantic(profile_data: Dict[str, Any]) -> List[str]:
    """
    Validate a profile using Pydantic models.
    
    Args:
        profile_data (Dict[str, Any]): Profile data as a dictionary.
        
    Returns:
        List[str]: List of validation errors, empty if valid.
    """
    try:
        TanzoProfile(**profile_data)
        return []
    except Exception as e:
        return [str(e)]


def load_profile(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a profile from a YAML or JSON file.
    
    Args:
        file_path (Union[str, Path]): Path to the profile file.
        
    Returns:
        Dict[str, Any]: The loaded profile as a dictionary.
        
    Raises:
        ValueError: If the file format is not supported or file doesn't exist.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise ValueError(f"File {file_path} does not exist")
    
    with open(file_path, "r") as f:
        if file_path.suffix.lower() in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif file_path.suffix.lower() == ".json":
            return json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")


def validate_profile(
    profile_path: Union[str, Path], use_pydantic: bool = True
) -> List[str]:
    """
    Validate a profile file against the TanzoLang schema.
    
    Args:
        profile_path (Union[str, Path]): Path to the profile file.
        use_pydantic (bool, optional): Whether to use Pydantic validation. Defaults to True.
        
    Returns:
        List[str]: List of validation errors, empty if valid.
        
    Raises:
        ValueError: If the file format is not supported or file doesn't exist.
    """
    profile_data = load_profile(profile_path)
    
    # Run schema validation
    schema_errors = validate_profile_against_schema(profile_data)
    
    # Run Pydantic validation if requested
    pydantic_errors = []
    if use_pydantic and not schema_errors:
        pydantic_errors = validate_profile_with_pydantic(profile_data)
    
    return schema_errors + pydantic_errors
