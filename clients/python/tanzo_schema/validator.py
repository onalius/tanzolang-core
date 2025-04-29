"""
Validation utilities for TanzoLang profiles
"""

import json
import os
from pathlib import Path
from typing import Dict, Union, Any, Optional

import yaml
import jsonschema
from jsonschema import ValidationError

from tanzo_schema.models import TanzoProfile


def load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON schema from the package
    
    Returns:
        Dict[str, Any]: The JSON schema as a dictionary
    """
    # Find the schema file relative to this file's location
    schema_path = Path(__file__).parents[3] / "spec" / "tanzo-schema.json"
    
    if not schema_path.exists():
        # If not found in the repo structure, try to use an installed schema
        schema_path = Path(__file__).parent / "schema" / "tanzo-schema.json"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Cannot find the TanzoLang schema file at {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a YAML file into a dictionary
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dict[str, Any]: The parsed YAML content
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Validate a TanzoLang profile file against the schema
    
    Args:
        file_path: Path to the YAML or JSON file
        
    Returns:
        Dict[str, Any]: The validated profile as a dictionary
        
    Raises:
        ValidationError: If the profile does not conform to the schema
        FileNotFoundError: If the file does not exist
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load the file based on extension
    if file_path.suffix.lower() in (".yaml", ".yml"):
        data = load_yaml_file(file_path)
    elif file_path.suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    # Validate against schema
    schema = load_schema()
    jsonschema.validate(data, schema)
    
    return data


def validate_profile(profile_path: Union[str, Path]) -> TanzoProfile:
    """
    Validate a TanzoLang profile and return a Pydantic model
    
    Args:
        profile_path: Path to the profile file
        
    Returns:
        TanzoProfile: A validated Pydantic model of the profile
        
    Raises:
        ValidationError: If the profile does not conform to the schema
    """
    # First validate using jsonschema
    data = validate_file(profile_path)
    
    # Then convert to Pydantic model for stronger typing
    return TanzoProfile.model_validate(data)
