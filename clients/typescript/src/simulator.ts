/**
 * Simulator for TanzoLang profiles.
 * 
 * This module provides functionality to simulate TanzoLang profiles through
 * Monte Carlo trials.
 */

import * as fs from 'fs';
import { YAML } from 'yaml';
import { Archetype, Behavior, Skill, TanzoProfile } from './schema';
import { TanzoValidator } from './validator';

interface SkillUsage {
  proficiency: number;
  success_rate: number;
  average_score: number;
}

interface BehaviorOccurrence {
  probability: number;
  occurrences: number;
  percentage: number;
}

interface ArchetypeSimulation {
  behavior_occurrences: Record<string, BehaviorOccurrence>;
  skill_usage: Record<string, SkillUsage>;
}

interface ArchetypeResult {
  name: string;
  weight: number;
  type: string;
  simulation: ArchetypeSimulation;
}

interface BehaviorResult {
  probability: number;
  weighted_probability: number;
  occurrences: number;
}

interface SkillResult {
  proficiency: number;
  weighted_proficiency: number;
}

interface SimulationResults {
  profile_name: string;
  iterations: number;
  archetypes: ArchetypeResult[];
  behaviors: Record<string, BehaviorResult>;
  skills: Record<string, SkillResult>;
}

export class TanzoSimulator {
  private validator: TanzoValidator;
  private profile?: TanzoProfile;

  /**
   * Initialize the simulator with an optional profile.
   * 
   * @param profile - A TanzoLang profile, which can be a file path, an object, or a TanzoProfile.
   */
  constructor(profile?: string | any | TanzoProfile) {
    this.validator = new TanzoValidator();
    
    if (profile) {
      this.loadProfile(profile);
    }
  }

  /**
   * Load a TanzoLang profile.
   * 
   * @param profile - A TanzoLang profile, which can be a file path, an object, or a TanzoProfile.
   * @throws {Error} If the profile file cannot be found or if the profile is invalid.
   */
  public loadProfile(profile: string | any | TanzoProfile): void {
    if (typeof profile === 'string') {
      // Load the profile from a file
      const fileContent = fs.readFileSync(profile, 'utf8');
      let profileData: any;

      if (profile.endsWith('.yaml') || profile.endsWith('.yml')) {
        profileData = YAML.parse(fileContent);
      } else if (profile.endsWith('.json')) {
        profileData = JSON.parse(fileContent);
      } else {
        throw new Error(`Unsupported file format: ${profile}`);
      }
      
      // Validate the profile
      this.validator.validate(profileData);
      this.profile = this.validator.parseProfile(profileData);
    } else if (typeof profile === 'object') {
      // Validate the profile as an object
      this.validator.validate(profile);
      this.profile = this.validator.parseProfile(profile);
    } else {
      throw new Error(`Unsupported profile type: ${typeof profile}`);
    }
  }

  /**
   * Run a Monte Carlo simulation on the profile.
   * 
   * @param iterations - Number of iterations to run.
   * @returns A object containing the simulation results.
   * @throws {Error} If no profile has been loaded.
   */
  public runSimulation(iterations: number = 100): SimulationResults {
    if (!this.profile) {
      throw new Error('No profile has been loaded.');
    }

    const results: SimulationResults = {
      profile_name: this.profile.profile.identity.name,
      iterations,
      archetypes: [],
      behaviors: {},
      skills: {},
    };

    // Process each archetype
    for (const archetype of this.profile.profile.archetypes) {
      const archetypeResults = this.simulateArchetype(archetype, iterations);
      results.archetypes.push({
        name: archetype.attributes.core.name,
        weight: archetype.weight,
        type: archetype.type,
        simulation: archetypeResults,
      });
      
      // Aggregate behavior probabilities
      const behaviors = archetype.attributes.capabilities.behaviors || [];
      for (const behavior of behaviors) {
        if (!results.behaviors[behavior.name]) {
          results.behaviors[behavior.name] = {
            probability: 0,
            weighted_probability: 0,
            occurrences: 0,
          };
        }
        
        const weightedProb = behavior.probability * archetype.weight;
        results.behaviors[behavior.name].probability = behavior.probability;
        results.behaviors[behavior.name].weighted_probability += weightedProb;
        results.behaviors[behavior.name].occurrences += Math.floor(
          weightedProb * iterations
        );
      }
      
      // Aggregate skill proficiencies
      for (const skill of archetype.attributes.capabilities.skills) {
        if (!results.skills[skill.name]) {
          results.skills[skill.name] = {
            proficiency: 0,
            weighted_proficiency: 0,
          };
        }
        
        const weightedProf = skill.proficiency * archetype.weight;
        results.skills[skill.name].proficiency = skill.proficiency;
        results.skills[skill.name].weighted_proficiency += weightedProf;
      }
    }

    return results;
  }

  /**
   * Simulate a single archetype.
   * 
   * @param archetype - The archetype to simulate.
   * @param iterations - Number of iterations to run.
   * @returns A object containing the simulation results for the archetype.
   */
  private simulateArchetype(archetype: Archetype, iterations: number): ArchetypeSimulation {
    const results: ArchetypeSimulation = {
      behavior_occurrences: {},
      skill_usage: {},
    };

    // Simulate behaviors
    const behaviors = archetype.attributes.capabilities.behaviors || [];
    for (const behavior of behaviors) {
      let occurrences = 0;
      for (let i = 0; i < iterations; i++) {
        if (Math.random() < behavior.probability) {
          occurrences++;
        }
      }
      
      results.behavior_occurrences[behavior.name] = {
        probability: behavior.probability,
        occurrences,
        percentage: (occurrences / iterations) * 100,
      };
    }

    // Simulate skills
    for (const skill of archetype.attributes.capabilities.skills) {
      let successCount = 0;
      let totalScore = 0.0;
      
      for (let i = 0; i < iterations; i++) {
        // Simulate skill usage with proficiency as success probability
        const skillScore = Math.random();
        const isSuccessful = skillScore <= skill.proficiency;
        
        if (isSuccessful) {
          successCount++;
        }
        
        totalScore += skillScore;
      }
      
      results.skill_usage[skill.name] = {
        proficiency: skill.proficiency,
        success_rate: (successCount / iterations) * 100,
        average_score: totalScore / iterations,
      };
    }

    return results;
  }

  /**
   * Get a human-readable summary of the simulation results.
   * 
   * @param simulationResults - The simulation results. If undefined, runs a new simulation.
   * @returns A string containing the summary of the simulation results.
   * @throws {Error} If no profile has been loaded and no simulation results are provided.
   */
  public getSummary(simulationResults?: SimulationResults): string {
    if (!simulationResults) {
      if (!this.profile) {
        throw new Error('No profile has been loaded.');
      }
      simulationResults = this.runSimulation();
    }

    const summary: string[] = [
      `Simulation Summary for ${simulationResults.profile_name}`,
      `Iterations: ${simulationResults.iterations}`,
      '',
      'Archetype Weights:',
    ];

    // Add archetype information
    for (const archetype of simulationResults.archetypes) {
      summary.push(`  - ${archetype.name} (${archetype.type}): ${(archetype.weight * 100).toFixed(1)}%`);
    }

    // Add behavior probabilities
    if (Object.keys(simulationResults.behaviors).length > 0) {
      summary.push('');
      summary.push('Behavior Probabilities (Weighted by Archetype):');
      for (const [name, behavior] of Object.entries(simulationResults.behaviors)) {
        summary.push(
          `  - ${name}: ${(behavior.weighted_probability * 100).toFixed(1)}% ` +
          `(Expected occurrences: ${behavior.occurrences})`
        );
      }
    }

    // Add skill proficiencies
    if (Object.keys(simulationResults.skills).length > 0) {
      summary.push('');
      summary.push('Skill Proficiencies (Weighted by Archetype):');
      for (const [name, skill] of Object.entries(simulationResults.skills)) {
        summary.push(`  - ${name}: ${(skill.weighted_proficiency * 100).toFixed(1)}%`);
      }
    }

    // Add detailed archetype simulation results
    summary.push('');
    summary.push('Detailed Archetype Simulation Results:');
    for (const archetype of simulationResults.archetypes) {
      summary.push(`  ${archetype.name}:`);
      
      // Add behavior occurrences
      const behaviorOccurrences = archetype.simulation.behavior_occurrences;
      if (Object.keys(behaviorOccurrences).length > 0) {
        summary.push('    Behavior Occurrences:');
        for (const [name, occurrence] of Object.entries(behaviorOccurrences)) {
          summary.push(
            `      - ${name}: ${occurrence.occurrences} times ` +
            `(${occurrence.percentage.toFixed(1)}%)`
          );
        }
      }
      
      // Add skill usage
      const skillUsage = archetype.simulation.skill_usage;
      if (Object.keys(skillUsage).length > 0) {
        summary.push('    Skill Usage:');
        for (const [name, usage] of Object.entries(skillUsage)) {
          summary.push(
            `      - ${name}: ${usage.success_rate.toFixed(1)}% success rate ` +
            `(avg score: ${usage.average_score.toFixed(2)})`
          );
        }
      }
    }

    return summary.join('\n');
  }
}
