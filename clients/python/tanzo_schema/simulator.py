"""
Simulation utilities for TanzoLang profiles
"""

import random
from typing import Dict, Any, List, Union, Optional, Tuple
import numpy as np

from clients.python.tanzo_schema.models import (
    TanzoProfile,
    Attribute,
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
    AttributeValue,
    ZodiacTypology,
    KabbalahTypology,
    PurposeQuadrantTypology,
)
from clients.python.tanzo_schema.validator import validate_profile


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


def extract_typologies(profile: TanzoProfile) -> Dict[str, Dict[str, Any]]:
    """
    Extract typology information from a profile
    
    Args:
        profile: The profile containing typologies
        
    Returns:
        Dict[str, Dict[str, Any]]: Typology data organized by system
    """
    result = {}
    
    # Skip if typologies aren't present
    if not hasattr(profile.profile, 'typologies') or profile.profile.typologies is None:
        return result
    
    typologies = profile.profile.typologies
    
    # Extract zodiac typology if present
    if hasattr(typologies, 'zodiac') and typologies.zodiac:
        result['zodiac'] = {
            'sun': typologies.zodiac.sun,
            'moon': typologies.zodiac.moon,
            'rising': typologies.zodiac.rising
        }
    
    # Extract kabbalah typology if present
    if hasattr(typologies, 'kabbalah') and typologies.kabbalah:
        result['kabbalah'] = {
            'primary_sefira': typologies.kabbalah.primary_sefira,
            'secondary_sefira': typologies.kabbalah.secondary_sefira,
            'path': typologies.kabbalah.path
        }
    
    # Extract purpose quadrant typology if present
    if hasattr(typologies, 'purpose_quadrant') and typologies.purpose_quadrant:
        result['purpose_quadrant'] = {
            'passion': typologies.purpose_quadrant.passion,
            'expertise': typologies.purpose_quadrant.expertise,
            'contribution': typologies.purpose_quadrant.contribution,
            'sustainability': typologies.purpose_quadrant.sustainability
        }
    
    # Extract any custom typologies
    for name, typology in typologies.__dict__.items():
        if name not in ['zodiac', 'kabbalah', 'purpose_quadrant'] and typology is not None:
            custom_typology = {}
            for key, value in typology.__dict__.items():
                if value is not None:
                    custom_typology[key] = value
            
            if custom_typology:  # Only add if not empty
                result[name] = custom_typology
    
    return result


def simulate_profile_once(profile: TanzoProfile) -> Dict[str, Dict[str, Any]]:
    """
    Perform a single simulation of a TanzoLang profile
    
    Args:
        profile: The profile to simulate
        
    Returns:
        Dict[str, Dict[str, Any]]: Simulated values for each archetype and attribute
    """
    result = {}
    
    # Simulate archetypes and their attributes
    for archetype in profile.profile.archetypes:
        archetype_name = archetype.name or archetype.type.value
        archetype_result = {}
        
        for attribute in archetype.attributes:
            name, value = simulate_attribute(attribute)
            archetype_result[name] = value
        
        result[archetype_name] = archetype_result
    
    # Extract typologies (no simulation needed as they're not probabilistic)
    typologies = extract_typologies(profile)
    if typologies:
        result['typologies'] = typologies
    
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
    
    # Add typologies if present (these don't need statistics as they're deterministic)
    typologies = extract_typologies(profile)
    if typologies:
        summary["typologies"] = typologies
    
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
