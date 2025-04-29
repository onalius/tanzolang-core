"""
Validation functions for TanzoLang profiles.

This module provides functions to validate TanzoLang profiles against
the schema and load profiles from various formats.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

import yaml
import jsonschema
from pydantic import ValidationError

from tanzo_schema.models import TanzoProfile


def get_schema_path() -> Path:
    """
    Get the path to the tanzo-schema.json file.
    
    Returns:
        Path: Path to the schema file
    """
    # Try to locate the schema in a few different places
    possible_locations = [
        Path("spec/tanzo-schema.json"),
        Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json",
        Path.home() / ".tanzo" / "tanzo-schema.json",
    ]
    
    for path in possible_locations:
        if path.exists():
            return path
    
    raise FileNotFoundError(
        "Could not find tanzo-schema.json. Please ensure the tanzo-lang-core "
        "repository is properly installed or provide a path to the schema file."
    )


def load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON schema.
    
    Returns:
        Dict[str, Any]: The loaded schema as a dictionary
    """
    schema_path = get_schema_path()
    with open(schema_path, "r") as schema_file:
        return json.load(schema_file)


def validate_with_jsonschema(data: Dict[str, Any], schema: Optional[Dict[str, Any]] = None) -> bool:
    """
    Validate data against the TanzoLang JSON schema using jsonschema.
    
    Args:
        data: The data to validate
        schema: Optional schema to use instead of the default
        
    Returns:
        bool: True if validation succeeds, raises exception otherwise
    """
    if schema is None:
        schema = load_schema()
    
    jsonschema.validate(instance=data, schema=schema)
    return True


def validate_with_pydantic(data: Dict[str, Any]) -> TanzoProfile:
    """
    Validate data using Pydantic models.
    
    Args:
        data: The data to validate
        
    Returns:
        TanzoProfile: A validated TanzoProfile object
    """
    return TanzoProfile.model_validate(data)


def validate_tanzo_profile(
    data: Dict[str, Any], 
    use_jsonschema: bool = True,
    use_pydantic: bool = True
) -> TanzoProfile:
    """
    Validate a TanzoLang profile using both jsonschema and Pydantic.
    
    Args:
        data: The profile data to validate
        use_jsonschema: Whether to validate with jsonschema
        use_pydantic: Whether to validate with Pydantic
        
    Returns:
        TanzoProfile: A validated TanzoProfile object
    
    Raises:
        jsonschema.exceptions.ValidationError: If jsonschema validation fails
        pydantic.ValidationError: If Pydantic validation fails
    """
    if use_jsonschema:
        validate_with_jsonschema(data)
    
    if use_pydantic:
        return validate_with_pydantic(data)
    
    # If we don't use Pydantic validation but need to return a TanzoProfile
    return TanzoProfile.model_validate(data)


def load_profile_from_yaml(file_path: Union[str, Path]) -> TanzoProfile:
    """
    Load and validate a TanzoLang profile from a YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        TanzoProfile: A validated TanzoProfile object
    """
    with open(file_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    
    return validate_tanzo_profile(data)


def load_profile_from_json(file_path: Union[str, Path]) -> TanzoProfile:
    """
    Load and validate a TanzoLang profile from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        TanzoProfile: A validated TanzoProfile object
    """
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    
    return validate_tanzo_profile(data)
