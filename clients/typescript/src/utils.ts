/**
 * Utility functions for working with TanzoLang profiles
 */

import { TanzoProfile, TanzoProfileSchema } from './schema';
import * as fs from 'fs';
import * as path from 'path';
import * as YAML from 'yaml';

/**
 * Load and validate a profile from a file
 * 
 * @param filePath Path to a YAML or JSON file containing a Tanzo profile
 * @returns Validated TanzoProfile object
 */
export function loadProfileFromFile(filePath: string): TanzoProfile {
  const fileContent = fs.readFileSync(filePath, 'utf-8');
  const extension = path.extname(filePath).toLowerCase();
  
  let profileData: unknown;
  
  if (extension === '.json') {
    profileData = JSON.parse(fileContent);
  } else if (extension === '.yaml' || extension === '.yml') {
    profileData = YAML.parse(fileContent);
  } else {
    throw new Error(`Unsupported file extension: ${extension}. Use .json, .yaml, or .yml`);
  }
  
  return TanzoProfileSchema.parse(profileData);
}

/**
 * Export a profile to a shorthand string representation
 * 
 * @param profile TanzoProfile object or path to a profile file
 * @returns Shorthand string representation
 */
export function exportProfile(profile: TanzoProfile | string): string {
  // Load profile if path is provided
  const tanzoProfile = typeof profile === 'string' 
    ? loadProfileFromFile(profile) 
    : profile;
  
  // Extract key components for the shorthand
  const personality = tanzoProfile.digital_archetype.personality_traits;
  
  // Format: Name(O{openness}C{conscientiousness}E{extraversion}A{agreeableness}N{neuroticism})
  // Example: "Kai(O8C9E6A9N2)" - Kai with openness 0.8, conscientiousness 0.9, etc.
  let shorthand = `${tanzoProfile.digital_archetype.identity.name}(`;
  shorthand += `O${Math.round(personality.openness * 10)}`;
  shorthand += `C${Math.round(personality.conscientiousness * 10)}`;
  shorthand += `E${Math.round(personality.extraversion * 10)}`;
  shorthand += `A${Math.round(personality.agreeableness * 10)}`;
  shorthand += `N${Math.round(personality.neuroticism * 10)}`;
  shorthand += ')';
  
  return shorthand;
}

/**
 * Generate a random value within specified variance
 * 
 * @param value Base value
 * @param variance Maximum variance as a fraction
 * @returns Random value within variance
 */
function randomVariant(value: number, variance: number = 0.1): number {
  // Calculate the amount to vary by (up to variance in either direction)
  const variation = (Math.random() * 2 - 1) * variance;
  
  // Apply the variation
  const result = value + variation;
  
  // Ensure the result is within [0, 1]
  return Math.max(0, Math.min(1, result));
}

/**
 * Calculate mean of an array of numbers
 */
function mean(values: number[]): number {
  return values.reduce((sum, val) => sum + val, 0) / values.length;
}

/**
 * Calculate standard deviation of an array of numbers
 */
function stdDev(values: number[]): number {
  if (values.length <= 1) {
    return 0;
  }
  
  const avg = mean(values);
  const squareDiffs = values.map(value => {
    const diff = value - avg;
    return diff * diff;
  });
  
  const avgSquareDiff = mean(squareDiffs);
  return Math.sqrt(avgSquareDiff);
}

interface SimulationMetric {
  mean: number;
  min: number;
  max: number;
  std_dev: number;
}

interface SimulationResult {
  [key: string]: SimulationMetric | string | number;
  iterations: number;
  profile_name: string;
  profile_id: string;
}

/**
 * Run a Monte Carlo simulation of a profile with variations
 * 
 * @param profile TanzoProfile object or path to a profile file
 * @param iterations Number of simulation iterations
 * @param variance Maximum variance as a fraction of the base values
 * @returns Simulation results
 */
export function simulateProfile(
  profile: TanzoProfile | string,
  iterations: number = 100,
  variance: number = 0.1
): SimulationResult {
  // Load profile if path is provided
  const tanzoProfile = typeof profile === 'string' 
    ? loadProfileFromFile(profile) 
    : profile;
  
  // Initialize results collection
  const resultValues: Record<string, number[]> = {
    openness: [],
    conscientiousness: [],
    extraversion: [],
    agreeableness: [],
    neuroticism: [],
  };
  
  // Optional metrics if available in the profile
  const cogAbilities = tanzoProfile.digital_archetype.cognitive_abilities;
  const commStyle = tanzoProfile.digital_archetype.communication_style;
  
  if (cogAbilities) {
    if (cogAbilities.problem_solving !== undefined) resultValues.problem_solving = [];
    if (cogAbilities.creativity !== undefined) resultValues.creativity = [];
    if (cogAbilities.memory !== undefined) resultValues.memory = [];
    if (cogAbilities.learning !== undefined) resultValues.learning = [];
    if (cogAbilities.spatial_awareness !== undefined) resultValues.spatial_awareness = [];
  }
  
  if (commStyle) {
    if (commStyle.verbosity !== undefined) resultValues.verbosity = [];
    if (commStyle.formality !== undefined) resultValues.formality = [];
    if (commStyle.humor !== undefined) resultValues.humor = [];
    if (commStyle.empathy !== undefined) resultValues.empathy = [];
    if (commStyle.assertiveness !== undefined) resultValues.assertiveness = [];
  }
  
  // Run iterations
  for (let i = 0; i < iterations; i++) {
    // Personality traits (required)
    const personality = tanzoProfile.digital_archetype.personality_traits;
    resultValues.openness.push(randomVariant(personality.openness, variance));
    resultValues.conscientiousness.push(randomVariant(personality.conscientiousness, variance));
    resultValues.extraversion.push(randomVariant(personality.extraversion, variance));
    resultValues.agreeableness.push(randomVariant(personality.agreeableness, variance));
    resultValues.neuroticism.push(randomVariant(personality.neuroticism, variance));
    
    // Optional cognitive abilities
    if (cogAbilities) {
      if (cogAbilities.problem_solving !== undefined) {
        resultValues.problem_solving.push(randomVariant(cogAbilities.problem_solving, variance));
      }
      if (cogAbilities.creativity !== undefined) {
        resultValues.creativity.push(randomVariant(cogAbilities.creativity, variance));
      }
      if (cogAbilities.memory !== undefined) {
        resultValues.memory.push(randomVariant(cogAbilities.memory, variance));
      }
      if (cogAbilities.learning !== undefined) {
        resultValues.learning.push(randomVariant(cogAbilities.learning, variance));
      }
      if (cogAbilities.spatial_awareness !== undefined) {
        resultValues.spatial_awareness.push(randomVariant(cogAbilities.spatial_awareness, variance));
      }
    }
    
    // Optional communication style
    if (commStyle) {
      if (commStyle.verbosity !== undefined) {
        resultValues.verbosity.push(randomVariant(commStyle.verbosity, variance));
      }
      if (commStyle.formality !== undefined) {
        resultValues.formality.push(randomVariant(commStyle.formality, variance));
      }
      if (commStyle.humor !== undefined) {
        resultValues.humor.push(randomVariant(commStyle.humor, variance));
      }
      if (commStyle.empathy !== undefined) {
        resultValues.empathy.push(randomVariant(commStyle.empathy, variance));
      }
      if (commStyle.assertiveness !== undefined) {
        resultValues.assertiveness.push(randomVariant(commStyle.assertiveness, variance));
      }
    }
  }
  
  // Compute statistics for each metric
  const summary: SimulationResult = {
    iterations,
    profile_name: tanzoProfile.profile_name || tanzoProfile.digital_archetype.identity.name,
    profile_id: tanzoProfile.profile_id,
  };
  
  // Calculate statistics for each metric
  for (const [metric, values] of Object.entries(resultValues)) {
    if (values.length > 0) {
      summary[metric] = {
        mean: mean(values),
        min: Math.min(...values),
        max: Math.max(...values),
        std_dev: stdDev(values),
      };
    }
  }
  
  return summary;
}
