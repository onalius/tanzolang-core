/**
 * Utility functions for working with TanzoLang profiles.
 * 
 * This module provides helper functions for common tasks such as
 * exporting profiles to different formats.
 */

import YAML from 'yaml';
import { TanzoProfile } from './schema';

/**
 * Convert a profile to a JSON string
 * 
 * @param profile - The profile to convert
 * @param indent - Number of spaces for indentation
 * @returns A JSON string representation
 */
export function toJson(profile: TanzoProfile, indent: number = 2): string {
  return JSON.stringify(profile, null, indent);
}

/**
 * Convert a profile to a YAML string
 * 
 * @param profile - The profile to convert
 * @returns A YAML string representation
 */
export function toYaml(profile: TanzoProfile): string {
  return YAML.stringify(profile);
}

/**
 * Simulate a profile using Monte Carlo methods
 * 
 * @param profile - The profile to simulate
 * @param numIterations - Number of simulation iterations
 * @returns A simulation result object
 */
export interface SimulationResult {
  profileName: string;
  numIterations: number;
  traitMeans: Record<string, number>;
  traitStdDevs: Record<string, number>;
  traitRanges: Record<string, [number, number]>;
}

/**
 * Simulate a profile using Monte Carlo methods
 * 
 * @param profile - The profile to simulate
 * @param numIterations - Number of simulation iterations
 * @param seed - Optional random seed for reproducibility
 * @returns A simulation result object
 */
export function simulateProfile(
  profile: TanzoProfile,
  numIterations: number = 100,
  seed?: number
): SimulationResult {
  // Set random seed if provided
  let rng = Math.random;
  if (seed !== undefined) {
    // Simple seedable RNG for simulation purposes
    rng = function() {
      seed = (seed * 9301 + 49297) % 233280;
      return seed / 233280;
    };
  }
  
  const archetype = profile.digital_archetype;
  const traits = archetype.traits;
  
  // Run simulations for each trait
  const simulatedTraits: Record<string, number[]> = {};
  
  for (const [traitName, trait] of Object.entries(traits)) {
    simulatedTraits[traitName] = [];
    const mean = trait.value;
    const stddev = trait.variance || 0.1;
    
    for (let i = 0; i < numIterations; i++) {
      // Box-Muller transform for normal distribution
      const u1 = rng();
      const u2 = rng();
      const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
      
      // Apply mean and standard deviation
      let value = mean + z0 * stddev;
      // Truncate to valid range
      value = Math.max(0.0, Math.min(1.0, value));
      simulatedTraits[traitName].push(value);
    }
  }
  
  // Calculate statistics
  const traitMeans: Record<string, number> = {};
  const traitStdDevs: Record<string, number> = {};
  const traitRanges: Record<string, [number, number]> = {};
  
  for (const [traitName, values] of Object.entries(simulatedTraits)) {
    // Calculate mean
    traitMeans[traitName] = values.reduce((sum, val) => sum + val, 0) / values.length;
    
    // Calculate standard deviation
    const variance = values.reduce(
      (sum, val) => sum + Math.pow(val - traitMeans[traitName], 2),
      0
    ) / values.length;
    traitStdDevs[traitName] = Math.sqrt(variance);
    
    // Calculate range
    traitRanges[traitName] = [
      Math.min(...values),
      Math.max(...values)
    ];
  }
  
  return {
    profileName: profile.profile.name,
    numIterations,
    traitMeans,
    traitStdDevs,
    traitRanges
  };
}

/**
 * Generate a human-readable summary of simulation results
 * 
 * @param results - Simulation results to summarize
 * @returns A formatted summary string
 */
export function formatSimulationSummary(results: SimulationResult): string {
  const lines = [
    `Simulation Results for '${results.profileName}'`,
    `Number of iterations: ${results.numIterations}`,
    '',
    'Traits:',
  ];
  
  // Sort traits by mean value (descending)
  const sortedTraits = Object.entries(results.traitMeans)
    .sort(([, a], [, b]) => b - a);
  
  for (const [traitName, meanValue] of sortedTraits) {
    const stddev = results.traitStdDevs[traitName];
    const [minVal, maxVal] = results.traitRanges[traitName];
    
    lines.push(
      `  ${traitName}:`
      + ` mean=${meanValue.toFixed(2)},`
      + ` stddev=${stddev.toFixed(2)},`
      + ` range=[${minVal.toFixed(2)}, ${maxVal.toFixed(2)}]`
    );
  }
  
  return lines.join('\n');
}

/**
 * Export a TanzoLang profile to a concise string representation
 * 
 * @param profile - The profile to export
 * @returns A shorthand string representation
 */
export function exportShorthand(profile: TanzoProfile): string {
  const archetype = profile.digital_archetype;
  const identity = archetype.identity;
  
  // Start with basic information
  const parts: string[] = [`${identity.name}`];
  
  // Add identity information if available
  if (identity.age !== undefined) {
    parts.push(`age:${identity.age}`);
  }
  if (identity.occupation) {
    parts.push(`job:${identity.occupation}`);
  }
  
  // Add top traits (up to 3)
  const topTraits = Object.entries(archetype.traits)
    .sort(([, a], [, b]) => b.value - a.value)
    .slice(0, 3);
  
  const traitsStr = topTraits
    .map(([name, { value }]) => `${name}:${value.toFixed(1)}`)
    .join(',');
    
  parts.push(`traits:[${traitsStr}]`);
  
  // Add behavioral rules if available (up to 2)
  if (profile.behavioral_rules && profile.behavioral_rules.length > 0) {
    const topRules = profile.behavioral_rules
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 2);
    
    const rulesStr = topRules
      .map(rule => rule.rule)
      .join(';');
    
    parts.push(`rules:[${rulesStr}]`);
  }
  
  return parts.join(' | ');
}
