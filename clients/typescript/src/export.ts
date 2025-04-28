/**
 * Export functions for Tanzo profiles
 */

import * as yaml from 'js-yaml';
import { TanzoProfile } from './models';

/**
 * Export formats supported
 */
export type ExportFormat = 'shorthand' | 'json' | 'yaml';

/**
 * Export a Tanzo profile to a specific format
 * 
 * @param profile The profile to export
 * @param format The format to export to (shorthand, json, or yaml)
 * @returns The exported profile in the specified format
 * @throws If an unknown format is requested
 */
export function exportProfile(
  profile: TanzoProfile,
  format: ExportFormat = 'shorthand'
): string {
  if (format === 'shorthand') {
    return exportShorthand(profile);
  } else if (format === 'json') {
    return JSON.stringify(profile, null, 2);
  } else if (format === 'yaml') {
    return yaml.dump(profile);
  } else {
    throw new Error(`Unknown export format: ${format}`);
  }
}

/**
 * Export a Tanzo profile to a shorthand string representation
 * 
 * @param profile The profile to export
 * @returns The shorthand string representation
 */
export function exportShorthand(profile: TanzoProfile): string {
  // Basic profile info
  let result = `${profile.profile.name}@${profile.profile.version}`;
  
  // Archetype
  result += ` [${profile.archetype.type}`;
  
  // Core attributes (take first letter of each)
  const coreAttr = profile.archetype.attributes.core
    .map(attr => attr.charAt(0).toUpperCase())
    .join('');
  result += `:${coreAttr}`;
  
  // Elements (if present)
  if (profile.archetype.affinity?.elements && profile.archetype.affinity.elements.length > 0) {
    const elements = profile.archetype.affinity.elements
      .map(element => element.charAt(0).toUpperCase())
      .join('');
    result += `|${elements}`;
  }
  
  result += ']';
  
  // State
  const baseline = profile.properties.state.baseline;
  result += ` E${Math.round(baseline.energy)}/R${Math.round(baseline.resilience)}/A${Math.round(baseline.adaptability)}`;
  
  // Top capability
  if (profile.properties.capabilities.length > 0) {
    // Find capability with highest power
    const topCapability = profile.properties.capabilities.reduce((prev, current) => 
      prev.power > current.power ? prev : current
    );
    result += ` «${topCapability.name}:${topCapability.power.toFixed(1)}»`;
  }
  
  return result;
}
