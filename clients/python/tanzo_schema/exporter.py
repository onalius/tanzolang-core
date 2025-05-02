"""
Export utilities for TanzoLang profiles
"""

import json
import yaml
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

from clients.python.tanzo_schema.models import (
    TanzoProfile,
    Attribute,
    NormalDistribution,
    UniformDistribution,
    DiscreteDistribution,
    ZodiacTypology,
    KabbalahTypology,
    PurposeQuadrantTypology,
)
from clients.python.tanzo_schema.validator import validate_profile


def format_distribution(distribution: Union[NormalDistribution, UniformDistribution, DiscreteDistribution]) -> str:
    """
    Format a probability distribution as a concise string
    
    Args:
        distribution: The distribution to format
        
    Returns:
        str: A formatted string representation
    """
    if isinstance(distribution, NormalDistribution):
        return f"N({distribution.mean:.2f}, {distribution.stdDev:.2f})"
    
    elif isinstance(distribution, UniformDistribution):
        return f"U({distribution.min:.2f}, {distribution.max:.2f})"
    
    elif isinstance(distribution, DiscreteDistribution):
        # Format discrete values and weights
        pairs = []
        for val, weight in zip(distribution.values, distribution.weights):
            # Format the value based on its type
            if isinstance(val, str):
                formatted_val = f'"{val}"'
            elif isinstance(val, bool):
                formatted_val = str(val).lower()
            else:
                formatted_val = str(val)
            
            pairs.append(f"{formatted_val}:{weight:.2f}")
        
        return f"D({', '.join(pairs)})"
    
    else:
        raise ValueError(f"Unknown distribution type: {type(distribution)}")


def format_attribute(attribute: Attribute) -> str:
    """
    Format an attribute as a concise string
    
    Args:
        attribute: The attribute to format
        
    Returns:
        str: A formatted string representation
    """
    value = attribute.value
    
    # Format based on value type
    if isinstance(value, (NormalDistribution, UniformDistribution, DiscreteDistribution)):
        formatted_value = format_distribution(value)
    elif isinstance(value, str):
        formatted_value = f'"{value}"'
    elif isinstance(value, bool):
        formatted_value = str(value).lower()
    else:
        formatted_value = str(value)
    
    # Include unit if available
    if attribute.unit:
        return f"{attribute.name}={formatted_value} {attribute.unit}"
    else:
        return f"{attribute.name}={formatted_value}"


def format_zodiac(zodiac: ZodiacTypology) -> List[str]:
    """
    Format a zodiac typology as a list of strings
    
    Args:
        zodiac: The zodiac typology to format
        
    Returns:
        List[str]: Formatted strings for the zodiac typology
    """
    lines = ["  TYPOLOGY:Zodiac"]
    lines.append(f"    Sun={zodiac.sun}")
    
    if zodiac.moon:
        lines.append(f"    Moon={zodiac.moon}")
    if zodiac.rising:
        lines.append(f"    Rising={zodiac.rising}")
        
    return lines


def format_kabbalah(kabbalah: KabbalahTypology) -> List[str]:
    """
    Format a kabbalah typology as a list of strings
    
    Args:
        kabbalah: The kabbalah typology to format
        
    Returns:
        List[str]: Formatted strings for the kabbalah typology
    """
    lines = ["  TYPOLOGY:Kabbalah"]
    lines.append(f"    PrimarySefira={kabbalah.primary_sefira}")
    
    if kabbalah.secondary_sefira:
        lines.append(f"    SecondarySefira={kabbalah.secondary_sefira}")
    if kabbalah.path:
        lines.append(f"    Path={kabbalah.path}")
        
    return lines


def format_purpose_quadrant(purpose: PurposeQuadrantTypology) -> List[str]:
    """
    Format a purpose quadrant typology as a list of strings
    
    Args:
        purpose: The purpose quadrant typology to format
        
    Returns:
        List[str]: Formatted strings for the purpose quadrant typology
    """
    lines = ["  TYPOLOGY:PurposeQuadrant"]
    lines.append(f"    Passion={purpose.passion}")
    lines.append(f"    Expertise={purpose.expertise}")
    lines.append(f"    Contribution={purpose.contribution}")
    lines.append(f"    Sustainability={purpose.sustainability}")
        
    return lines


def load_profile_from_yaml(file_path: Union[str, Path]) -> TanzoProfile:
    """
    Load a profile from a YAML file
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        TanzoProfile: The loaded profile
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return TanzoProfile.parse_obj(data)


def export_profile_shorthand(profile: TanzoProfile) -> str:
    """
    Export a profile to a concise shorthand representation
    
    Args:
        profile: The profile to export
        
    Returns:
        str: A shorthand string representation
    """
    # Basic profile info
    parts = [f"{profile.profile.name}"]
    
    # Add archetypes in brackets
    if hasattr(profile.profile, 'archetype'):
        # Handle legacy profile format with 'archetype' field
        archetypes = []
        if profile.profile.archetype.primary:
            archetypes.append(profile.profile.archetype.primary)
        if hasattr(profile.profile.archetype, 'secondary') and profile.profile.archetype.secondary:
            archetypes.append(profile.profile.archetype.secondary)
        parts[0] += f" [{'/'.join(archetypes)}]"
    elif hasattr(profile.profile, 'archetypes'):
        # Handle new format with 'archetypes' list
        archetype_names = []
        for archetype in profile.profile.archetypes:
            if archetype.name:
                archetype_names.append(archetype.name)
            else:
                archetype_names.append(archetype.type.value)
        
        if archetype_names:
            parts[0] += f" [{'/'.join(archetype_names)}]"
    
    # Add personality traits if present
    if hasattr(profile.profile, 'personality') and profile.profile.personality:
        if hasattr(profile.profile.personality, 'traits') and profile.profile.personality.traits:
            traits = profile.profile.personality.traits
            traits_str = f"O:{traits.get('openness', 0):.1f} C:{traits.get('conscientiousness', 0):.1f} "
            traits_str += f"E:{traits.get('extraversion', 0):.1f} A:{traits.get('agreeableness', 0):.1f} "
            traits_str += f"N:{traits.get('neuroticism', 0):.1f}"
            parts.append(traits_str)
    
    # Add communication style if present
    if hasattr(profile.profile, 'communication') and profile.profile.communication:
        comm = profile.profile.communication
        comm_parts = []
        if hasattr(comm, 'style') and comm.style:
            comm_parts.append(comm.style)
        if hasattr(comm, 'tone') and comm.tone:
            comm_parts.append(comm.tone)
        if comm_parts:
            parts.append(", ".join(comm_parts))
    
    return "\n".join(parts)


def export_profile_json(profile: TanzoProfile, output_path: Optional[Union[str, Path]] = None) -> str:
    """
    Export a profile to JSON format
    
    Args:
        profile: The profile to export
        output_path: Optional path to save the JSON file
        
    Returns:
        str: The profile as a JSON string
    """
    # Convert to dict and serialize to JSON
    profile_dict = profile.dict()
    json_str = json.dumps(profile_dict, indent=2)
    
    # Write to file if output_path is provided
    if output_path:
        with open(output_path, 'w') as f:
            f.write(json_str)
    
    return json_str


def export_profile_yaml(profile: TanzoProfile, output_path: Optional[Union[str, Path]] = None) -> str:
    """
    Export a profile to YAML format
    
    Args:
        profile: The profile to export
        output_path: Optional path to save the YAML file
        
    Returns:
        str: The profile as a YAML string
    """
    # Convert to dict and serialize to YAML
    profile_dict = profile.dict()
    yaml_str = yaml.dump(profile_dict, sort_keys=False, indent=2)
    
    # Write to file if output_path is provided
    if output_path:
        with open(output_path, 'w') as f:
            f.write(yaml_str)
    
    return yaml_str


def export_profile(profile_path: Union[str, Path]) -> str:
    """
    Export a TanzoLang profile as a concise string representation
    
    Args:
        profile_path: Path to the profile file
        
    Returns:
        str: A formatted string representation of the profile
    """
    # Validate the profile first
    profile = validate_profile(profile_path)
    
    # Format the profile
    lines = [f"TanzoProfile: {profile.profile.name} (v{profile.version})"]
    
    # Format each archetype
    lines.append("\nARCHETYPES:")
    for archetype in profile.profile.archetypes:
        archetype_name = archetype.name or archetype.type.value
        archetype_line = f"  {archetype.type.value.upper()}:{archetype_name}"
        lines.append(archetype_line)
        
        # Format attributes for this archetype
        for attribute in archetype.attributes:
            attribute_line = f"    {format_attribute(attribute)}"
            lines.append(attribute_line)
    
    # Format parent archetypes if present
    if hasattr(profile.profile, 'parent_archetypes') and profile.profile.parent_archetypes:
        lines.append("\nPARENT ARCHETYPES:")
        for parent in profile.profile.parent_archetypes:
            parent_line = f"  {parent.name} (influence: {parent.influence:.2f})"
            lines.append(parent_line)
            if parent.reference:
                lines.append(f"    Reference: {parent.reference}")
    
    # Format typologies if present
    if hasattr(profile.profile, 'typologies') and profile.profile.typologies:
        typologies = profile.profile.typologies
        lines.append("\nTYPOLOGIES:")
        
        # Format zodiac typology if present
        if hasattr(typologies, 'zodiac') and typologies.zodiac:
            lines.extend(format_zodiac(typologies.zodiac))
            
        # Format kabbalah typology if present
        if hasattr(typologies, 'kabbalah') and typologies.kabbalah:
            lines.extend(format_kabbalah(typologies.kabbalah))
            
        # Format purpose quadrant typology if present
        if hasattr(typologies, 'purpose_quadrant') and typologies.purpose_quadrant:
            lines.extend(format_purpose_quadrant(typologies.purpose_quadrant))
            
        # Format any custom typologies
        for name, typology in typologies.__dict__.items():
            if name not in ['zodiac', 'kabbalah', 'purpose_quadrant'] and typology is not None:
                lines.append(f"  TYPOLOGY:{name}")
                for key, value in typology.__dict__.items():
                    if value is not None:
                        lines.append(f"    {key}={value}")
    
    return "\n".join(lines)
