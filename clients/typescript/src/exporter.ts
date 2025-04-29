/**
 * Export utilities for TanzoLang profiles
 */

import { 
  TanzoProfile,
  Attribute,
  NormalDistribution,
  UniformDistribution,
  DiscreteDistribution
} from './models';
import { validateProfile } from './validator';

/**
 * Format a probability distribution as a concise string
 * 
 * @param distribution The distribution to format
 * @returns A formatted string representation
 */
export function formatDistribution(
  distribution: NormalDistribution | UniformDistribution | DiscreteDistribution
): string {
  if (distribution.distribution === 'normal') {
    return `N(${distribution.mean.toFixed(2)}, ${distribution.stdDev.toFixed(2)})`;
  }
  
  else if (distribution.distribution === 'uniform') {
    return `U(${distribution.min.toFixed(2)}, ${distribution.max.toFixed(2)})`;
  }
  
  else if (distribution.distribution === 'discrete') {
    // Format discrete values and weights
    const pairs = distribution.values.map((val, i) => {
      // Format the value based on its type
      let formattedVal: string;
      if (typeof val === 'string') {
        formattedVal = `"${val}"`;
      } else if (typeof val === 'boolean') {
        formattedVal = String(val).toLowerCase();
      } else {
        formattedVal = String(val);
      }
      
      return `${formattedVal}:${distribution.weights[i].toFixed(2)}`;
    });
    
    return `D(${pairs.join(', ')})`;
  }
  
  throw new Error(`Unknown distribution type: ${(distribution as any).distribution}`);
}

/**
 * Format an attribute as a concise string
 * 
 * @param attribute The attribute to format
 * @returns A formatted string representation
 */
export function formatAttribute(attribute: Attribute): string {
  const value = attribute.value;
  
  // Format based on value type
  let formattedValue: string;
  if (typeof value === 'object' && 'distribution' in value) {
    formattedValue = formatDistribution(value);
  } else if (typeof value === 'string') {
    formattedValue = `"${value}"`;
  } else if (typeof value === 'boolean') {
    formattedValue = String(value).toLowerCase();
  } else {
    formattedValue = String(value);
  }
  
  // Include unit if available
  if (attribute.unit) {
    return `${attribute.name}=${formattedValue} ${attribute.unit}`;
  } else {
    return `${attribute.name}=${formattedValue}`;
  }
}

/**
 * Export a TanzoLang profile as a concise string representation
 * 
 * @param profilePath Path to the profile file
 * @returns A formatted string representation of the profile
 */
export function exportProfile(profilePath: string): string {
  // Validate the profile first
  const profile = validateProfile(profilePath);
  
  // Format the profile
  const lines: string[] = [`TanzoProfile: ${profile.profile.name} (v${profile.version})`];
  
  // Format each archetype
  for (const archetype of profile.profile.archetypes) {
    const archetypeName = archetype.name || archetype.type;
    const archetypeLine = `  ${archetype.type.toUpperCase()}:${archetypeName}`;
    lines.push(archetypeLine);
    
    // Format attributes for this archetype
    for (const attribute of archetype.attributes) {
      const attributeLine = `    ${formatAttribute(attribute)}`;
      lines.push(attributeLine);
    }
  }
  
  return lines.join('\n');
}
