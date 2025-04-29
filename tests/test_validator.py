"""
Tests for the validator module of the tanzo_schema package.
"""

import os
import pytest
from pathlib import Path

from clients.python.tanzo_schema import validate_document
from clients.python.tanzo_schema.validator import load_schema, load_document


def test_load_schema():
    """Test loading the schema."""
    schema = load_schema()
    assert isinstance(schema, dict)
    assert "$schema" in schema
    assert "properties" in schema
    assert "profile" in schema["properties"]


def test_load_document_yaml(example_file_path):
    """Test loading a YAML document."""
    document = load_document(example_file_path)
    assert isinstance(document, dict)
    assert "profile" in document
    assert "version" in document


def test_load_document_json(example_json_path):
    """Test loading a JSON document."""
    document = load_document(example_json_path)
    assert isinstance(document, dict)
    assert "profile" in document
    assert "version" in document


def test_load_document_nonexistent_file():
    """Test loading a nonexistent file."""
    with pytest.raises(FileNotFoundError):
        load_document("nonexistent.yaml")


def test_load_document_invalid_yaml(invalid_yaml_path):
    """Test loading an invalid YAML document."""
    with pytest.raises(ValueError):
        load_document(invalid_yaml_path)


def test_validate_document_valid(example_file_path):
    """Test validating a valid document."""
    errors = validate_document(example_file_path)
    assert errors == []


def test_validate_document_invalid(invalid_schema_path):
    """Test validating an invalid document."""
    errors = validate_document(invalid_schema_path)
    assert len(errors) > 0


def test_validate_document_dict():
    """Test validating a document provided as a dictionary."""
    document = {
        "version": "0.1.0",
        "profile": {
            "name": "Test Profile",
            "archetypes": [
                {
                    "type": "digital",
                    "weight": 0.8
                }
            ]
        }
    }
    errors = validate_document(document)
    assert errors == []


def test_validate_document_missing_required():
    """Test validating a document with missing required fields."""
    document = {
        "version": "0.1.0",
        "profile": {
            "name": "Test Profile",
            "archetypes": []
        }
    }
    errors = validate_document(document)
    assert len(errors) > 0
    assert any("archetypes" in error for error in errors)
