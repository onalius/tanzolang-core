"""
Validation functions for TanzoLang schemas.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import jsonschema
import yaml

from tanzo_schema.models import TanzoSchema


def get_schema_path() -> str:
    """
    Get the path to the TanzoLang schema file.
    
    Returns:
        str: Path to the schema file
    """
    # Try to find schema in several possible locations
    possible_paths = [
        # Local development path
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "spec", "tanzo-schema.json"),
        # Installed package path
        os.path.join(os.path.dirname(__file__), "schema", "tanzo-schema.json"),
        # Fallback to the GitHub URL
        "https://github.com/onalius/tanzo-lang-core/raw/main/spec/tanzo-schema.json"
    ]
    
    for path in possible_paths:
        if path.startswith("http"):
            return path
        if os.path.exists(path):
            return path
    
    # Fallback to the last path even if it doesn't exist
    return possible_paths[-1]


def validate_tanzo_dict(data: Dict[str, Any]) -> bool:
    """
    Validate a TanzoLang schema from a dictionary.
    
    Args:
        data: Dictionary containing the TanzoLang data
    
    Returns:
        bool: True if valid, raises ValidationError otherwise
    """
    # Validate with Pydantic
    TanzoSchema(**data)
    return True


def validate_tanzo_file(file_path: Union[str, Path]) -> bool:
    """
    Validate a TanzoLang file.
    
    Args:
        file_path: Path to the file to validate
    
    Returns:
        bool: True if valid, raises ValidationError otherwise
    """
    data = load_tanzo_file(file_path)
    return validate_tanzo_dict(data)


def load_tanzo_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a TanzoLang file (YAML or JSON).
    
    Args:
        file_path: Path to the file to load
    
    Returns:
        Dict: The parsed TanzoLang data
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        if path.suffix.lower() in [".yaml", ".yml"]:
            return yaml.safe_load(f)
        elif path.suffix.lower() == ".json":
            return json.load(f)
        else:
            # Try to detect the format based on content
            content = f.read()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                try:
                    return yaml.safe_load(content)
                except yaml.YAMLError:
                    raise ValueError(f"Unsupported file format: {path.suffix}")


def load_tanzo_pydantic(file_path: Union[str, Path]) -> TanzoSchema:
    """
    Load a TanzoLang file and return a Pydantic model.
    
    Args:
        file_path: Path to the file to load
    
    Returns:
        TanzoSchema: The parsed TanzoLang data as a Pydantic model
    """
    data = load_tanzo_file(file_path)
    return TanzoSchema(**data)
