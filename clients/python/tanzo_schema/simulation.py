"""
Simulation functions for Tanzo profiles
"""

import random
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from tanzo_schema.models import TanzoProfile


class SimulationResult:
    """
    Class to hold the results of a profile simulation
    """
    
    def __init__(self, profile: TanzoProfile):
        """
        Initialize a new simulation result
        
        Args:
            profile: The profile being simulated
        """
        self.profile_name = profile.profile.name
        self.iterations = 0
        self.energy_values: List[float] = []
        self.resilience_values: List[float] = []
        self.adaptability_values: List[float] = []
        self.capability_activations: Dict[str, int] = {}
        
        # Initialize capability activations counter
        for capability in profile.properties.capabilities:
            self.capability_activations[capability.name] = 0
    
    def add_iteration(
        self, energy: float, resilience: float, adaptability: float, activated_capability: Optional[str]
    ) -> None:
        """
        Add the results of one simulation iteration
        
        Args:
            energy: The energy value for this iteration
            resilience: The resilience value for this iteration
            adaptability: The adaptability value for this iteration
            activated_capability: The name of any capability that was activated
        """
        self.iterations += 1
        self.energy_values.append(energy)
        self.resilience_values.append(resilience)
        self.adaptability_values.append(adaptability)
        
        if activated_capability:
            self.capability_activations[activated_capability] += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the simulation results
        
        Returns:
            Dict[str, Any]: A dictionary containing the simulation summary
        """
        return {
            "profile_name": self.profile_name,
            "iterations": self.iterations,
            "energy": {
                "min": min(self.energy_values),
                "max": max(self.energy_values),
                "mean": np.mean(self.energy_values),
                "std": np.std(self.energy_values),
            },
            "resilience": {
                "min": min(self.resilience_values),
                "max": max(self.resilience_values),
                "mean": np.mean(self.resilience_values),
                "std": np.std(self.resilience_values),
            },
            "adaptability": {
                "min": min(self.adaptability_values),
                "max": max(self.adaptability_values),
                "mean": np.mean(self.adaptability_values),
                "std": np.std(self.adaptability_values),
            },
            "capability_activations": self.capability_activations,
        }
    
    def __str__(self) -> str:
        """
        Get a string representation of the simulation results
        
        Returns:
            str: A formatted string summary
        """
        summary = self.get_summary()
        
        result = [
            f"Simulation Results for: {summary['profile_name']}",
            f"Total Iterations: {summary['iterations']}",
            "\nState Variables:",
            f"  Energy: min={summary['energy']['min']:.2f}, max={summary['energy']['max']:.2f}, "
            f"mean={summary['energy']['mean']:.2f}, std={summary['energy']['std']:.2f}",
            f"  Resilience: min={summary['resilience']['min']:.2f}, max={summary['resilience']['max']:.2f}, "
            f"mean={summary['resilience']['mean']:.2f}, std={summary['resilience']['std']:.2f}",
            f"  Adaptability: min={summary['adaptability']['min']:.2f}, max={summary['adaptability']['max']:.2f}, "
            f"mean={summary['adaptability']['mean']:.2f}, std={summary['adaptability']['std']:.2f}",
            "\nCapability Activations:",
        ]
        
        for capability, count in summary["capability_activations"].items():
            percentage = 0
            if summary["iterations"] > 0:
                percentage = (count / summary["iterations"]) * 100
            result.append(f"  {capability}: {count} times ({percentage:.1f}%)")
        
        return "\n".join(result)


def _apply_variance(base_value: float, variance: Optional[float]) -> float:
    """
    Apply random variance to a base value
    
    Args:
        base_value: The base value
        variance: The maximum variance to apply
        
    Returns:
        float: The value after applying variance
    """
    if variance is None or variance <= 0:
        return base_value
    
    actual_variance = random.uniform(-variance, variance)
    result = base_value + actual_variance
    
    # Ensure the result is within valid range (0-100)
    return max(0.0, min(100.0, result))


def _should_activate_capability(capability_power: float) -> bool:
    """
    Determine if a capability should be activated based on its power
    
    Args:
        capability_power: The power level of the capability (1-10)
        
    Returns:
        bool: Whether the capability should be activated
    """
    # Convert power (1-10) to a probability (0.1-1.0)
    activation_probability = capability_power / 10.0
    return random.random() < activation_probability


def simulate_profile(profile: TanzoProfile, iterations: int = 100) -> SimulationResult:
    """
    Run a Monte Carlo simulation of a Tanzo profile
    
    Args:
        profile: The profile to simulate
        iterations: The number of iterations to simulate
        
    Returns:
        SimulationResult: The simulation results
    """
    result = SimulationResult(profile)
    
    for _ in range(iterations):
        # Get base values
        base_energy = profile.properties.state.baseline.energy
        base_resilience = profile.properties.state.baseline.resilience
        base_adaptability = profile.properties.state.baseline.adaptability
        
        # Get variance values
        energy_variance = getattr(profile.properties.state.variance, 'energy', None) if profile.properties.state.variance else None
        resilience_variance = getattr(profile.properties.state.variance, 'resilience', None) if profile.properties.state.variance else None
        adaptability_variance = getattr(profile.properties.state.variance, 'adaptability', None) if profile.properties.state.variance else None
        
        # Apply variance
        energy = _apply_variance(base_energy, energy_variance)
        resilience = _apply_variance(base_resilience, resilience_variance)
        adaptability = _apply_variance(base_adaptability, adaptability_variance)
        
        # Simulate capability activation
        activated_capability = None
        for capability in profile.properties.capabilities:
            if _should_activate_capability(capability.power):
                activated_capability = capability.name
                break
        
        # Record this iteration
        result.add_iteration(energy, resilience, adaptability, activated_capability)
    
    return result
