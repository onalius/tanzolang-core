"""
Validation utilities for TanzoLang profiles.
"""

import json
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Union, Optional
from jsonschema import validate, ValidationError as JsonSchemaValidationError
from pydantic import ValidationError as PydanticValidationError

from tanzo_schema.models import TanzoProfile


def _load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON schema.
    
    Returns:
        Dict[str, Any]: The loaded JSON schema
    """
    # Try to find the schema file in different locations
    possible_paths = [
        # Local package installation
        Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json",
        # Repository root
        Path(__file__).parent.parent.parent.parent.parent / "spec" / "tanzo-schema.json",
        # Current directory
        Path.cwd() / "spec" / "tanzo-schema.json",
    ]
    
    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return json.load(f)
    
    raise FileNotFoundError(
        "Could not find tanzo-schema.json. Make sure it exists in the 'spec' directory."
    )


def validate_tanzo_profile(
    profile_data: Union[str, Dict[str, Any]], 
    use_pydantic: bool = True
) -> TanzoProfile:
    """
    Validate a TanzoLang profile against the schema.
    
    Args:
        profile_data (Union[str, Dict[str, Any]]): Either a JSON/YAML string or a Python dictionary
                                               containing the profile data
        use_pydantic (bool): Whether to use Pydantic validation (True) or jsonschema validation (False)
        
    Returns:
        TanzoProfile: A validated Pydantic model representing the profile
        
    Raises:
        ValueError: If validation fails
        FileNotFoundError: If the schema file cannot be found
    """
    # Convert string to dictionary if needed
    if isinstance(profile_data, str):
        try:
            # Try JSON first
            profile_dict = json.loads(profile_data)
        except json.JSONDecodeError:
            # Try YAML next
            try:
                profile_dict = yaml.safe_load(profile_data)
            except yaml.YAMLError as e:
                raise ValueError(f"Invalid profile format (not valid JSON or YAML): {e}")
    else:
        profile_dict = profile_data
    
    if use_pydantic:
        try:
            # Validate using Pydantic
            return TanzoProfile.model_validate(profile_dict)
        except PydanticValidationError as e:
            raise ValueError(f"Profile validation failed: {str(e)}")
    else:
        # Validate using jsonschema
        try:
            schema = _load_schema()
            validate(instance=profile_dict, schema=schema)
            # If validation passes, return a Pydantic model
            return TanzoProfile.model_validate(profile_dict)
        except JsonSchemaValidationError as e:
            raise ValueError(f"Profile validation failed: {e.message}")
        except FileNotFoundError as e:
            raise e


def load_profile_from_yaml(yaml_path: Union[str, Path]) -> TanzoProfile:
    """
    Load and validate a TanzoLang profile from a YAML file.
    
    Args:
        yaml_path (Union[str, Path]): Path to the YAML file
        
    Returns:
        TanzoProfile: A validated Pydantic model representing the profile
        
    Raises:
        FileNotFoundError: If the file cannot be found
        ValueError: If validation fails
    """
    yaml_path = Path(yaml_path)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Profile file not found: {yaml_path}")
    
    with open(yaml_path, "r") as f:
        yaml_content = f.read()
    
    return validate_tanzo_profile(yaml_content)
