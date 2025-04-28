"""
Simulator for Tanzo profiles.
"""

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np

from .models import (Archetype, Attribute, ComparisonOperator, Effect, Modifier,
                     OperationType, TanzoProfile)


@dataclass
class SimulationState:
    """State tracked during a simulation run."""
    archetype_values: Dict[str, float]
    attribute_values: Dict[str, float]
    active_modifiers: List[Modifier]


def _apply_effect(
    effect: Effect, 
    state: SimulationState, 
    archetypes_by_name: Dict[str, Archetype]
) -> None:
    """Apply a modifier effect to the simulation state."""
    # Check if condition is met (if any)
    if effect.condition:
        attr_name = effect.condition.attribute
        if attr_name not in state.attribute_values:
            return  # Attribute not found, can't apply condition
        
        attr_val = state.attribute_values[attr_name]
        cond_val = effect.condition.value
        
        # Evaluate the condition
        if effect.condition.operator == ComparisonOperator.EQ and attr_val != cond_val:
            return
        elif effect.condition.operator == ComparisonOperator.NEQ and attr_val == cond_val:
            return
        elif effect.condition.operator == ComparisonOperator.GT and attr_val <= cond_val:
            return
        elif effect.condition.operator == ComparisonOperator.LT and attr_val >= cond_val:
            return
        elif effect.condition.operator == ComparisonOperator.GTE and attr_val < cond_val:
            return
        elif effect.condition.operator == ComparisonOperator.LTE and attr_val > cond_val:
            return
    
    # Apply the effect
    target = effect.target
    value = effect.value
    
    # Check if target is an archetype
    if target in archetypes_by_name:
        current = state.archetype_values.get(target, 0.0)
        if effect.operation == OperationType.ADD:
            new_val = current + value
        elif effect.operation == OperationType.MULTIPLY:
            new_val = current * value
        elif effect.operation == OperationType.SET:
            new_val = value
        elif effect.operation == OperationType.MIN:
            new_val = min(current, value)
        elif effect.operation == OperationType.MAX:
            new_val = max(current, value)
        else:
            raise ValueError(f"Unknown operation type: {effect.operation}")
        
        # Clamp value to [0, 1]
        state.archetype_values[target] = max(0.0, min(1.0, new_val))
    
    # Otherwise assume it's an attribute
    elif target in state.attribute_values:
        current = state.attribute_values[target]
        if effect.operation == OperationType.ADD:
            new_val = current + value
        elif effect.operation == OperationType.MULTIPLY:
            new_val = current * value
        elif effect.operation == OperationType.SET:
            new_val = value
        elif effect.operation == OperationType.MIN:
            new_val = min(current, value)
        elif effect.operation == OperationType.MAX:
            new_val = max(current, value)
        else:
            raise ValueError(f"Unknown operation type: {effect.operation}")
        
        # Clamp value to [0, 1]
        state.attribute_values[target] = max(0.0, min(1.0, new_val))


def simulate_profile(
    profile: TanzoProfile, 
    randomize: bool = False, 
    seed: Optional[int] = None
) -> Dict[str, float]:
    """
    Simulate a single run of a Tanzo profile.
    
    Args:
        profile: TanzoProfile to simulate
        randomize: If True, apply random variance to attributes
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary of attribute and archetype values
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Initialize state
    state = SimulationState(
        archetype_values={},
        attribute_values={},
        active_modifiers=[]
    )
    
    # Get all archetypes by name for easy lookup
    archetypes_by_name = profile.archetypes_by_name
    
    # Initialize attribute values
    for archetype in profile.profile.archetypes:
        # Store base archetype value from weight
        state.archetype_values[archetype.name] = archetype.weight
        
        if archetype.attributes:
            for attr in archetype.attributes:
                # Apply variance if randomize is enabled
                value = attr.value
                if randomize and attr.variance:
                    # Use normal distribution centered on value with variance as std dev
                    variance = attr.variance
                    value = np.random.normal(value, variance)
                    # Clamp to [0, 1]
                    value = max(0.0, min(1.0, value))
                
                state.attribute_values[attr.name] = value
    
    # Apply global modifiers
    if profile.profile.modifiers:
        for modifier in profile.profile.modifiers:
            _apply_effect(modifier.effect, state, archetypes_by_name)
            state.active_modifiers.append(modifier)
    
    # Apply archetype-specific modifiers
    for archetype in profile.profile.archetypes:
        if archetype.modifiers:
            for modifier in archetype.modifiers:
                _apply_effect(modifier.effect, state, archetypes_by_name)
                state.active_modifiers.append(modifier)
    
    # Merge results
    result = {**state.attribute_values, **state.archetype_values}
    return result


def run_monte_carlo(
    profile: TanzoProfile,
    iterations: int = 100
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Run a Monte Carlo simulation with many iterations.
    
    Args:
        profile: TanzoProfile to simulate
        iterations: Number of simulation iterations
        
    Returns:
        Tuple of (means, standard deviations) for attributes and archetypes
    """
    # Track results across iterations
    results = []
    
    for i in range(iterations):
        # Use a different seed for each iteration for reproducibility
        sim_result = simulate_profile(profile, randomize=True, seed=i)
        results.append(sim_result)
    
    # Calculate statistics
    all_keys = set()
    for result in results:
        all_keys.update(result.keys())
    
    means = {}
    stdevs = {}
    
    for key in all_keys:
        values = [r.get(key, 0.0) for r in results]
        means[key] = sum(values) / len(values)
        
        # Calculate standard deviation
        variance = sum((x - means[key])**2 for x in values) / len(values)
        stdevs[key] = math.sqrt(variance)
    
    return means, stdevs
