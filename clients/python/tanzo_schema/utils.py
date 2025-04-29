"""Utility functions for working with TanzoLang profiles."""

import random
from typing import Dict, Any, List, Optional, Union
import statistics
from pathlib import Path

from tanzo_schema.models import TanzoProfile
from tanzo_schema.validators import load_profile_from_file


def export_profile(profile: Union[TanzoProfile, str, Path]) -> str:
    """
    Export a profile to a shorthand string representation.
    
    Args:
        profile: TanzoProfile instance or path to profile file
        
    Returns:
        A shorthand string representation of the profile
    """
    # Load profile if string or Path is provided
    if isinstance(profile, (str, Path)):
        profile = load_profile_from_file(profile)
    
    # Extract key components for the shorthand
    personality = profile.digital_archetype.personality_traits
    
    # Format: Name(O{openness}C{conscientiousness}E{extraversion}A{agreeableness}N{neuroticism})
    # Example: "Kai(O8C9E6A9N2)" - Kai with openness 0.8, conscientiousness 0.9, etc.
    shorthand = f"{profile.digital_archetype.identity.name}("
    shorthand += f"O{int(personality.openness * 10)}"
    shorthand += f"C{int(personality.conscientiousness * 10)}"
    shorthand += f"E{int(personality.extraversion * 10)}"
    shorthand += f"A{int(personality.agreeableness * 10)}"
    shorthand += f"N{int(personality.neuroticism * 10)}"
    shorthand += ")"
    
    return shorthand


def _random_variant(value: float, variance: float = 0.1) -> float:
    """
    Generate a random variant of a value within a specified variance.
    
    Args:
        value: Base value
        variance: Maximum variance as a fraction of the base value
        
    Returns:
        Random variant within the specified range
    """
    # Calculate the amount to vary by (up to variance in either direction)
    variation = random.uniform(-variance, variance)
    
    # Apply the variation
    result = value + variation
    
    # Ensure the result is within [0, 1]
    return max(0.0, min(1.0, result))


def simulate_profile(
    profile: Union[TanzoProfile, str, Path], 
    iterations: int = 100,
    variance: float = 0.1
) -> Dict[str, Any]:
    """
    Run a Monte Carlo simulation of a profile with variations.
    
    Args:
        profile: TanzoProfile instance or path to profile file
        iterations: Number of simulation iterations
        variance: Maximum variance as a fraction of the base values
        
    Returns:
        Dictionary containing simulation results
    """
    # Load profile if string or Path is provided
    if isinstance(profile, (str, Path)):
        profile = load_profile_from_file(profile)
    
    # Initialize simulation results
    results: Dict[str, List[float]] = {
        "openness": [],
        "conscientiousness": [],
        "extraversion": [],
        "agreeableness": [],
        "neuroticism": [],
    }
    
    # Optional metrics if available in the profile
    optional_metrics = [
        "problem_solving", "creativity", "memory", "learning", "spatial_awareness",
        "verbosity", "formality", "humor", "empathy", "assertiveness"
    ]
    
    for metric in optional_metrics:
        # Initialize lists for metrics that exist in the profile
        if (hasattr(profile.digital_archetype, "cognitive_abilities") and 
            profile.digital_archetype.cognitive_abilities and
            hasattr(profile.digital_archetype.cognitive_abilities, metric)):
            results[metric] = []
        elif (hasattr(profile.digital_archetype, "communication_style") and 
              profile.digital_archetype.communication_style and
              hasattr(profile.digital_archetype.communication_style, metric)):
            results[metric] = []
    
    # Run iterations
    for _ in range(iterations):
        # Personality traits (required)
        personality = profile.digital_archetype.personality_traits
        results["openness"].append(_random_variant(personality.openness, variance))
        results["conscientiousness"].append(_random_variant(personality.conscientiousness, variance))
        results["extraversion"].append(_random_variant(personality.extraversion, variance))
        results["agreeableness"].append(_random_variant(personality.agreeableness, variance))
        results["neuroticism"].append(_random_variant(personality.neuroticism, variance))
        
        # Optional cognitive abilities
        if profile.digital_archetype.cognitive_abilities:
            cog = profile.digital_archetype.cognitive_abilities
            if cog.problem_solving is not None:
                results["problem_solving"].append(_random_variant(cog.problem_solving, variance))
            if cog.creativity is not None:
                results["creativity"].append(_random_variant(cog.creativity, variance))
            if cog.memory is not None:
                results["memory"].append(_random_variant(cog.memory, variance))
            if cog.learning is not None:
                results["learning"].append(_random_variant(cog.learning, variance))
            if cog.spatial_awareness is not None:
                results["spatial_awareness"].append(_random_variant(cog.spatial_awareness, variance))
        
        # Optional communication style
        if profile.digital_archetype.communication_style:
            comm = profile.digital_archetype.communication_style
            if comm.verbosity is not None:
                results["verbosity"].append(_random_variant(comm.verbosity, variance))
            if comm.formality is not None:
                results["formality"].append(_random_variant(comm.formality, variance))
            if comm.humor is not None:
                results["humor"].append(_random_variant(comm.humor, variance))
            if comm.empathy is not None:
                results["empathy"].append(_random_variant(comm.empathy, variance))
            if comm.assertiveness is not None:
                results["assertiveness"].append(_random_variant(comm.assertiveness, variance))
    
    # Compute statistics for each metric
    summary = {}
    for metric, values in results.items():
        if values:  # Only process metrics that have values
            summary[metric] = {
                "mean": statistics.mean(values),
                "min": min(values),
                "max": max(values),
                "std_dev": statistics.stdev(values) if len(values) > 1 else 0.0,
            }
    
    # Add some aggregate information
    summary["iterations"] = iterations
    summary["profile_name"] = profile.profile_name or profile.digital_archetype.identity.name
    summary["profile_id"] = str(profile.profile_id)
    
    return summary
