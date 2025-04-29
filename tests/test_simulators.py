"""
Tests for the simulation functionality in the Tanzo CLI.
"""

import random
import pytest
from cli.tanzo_cli import run_simulation
from clients.python.tanzo_schema import TanzoProfile, Archetype, TraitScore, Skill


@pytest.fixture
def simple_profile():
    """Return a simple TanzoProfile for simulation testing."""
    return TanzoProfile(
        version="0.1.0",
        profile_type="simulation",
        archetype=Archetype(
            name="Simulation Test",
            core_traits={
                "intelligence": TraitScore(base=7.0, range=(6.0, 8.0), distribution="normal"),
                "creativity": TraitScore(base=6.0, range=(5.0, 7.0), distribution="uniform"),
                "sociability": TraitScore(base=5.0, range=(4.0, 6.0)),
            },
            skills=[
                Skill(
                    name="Test Skill 1",
                    proficiency=TraitScore(base=8.0, range=(7.0, 9.0), distribution="normal")
                ),
                Skill(
                    name="Test Skill 2",
                    proficiency=TraitScore(base=6.0, range=(5.0, 7.0), distribution="uniform")
                )
            ]
        ),
        simulation_parameters={
            "variation_factor": 0.2,
            "seed": 12345,
            "iterations": 100,
            "environments": ["Test Environment 1", "Test Environment 2"]
        }
    )


def test_simulation_reproducibility(simple_profile):
    """Test that simulations with the same seed produce the same results."""
    # Set seed explicitly to ensure reproducibility
    simple_profile.simulation_parameters.seed = 12345
    
    # Run two simulations with the same configuration
    results1 = run_simulation(simple_profile, iterations=50)
    
    # Reset random seed to ensure it's not affecting the test
    random.seed(None)
    
    # Run second simulation with same seed
    simple_profile.simulation_parameters.seed = 12345
    results2 = run_simulation(simple_profile, iterations=50)
    
    # Compare results - should be identical
    for category in ["traits", "skills", "environments"]:
        for name, stats in results1[category].items():
            assert name in results2[category], f"{name} missing from second simulation results"
            for stat_name, value in stats.items():
                assert pytest.approx(value, abs=1e-10) == results2[category][name][stat_name], \
                    f"Value mismatch for {category}.{name}.{stat_name}"


def test_simulation_different_seeds(simple_profile):
    """Test that simulations with different seeds produce different results."""
    # First simulation with seed 12345
    simple_profile.simulation_parameters.seed = 12345
    results1 = run_simulation(simple_profile, iterations=50)
    
    # Reset random seed
    random.seed(None)
    
    # Second simulation with different seed
    simple_profile.simulation_parameters.seed = 54321
    results2 = run_simulation(simple_profile, iterations=50)
    
    # Check that at least some values are different
    different_values = False
    for category in ["traits", "skills", "environments"]:
        for name, stats in results1[category].items():
            for stat_name, value in stats.items():
                if abs(value - results2[category][name][stat_name]) > 1e-10:
                    different_values = True
                    break
            if different_values:
                break
        if different_values:
            break
    
    assert different_values, "Simulations with different seeds produced identical results"


def test_simulation_respects_distributions(simple_profile):
    """Test that simulations respect the specified distributions."""
    # Run a large number of iterations to get better statistical properties
    results = run_simulation(simple_profile, iterations=1000)
    
    # Normal distribution (intelligence) should have mean close to base value
    intel_mean = results["traits"]["intelligence"]["mean"]
    assert abs(intel_mean - 7.0) < 0.2, "Mean of normal distribution far from base value"
    
    # Uniform distribution (creativity) should have mean close to midpoint of range
    uniform_mean = results["traits"]["creativity"]["mean"]
    expected_mean = (5.0 + 7.0) / 2  # Midpoint of range
    assert abs(uniform_mean - expected_mean) < 0.2, "Mean of uniform distribution far from expected"


def test_simulation_respects_ranges(simple_profile):
    """Test that simulation values stay within specified ranges."""
    results = run_simulation(simple_profile, iterations=100)
    
    # Check all traits stay within their ranges
    assert results["traits"]["intelligence"]["min"] >= 6.0
    assert results["traits"]["intelligence"]["max"] <= 8.0
    
    assert results["traits"]["creativity"]["min"] >= 5.0
    assert results["traits"]["creativity"]["max"] <= 7.0
    
    assert results["traits"]["sociability"]["min"] >= 4.0
    assert results["traits"]["sociability"]["max"] <= 6.0
    
    # Check all skills stay within their ranges
    assert results["skills"]["Test Skill 1"]["min"] >= 7.0
    assert results["skills"]["Test Skill 1"]["max"] <= 9.0
    
    assert results["skills"]["Test Skill 2"]["min"] >= 5.0
    assert results["skills"]["Test Skill 2"]["max"] <= 7.0


def test_simulation_specific_environment(simple_profile):
    """Test simulation with a specific environment."""
    # Run simulation with specific environment
    env_name = "Test Environment 1"
    results = run_simulation(simple_profile, iterations=50, environment=env_name)
    
    # Should only include the specified environment
    assert len(results["environments"]) == 1
    assert env_name in results["environments"]
    
    # Environment should have expected statistics keys
    env_stats = results["environments"][env_name]
    assert "mean" in env_stats
    assert "median" in env_stats
    assert "min" in env_stats
    assert "max" in env_stats
    assert "stddev" in env_stats


def test_simulation_all_environments(simple_profile):
    """Test simulation with all environments."""
    # Run simulation with all environments
    results = run_simulation(simple_profile, iterations=50)
    
    # Should include all environments from the profile
    assert len(results["environments"]) == 2
    assert "Test Environment 1" in results["environments"]
    assert "Test Environment 2" in results["environments"]


def test_simulation_no_environments(simple_profile):
    """Test simulation with no specified environments."""
    # Remove environments from profile
    simple_profile.simulation_parameters.environments = None
    
    # Run simulation
    results = run_simulation(simple_profile, iterations=50)
    
    # Should include default environment
    assert len(results["environments"]) == 1
    assert "default" in results["environments"]


def test_simulation_variation_factor(simple_profile):
    """Test that variation factor affects simulation results."""
    # First simulation with low variation factor
    simple_profile.simulation_parameters.variation_factor = 0.1
    simple_profile.simulation_parameters.seed = 12345
    results_low = run_simulation(simple_profile, iterations=100)
    
    # Reset random seed
    random.seed(None)
    
    # Second simulation with high variation factor
    simple_profile.simulation_parameters.variation_factor = 0.4
    simple_profile.simulation_parameters.seed = 12345
    results_high = run_simulation(simple_profile, iterations=100)
    
    # High variation should typically result in higher standard deviations
    assert results_high["environments"]["Test Environment 1"]["stddev"] > \
           results_low["environments"]["Test Environment 1"]["stddev"], \
           "Higher variation factor did not increase standard deviation"
