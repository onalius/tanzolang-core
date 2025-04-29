"""
Validation utilities for Tanzo Schema.

This module provides functions for validating Tanzo profiles against
the canonical JSON Schema.
"""

import json
import os
import pathlib
from typing import Dict, List, Optional, Union

import jsonschema
import yaml
from jsonschema import ValidationError
from pydantic import ValidationError as PydanticValidationError

from .models import TanzoProfile


class SchemaValidationError(Exception):
    """Exception raised for schema validation errors."""

    def __init__(self, message: str, details: Optional[List[Dict]] = None):
        self.message = message
        self.details = details or []
        super().__init__(self.message)


def get_schema_path() -> str:
    """
    Get the path to the canonical schema file.
    
    Returns:
        str: Path to the schema file
    """
    # Try to find the schema in a few common locations
    possible_paths = [
        # Current package directory's parent's parent's parent + spec
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "..", "..", "..", "spec", "tanzo-schema.json"
        ),
        # Current working directory + spec
        os.path.join(os.getcwd(), "spec", "tanzo-schema.json"),
        # Installed package data
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "tanzo-schema.json"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    raise FileNotFoundError(
        "Could not find tanzo-schema.json. Please ensure the schema file is accessible."
    )


def load_schema() -> Dict:
    """
    Load the canonical JSON Schema.
    
    Returns:
        Dict: The schema as a dictionary
    
    Raises:
        FileNotFoundError: If the schema file cannot be found
        json.JSONDecodeError: If the schema file contains invalid JSON
    """
    schema_path = get_schema_path()
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_profile(profile_data: Union[Dict, str, pathlib.Path]) -> TanzoProfile:
    """
    Validate a Tanzo profile against the schema.
    
    Args:
        profile_data: Profile data as a dictionary, YAML string, or path to a YAML file
    
    Returns:
        TanzoProfile: A validated Pydantic model of the profile
    
    Raises:
        SchemaValidationError: If validation fails
        FileNotFoundError: If a provided file path doesn't exist
    """
    # Load profile data if it's a file path
    if isinstance(profile_data, (str, pathlib.Path)) and os.path.exists(str(profile_data)):
        with open(profile_data, "r") as f:
            if str(profile_data).endswith((".yaml", ".yml")):
                try:
                    profile_dict = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    raise SchemaValidationError(f"Invalid YAML: {str(e)}")
            else:
                try:
                    profile_dict = json.load(f)
                except json.JSONDecodeError as e:
                    raise SchemaValidationError(f"Invalid JSON: {str(e)}")
    # Parse YAML string
    elif isinstance(profile_data, str) and (
        profile_data.strip().startswith(("{", "[")) or profile_data.strip().startswith(("---"))
    ):
        try:
            if profile_data.strip().startswith(("{", "[")):
                profile_dict = json.loads(profile_data)
            else:
                profile_dict = yaml.safe_load(profile_data)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise SchemaValidationError(f"Invalid profile data: {str(e)}")
    # Use dictionary directly
    elif isinstance(profile_data, dict):
        profile_dict = profile_data
    else:
        raise SchemaValidationError(
            "Profile data must be a dictionary, valid YAML/JSON string, or file path"
        )
    
    # Validate against JSON Schema
    try:
        schema = load_schema()
        jsonschema.validate(instance=profile_dict, schema=schema)
    except ValidationError as e:
        raise SchemaValidationError(
            f"JSON Schema validation failed: {e.message}",
            details=[{"path": "/".join(str(p) for p in e.path), "message": e.message}]
        )
    except FileNotFoundError as e:
        raise SchemaValidationError(f"Schema file not found: {str(e)}")
    
    # Validate using Pydantic model
    try:
        return TanzoProfile.model_validate(profile_dict)
    except PydanticValidationError as e:
        errors = e.errors()
        raise SchemaValidationError(
            "Pydantic validation failed",
            details=[{"path": "/".join(str(p) for p in err["loc"]), "message": err["msg"]} for err in errors]
        )
