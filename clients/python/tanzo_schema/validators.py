"""
Validation functions for TanzoLang profiles.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
import jsonschema
from jsonschema import Draft7Validator

from .models import TanzoProfile


def get_schema_path() -> str:
    """
    Get the path to the canonical tanzo-schema.json file.
    
    Returns:
        str: Path to the schema file
    """
    # Try to find the schema in various locations
    possible_paths = [
        # Current directory
        Path("tanzo-schema.json"),
        Path("spec/tanzo-schema.json"),
        # Relative to this file
        Path(__file__).parent.parent.parent.parent / "spec" / "tanzo-schema.json",
        # Package data directory (if installed)
        Path(__file__).parent / "data" / "tanzo-schema.json",
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path.absolute())
    
    raise FileNotFoundError(
        "Could not locate tanzo-schema.json. Please ensure the schema file "
        "is available in the spec directory or current working directory."
    )


def load_schema() -> Dict[str, Any]:
    """
    Load the TanzoLang JSON schema.
    
    Returns:
        Dict[str, Any]: The loaded schema
    """
    schema_path = get_schema_path()
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_against_schema(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate data against the TanzoLang JSON schema.
    
    Args:
        data: The data to validate
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, error_messages)
    """
    try:
        schema = load_schema()
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))
        
        if not errors:
            return True, []
        
        error_messages = []
        for error in errors:
            # Format a user-friendly error message
            path = "/".join(str(p) for p in error.path) if error.path else "root"
            message = f"{path}: {error.message}"
            error_messages.append(message)
        
        return False, error_messages
    
    except Exception as e:
        return False, [f"Validation error: {str(e)}"]


def validate_profile(profile: Union[Dict[str, Any], TanzoProfile]) -> Tuple[bool, List[str]]:
    """
    Validate a TanzoProfile against the schema.
    
    Args:
        profile: Either a dict or a TanzoProfile instance
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, error_messages)
    """
    if isinstance(profile, TanzoProfile):
        data = profile.model_dump()
    else:
        data = profile
    
    # First validate against JSON Schema
    schema_valid, schema_errors = validate_against_schema(data)
    
    # Then validate using Pydantic
    pydantic_errors = []
    if schema_valid:
        try:
            TanzoProfile.model_validate(data)
        except Exception as e:
            pydantic_errors = [str(e)]
    
    is_valid = schema_valid and not pydantic_errors
    all_errors = schema_errors + pydantic_errors
    
    return is_valid, all_errors


def load_profile_from_file(filepath: str) -> Tuple[Optional[TanzoProfile], List[str]]:
    """
    Load and validate a TanzoProfile from a YAML or JSON file.
    
    Args:
        filepath: Path to the file to load
        
    Returns:
        Tuple[Optional[TanzoProfile], List[str]]: (profile, error_messages)
    """
    errors = []
    
    try:
        with open(filepath, "r") as f:
            if filepath.endswith(".yaml") or filepath.endswith(".yml"):
                data = yaml.safe_load(f)
            elif filepath.endswith(".json"):
                data = json.load(f)
            else:
                errors.append(f"Unsupported file format: {filepath}. Use .yaml, .yml, or .json")
                return None, errors
        
        # Validate against schema
        valid, validation_errors = validate_profile(data)
        if not valid:
            errors.extend(validation_errors)
            return None, errors
        
        # Convert to Pydantic model
        profile = TanzoProfile.model_validate(data)
        return profile, []
    
    except FileNotFoundError:
        errors.append(f"File not found: {filepath}")
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing error: {str(e)}")
    except json.JSONDecodeError as e:
        errors.append(f"JSON parsing error: {str(e)}")
    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
    
    return None, errors
