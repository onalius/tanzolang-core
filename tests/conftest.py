"""
Test fixtures for the TanzoLang test suite.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def example_file_path():
    """Fixture providing the path to the Kai_profile.yaml example file."""
    root_dir = Path(__file__).parent.parent
    example_path = root_dir / "examples" / "Kai_profile.yaml"
    
    # Make sure the file exists
    if not example_path.exists():
        pytest.skip(f"Example file not found: {example_path}")
    
    return example_path


@pytest.fixture
def example_json_path():
    """
    Fixture providing a temporary JSON version of the example file.
    """
    root_dir = Path(__file__).parent.parent
    example_path = root_dir / "examples" / "Kai_profile.yaml"
    
    # Make sure the file exists
    if not example_path.exists():
        pytest.skip(f"Example file not found: {example_path}")
    
    # Load the YAML file
    with open(example_path, "r") as f:
        data = yaml.safe_load(f)
    
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp:
        temp.write(json.dumps(data).encode("utf-8"))
        temp_path = temp.name
    
    # Return the path to the temporary file
    yield Path(temp_path)
    
    # Clean up the temporary file
    os.unlink(temp_path)


@pytest.fixture
def invalid_yaml_path():
    """
    Fixture providing a path to an invalid YAML file.
    """
    # Create a temporary file with invalid YAML
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
        temp.write(b"invalid: yaml: file:")
        temp_path = temp.name
    
    # Return the path to the temporary file
    yield Path(temp_path)
    
    # Clean up the temporary file
    os.unlink(temp_path)


@pytest.fixture
def invalid_schema_path():
    """
    Fixture providing a path to a file that doesn't match the schema.
    """
    # Create a temporary file with valid YAML but invalid schema
    invalid_data = {
        "version": "0.1.0",
        "profile": {
            "name": "Invalid Profile",
            # Missing required archetypes field
            "invalid_field": "invalid value"
        }
    }
    
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp:
        temp.write(yaml.dump(invalid_data).encode("utf-8"))
        temp_path = temp.name
    
    # Return the path to the temporary file
    yield Path(temp_path)
    
    # Clean up the temporary file
    os.unlink(temp_path)
