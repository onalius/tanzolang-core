"""
Tests for the simulator module of the tanzo_schema package.
"""

import pytest
import numpy as np

from clients.python.tanzo_schema import run_simulation
from clients.python.tanzo_schema.models import Archetype, Profile, Trait, TanzoDocument


def test_run_simulation_file(example_file_path):
    """Test running a simulation from a file."""
    results = run_simulation(example_file_path, iterations=10)
    assert results.num_iterations == 10
    assert len(results.trait_means) > 0
    assert len(results.trait_std_devs) > 0
    assert len(results.archetype_weights) > 0


def test_run_simulation_document():
    """Test running a simulation from a document object."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="trait1",
                            value=0.5,
                            variance=0.1
                        ),
                        Trait(
                            name="trait2",
                            value=0.7,
                            variance=0.2
                        )
                    ]
                )
            ]
        )
    )
    
    results = run_simulation(document, iterations=50)
    assert results.num_iterations == 50
    assert "digital" in results.trait_means
    assert "trait1" in results.trait_means["digital"]
    assert "trait2" in results.trait_means["digital"]
    assert results.archetype_weights["digital"] == 0.8


def test_run_simulation_variance():
    """Test that simulation produces variance in trait values."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="high_variance",
                            value=0.5,
                            variance=0.3
                        ),
                        Trait(
                            name="low_variance",
                            value=0.5,
                            variance=0.01
                        )
                    ]
                )
            ]
        )
    )
    
    results = run_simulation(document, iterations=100)
    
    # High variance trait should have a higher standard deviation
    high_std_dev = results.trait_std_devs["digital"]["high_variance"]
    low_std_dev = results.trait_std_devs["digital"]["low_variance"]
    
    assert high_std_dev > low_std_dev
    assert high_std_dev > 0.05
    assert low_std_dev < 0.05


def test_run_simulation_str_representation():
    """Test that the simulation result can be converted to a string."""
    document = TanzoDocument(
        version="0.1.0",
        profile=Profile(
            name="Test Profile",
            archetypes=[
                Archetype(
                    type="digital",
                    weight=0.8,
                    traits=[
                        Trait(
                            name="trait1",
                            value=0.5,
                            variance=0.1
                        )
                    ]
                )
            ]
        )
    )
    
    results = run_simulation(document, iterations=10)
    result_str = str(results)
    
    assert "Simulation Results" in result_str
    assert "digital" in result_str
    assert "trait1" in result_str
    assert "Mean" in result_str
    assert "Std Dev" in result_str
