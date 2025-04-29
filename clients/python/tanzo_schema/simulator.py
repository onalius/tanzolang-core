"""
Simulator module for TanzoLang profiles.

This module provides functions to run Monte Carlo simulations on TanzoLang
profiles, generating variations based on trait variance.
"""

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

from tanzo_schema.models import Archetype, TanzoDocument, Trait
from tanzo_schema.validator import validate_and_parse


@dataclass
class SimulationResult:
    """Results from a Monte Carlo simulation on a TanzoLang profile."""
    
    trait_means: Dict[str, Dict[str, float]]
    trait_std_devs: Dict[str, Dict[str, float]]
    archetype_weights: Dict[str, float]
    num_iterations: int
    
    def __str__(self) -> str:
        """Generate a human-readable representation of the simulation results."""
        lines = [
            f"Simulation Results ({self.num_iterations} iterations):",
            "=" * 50,
            "Archetype Weights:",
        ]
        
        for archetype, weight in self.archetype_weights.items():
            lines.append(f"  {archetype}: {weight:.2f}")
        
        lines.append("\nTrait Statistics by Archetype:")
        lines.append("=" * 50)
        
        for archetype, traits in self.trait_means.items():
            lines.append(f"\n{archetype}:")
            for trait_name, mean_val in traits.items():
                std_dev = self.trait_std_devs[archetype][trait_name]
                lines.append(f"  {trait_name}:")
                lines.append(f"    Mean: {mean_val:.2f}")
                lines.append(f"    Std Dev: {std_dev:.2f}")
                lines.append(f"    Range: [{max(0.0, mean_val - std_dev):.2f} - {min(1.0, mean_val + std_dev):.2f}]")
        
        return "\n".join(lines)


def _simulate_trait(trait: Trait) -> float:
    """Simulate a trait value based on its base value and variance."""
    # Generate a value from a normal distribution centered at the trait value
    # with standard deviation equal to the trait variance
    value = np.random.normal(trait.value, trait.variance)
    
    # Clamp the value to the range [0, 1]
    return max(0.0, min(1.0, value))


def _simulate_archetype(archetype: Archetype) -> Archetype:
    """Simulate an archetype by varying its traits."""
    result = copy.deepcopy(archetype)
    
    if result.traits:
        for i, trait in enumerate(result.traits):
            result.traits[i].value = _simulate_trait(trait)
    
    return result


def run_simulation(
    document: Union[str, Path, Dict[str, Any], TanzoDocument],
    iterations: int = 100
) -> SimulationResult:
    """
    Run a Monte Carlo simulation on a TanzoLang profile.
    
    Args:
        document: The document to simulate. Can be a file path, a dictionary,
                 or a TanzoDocument instance.
        iterations: The number of simulation iterations to run.
    
    Returns:
        A SimulationResult containing statistics from the simulation.
    """
    # Parse the document if needed
    if not isinstance(document, TanzoDocument):
        document = validate_and_parse(document)
    
    # Initialize result structures
    trait_values: Dict[str, Dict[str, List[float]]] = {}
    archetype_types: Set[str] = set()
    
    # Run the simulation
    for _ in range(iterations):
        # Create a new profile for this iteration
        profile = copy.deepcopy(document.profile)
        
        for archetype in profile.archetypes:
            archetype_type = archetype.type
            archetype_types.add(archetype_type)
            
            # Simulate the archetype
            simulated = _simulate_archetype(archetype)
            
            # Record trait values
            if simulated.traits:
                if archetype_type not in trait_values:
                    trait_values[archetype_type] = {}
                
                for trait in simulated.traits:
                    if trait.name not in trait_values[archetype_type]:
                        trait_values[archetype_type][trait.name] = []
                    
                    trait_values[archetype_type][trait.name].append(trait.value)
    
    # Calculate statistics
    trait_means: Dict[str, Dict[str, float]] = {}
    trait_std_devs: Dict[str, Dict[str, float]] = {}
    archetype_weights: Dict[str, float] = {}
    
    # Get original archetype weights
    for archetype in document.profile.archetypes:
        archetype_weights[archetype.type] = archetype.weight
    
    # Calculate means and standard deviations
    for archetype_type, traits in trait_values.items():
        trait_means[archetype_type] = {}
        trait_std_devs[archetype_type] = {}
        
        for trait_name, values in traits.items():
            trait_means[archetype_type][trait_name] = np.mean(values)
            trait_std_devs[archetype_type][trait_name] = np.std(values)
    
    return SimulationResult(
        trait_means=trait_means,
        trait_std_devs=trait_std_devs,
        archetype_weights=archetype_weights,
        num_iterations=iterations
    )
