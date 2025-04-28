"""
Validation functions for TanzoLang profiles.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Union, Optional

import yaml
import jsonschema
from jsonschema import validate
from pydantic import ValidationError

from tanzo_schema.models import Profile


def _load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON Schema.
    
    Returns:
        Dict[str, Any]: The schema as a dictionary
    """
    # Try to find the schema file in a few common locations
    possible_paths = [
        Path("spec/tanzo-schema.json"),  # Current working directory
        Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json",  # From package to repo root
        Path("/spec/tanzo-schema.json"),  # Absolute path
    ]
    
    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
    
    # If schema not found, raise an error
    raise FileNotFoundError(
        "Could not find tanzo-schema.json. Make sure it exists in the spec directory."
    )


def validate_profile(profile_data: Dict[str, Any]) -> bool:
    """
    Validate a profile against the TanzoLang schema.
    
    Args:
        profile_data (Dict[str, Any]): The profile data to validate
        
    Returns:
        bool: True if valid, raises exception if invalid
        
    Raises:
        jsonschema.exceptions.ValidationError: If profile does not conform to schema
    """
    schema = _load_schema()
    validate(instance=profile_data, schema=schema)
    return True


def load_profile(file_path: Union[str, Path]) -> Profile:
    """
    Load and validate a profile from a file.
    
    Args:
        file_path (Union[str, Path]): Path to the profile file (YAML or JSON)
        
    Returns:
        Profile: A validated Pydantic model of the profile
        
    Raises:
        FileNotFoundError: If file does not exist
        ValidationError: If profile does not conform to the Pydantic model
        jsonschema.exceptions.ValidationError: If profile does not conform to schema
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Profile file not found: {file_path}")
    
    # Load file based on extension
    with open(file_path, "r") as f:
        if file_path.suffix.lower() in [".yaml", ".yml"]:
            profile_data = yaml.safe_load(f)
        elif file_path.suffix.lower() == ".json":
            profile_data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    # Validate against JSON Schema
    validate_profile(profile_data)
    
    # Parse with Pydantic
    return Profile.model_validate(profile_data)


def save_profile(profile: Profile, file_path: Union[str, Path], format: str = "yaml") -> None:
    """
    Save a profile to a file.
    
    Args:
        profile (Profile): The profile to save
        file_path (Union[str, Path]): Path where to save the file
        format (str, optional): Format to save as ("yaml" or "json"). Defaults to "yaml".
        
    Raises:
        ValueError: If format is not supported
    """
    file_path = Path(file_path)
    
    # Convert to dictionary
    profile_data = profile.model_dump(exclude_none=True)
    
    # Save in requested format
    with open(file_path, "w") as f:
        if format.lower() == "yaml":
            yaml.dump(profile_data, f, sort_keys=False, default_flow_style=False)
        elif format.lower() == "json":
            json.dump(profile_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'.")
