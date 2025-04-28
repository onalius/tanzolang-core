"""
Validation functions for Tanzo profiles
"""

import json
import os
import pathlib
from typing import Any, Dict, List, Optional, Tuple, Union

import jsonschema
import yaml

from tanzo_schema.models import TanzoProfile


def _load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang schema from the package directory
    
    Returns:
        Dict[str, Any]: The schema as a Python dictionary
    """
    schema_path = pathlib.Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json"
    if not schema_path.exists():
        # If not found in the repo structure, try package data
        module_dir = pathlib.Path(__file__).parent
        schema_path = module_dir / "tanzo-schema.json"
        if not schema_path.exists():
            raise FileNotFoundError("Could not locate tanzo-schema.json")
    
    with open(schema_path, "r") as f:
        return json.load(f)


def load_yaml_file(file_path: Union[str, pathlib.Path]) -> Dict[str, Any]:
    """
    Load a YAML file into a Python dictionary
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dict[str, Any]: The loaded YAML content
        
    Raises:
        FileNotFoundError: If the file does not exist
        yaml.YAMLError: If the file cannot be parsed as YAML
    """
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def validate_tanzo_profile(
    data: Union[Dict[str, Any], str, pathlib.Path]
) -> Tuple[bool, Optional[List[str]]]:
    """
    Validate a Tanzo profile against the schema
    
    Args:
        data: Either a dictionary containing profile data, a file path to a YAML file,
              or a string containing YAML content
              
    Returns:
        Tuple[bool, Optional[List[str]]]: A tuple containing (is_valid, error_messages)
        
    Raises:
        ValueError: If the input data cannot be parsed
    """
    # Load the schema
    schema = _load_schema()
    
    # Process the input data
    profile_data: Dict[str, Any]
    
    if isinstance(data, dict):
        profile_data = data
    elif isinstance(data, (str, pathlib.Path)):
        # Check if it's a file path
        path = pathlib.Path(data)
        if path.exists() and path.is_file():
            profile_data = load_yaml_file(path)
        else:
            # Assume it's YAML content
            try:
                profile_data = yaml.safe_load(data)
                if not isinstance(profile_data, dict):
                    raise ValueError("YAML content does not represent a dictionary")
            except yaml.YAMLError as e:
                return False, [f"Invalid YAML content: {str(e)}"]
    else:
        return False, ["Input must be a dictionary, file path, or YAML string"]
    
    # Validate against JSON Schema
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(profile_data))
    
    if errors:
        error_messages = [
            f"{error.path}: {error.message}" if error.path else error.message
            for error in errors
        ]
        return False, error_messages
    
    # Additional validation with Pydantic
    try:
        TanzoProfile.model_validate(profile_data)
        return True, None
    except Exception as e:
        return False, [str(e)]
