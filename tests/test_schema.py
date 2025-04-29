"""
Tests for the TanzoLang schema validation.
"""

import json
import os
from pathlib import Path

import pytest
import yaml
from jsonschema import validate

from clients.python.tanzo_schema import (
    load_tanzo_file, validate_tanzo_file, load_tanzo_pydantic
)
from clients.python.tanzo_schema.models import TanzoSchema


# Find the root directory
ROOT_DIR = Path(__file__).parent.parent


def test_schema_validation_json():
    """Test loading and validating the JSON schema."""
    schema_path = ROOT_DIR / "spec" / "tanzo-schema.json"
    assert schema_path.exists(), "Schema file does not exist"
    
    with open(schema_path, "r") as f:
        schema = json.load(f)
    
    # Basic schema structure validation
    assert "$schema" in schema, "Missing $schema key"
    assert "$id" in schema, "Missing $id key"
    assert "title" in schema, "Missing title"
    assert "properties" in schema, "Missing properties"
    assert "definitions" in schema, "Missing definitions"


def test_schema_validation_yaml():
    """Test loading and validating the YAML schema."""
    schema_path = ROOT_DIR / "spec" / "tanzo-schema.yaml"
    assert schema_path.exists(), "Schema file does not exist"
    
    with open(schema_path, "r") as f:
        schema = yaml.safe_load(f)
    
    # Basic schema structure validation
    assert "$schema" in schema, "Missing $schema key"
    assert "$id" in schema, "Missing $id key"
    assert "title" in schema, "Missing title"
    assert "properties" in schema, "Missing properties"
    assert "definitions" in schema, "Missing definitions"


def test_example_validation():
    """Test validating example files against the schema."""
    schema_path = ROOT_DIR / "spec" / "tanzo-schema.json"
    example_files = [
        ROOT_DIR / "examples" / "Kai_profile.yaml",
        ROOT_DIR / "examples" / "digital_archetype_only.yaml",
    ]
    
    with open(schema_path, "r") as f:
        schema = json.load(f)
    
    for example_file in example_files:
        assert example_file.exists(), f"Example file {example_file} does not exist"
        
        with open(example_file, "r") as f:
            if example_file.suffix.lower() in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
        
        # Validate using jsonschema
        validate(instance=data, schema=schema)
        
        # Validate using our validator
        assert validate_tanzo_file(example_file) is True


def test_pydantic_validation():
    """Test validating examples using Pydantic models."""
    example_files = [
        ROOT_DIR / "examples" / "Kai_profile.yaml",
        ROOT_DIR / "examples" / "digital_archetype_only.yaml",
    ]
    
    for example_file in example_files:
        data = load_tanzo_file(example_file)
        
        # Validate using Pydantic
        tanzo_schema = TanzoSchema(**data)
        
        # Check basic properties
        assert tanzo_schema.version == "0.1.0"
        assert tanzo_schema.profile.name is not None
        assert tanzo_schema.profile.archetype.type in ["digital", "physical", "hybrid"]
        assert len(tanzo_schema.profile.archetype.attributes.personality.traits) > 0


def test_load_tanzo_pydantic():
    """Test loading files into Pydantic models."""
    example_file = ROOT_DIR / "examples" / "Kai_profile.yaml"
    
    # Load the file as a Pydantic model
    tanzo_schema = load_tanzo_pydantic(example_file)
    
    # Check that it loaded correctly
    assert tanzo_schema.version == "0.1.0"
    assert tanzo_schema.profile.name == "Kai"
    assert tanzo_schema.profile.archetype.type == "digital"
    
    # Check traits
    traits = tanzo_schema.profile.archetype.attributes.personality.traits
    trait_names = [t.name for t in traits]
    assert "empathy" in trait_names
    assert "curiosity" in trait_names
    
    # Check behavior patterns if they exist
    if (tanzo_schema.profile.archetype.attributes.behavior and 
        tanzo_schema.profile.archetype.attributes.behavior.patterns):
        patterns = tanzo_schema.profile.archetype.attributes.behavior.patterns
        pattern_names = [p.name for p in patterns]
        assert len(pattern_names) > 0


def test_invalid_schema_version():
    """Test that invalid schema versions are rejected."""
    # Create a copy of a valid schema with an invalid version
    example_file = ROOT_DIR / "examples" / "Kai_profile.yaml"
    with open(example_file, "r") as f:
        data = yaml.safe_load(f)
    
    # Change the version
    data["version"] = "0.2.0"
    
    # This should raise a validation error
    with pytest.raises(Exception):
        TanzoSchema(**data)
