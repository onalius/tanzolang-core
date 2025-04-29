"""
Simulation functions for TanzoLang profiles.

This module provides functions to simulate and analyze TanzoLang
profiles through Monte Carlo methods and other techniques.
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple

import numpy as np

from tanzo_schema.models import TanzoProfile, Trait


@dataclass
class SimulationResult:
    """Results from a profile simulation."""
    
    profile_name: str
    num_iterations: int
    trait_means: Dict[str, float]
    trait_stddevs: Dict[str, float]
    trait_ranges: Dict[str, Tuple[float, float]]
    
    def summary(self) -> str:
        """
        Generate a human-readable summary of the simulation results.
        
        Returns:
            str: A formatted summary string
        """
        lines = [
            f"Simulation Results for '{self.profile_name}'",
            f"Number of iterations: {self.num_iterations}",
            "",
            "Traits:",
        ]
        
        # Sort traits by mean value (descending)
        sorted_traits = sorted(
            self.trait_means.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for trait_name, mean_value in sorted_traits:
            stddev = self.trait_stddevs[trait_name]
            min_val, max_val = self.trait_ranges[trait_name]
            
            lines.append(
                f"  {trait_name}:"
                f" mean={mean_value:.2f},"
                f" stddev={stddev:.2f},"
                f" range=[{min_val:.2f}, {max_val:.2f}]"
            )
        
        return "\n".join(lines)


def simulate_trait(trait: Trait, num_iterations: int = 100) -> List[float]:
    """
    Simulate a trait's value over multiple iterations.
    
    Args:
        trait: The trait to simulate
        num_iterations: Number of simulation iterations
        
    Returns:
        List[float]: List of simulated values
    """
    mean = trait.value
    stddev = trait.variance
    
    # Generate values from a normal distribution, truncated to [0, 1]
    values = []
    for _ in range(num_iterations):
        value = random.normalvariate(mean, stddev)
        # Truncate to valid range
        value = max(0.0, min(1.0, value))
        values.append(value)
    
    return values


def simulate_profile(
    profile: TanzoProfile, 
    num_iterations: int = 100,
    seed: Optional[int] = None
) -> SimulationResult:
    """
    Perform a Monte Carlo simulation of a TanzoLang profile.
    
    This simulates the profile by varying traits according to their
    variance values over multiple iterations.
    
    Args:
        profile: The profile to simulate
        num_iterations: Number of simulation iterations
        seed: Optional random seed for reproducibility
        
    Returns:
        SimulationResult: Results of the simulation
    """
    if seed is not None:
        random.seed(seed)
    
    archetype = profile.digital_archetype
    traits = archetype.traits
    
    # Run simulations for each trait
    simulated_traits: Dict[str, List[float]] = {}
    for trait_name, trait in traits.items():
        simulated_traits[trait_name] = simulate_trait(trait, num_iterations)
    
    # Calculate statistics
    trait_means: Dict[str, float] = {}
    trait_stddevs: Dict[str, float] = {}
    trait_ranges: Dict[str, Tuple[float, float]] = {}
    
    for trait_name, values in simulated_traits.items():
        trait_means[trait_name] = sum(values) / len(values)
        # Calculate standard deviation
        variance = sum((x - trait_means[trait_name]) ** 2 for x in values) / len(values)
        trait_stddevs[trait_name] = variance ** 0.5
        trait_ranges[trait_name] = (min(values), max(values))
    
    return SimulationResult(
        profile_name=profile.profile.name,
        num_iterations=num_iterations,
        trait_means=trait_means,
        trait_stddevs=trait_stddevs,
        trait_ranges=trait_ranges
    )
