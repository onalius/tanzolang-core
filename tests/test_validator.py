"""
Tests for the TanzoLang validator
"""

import os
import sys
import unittest
from pathlib import Path
import tempfile
import json
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from clients.python.tanzo_schema.validator import (
    load_schema,
    load_yaml_file,
    validate_file,
    validate_profile
)
from clients.python.tanzo_schema.models import TanzoProfile


class TestValidator(unittest.TestCase):
    """Tests for the tanzo_schema validator module"""
    
    def setUp(self):
        """Setup test files and paths"""
        self.examples_dir = Path(__file__).parent.parent / "examples"
        self.schema_path = Path(__file__).parent.parent / "spec" / "tanzo-schema.json"
        self.valid_example = self.examples_dir / "Kai_profile.yaml"
        
        # Ensure required files exist
        self.assertTrue(self.schema_path.exists(), f"Schema file not found: {self.schema_path}")
        self.assertTrue(self.valid_example.exists(), f"Example file not found: {self.valid_example}")
        
        # Create an invalid example file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.invalid_file = Path(self.temp_dir.name) / "invalid.yaml"
        
        with open(self.invalid_file, "w", encoding="utf-8") as f:
            yaml.dump({
                "version": "0.1.0",
                "profile": {
                    "name": "Invalid Profile",
                    # Missing required archetypes
                }
            }, f)
    
    def tearDown(self):
        """Clean up temporary files"""
        self.temp_dir.cleanup()
    
    def test_load_schema(self):
        """Test loading the JSON schema"""
        schema = load_schema()
        
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema["$schema"], "http://json-schema.org/draft-07/schema#")
        self.assertIn("title", schema)
        self.assertIn("TanzoLang", schema["title"])
    
    def test_load_yaml_file(self):
        """Test loading a YAML file"""
        data = load_yaml_file(self.valid_example)
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["version"], "0.1.0")
        self.assertIn("profile", data)
        self.assertEqual(data["profile"]["name"], "Kai's Digital Twin")
    
    def test_validate_file_valid(self):
        """Test validating a valid file"""
        # Should not raise exception
        result = validate_file(self.valid_example)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["version"], "0.1.0")
        self.assertIn("profile", result)
    
    def test_validate_file_invalid(self):
        """Test validating an invalid file"""
        from jsonschema import ValidationError
        
        # Should raise ValidationError
        with self.assertRaises(ValidationError):
            validate_file(self.invalid_file)
    
    def test_validate_file_nonexistent(self):
        """Test validating a nonexistent file"""
        # Should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            validate_file("nonexistent_file.yaml")
    
    def test_validate_profile(self):
        """Test validating a profile and returning a Pydantic model"""
        profile = validate_profile(self.valid_example)
        
        self.assertIsInstance(profile, TanzoProfile)
        self.assertEqual(profile.version, "0.1.0")
        self.assertEqual(profile.profile.name, "Kai's Digital Twin")
        
        # Check archetypes
        self.assertEqual(len(profile.profile.archetypes), 2)
        
        # Check first archetype
        archetype = profile.profile.archetypes[0]
        self.assertEqual(archetype.type.value, "digital")
        self.assertEqual(archetype.name, "Online Avatar")
        
        # Check an attribute with a distribution
        screen_time = archetype.attributes[1]
        self.assertEqual(screen_time.name, "screen_time")
        self.assertEqual(screen_time.value.distribution, "normal")
        self.assertEqual(screen_time.value.mean, 4.5)
        self.assertEqual(screen_time.value.stdDev, 1.2)


if __name__ == "__main__":
    unittest.main()
