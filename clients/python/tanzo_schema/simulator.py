"""
Simulator module for TanzoLang profiles.

This module provides functions to simulate variability in TanzoLang profiles
through Monte-Carlo methods, generating variations of traits and attributes
based on their defined variance.
"""

import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np

from tanzo_schema.models import TanzoProfile
from tanzo_schema.validator import load_profile


def _simulate_value(
    base_value: int, 
    variance: Optional[int] = None, 
    global_variance_factor: float = 0.2,
    min_value: int = 0,
    max_value: int = 100
) -> int:
    """
    Simulate a value with random variation.
    
    Args:
        base_value (int): The base value to simulate around.
        variance (Optional[int], optional): The specific variance for this value. Defaults to None.
        global_variance_factor (float, optional): A global factor for variance. Defaults to 0.2.
        min_value (int, optional): Minimum allowed value. Defaults to 0.
        max_value (int, optional): Maximum allowed value. Defaults to 100.
        
    Returns:
        int: The simulated value.
    """
    # If a specific variance is provided, use it, otherwise use the global factor
    if variance is not None:
        std_dev = variance
    else:
        # Calculate standard deviation as a percentage of the range
        std_dev = (max_value - min_value) * global_variance_factor
    
    # Generate a random value using a normal distribution
    value = int(np.random.normal(base_value, std_dev))
    
    # Ensure the value stays within bounds
    return max(min_value, min(value, max_value))


def _simulate_trait(trait_data: Dict[str, Any], global_variance: float) -> Dict[str, Any]:
    """
    Simulate a trait with random variation.
    
    Args:
        trait_data (Dict[str, Any]): The trait data.
        global_variance (float): Global variance factor.
        
    Returns:
        Dict[str, Any]: The simulated trait data.
    """
    base_value = trait_data["value"]
    variance = trait_data.get("variance")
    
    simulated_value = _simulate_value(base_value, variance, global_variance)
    
    # Create a copy of the trait with the simulated value
    simulated_trait = trait_data.copy()
    simulated_trait["value"] = simulated_value
    simulated_trait["simulated"] = True
    
    return simulated_trait


def _simulate_attribute(attr_data: Dict[str, Any], global_variance: float) -> Dict[str, Any]:
    """
    Simulate an attribute with random variation, similar to trait simulation.
    
    Args:
        attr_data (Dict[str, Any]): The attribute data.
        global_variance (float): Global variance factor.
        
    Returns:
        Dict[str, Any]: The simulated attribute data.
    """
    # Attributes follow the same simulation logic as traits
    return _simulate_trait(attr_data, global_variance)


def _deep_copy_with_simulation(
    data: Any, global_variance: float, current_path: str = ""
) -> Any:
    """
    Deep copy a data structure, simulating traits and attributes.
    
    Args:
        data (Any): The data to copy and simulate.
        global_variance (float): Global variance factor.
        current_path (str, optional): Current path in the data structure. Defaults to "".
        
    Returns:
        Any: The simulated data structure.
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            path = f"{current_path}.{key}" if current_path else key
            
            # Special handling for traits and attributes
            if (path.endswith("openness") or path.endswith("conscientiousness") or
                path.endswith("extraversion") or path.endswith("agreeableness") or
                path.endswith("neuroticism") or "cognitive_style" in path or
                "communication_style" in path or "social" in path or 
                "problem_solving" in path) and isinstance(value, dict) and "value" in value:
                
                # This is a trait or attribute
                if "digital_archetype.traits" in path:
                    result[key] = _simulate_trait(value, global_variance)
                else:
                    result[key] = _simulate_attribute(value, global_variance)
            else:
                # Regular recursive copy
                result[key] = _deep_copy_with_simulation(value, global_variance, path)
        return result
    elif isinstance(data, list):
        return [_deep_copy_with_simulation(item, global_variance, current_path) for item in data]
    else:
        # Return primitive values as-is
        return data


def simulate_single_profile(profile_data: Dict[str, Any], global_variance: Optional[float] = None) -> Dict[str, Any]:
    """
    Simulate a single profile with random variations.
    
    Args:
        profile_data (Dict[str, Any]): The profile data.
        global_variance (Optional[float], optional): Global variance factor. Defaults to None.
        
    Returns:
        Dict[str, Any]: The simulated profile.
    """
    # If no global variance is provided, try to get it from the profile
    if global_variance is None:
        global_variance = profile_data.get("simulation_parameters", {}).get("variance", 0.2)
    
    # Create a deep copy with simulated values
    simulated_profile = _deep_copy_with_simulation(profile_data, global_variance)
    
    # Add simulation metadata
    if "metadata" in simulated_profile:
        simulated_profile["metadata"]["simulated"] = True
    
    return simulated_profile


def simulate_profile(
    profile_path: Union[str, Path], 
    iterations: int = 100,
    global_variance: Optional[float] = None
) -> List[Dict[str, Any]]:
    """
    Simulate a profile multiple times with Monte-Carlo variations.
    
    Args:
        profile_path (Union[str, Path]): Path to the profile file.
        iterations (int, optional): Number of simulation iterations. Defaults to 100.
        global_variance (Optional[float], optional): Global variance factor. Defaults to None.
        
    Returns:
        List[Dict[str, Any]]: List of simulated profiles.
        
    Raises:
        ValueError: If the file format is not supported or file doesn't exist.
    """
    profile_data = load_profile(profile_path)
    
    # Set random seed for reproducibility
    random.seed()
    np.random.seed()
    
    # Run simulations
    simulations = []
    for _ in range(iterations):
        sim = simulate_single_profile(profile_data, global_variance)
        simulations.append(sim)
    
    return simulations


def summarize_simulations(simulations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a statistical summary of simulations.
    
    Args:
        simulations (List[Dict[str, Any]]): List of simulated profiles.
        
    Returns:
        Dict[str, Any]: Statistical summary with mean, median, std_dev, min, max for each trait/attribute.
    """
    if not simulations:
        return {}
    
    # Structure to hold extracted values for each trait and attribute
    values = {}
    
    # Extract all trait values
    for sim in simulations:
        traits = sim.get("digital_archetype", {}).get("traits", {})
        for trait_name, trait_data in traits.items():
            if trait_name not in values:
                values[trait_name] = []
            values[trait_name].append(trait_data.get("value", 0))
        
        # Extract attribute values (nested structure, so we need a more complex approach)
        attributes = sim.get("digital_archetype", {}).get("attributes", {})
        for attr_category, attr_group in attributes.items():
            if isinstance(attr_group, dict):
                for attr_name, attr_data in attr_group.items():
                    if isinstance(attr_data, dict) and "value" in attr_data:
                        attr_key = f"{attr_category}.{attr_name}"
                        if attr_key not in values:
                            values[attr_key] = []
                        values[attr_key].append(attr_data.get("value", 0))
        
        # Extract behavior values
        behaviors = sim.get("digital_archetype", {}).get("behaviors", {})
        for behavior_category, behavior_group in behaviors.items() if behaviors else {}:
            if isinstance(behavior_group, dict):
                for behavior_name, behavior_data in behavior_group.items():
                    if isinstance(behavior_data, dict) and "value" in behavior_data:
                        behavior_key = f"behaviors.{behavior_category}.{behavior_name}"
                        if behavior_key not in values:
                            values[behavior_key] = []
                        values[behavior_key].append(behavior_data.get("value", 0))
    
    # Calculate statistics for each extracted value
    stats = {}
    for key, val_list in values.items():
        if val_list:
            stats[key] = {
                "mean": float(np.mean(val_list)),
                "median": float(np.median(val_list)),
                "std_dev": float(np.std(val_list)),
                "min": float(np.min(val_list)),
                "max": float(np.max(val_list)),
                "samples": len(val_list)
            }
    
    return stats
