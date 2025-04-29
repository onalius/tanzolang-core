"""
Tests for the TanzoLang schema
"""

import json
import os
from pathlib import Path
import unittest

import jsonschema
from jsonschema import ValidationError


class TestTanzoSchema(unittest.TestCase):
    """Tests for the TanzoLang JSON schema definitions"""
    
    def setUp(self):
        """Load the schema before each test"""
        # Find the schema file
        schema_path = Path(__file__).parent.parent / "spec" / "tanzo-schema.json"
        
        with open(schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
    
    def test_schema_basics(self):
        """Test the basic schema properties"""
        self.assertEqual(self.schema["$schema"], "http://json-schema.org/draft-07/schema#")
        self.assertIn("$id", self.schema)
        self.assertIn("title", self.schema)
        self.assertEqual(self.schema["type"], "object")
        
        # Check required properties
        self.assertIn("required", self.schema)
        self.assertIn("version", self.schema["required"])
        self.assertIn("profile", self.schema["required"])
        
        # Check properties definitions
        self.assertIn("properties", self.schema)
        self.assertIn("version", self.schema["properties"])
        self.assertIn("profile", self.schema["properties"])
        
        # Check definitions section
        self.assertIn("definitions", self.schema)
        self.assertIn("archetype", self.schema["definitions"])
        self.assertIn("attribute", self.schema["definitions"])
        self.assertIn("probabilityDistribution", self.schema["definitions"])
    
    def test_valid_simple_profile(self):
        """Test validation of a simple profile"""
        # Define a minimal valid profile
        profile = {
            "version": "0.1.0",
            "profile": {
                "name": "Test Profile",
                "archetypes": [
                    {
                        "type": "digital",
                        "attributes": [
                            {
                                "name": "test_attribute",
                                "value": "test_value"
                            }
                        ]
                    }
                ]
            }
        }
        
        # Should not raise ValidationError
        jsonschema.validate(profile, self.schema)
    
    def test_invalid_missing_required(self):
        """Test validation fails on missing required properties"""
        # Missing version
        profile_missing_version = {
            "profile": {
                "name": "Test Profile",
                "archetypes": [
                    {
                        "type": "digital",
                        "attributes": [
                            {
                                "name": "test_attribute",
                                "value": "test_value"
                            }
                        ]
                    }
                ]
            }
        }
        
        with self.assertRaises(ValidationError):
            jsonschema.validate(profile_missing_version, self.schema)
        
        # Missing profile
        profile_missing_profile = {
            "version": "0.1.0"
        }
        
        with self.assertRaises(ValidationError):
            jsonschema.validate(profile_missing_profile, self.schema)
        
        # Missing archetypes
        profile_missing_archetypes = {
            "version": "0.1.0",
            "profile": {
                "name": "Test Profile"
            }
        }
        
        with self.assertRaises(ValidationError):
            jsonschema.validate(profile_missing_archetypes, self.schema)
    
    def test_normal_distribution(self):
        """Test validation of normal distribution attributes"""
        profile = {
            "version": "0.1.0",
            "profile": {
                "name": "Test Profile",
                "archetypes": [
                    {
                        "type": "digital",
                        "attributes": [
                            {
                                "name": "normal_attr",
                                "value": {
                                    "distribution": "normal",
                                    "mean": 10.0,
                                    "stdDev": 2.0
                                }
                            }
                        ]
                    }
                ]
            }
        }
        
        # Should not raise ValidationError
        jsonschema.validate(profile, self.schema)
    
    def test_uniform_distribution(self):
        """Test validation of uniform distribution attributes"""
        profile = {
            "version": "0.1.0",
            "profile": {
                "name": "Test Profile",
                "archetypes": [
                    {
                        "type": "digital",
                        "attributes": [
                            {
                                "name": "uniform_attr",
                                "value": {
                                    "distribution": "uniform",
                                    "min": 5.0,
                                    "max": 15.0
                                }
                            }
                        ]
                    }
                ]
            }
        }
        
        # Should not raise ValidationError
        jsonschema.validate(profile, self.schema)
    
    def test_discrete_distribution(self):
        """Test validation of discrete distribution attributes"""
        profile = {
            "version": "0.1.0",
            "profile": {
                "name": "Test Profile",
                "archetypes": [
                    {
                        "type": "digital",
                        "attributes": [
                            {
                                "name": "discrete_attr",
                                "value": {
                                    "distribution": "discrete",
                                    "values": ["low", "medium", "high"],
                                    "weights": [0.2, 0.5, 0.3]
                                }
                            }
                        ]
                    }
                ]
            }
        }
        
        # Should not raise ValidationError
        jsonschema.validate(profile, self.schema)
    
    def test_example_files(self):
        """Test that example files validate against the schema"""
        examples_dir = Path(__file__).parent.parent / "examples"
        
        # Find all example YAML files
        example_files = list(examples_dir.glob("*.yaml"))
        self.assertGreater(len(example_files), 0, "No example files found")
        
        for example_file in example_files:
            import yaml
            
            with open(example_file, "r", encoding="utf-8") as f:
                example_data = yaml.safe_load(f)
            
            # Should not raise ValidationError
            try:
                jsonschema.validate(example_data, self.schema)
            except ValidationError as e:
                self.fail(f"Example {example_file.name} failed validation: {e}")


if __name__ == "__main__":
    unittest.main()
