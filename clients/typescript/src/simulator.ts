/**
 * Monte Carlo simulator for TanzoLang profiles
 */

import { TanzoProfileType } from './models';

/**
 * Result of a Monte Carlo simulation
 */
export interface SimulationResult {
  profileName: string;
  iterations: number;
  traitVariations: Record<string, number[]>;
  responseVariations: Record<string, number[]>;
  decisionOutcomes: Record<string, number>;
  summaryStats: Record<string, any>;
}

/**
 * Monte Carlo simulator for TanzoLang profiles
 */
export class TanzoSimulator {
  private profile: TanzoProfileType;
  private personalityDrift: number = 0.1;
  private knowledgeUncertainty: number = 0.1;
  private decisionNoise: number = 0.1;
  private scenarioWeights: Record<string, number> = {};

  /**
   * Initialize the simulator with a profile
   * 
   * @param profile TanzoProfile instance
   */
  constructor(profile: TanzoProfileType) {
    this.profile = profile;

    // Initialize from profile simulation parameters if available
    if (
      this.profile.simulation_parameters &&
      this.profile.simulation_parameters.variance_factors
    ) {
      const factors = this.profile.simulation_parameters.variance_factors;
      if (factors.personality_drift !== undefined) {
        this.personalityDrift = factors.personality_drift;
      }
      if (factors.knowledge_uncertainty !== undefined) {
        this.knowledgeUncertainty = factors.knowledge_uncertainty;
      }
      if (factors.decision_noise !== undefined) {
        this.decisionNoise = factors.decision_noise;
      }
    }

    // Get scenario weights if available
    if (
      this.profile.simulation_parameters &&
      this.profile.simulation_parameters.scenario_weights
    ) {
      this.scenarioWeights = this.profile.simulation_parameters.scenario_weights;
    }
  }

  /**
   * Simulate personality trait variations
   * 
   * @returns Dictionary of trait names to simulated values
   */
  private simulateTraits(): Record<string, number> {
    const traits = this.profile.attributes.personality.traits;
    const simulatedTraits: Record<string, number> = {};

    // Apply drift to each trait
    for (const [traitName, traitValue] of Object.entries(traits)) {
      // Apply normal distribution centered on trait value with stddev based on drift
      const drift = this.personalityDrift * 10; // Scale to trait range
      const newValue = this.normalRandom(traitValue, drift);
      // Clamp to valid range
      simulatedTraits[traitName] = Math.max(0, Math.min(10, newValue));
    }

    return simulatedTraits;
  }

  /**
   * Simulate response pattern variations
   * 
   * @returns Dictionary of response pattern attributes to simulated values
   */
  private simulateResponse(): Record<string, number> {
    const responsePatterns: Record<string, number> = {};

    // Default response patterns if not specified
    let verbosity = 5;
    let detailLevel = 5;
    let formality = 5;

    // Use profile response patterns if available
    if (
      this.profile.interaction_framework &&
      this.profile.interaction_framework.response_patterns
    ) {
      const patterns = this.profile.interaction_framework.response_patterns;
      if (patterns.verbosity !== undefined) {
        verbosity = patterns.verbosity;
      }
      if (patterns.detail_level !== undefined) {
        detailLevel = patterns.detail_level;
      }
      if (patterns.formality !== undefined) {
        formality = patterns.formality;
      }
    }

    // Apply noise to each pattern
    const noise = this.decisionNoise * 10; // Scale to pattern range
    responsePatterns['verbosity'] = Math.max(0, Math.min(10, this.normalRandom(verbosity, noise)));
    responsePatterns['detail_level'] = Math.max(0, Math.min(10, this.normalRandom(detailLevel, noise)));
    responsePatterns['formality'] = Math.max(0, Math.min(10, this.normalRandom(formality, noise)));

    return responsePatterns;
  }

  /**
   * Simulate a decision outcome based on profile parameters
   * 
   * @param scenario Optional scenario name to use specific weights
   * @returns Decision outcome string
   */
  private simulateDecision(scenario?: string): string {
    // Define generic outcomes if no scenario is specified
    const outcomes = ['conservative', 'balanced', 'creative'];
    let weights = [0.25, 0.5, 0.25]; // Default weights

    // Adjust weights based on personality traits
    const traits = this.profile.attributes.personality.traits;

    // Creativity influences creative decisions
    if (traits.creativity > 7) {
      weights[2] += 0.1;
      weights[0] -= 0.05;
      weights[1] -= 0.05;
    } else if (traits.creativity < 3) {
      weights[0] += 0.1;
      weights[2] -= 0.1;
    }

    // Conscientiousness influences conservative decisions
    if (traits.conscientiousness > 7) {
      weights[0] += 0.1;
      weights[2] -= 0.1;
    } else if (traits.conscientiousness < 3) {
      weights[2] += 0.1;
      weights[0] -= 0.1;
    }

    // Use scenario-specific outcomes if available
    if (scenario && this.scenarioWeights[scenario] !== undefined) {
      // This is a simplified model - in a real implementation, 
      // we would have a more complex decision model per scenario
      const factor = this.scenarioWeights[scenario];
      // Adjust weights based on scenario factor
      weights[1] += factor * 0.2;
      weights[0] -= factor * 0.1;
      weights[2] -= factor * 0.1;
    }

    // Add noise to weights
    const noiseFactor = this.decisionNoise;
    for (let i = 0; i < weights.length; i++) {
      weights[i] += (Math.random() * 2 - 1) * noiseFactor;
      weights[i] = Math.max(0.05, weights[i]); // Ensure minimum probability
    }

    // Normalize weights
    const total = weights.reduce((a, b) => a + b, 0);
    weights = weights.map(w => w / total);

    // Choose outcome based on weights
    return this.weightedRandom(outcomes, weights);
  }

  /**
   * Run a Monte Carlo simulation
   * 
   * @param iterations Number of simulation iterations
   * @param scenarios Optional list of scenarios to simulate decisions for
   * @returns SimulationResult object with simulation results
   */
  public runSimulation(iterations: number = 100, scenarios?: string[]): SimulationResult {
    const traitVariations: Record<string, number[]> = {};
    const responseVariations: Record<string, number[]> = {};
    const decisionOutcomes: Record<string, number> = {};

    // Use profile scenarios if available and none specified
    if (!scenarios && Object.keys(this.scenarioWeights).length > 0) {
      scenarios = Object.keys(this.scenarioWeights);
    }

    // Use a default scenario if none specified
    if (!scenarios || scenarios.length === 0) {
      scenarios = ['default'];
    }

    for (let i = 0; i < iterations; i++) {
      // Simulate traits
      const simulatedTraits = this.simulateTraits();
      for (const [traitName, traitValue] of Object.entries(simulatedTraits)) {
        if (!traitVariations[traitName]) {
          traitVariations[traitName] = [];
        }
        traitVariations[traitName].push(traitValue);
      }

      // Simulate responses
      const simulatedResponses = this.simulateResponse();
      for (const [patternName, patternValue] of Object.entries(simulatedResponses)) {
        if (!responseVariations[patternName]) {
          responseVariations[patternName] = [];
        }
        responseVariations[patternName].push(patternValue);
      }

      // Simulate decisions for each scenario
      for (const scenario of scenarios) {
        const outcome = this.simulateDecision(scenario);
        const key = `${scenario}_${outcome}`;
        decisionOutcomes[key] = (decisionOutcomes[key] || 0) + 1;
      }
    }

    // Calculate summary statistics
    const summaryStats: Record<string, any> = {};

    // Trait stats
    for (const [traitName, values] of Object.entries(traitVariations)) {
      summaryStats[`${traitName}_mean`] = this.mean(values);
      summaryStats[`${traitName}_std`] = this.stdDev(values);
      summaryStats[`${traitName}_min`] = Math.min(...values);
      summaryStats[`${traitName}_max`] = Math.max(...values);
    }

    // Response stats
    for (const [patternName, values] of Object.entries(responseVariations)) {
      summaryStats[`${patternName}_mean`] = this.mean(values);
      summaryStats[`${patternName}_std`] = this.stdDev(values);
    }

    // Decision stats
    for (const [outcome, count] of Object.entries(decisionOutcomes)) {
      summaryStats[`${outcome}_probability`] = count / iterations;
    }

    return {
      profileName: this.profile.digital_archetype.name,
      iterations,
      traitVariations,
      responseVariations,
      decisionOutcomes,
      summaryStats,
    };
  }

  /**
   * Generate a human-readable summary of simulation results
   * 
   * @param result SimulationResult object
   * @returns Summary string
   */
  public summarizeSimulation(result: SimulationResult): string {
    const summary = [
      `Monte Carlo Simulation Results for '${result.profileName}'`,
      `Iterations: ${result.iterations}`,
      '',
      'Personality Trait Variations:',
    ];

    // Format trait statistics
    for (const traitName of Object.keys(result.traitVariations).sort()) {
      const mean = result.summaryStats[`${traitName}_mean`];
      const std = result.summaryStats[`${traitName}_std`];
      const minVal = result.summaryStats[`${traitName}_min`];
      const maxVal = result.summaryStats[`${traitName}_max`];

      summary.push(
        `  ${traitName}: mean=${mean.toFixed(2)}, std=${std.toFixed(2)}, ` +
        `range=[${minVal.toFixed(2)}, ${maxVal.toFixed(2)}]`
      );
    }

    summary.push('');
    summary.push('Response Pattern Variations:');

    // Format response statistics
    for (const patternName of Object.keys(result.responseVariations).sort()) {
      const mean = result.summaryStats[`${patternName}_mean`];
      const std = result.summaryStats[`${patternName}_std`];

      summary.push(`  ${patternName}: mean=${mean.toFixed(2)}, std=${std.toFixed(2)}`);
    }

    summary.push('');
    summary.push('Decision Outcomes:');

    // Group decision outcomes by scenario
    const scenarioOutcomes: Record<string, Record<string, number>> = {};
    for (const [outcomeKey, count] of Object.entries(result.decisionOutcomes)) {
      const [scenario, outcome] = outcomeKey.split('_', 2);
      if (!scenarioOutcomes[scenario]) {
        scenarioOutcomes[scenario] = {};
      }
      scenarioOutcomes[scenario][outcome] = count;
    }

    // Format decision statistics
    for (const [scenario, outcomes] of Object.entries(scenarioOutcomes)) {
      summary.push(`  Scenario: ${scenario}`);
      const total = Object.values(outcomes).reduce((a, b) => a + b, 0);
      for (const [outcome, count] of Object.entries(outcomes).sort()) {
        const percentage = (count / total) * 100;
        summary.push(`    ${outcome}: ${count} (${percentage.toFixed(1)}%)`);
      }
    }

    return summary.join('\n');
  }

  /**
   * Generate a random number from a normal distribution
   * 
   * @param mean Mean of the distribution
   * @param stdDev Standard deviation of the distribution
   * @returns Random number from the normal distribution
   */
  private normalRandom(mean: number, stdDev: number): number {
    // Box-Muller transform
    const u1 = Math.random();
    const u2 = Math.random();
    const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
    return z0 * stdDev + mean;
  }

  /**
   * Calculate the mean of an array of numbers
   * 
   * @param values Array of numbers
   * @returns Mean value
   */
  private mean(values: number[]): number {
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  /**
   * Calculate the standard deviation of an array of numbers
   * 
   * @param values Array of numbers
   * @returns Standard deviation
   */
  private stdDev(values: number[]): number {
    const avg = this.mean(values);
    const squareDiffs = values.map(value => {
      const diff = value - avg;
      return diff * diff;
    });
    const avgSquareDiff = this.mean(squareDiffs);
    return Math.sqrt(avgSquareDiff);
  }

  /**
   * Choose a random value from an array based on weights
   * 
   * @param values Array of values to choose from
   * @param weights Array of weights for each value
   * @returns Randomly selected value
   */
  private weightedRandom(values: string[], weights: number[]): string {
    const r = Math.random();
    let cumulativeWeight = 0;
    
    for (let i = 0; i < values.length; i++) {
      cumulativeWeight += weights[i];
      if (r <= cumulativeWeight) {
        return values[i];
      }
    }
    
    return values[values.length - 1]; // Fallback
  }
}
