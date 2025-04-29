"""
Simulation utilities for TanzoLang profiles
"""

import random
from typing import Dict, Any, List, Union, Optional, Tuple
import numpy as np

from tanzo_schema.models import (
    TanzoProfile,
    Attribute,
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
    AttributeValue,
)
from tanzo_schema.validator import validate_profile


def sample_distribution(distribution: Union[NormalDistribution, UniformDistribution, DiscreteDistribution]) -> Any:
    """
    Sample a value from a probability distribution
    
    Args:
        distribution: A probability distribution model
        
    Returns:
        Any: A sampled value from the distribution
    """
    if isinstance(distribution, NormalDistribution):
        return np.random.normal(distribution.mean, distribution.stdDev)
    
    elif isinstance(distribution, UniformDistribution):
        return np.random.uniform(distribution.min, distribution.max)
    
    elif isinstance(distribution, DiscreteDistribution):
        # Normalize weights to ensure they sum to 1
        weights = np.array(distribution.weights)
        weights = weights / np.sum(weights)
        
        # Sample based on weights
        return np.random.choice(distribution.values, p=weights)
    
    else:
        raise ValueError(f"Unknown distribution type: {type(distribution)}")


def simulate_attribute(attribute: Attribute) -> Tuple[str, Any]:
    """
    Simulate a value for an attribute, sampling from its distribution if needed
    
    Args:
        attribute: The attribute to simulate
        
    Returns:
        Tuple[str, Any]: The attribute name and simulated value
    """
    value = attribute.value
    
    # If the value is a distribution, sample from it
    if isinstance(value, (NormalDistribution, UniformDistribution, DiscreteDistribution)):
        simulated_value = sample_distribution(value)
    else:
        # Use the fixed value as is
        simulated_value = value
    
    return attribute.name, simulated_value


def simulate_profile_once(profile: TanzoProfile) -> Dict[str, Dict[str, Any]]:
    """
    Perform a single simulation of a TanzoLang profile
    
    Args:
        profile: The profile to simulate
        
    Returns:
        Dict[str, Dict[str, Any]]: Simulated values for each archetype and attribute
    """
    result = {}
    
    for archetype in profile.profile.archetypes:
        archetype_name = archetype.name or archetype.type.value
        archetype_result = {}
        
        for attribute in archetype.attributes:
            name, value = simulate_attribute(attribute)
            archetype_result[name] = value
        
        result[archetype_name] = archetype_result
    
    return result


def simulate_profile(profile_path: str, iterations: int = 100) -> Dict[str, Any]:
    """
    Perform multiple simulations of a TanzoLang profile
    
    Args:
        profile_path: Path to the profile file
        iterations: Number of simulation iterations to run
        
    Returns:
        Dict[str, Any]: Summary statistics for the simulations
    """
    # Validate the profile first
    profile = validate_profile(profile_path)
    
    # Run simulations
    all_results = [simulate_profile_once(profile) for _ in range(iterations)]
    
    # Prepare summary statistics
    summary = {
        "profile_name": profile.profile.name,
        "iterations": iterations,
        "archetypes": {}
    }
    
    # For each archetype
    for archetype in profile.profile.archetypes:
        archetype_name = archetype.name or archetype.type.value
        attribute_stats = {}
        
        # For each attribute
        for attribute in archetype.attributes:
            attr_name = attribute.name
            
            # Check if the attribute has a distribution (needs statistics)
            if isinstance(attribute.value, (NormalDistribution, UniformDistribution, DiscreteDistribution)):
                # Collect all simulated values for this attribute
                values = [result[archetype_name][attr_name] for result in all_results]
                
                # Calculate statistics based on type
                if all(isinstance(v, (int, float)) for v in values):
                    # Numeric statistics
                    stats = {
                        "mean": np.mean(values),
                        "median": np.median(values),
                        "min": np.min(values),
                        "max": np.max(values),
                        "std_dev": np.std(values)
                    }
                else:
                    # Categorical statistics (frequencies)
                    unique_values = set(values)
                    frequencies = {str(val): values.count(val) / len(values) for val in unique_values}
                    stats = {"frequencies": frequencies}
                
                attribute_stats[attr_name] = stats
            else:
                # Fixed value, no statistics needed
                attribute_stats[attr_name] = {"fixed_value": attribute.value}
        
        summary["archetypes"][archetype_name] = attribute_stats
    
    return summary
