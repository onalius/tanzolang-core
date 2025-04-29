/**
 * Exporter for TanzoLang profiles.
 * 
 * This module provides functionality to export TanzoLang profiles in different formats.
 */

import * as fs from 'fs';
import { YAML } from 'yaml';
import { Archetype, Skill, TanzoProfile } from './schema';
import { TanzoValidator } from './validator';

export class TanzoExporter {
  private validator: TanzoValidator;
  private profile?: TanzoProfile;

  /**
   * Initialize the exporter with an optional profile.
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
   * Export the profile to JSON.
   * 
   * @param pretty - Whether to format the JSON with indentation.
   * @returns The profile as a JSON string.
   * @throws {Error} If no profile has been loaded.
   */
  public exportJson(pretty: boolean = true): string {
    if (!this.profile) {
      throw new Error('No profile has been loaded.');
    }

    if (pretty) {
      return JSON.stringify(this.profile, null, 2);
    } else {
      return JSON.stringify(this.profile);
    }
  }

  /**
   * Export the profile to YAML.
   * 
   * @returns The profile as a YAML string.
   * @throws {Error} If no profile has been loaded.
   */
  public exportYaml(): string {
    if (!this.profile) {
      throw new Error('No profile has been loaded.');
    }

    return YAML.stringify(this.profile);
  }

  /**
   * Export the profile to a shorthand string format.
   * 
   * This provides a compact representation of the profile for quick reference.
   * 
   * @returns A shorthand string representation of the profile.
   * @throws {Error} If no profile has been loaded.
   */
  public exportShorthand(): string {
    if (!this.profile) {
      throw new Error('No profile has been loaded.');
    }

    const profile = this.profile.profile;
    const result: string[] = [`${profile.identity.name} v${profile.identity.version}`];
    
    // Add tags if they exist
    if (profile.identity.tags && profile.identity.tags.length > 0) {
      result.push(`Tags: ${profile.identity.tags.join(', ')}`);
    }
    
    // Add archetypes
    result.push(`Archetypes (${profile.archetypes.length}):`);
    
    for (const archetype of profile.archetypes) {
      const core = archetype.attributes.core;
      const skillsCount = archetype.attributes.capabilities.skills.length;
      const behaviorsCount = (archetype.attributes.capabilities.behaviors || []).length;
      
      result.push(
        `  - ${core.name} (${archetype.type}, ${archetype.weight.toFixed(2)}): ` +
        `${skillsCount} skills, ${behaviorsCount} behaviors`
      );
      
      // Add top skills
      if (archetype.attributes.capabilities.skills.length > 0) {
        const topSkills = [...archetype.attributes.capabilities.skills]
          .sort((a, b) => b.proficiency - a.proficiency)
          .slice(0, 3);  // Top 3 skills
        
        result.push('    Top skills:');
        for (const skill of topSkills) {
          result.push(`      * ${skill.name} (${skill.proficiency.toFixed(2)})`);
        }
      }
    }
    
    return result.join('\n');
  }
}
