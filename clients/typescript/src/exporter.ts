/**
 * Export functionality for Tanzo profiles
 */

import { Archetype, TanzoProfile } from './schema';

/**
 * Convert an attribute to shorthand notation
 */
function attributeToShorthand(name: string, value: number): string {
  // Format value as percentage with no decimal places
  const valueStr = `${Math.round(value * 100)}%`;
  return `${name}:${valueStr}`;
}

/**
 * Convert an archetype to shorthand notation
 */
function archetypeToShorthand(
  name: string, 
  weight: number, 
  attrValues: Record<string, number>
): string {
  // Format weight as percentage with no decimal places
  const weightStr = `${Math.round(weight * 100)}%`;
  
  // Get top 3 attributes by value
  const attrs = Object.entries(attrValues)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);
  
  // Format attributes
  const attrStr = attrs
    .map(([name, value]) => attributeToShorthand(name, value))
    .join(',');
  
  return `${name}@${weightStr}[${attrStr}]`;
}

/**
 * Export a Tanzo profile to a shorthand string representation
 */
export function exportProfile(profile: TanzoProfile): string {
  const profileName = profile.profile.name;
  
  // Process archetypes
  const archetypeStrings: string[] = [];
  
  for (const archetype of profile.profile.archetypes) {
    // Get attribute values for this archetype
    const attrValues: Record<string, number> = {};
    if (archetype.attributes) {
      for (const attr of archetype.attributes) {
        attrValues[attr.name] = attr.value;
      }
    }
    
    // Convert to shorthand
    const archStr = archetypeToShorthand(
      archetype.name,
      archetype.weight,
      attrValues
    );
    archetypeStrings.push(archStr);
  }
  
  // Combine into final string
  const result = `${profileName}:{${archetypeStrings.join(';')}}`;
  return result;
}
