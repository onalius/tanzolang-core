"""
Pytest configuration file for Tanzo Schema tests.
"""

import json
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def sample_profile_dict():
    """Return a sample profile dictionary for testing."""
    return {
        "version": "0.1.0",
        "profile": {
            "id": "test-profile",
            "type": "human",
            "properties": {
                "name": "Test Person",
                "description": "A test profile for unit tests",
                "traits": [
                    {"name": "creativity", "value": 75, "variance": 10},
                    {"name": "logic", "value": 80, "variance": 5},
                ],
                "archetypes": [
                    {
                        "name": "tester",
                        "influence": 90,
                        "description": "Testing archetype",
                        "traits": [
                            {"name": "precision", "value": 85},
                            {"name": "thoroughness", "value": 90},
                        ],
                    }
                ],
                "capabilities": [
                    {
                        "name": "testing",
                        "level": 95,
                        "description": "Software testing capability",
                    }
                ],
            },
        },
    }


@pytest.fixture
def sample_profile_file(tmp_path, sample_profile_dict):
    """Create a sample profile YAML file for testing."""
    # Create a temporary YAML file
    test_file = tmp_path / "test_profile.yaml"
    with open(test_file, "w") as f:
        yaml.dump(sample_profile_dict, f)
    return test_file


@pytest.fixture
def sample_invalid_profile_file(tmp_path):
    """Create an invalid profile YAML file for testing."""
    # Create a temporary invalid YAML file
    test_file = tmp_path / "invalid_profile.yaml"
    invalid_profile = {
        "version": "0.1.0",
        "profile": {
            "id": "invalid-profile",
            # Missing required 'type' field
            "properties": {
                "name": "Invalid Profile",
                # Missing required 'name' field in traits
                "traits": [{"value": 75, "variance": 10}],
            },
        },
    }
    with open(test_file, "w") as f:
        yaml.dump(invalid_profile, f)
    return test_file


@pytest.fixture
def schema_file():
    """Return the path to the schema file (either JSON or YAML)."""
    repo_root = Path(__file__).resolve().parent.parent
    
    # Try different possible locations for the schema
    schema_paths = [
        repo_root / "spec" / "tanzo-schema.json",
        repo_root / "spec" / "tanzo-schema.yaml",
        repo_root / "clients" / "python" / "tanzo_schema" / "schema" / "tanzo-schema.json",
        repo_root / "clients" / "python" / "tanzo_schema" / "schema" / "tanzo-schema.yaml"
    ]
    
    for path in schema_paths:
        if path.exists():
            return path
    
    # If we're running in CI, create a fixture from the sample profile
    # by extracting the schema information
    test_data_dir = repo_root / "tests" / "test_data"
    if test_data_dir.exists():
        yaml_files = list(test_data_dir.glob("*.yaml"))
        if yaml_files:
            # Use the first YAML file to extract schema info
            print(f"Creating schema fixture from {yaml_files[0]}")
            return yaml_files[0]
    
    # If all else fails, return the default path and let the test handle if it's missing
    return schema_paths[0]
