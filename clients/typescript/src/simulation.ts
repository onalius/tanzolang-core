/**
 * Simulation functions for Tanzo profiles
 */

import { TanzoProfile, Capability } from './models';

/**
 * Results of a profile simulation
 */
export interface SimulationSummary {
  profileName: string;
  iterations: number;
  energy: {
    min: number;
    max: number;
    mean: number;
    std: number;
  };
  resilience: {
    min: number;
    max: number;
    mean: number;
    std: number;
  };
  adaptability: {
    min: number;
    max: number;
    mean: number;
    std: number;
  };
  capabilityActivations: Record<string, number>;
}

/**
 * Class to hold the results of a profile simulation
 */
export class SimulationResult {
  profileName: string;
  iterations: number = 0;
  energyValues: number[] = [];
  resilienceValues: number[] = [];
  adaptabilityValues: number[] = [];
  capabilityActivations: Record<string, number> = {};
  
  constructor(profile: TanzoProfile) {
    this.profileName = profile.profile.name;
    
    // Initialize capability activations counter
    for (const capability of profile.properties.capabilities) {
      this.capabilityActivations[capability.name] = 0;
    }
  }
  
  /**
   * Add the results of one simulation iteration
   * 
   * @param energy The energy value for this iteration
   * @param resilience The resilience value for this iteration
   * @param adaptability The adaptability value for this iteration
   * @param activatedCapability The name of any capability that was activated
   */
  addIteration(
    energy: number,
    resilience: number,
    adaptability: number,
    activatedCapability?: string
  ): void {
    this.iterations += 1;
    this.energyValues.push(energy);
    this.resilienceValues.push(resilience);
    this.adaptabilityValues.push(adaptability);
    
    if (activatedCapability && this.capabilityActivations[activatedCapability] !== undefined) {
      this.capabilityActivations[activatedCapability] += 1;
    }
  }
  
  /**
   * Calculate the mean of an array of numbers
   */
  private mean(values: number[]): number {
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  }
  
  /**
   * Calculate the standard deviation of an array of numbers
   */
  private std(values: number[]): number {
    const avg = this.mean(values);
    const squareDiffs = values.map(value => Math.pow(value - avg, 2));
    const avgSquareDiff = this.mean(squareDiffs);
    return Math.sqrt(avgSquareDiff);
  }
  
  /**
   * Get a summary of the simulation results
   * 
   * @returns A summary object with statistics
   */
  getSummary(): SimulationSummary {
    return {
      profileName: this.profileName,
      iterations: this.iterations,
      energy: {
        min: Math.min(...this.energyValues),
        max: Math.max(...this.energyValues),
        mean: this.mean(this.energyValues),
        std: this.std(this.energyValues),
      },
      resilience: {
        min: Math.min(...this.resilienceValues),
        max: Math.max(...this.resilienceValues),
        mean: this.mean(this.resilienceValues),
        std: this.std(this.resilienceValues),
      },
      adaptability: {
        min: Math.min(...this.adaptabilityValues),
        max: Math.max(...this.adaptabilityValues),
        mean: this.mean(this.adaptabilityValues),
        std: this.std(this.adaptabilityValues),
      },
      capabilityActivations: this.capabilityActivations,
    };
  }
  
  /**
   * Get a string representation of the simulation results
   * 
   * @returns A formatted string summary
   */
  toString(): string {
    const summary = this.getSummary();
    
    let result = [
      `Simulation Results for: ${summary.profileName}`,
      `Total Iterations: ${summary.iterations}`,
      '\nState Variables:',
      `  Energy: min=${summary.energy.min.toFixed(2)}, max=${summary.energy.max.toFixed(2)}, ` +
      `mean=${summary.energy.mean.toFixed(2)}, std=${summary.energy.std.toFixed(2)}`,
      `  Resilience: min=${summary.resilience.min.toFixed(2)}, max=${summary.resilience.max.toFixed(2)}, ` +
      `mean=${summary.resilience.mean.toFixed(2)}, std=${summary.resilience.std.toFixed(2)}`,
      `  Adaptability: min=${summary.adaptability.min.toFixed(2)}, max=${summary.adaptability.max.toFixed(2)}, ` +
      `mean=${summary.adaptability.mean.toFixed(2)}, std=${summary.adaptability.std.toFixed(2)}`,
      '\nCapability Activations:',
    ];
    
    for (const [capability, count] of Object.entries(summary.capabilityActivations)) {
      const percentage = summary.iterations > 0 ? (count / summary.iterations) * 100 : 0;
      result.push(`  ${capability}: ${count} times (${percentage.toFixed(1)}%)`);
    }
    
    return result.join('\n');
  }
}

/**
 * Apply random variance to a base value
 * 
 * @param baseValue The base value
 * @param variance The maximum variance to apply
 * @returns The value after applying variance
 */
function applyVariance(baseValue: number, variance?: number): number {
  if (variance === undefined || variance <= 0) {
    return baseValue;
  }
  
  const actualVariance = (Math.random() * 2 - 1) * variance;
  const result = baseValue + actualVariance;
  
  // Ensure the result is within valid range (0-100)
  return Math.max(0, Math.min(100, result));
}

/**
 * Determine if a capability should be activated based on its power
 * 
 * @param capabilityPower The power level of the capability (1-10)
 * @returns Whether the capability should be activated
 */
function shouldActivateCapability(capabilityPower: number): boolean {
  // Convert power (1-10) to a probability (0.1-1.0)
  const activationProbability = capabilityPower / 10.0;
  return Math.random() < activationProbability;
}

/**
 * Run a Monte Carlo simulation of a Tanzo profile
 * 
 * @param profile The profile to simulate
 * @param iterations The number of iterations to simulate
 * @returns The simulation results
 */
export function simulateProfile(
  profile: TanzoProfile,
  iterations: number = 100
): SimulationResult {
  const result = new SimulationResult(profile);
  
  for (let i = 0; i < iterations; i++) {
    // Get base values
    const baseEnergy = profile.properties.state.baseline.energy;
    const baseResilience = profile.properties.state.baseline.resilience;
    const baseAdaptability = profile.properties.state.baseline.adaptability;
    
    // Get variance values
    const energyVariance = profile.properties.state.variance?.energy;
    const resilienceVariance = profile.properties.state.variance?.resilience;
    const adaptabilityVariance = profile.properties.state.variance?.adaptability;
    
    // Apply variance
    const energy = applyVariance(baseEnergy, energyVariance);
    const resilience = applyVariance(baseResilience, resilienceVariance);
    const adaptability = applyVariance(baseAdaptability, adaptabilityVariance);
    
    // Simulate capability activation
    let activatedCapability: string | undefined;
    for (const capability of profile.properties.capabilities) {
      if (shouldActivateCapability(capability.power)) {
        activatedCapability = capability.name;
        break;
      }
    }
    
    // Record this iteration
    result.addIteration(energy, resilience, adaptability, activatedCapability);
  }
  
  return result;
}
