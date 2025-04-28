"""
Simulation utilities for TanzoLang profiles.
"""

from typing import Dict, Any, List, Tuple, Optional
import random
import numpy as np
from dataclasses import dataclass

from tanzo_schema.models import TanzoProfile, Behavior


@dataclass
class SimulationMetric:
    """Represents a simulation metric with a name, value and description."""
    name: str
    value: float
    description: str


@dataclass
class SimulationResult:
    """Represents the result of a profile simulation."""
    profile_name: str
    metrics: List[SimulationMetric]
    summary: str
    iterations: int


def _sample_behavior_activation(
    behavior: Behavior, 
    simulation_params: Dict[str, Any]
) -> float:
    """
    Sample whether a behavior is activated based on its strength and context.
    
    Args:
        behavior (Behavior): The behavior to sample
        simulation_params (Dict[str, Any]): Simulation parameters
    
    Returns:
        float: Activation value between 0.0 and 1.0
    """
    base_strength = behavior.strength
    randomness = simulation_params.get("randomness", 0.3)
    
    # Add some noise based on randomness
    noise = random.uniform(-randomness, randomness)
    activation = base_strength + (noise * base_strength)
    
    # Clamp between 0.0 and 1.0
    return max(0.0, min(1.0, activation))


def _simulate_iteration(
    profile: TanzoProfile
) -> Dict[str, float]:
    """
    Run a single simulation iteration for a profile.
    
    Args:
        profile (TanzoProfile): The profile to simulate
    
    Returns:
        Dict[str, float]: A dictionary of metrics from the simulation
    """
    p = profile.profile
    metrics = {}
    
    # Get simulation parameters
    sim_params = {}
    if p.simulation and p.simulation.parameters:
        sim_params = p.simulation.parameters.model_dump()
    
    # Simulate behavior activations
    behavior_activations = []
    if p.behaviors:
        for behavior in p.behaviors:
            activation = _sample_behavior_activation(behavior, sim_params)
            behavior_activations.append(activation)
        
        if behavior_activations:
            metrics["mean_behavior_activation"] = np.mean(behavior_activations)
    
    # Simulate personality expression
    if p.personality and p.personality.traits:
        traits = p.personality.traits
        trait_dict = traits.model_dump()
        
        # Add some randomness to trait expression
        randomness = sim_params.get("randomness", 0.3)
        for trait, value in trait_dict.items():
            if value is not None:
                noise = random.uniform(-randomness, randomness)
                expressed_value = value + (noise * value)
                # Clamp between 0.0 and 1.0
                expressed_value = max(0.0, min(1.0, expressed_value))
                metrics[f"{trait}_expression"] = expressed_value
    
    # Simulate communication aspects
    if p.communication:
        comm = p.communication
        if comm.complexity is not None:
            randomness = sim_params.get("randomness", 0.3)
            noise = random.uniform(-randomness, randomness)
            metrics["expressed_complexity"] = max(0.0, min(1.0, comm.complexity + (noise * comm.complexity)))
        
        if comm.verbosity is not None:
            randomness = sim_params.get("randomness", 0.3)
            noise = random.uniform(-randomness, randomness)
            metrics["expressed_verbosity"] = max(0.0, min(1.0, comm.verbosity + (noise * comm.verbosity)))
    
    return metrics


def simulate_profile(
    profile: TanzoProfile, 
    iterations: int = 100
) -> SimulationResult:
    """
    Run a Monte Carlo simulation of a profile over multiple iterations.
    
    Args:
        profile (TanzoProfile): The profile to simulate
        iterations (int): Number of simulation iterations
    
    Returns:
        SimulationResult: The aggregated results of the simulation
    """
    p = profile.profile
    all_metrics: Dict[str, List[float]] = {}
    
    # Run simulations
    for _ in range(iterations):
        metrics = _simulate_iteration(profile)
        
        # Collect metrics
        for key, value in metrics.items():
            if key not in all_metrics:
                all_metrics[key] = []
            all_metrics[key].append(value)
    
    # Calculate summary metrics
    summary_metrics = []
    for key, values in all_metrics.items():
        mean_value = np.mean(values)
        std_dev = np.std(values)
        description = f"Mean: {mean_value:.2f}, StdDev: {std_dev:.2f}"
        
        summary_metrics.append(SimulationMetric(
            name=key,
            value=mean_value,
            description=description
        ))
    
    # Sort metrics by name
    summary_metrics.sort(key=lambda m: m.name)
    
    # Create summary text
    summary_lines = [
        f"Simulation Results for '{p.name}'",
        f"Ran {iterations} iterations",
        "",
        "Summary Metrics:",
    ]
    
    for metric in summary_metrics:
        summary_lines.append(f"- {metric.name}: {metric.value:.2f} ({metric.description})")
    
    summary = "\n".join(summary_lines)
    
    return SimulationResult(
        profile_name=p.name,
        metrics=summary_metrics,
        summary=summary,
        iterations=iterations
    )
