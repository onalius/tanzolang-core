/**
 * Simulation utilities for TanzoLang profiles
 */

import { 
  TanzoProfile, 
  Attribute,
  NormalDistribution,
  UniformDistribution,
  DiscreteDistribution,
  AttributeValue
} from './models';
import { validateProfile } from './validator';

/**
 * Sample a value from a probability distribution
 * 
 * @param distribution A probability distribution
 * @returns A sampled value from the distribution
 */
export function sampleDistribution(
  distribution: NormalDistribution | UniformDistribution | DiscreteDistribution
): any {
  if (distribution.distribution === 'normal') {
    // Box-Muller transform for normal distribution
    const u1 = Math.random();
    const u2 = Math.random();
    const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    return z0 * distribution.stdDev + distribution.mean;
  }
  
  else if (distribution.distribution === 'uniform') {
    return distribution.min + Math.random() * (distribution.max - distribution.min);
  }
  
  else if (distribution.distribution === 'discrete') {
    // Normalize weights
    const totalWeight = distribution.weights.reduce((sum, w) => sum + w, 0);
    const normalizedWeights = distribution.weights.map(w => w / totalWeight);
    
    // Cumulative distribution function
    const cdf = normalizedWeights.reduce<number[]>(
      (acc, weight, i) => {
        const lastValue = acc[i] || 0;
        acc.push(lastValue + weight);
        return acc;
      }, 
      []
    );
    
    // Sample using binary search
    const r = Math.random();
    let left = 0;
    let right = cdf.length - 1;
    
    while (left < right) {
      const mid = Math.floor((left + right) / 2);
      if (cdf[mid] < r) {
        left = mid + 1;
      } else {
        right = mid;
      }
    }
    
    return distribution.values[left];
  }
  
  throw new Error(`Unknown distribution type: ${(distribution as any).distribution}`);
}

/**
 * Simulate a value for an attribute, sampling from its distribution if needed
 * 
 * @param attribute The attribute to simulate
 * @returns The attribute name and simulated value
 */
export function simulateAttribute(attribute: Attribute): [string, any] {
  const value = attribute.value;
  
  // If the value is a distribution, sample from it
  if (typeof value === 'object' && 'distribution' in value) {
    const simulated = sampleDistribution(value);
    return [attribute.name, simulated];
  }
  
  // Use the fixed value as is
  return [attribute.name, value];
}

/**
 * Perform a single simulation of a TanzoLang profile
 * 
 * @param profile The profile to simulate
 * @returns Simulated values for each archetype and attribute
 */
export function simulateProfileOnce(profile: TanzoProfile): Record<string, Record<string, any>> {
  const result: Record<string, Record<string, any>> = {};
  
  for (const archetype of profile.profile.archetypes) {
    const archetypeName = archetype.name || archetype.type;
    const archetypeResult: Record<string, any> = {};
    
    for (const attribute of archetype.attributes) {
      const [name, value] = simulateAttribute(attribute);
      archetypeResult[name] = value;
    }
    
    result[archetypeName] = archetypeResult;
  }
  
  return result;
}

/**
 * Calculate statistics for an array of values
 * 
 * @param values Array of values
 * @returns Statistics for the values
 */
function calculateStats(values: any[]): Record<string, any> {
  // Check if all values are numbers
  if (values.every(v => typeof v === 'number')) {
    // Calculate numeric statistics
    const sorted = [...values].sort((a, b) => a - b);
    const sum = sorted.reduce((a, b) => a + b, 0);
    const mean = sum / sorted.length;
    const median = sorted.length % 2 === 0
      ? (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2
      : sorted[Math.floor(sorted.length / 2)];
    
    // Calculate standard deviation
    const squareDiffs = sorted.map(value => Math.pow(value - mean, 2));
    const avgSquareDiff = squareDiffs.reduce((a, b) => a + b, 0) / squareDiffs.length;
    const stdDev = Math.sqrt(avgSquareDiff);
    
    return {
      mean,
      median,
      min: sorted[0],
      max: sorted[sorted.length - 1],
      stdDev
    };
  } else {
    // Calculate frequencies for categorical data
    const frequencies: Record<string, number> = {};
    for (const value of values) {
      const key = String(value);
      frequencies[key] = (frequencies[key] || 0) + 1;
    }
    
    // Convert to relative frequencies
    const relativeFrequencies: Record<string, number> = {};
    for (const [key, count] of Object.entries(frequencies)) {
      relativeFrequencies[key] = count / values.length;
    }
    
    return { frequencies: relativeFrequencies };
  }
}

/**
 * Perform multiple simulations of a TanzoLang profile
 * 
 * @param profilePath Path to the profile file
 * @param iterations Number of simulation iterations to run
 * @returns Summary statistics for the simulations
 */
export function simulateProfile(
  profilePath: string, 
  iterations: number = 100
): Record<string, any> {
  // Validate the profile first
  const profile = validateProfile(profilePath);
  
  // Run simulations
  const allResults: Record<string, Record<string, any>>[] = [];
  for (let i = 0; i < iterations; i++) {
    allResults.push(simulateProfileOnce(profile));
  }
  
  // Prepare summary statistics
  const summary: Record<string, any> = {
    profile_name: profile.profile.name,
    iterations: iterations,
    archetypes: {}
  };
  
  // For each archetype
  for (const archetype of profile.profile.archetypes) {
    const archetypeName = archetype.name || archetype.type;
    const attributeStats: Record<string, any> = {};
    
    // For each attribute
    for (const attribute of archetype.attributes) {
      const attrName = attribute.name;
      
      // Check if attribute has a distribution
      if (typeof attribute.value === 'object' && 'distribution' in attribute.value) {
        // Collect all simulated values for this attribute
        const values = allResults.map(result => result[archetypeName][attrName]);
        
        // Calculate statistics
        attributeStats[attrName] = calculateStats(values);
      } else {
        // Fixed value, no statistics needed
        attributeStats[attrName] = { fixed_value: attribute.value };
      }
    }
    
    summary.archetypes[archetypeName] = attributeStats;
  }
  
  return summary;
}
