"""
Export functionality for Tanzo profiles.
"""

from typing import Dict, List

from .models import TanzoProfile


def _attribute_to_shorthand(name: str, value: float) -> str:
    """Convert an attribute to shorthand notation."""
    # Format value as percentage with no decimal places
    value_str = f"{int(value * 100)}%"
    return f"{name}:{value_str}"


def _archetype_to_shorthand(name: str, weight: float, attr_values: Dict[str, float]) -> str:
    """Convert an archetype to shorthand notation."""
    # Format weight as percentage with no decimal places
    weight_str = f"{int(weight * 100)}%"
    
    # Get top 3 attributes by value
    attrs = sorted(
        [(name, value) for name, value in attr_values.items()],
        key=lambda x: x[1],
        reverse=True
    )[:3]
    
    # Format attributes
    attr_str = ",".join(_attribute_to_shorthand(name, value) for name, value in attrs)
    
    return f"{name}@{weight_str}[{attr_str}]"


def export_profile(profile: TanzoProfile) -> str:
    """
    Export a Tanzo profile to a shorthand string representation.
    
    Args:
        profile: TanzoProfile to export
        
    Returns:
        String representation of the profile
    """
    profile_name = profile.profile.name
    
    # Process archetypes
    archetype_strings = []
    
    for archetype in profile.profile.archetypes:
        # Get attribute values for this archetype
        attr_values = {}
        if archetype.attributes:
            attr_values = {attr.name: attr.value for attr in archetype.attributes}
        
        # Convert to shorthand
        arch_str = _archetype_to_shorthand(
            archetype.name,
            archetype.weight,
            attr_values
        )
        archetype_strings.append(arch_str)
    
    # Combine into final string
    result = f"{profile_name}:{{{';'.join(archetype_strings)}}}"
    return result
