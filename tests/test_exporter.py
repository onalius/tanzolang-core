"""
Tests for the TanzoLang exporter
"""

import os
import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from clients.python.tanzo_schema.exporter import (
    format_distribution,
    format_attribute,
    export_profile
)
from clients.python.tanzo_schema.models import (
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
    Attribute
)


class TestExporter(unittest.TestCase):
    """Tests for the tanzo_schema exporter module"""
    
    def setUp(self):
        """Setup test distributions and attributes"""
        # Create test distributions
        self.normal_dist = NormalDistribution(distribution="normal", mean=10.0, stdDev=2.0)
        self.uniform_dist = UniformDistribution(distribution="uniform", min=5.0, max=15.0)
        self.discrete_dist = DiscreteDistribution(
            distribution="discrete",
            values=["low", "medium", "high"],
            weights=[0.2, 0.5, 0.3]
        )
        
        # Create test attributes
        self.normal_attr = Attribute(
            name="normal_attr",
            value=self.normal_dist,
            description="A normal distribution attribute",
            unit="points"
        )
        
        self.uniform_attr = Attribute(
            name="uniform_attr",
            value=self.uniform_dist
        )
        
        self.discrete_attr = Attribute(
            name="discrete_attr",
            value=self.discrete_dist
        )
        
        self.string_attr = Attribute(
            name="string_attr",
            value="string_value"
        )
        
        self.number_attr = Attribute(
            name="number_attr",
            value=42.5,
            unit="kg"
        )
        
        self.bool_attr = Attribute(
            name="bool_attr",
            value=True
        )
        
        # Path to example profiles
        self.examples_dir = Path(__file__).parent.parent / "examples"
        self.valid_example = self.examples_dir / "Kai_profile.yaml"
        self.digital_example = self.examples_dir / "digital_archetype_only.yaml"
    
    def test_format_normal_distribution(self):
        """Test formatting a normal distribution"""
        formatted = format_distribution(self.normal_dist)
        self.assertEqual(formatted, "N(10.00, 2.00)")
    
    def test_format_uniform_distribution(self):
        """Test formatting a uniform distribution"""
        formatted = format_distribution(self.uniform_dist)
        self.assertEqual(formatted, "U(5.00, 15.00)")
    
    def test_format_discrete_distribution(self):
        """Test formatting a discrete distribution"""
        formatted = format_distribution(self.discrete_dist)
        
        # Should contain all values and weights
        self.assertIn('"low":0.20', formatted)
        self.assertIn('"medium":0.50', formatted)
        self.assertIn('"high":0.30', formatted)
        
        # Should start with D( and end with )
        self.assertTrue(formatted.startswith("D("))
        self.assertTrue(formatted.endswith(")"))
    
    def test_format_attribute_with_distribution(self):
        """Test formatting an attribute with a distribution"""
        formatted = format_attribute(self.normal_attr)
        self.assertEqual(formatted, "normal_attr=N(10.00, 2.00) points")
    
    def test_format_attribute_with_string(self):
        """Test formatting an attribute with a string value"""
        formatted = format_attribute(self.string_attr)
        self.assertEqual(formatted, 'string_attr="string_value"')
    
    def test_format_attribute_with_number(self):
        """Test formatting an attribute with a number and unit"""
        formatted = format_attribute(self.number_attr)
        self.assertEqual(formatted, "number_attr=42.5 kg")
    
    def test_format_attribute_with_boolean(self):
        """Test formatting an attribute with a boolean value"""
        formatted = format_attribute(self.bool_attr)
        self.assertEqual(formatted, "bool_attr=true")
    
    def test_export_profile(self):
        """Test exporting a full profile"""
        # Export the digital archetype example
        exported = export_profile(self.digital_example)
        
        # Check the structure of the exported text
        lines = exported.strip().split("\n")
        
        # First line should contain the profile name and version
        self.assertIn("Digital Avatar Only", lines[0])
        self.assertIn("v0.1.0", lines[0])
        
        # Should have the archetype line
        self.assertIn("DIGITAL:Digital Avatar", lines[1])
        
        # Should have attributes with proper formatting
        self.assertIn('digital_id="DA-27491"', exported)
        self.assertIn('creation_date="2023-04-15"', exported)
        self.assertIn('popularity_score=N(85.00, 10.00) points', exported)
        
        # Should have the discrete distribution for access_level
        self.assertIn('access_level=D("basic":0.70, "premium":0.25, "admin":0.05)', exported)
        
        # Should have the uniform distribution for processing_power
        self.assertIn('processing_power=U(1.00, 5.00) TFlops', exported)


if __name__ == "__main__":
    unittest.main()
