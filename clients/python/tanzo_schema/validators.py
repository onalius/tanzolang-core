"""Validation utilities for TanzoLang schema."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Union

import jsonschema
import yaml

from tanzo_schema.models import TanzoProfile


def _get_schema_path() -> str:
    """Get the path to the schema file."""
    # Check if we're in the repository
    repo_schema = Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json"
    if repo_schema.exists():
        return str(repo_schema)
    
    # Otherwise use the packaged schema
    return os.path.join(os.path.dirname(__file__), "tanzo-schema.json")


def validate_profile_dict(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a profile against the TanzoLang schema.
    
    Args:
        profile_data: Dictionary containing profile data
        
    Returns:
        The validated profile data
        
    Raises:
        jsonschema.exceptions.ValidationError: If validation fails
    """
    schema_path = _get_schema_path()
    with open(schema_path, "r") as f:
        schema = json.load(f)
    
    jsonschema.validate(instance=profile_data, schema=schema)
    return profile_data


def validate_profile(profile: TanzoProfile) -> TanzoProfile:
    """
    Validate a TanzoProfile object against the schema.
    
    Args:
        profile: TanzoProfile object to validate
        
    Returns:
        The validated profile object
        
    Raises:
        jsonschema.exceptions.ValidationError: If validation fails
    """
    profile_dict = profile.to_dict()
    validate_profile_dict(profile_dict)
    return profile


def load_profile(file_path: str) -> TanzoProfile:
    """
    Load and validate a profile from a file.
    
    Args:
        file_path: Path to YAML or JSON file
        
    Returns:
        Validated TanzoProfile object
        
    Raises:
        ValueError: If the file format is not supported
        jsonschema.exceptions.ValidationError: If validation fails
    """
    if file_path.endswith((".yml", ".yaml")):
        with open(file_path, "r") as f:
            profile_data = yaml.safe_load(f)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            profile_data = json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    # Validate against JSON schema
    validate_profile_dict(profile_data)
    
    # Convert to Pydantic model
    return TanzoProfile.from_dict(profile_data)
