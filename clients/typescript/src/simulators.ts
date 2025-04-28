/**
 * Simulation utilities for TanzoLang profiles
 */
import { TanzoProfile, Behavior } from './schema';

/**
 * Represents a simulation metric with a name, value and description
 */
export interface SimulationMetric {
  name: string;
  value: number;
  description: string;
}

/**
 * Represents the result of a profile simulation
 */
export interface SimulationResult {
  profileName: string;
  metrics: SimulationMetric[];
  summary: string;
  iterations: number;
}

/**
 * Sample whether a behavior is activated based on its strength and context
 * 
 * @param behavior - The behavior to sample
 * @param simulationParams - Simulation parameters
 * @returns Activation value between 0.0 and 1.0
 */
function sampleBehaviorActivation(
  behavior: Behavior, 
  simulationParams: Record<string, any>
): number {
  const baseStrength = behavior.strength;
  const randomness = simulationParams.randomness ?? 0.3;
  
  // Add some noise based on randomness
  const noise = (Math.random() * 2 - 1) * randomness;
  const activation = baseStrength + (noise * baseStrength);
  
  // Clamp between 0.0 and 1.0
  return Math.max(0.0, Math.min(1.0, activation));
}

/**
 * Run a single simulation iteration for a profile
 * 
 * @param profile - The profile to simulate
 * @returns A dictionary of metrics from the simulation
 */
function simulateIteration(profile: TanzoProfile): Record<string, number> {
  const p = profile.profile;
  const metrics: Record<string, number> = {};
  
  // Get simulation parameters
  const simParams: Record<string, any> = p.simulation?.parameters ?? {
    randomness: 0.3,
    temperature: 0.7,
    creativity: 0.5
  };
  
  // Simulate behavior activations
  if (p.behaviors && p.behaviors.length > 0) {
    const behaviorActivations = p.behaviors.map(behavior => 
      sampleBehaviorActivation(behavior, simParams)
    );
    
    if (behaviorActivations.length > 0) {
      metrics["mean_behavior_activation"] = behaviorActivations.reduce((sum, val) => sum + val, 0) / behaviorActivations.length;
    }
  }
  
  // Simulate personality expression
  if (p.personality?.traits) {
    const traits = p.personality.traits;
    const traitDict: Record<string, number | undefined> = {
      openness: traits.openness,
      conscientiousness: traits.conscientiousness,
      extraversion: traits.extraversion,
      agreeableness: traits.agreeableness,
      neuroticism: traits.neuroticism
    };
    
    // Add some randomness to trait expression
    const randomness = simParams.randomness ?? 0.3;
    for (const [trait, value] of Object.entries(traitDict)) {
      if (value !== undefined) {
        const noise = (Math.random() * 2 - 1) * randomness;
        let expressedValue = value + (noise * value);
        // Clamp between 0.0 and 1.0
        expressedValue = Math.max(0.0, Math.min(1.0, expressedValue));
        metrics[`${trait}_expression`] = expressedValue;
      }
    }
  }
  
  // Simulate communication aspects
  if (p.communication) {
    const comm = p.communication;
    if (comm.complexity !== undefined) {
      const randomness = simParams.randomness ?? 0.3;
      const noise = (Math.random() * 2 - 1) * randomness;
      metrics["expressed_complexity"] = Math.max(0.0, Math.min(1.0, comm.complexity + (noise * comm.complexity)));
    }
    
    if (comm.verbosity !== undefined) {
      const randomness = simParams.randomness ?? 0.3;
      const noise = (Math.random() * 2 - 1) * randomness;
      metrics["expressed_verbosity"] = Math.max(0.0, Math.min(1.0, comm.verbosity + (noise * comm.verbosity)));
    }
  }
  
  return metrics;
}

/**
 * Calculate the mean of an array of numbers
 */
function mean(values: number[]): number {
  return values.reduce((sum, val) => sum + val, 0) / values.length;
}

/**
 * Calculate the standard deviation of an array of numbers
 */
function stdDev(values: number[], meanValue?: number): number {
  const avg = meanValue ?? mean(values);
  const squareDiffs = values.map(value => {
    const diff = value - avg;
    return diff * diff;
  });
  const variance = mean(squareDiffs);
  return Math.sqrt(variance);
}

/**
 * Run a Monte Carlo simulation of a profile over multiple iterations
 * 
 * @param profile - The profile to simulate
 * @param iterations - Number of simulation iterations
 * @returns The aggregated results of the simulation
 */
export function simulateProfile(
  profile: TanzoProfile, 
  iterations: number = 100
): SimulationResult {
  const p = profile.profile;
  const allMetrics: Record<string, number[]> = {};
  
  // Run simulations
  for (let i = 0; i < iterations; i++) {
    const metrics = simulateIteration(profile);
    
    // Collect metrics
    for (const [key, value] of Object.entries(metrics)) {
      if (!allMetrics[key]) {
        allMetrics[key] = [];
      }
      allMetrics[key].push(value);
    }
  }
  
  // Calculate summary metrics
  const summaryMetrics: SimulationMetric[] = [];
  for (const [key, values] of Object.entries(allMetrics)) {
    const meanValue = mean(values);
    const stdDevValue = stdDev(values, meanValue);
    const description = `Mean: ${meanValue.toFixed(2)}, StdDev: ${stdDevValue.toFixed(2)}`;
    
    summaryMetrics.push({
      name: key,
      value: meanValue,
      description: description
    });
  }
  
  // Sort metrics by name
  summaryMetrics.sort((a, b) => a.name.localeCompare(b.name));
  
  // Create summary text
  const summaryLines = [
    `Simulation Results for '${p.name}'`,
    `Ran ${iterations} iterations`,
    "",
    "Summary Metrics:",
  ];
  
  for (const metric of summaryMetrics) {
    summaryLines.push(`- ${metric.name}: ${metric.value.toFixed(2)} (${metric.description})`);
  }
  
  const summary = summaryLines.join('\n');
  
  return {
    profileName: p.name,
    metrics: summaryMetrics,
    summary,
    iterations
  };
}
