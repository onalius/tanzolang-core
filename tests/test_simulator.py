"""
Tests for the TanzoLang simulator
"""

import os
import sys
import unittest
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from clients.python.tanzo_schema.simulator import (
    sample_distribution,
    simulate_attribute,
    simulate_profile_once,
    simulate_profile
)
from clients.python.tanzo_schema.models import (
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
    Attribute
)


class TestSimulator(unittest.TestCase):
    """Tests for the tanzo_schema simulator module"""
    
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
        
        self.fixed_attr = Attribute(
            name="fixed_attr",
            value="fixed_value"
        )
        
        # Path to example profiles
        self.examples_dir = Path(__file__).parent.parent / "examples"
        self.valid_example = self.examples_dir / "Kai_profile.yaml"
    
    def test_sample_normal_distribution(self):
        """Test sampling from a normal distribution"""
        # Sample multiple times to test distribution properties
        samples = [sample_distribution(self.normal_dist) for _ in range(1000)]
        
        # Check basic statistics
        mean = np.mean(samples)
        std_dev = np.std(samples)
        
        # Should be approximately close to the specified parameters
        # (allowing for some random variation)
        self.assertAlmostEqual(mean, 10.0, delta=0.5)
        self.assertAlmostEqual(std_dev, 2.0, delta=0.5)
    
    def test_sample_uniform_distribution(self):
        """Test sampling from a uniform distribution"""
        # Sample multiple times
        samples = [sample_distribution(self.uniform_dist) for _ in range(1000)]
        
        # All samples should be within range
        for sample in samples:
            self.assertGreaterEqual(sample, 5.0)
            self.assertLessEqual(sample, 15.0)
        
        # Mean should be approximately the average of min and max
        mean = np.mean(samples)
        self.assertAlmostEqual(mean, 10.0, delta=0.5)
    
    def test_sample_discrete_distribution(self):
        """Test sampling from a discrete distribution"""
        # Sample multiple times
        samples = [sample_distribution(self.discrete_dist) for _ in range(1000)]
        
        # All samples should be one of the possible values
        for sample in samples:
            self.assertIn(sample, ["low", "medium", "high"])
        
        # Frequency should approximately match weights
        low_count = samples.count("low")
        medium_count = samples.count("medium")
        high_count = samples.count("high")
        
        self.assertAlmostEqual(low_count / 1000, 0.2, delta=0.05)
        self.assertAlmostEqual(medium_count / 1000, 0.5, delta=0.05)
        self.assertAlmostEqual(high_count / 1000, 0.3, delta=0.05)
    
    def test_simulate_attribute(self):
        """Test simulating an attribute"""
        # Test with normal distribution
        name, value = simulate_attribute(self.normal_attr)
        self.assertEqual(name, "normal_attr")
        self.assertIsInstance(value, float)
        
        # Test with fixed value
        name, value = simulate_attribute(self.fixed_attr)
        self.assertEqual(name, "fixed_attr")
        self.assertEqual(value, "fixed_value")
    
    def test_simulate_profile_once(self):
        """Test simulating a profile once"""
        # Use a real example profile
        from clients.python.tanzo_schema.validator import validate_profile
        profile = validate_profile(self.valid_example)
        
        # Run the simulation
        result = simulate_profile_once(profile)
        
        # Check the structure of the result
        self.assertIn("Online Avatar", result)
        self.assertIn("Physical Self", result)
        
        # Check attributes in the digital archetype
        digital = result["Online Avatar"]
        self.assertIn("username", digital)
        self.assertIn("screen_time", digital)
        self.assertIn("social_influence", digital)
        
        # Check attributes in the physical archetype
        physical = result["Physical Self"]
        self.assertIn("height", physical)
        self.assertIn("weight", physical)
        self.assertIn("activity_level", physical)
        
        # Username should be fixed
        self.assertEqual(digital["username"], "kai_digital")
        
        # Height should be fixed
        self.assertEqual(physical["height"], 175)
        
        # Activity level should be one of the discrete values
        self.assertIn(physical["activity_level"], ["low", "medium", "high"])
    
    def test_simulate_profile(self):
        """Test running multiple simulations and generating statistics"""
        # Run simulation with fewer iterations for speed
        result = simulate_profile(str(self.valid_example), iterations=10)
        
        # Check the structure of the result
        self.assertEqual(result["profile_name"], "Kai's Digital Twin")
        self.assertEqual(result["iterations"], 10)
        self.assertIn("archetypes", result)
        
        # Check archetypes
        archetypes = result["archetypes"]
        self.assertIn("Online Avatar", archetypes)
        self.assertIn("Physical Self", archetypes)
        
        # Check attributes and their statistics
        digital_attrs = archetypes["Online Avatar"]
        self.assertIn("username", digital_attrs)
        self.assertIn("fixed_value", digital_attrs["username"])
        
        # Screen time should have numeric statistics
        self.assertIn("screen_time", digital_attrs)
        screen_time_stats = digital_attrs["screen_time"]
        self.assertIn("mean", screen_time_stats)
        self.assertIn("median", screen_time_stats)
        self.assertIn("min", screen_time_stats)
        self.assertIn("max", screen_time_stats)
        self.assertIn("std_dev", screen_time_stats)
        
        # Activity level should have frequency statistics
        physical_attrs = archetypes["Physical Self"]
        self.assertIn("activity_level", physical_attrs)
        activity_stats = physical_attrs["activity_level"]
        self.assertIn("frequencies", activity_stats)
        
        # Check all possible values are represented in frequencies
        frequencies = activity_stats["frequencies"]
        for value in ["low", "medium", "high"]:
            self.assertIn(value, frequencies)


if __name__ == "__main__":
    unittest.main()
