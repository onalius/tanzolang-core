"""
Validator module for TanzoLang documents.

This module provides functions to validate TanzoLang documents against
the official JSON Schema.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jsonschema
import yaml
from jsonschema import Draft7Validator

from tanzo_schema.models import TanzoDocument

# Get the absolute path to the schema file
SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    "spec", 
    "tanzo-schema.json"
)


def load_schema() -> Dict[str, Any]:
    """Load the TanzoLang JSON Schema."""
    try:
        with open(SCHEMA_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to load schema: {e}")


def load_document(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a TanzoLang document from a file path.
    
    Supports both JSON and YAML formats.
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(file_path, "r") as f:
            if file_path.suffix.lower() in (".yaml", ".yml"):
                return yaml.safe_load(f)
            else:
                return json.load(f)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to parse document: {e}")


def validate_document(
    document: Union[str, Path, Dict[str, Any], TanzoDocument],
    schema: Optional[Dict[str, Any]] = None
) -> List[str]:
    """
    Validate a TanzoLang document against the schema.
    
    Args:
        document: The document to validate. Can be a file path, a dictionary,
                 or a TanzoDocument instance.
        schema: Optional schema to validate against. If not provided,
                the default schema will be used.
    
    Returns:
        A list of validation errors. Empty list if validation passed.
    """
    # Load the schema if not provided
    if schema is None:
        schema = load_schema()
    
    # Load the document if it's a file path
    if isinstance(document, (str, Path)):
        document = load_document(document)
    elif isinstance(document, TanzoDocument):
        document = document.model_dump(exclude_none=True)
    
    # Validate the document
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(document))
    
    # Convert errors to strings
    return [
        f"{'.'.join(str(p) for p in error.path)}: {error.message}"
        for error in errors
    ]


def validate_and_parse(
    document: Union[str, Path, Dict[str, Any]]
) -> TanzoDocument:
    """
    Validate a document and parse it into a TanzoDocument if valid.
    
    Args:
        document: The document to validate and parse.
    
    Returns:
        A TanzoDocument instance.
    
    Raises:
        ValueError: If the document is invalid.
    """
    # Load the document if it's a file path
    if isinstance(document, (str, Path)):
        document = load_document(document)
    
    # Validate the document
    errors = validate_document(document)
    
    if errors:
        raise ValueError(f"Invalid TanzoLang document: {'; '.join(errors)}")
    
    # Parse the document
    return TanzoDocument.model_validate(document)
