/**
 * Exporter for TanzoLang profiles to various formats
 */

import { TanzoProfileType } from './models';
import * as fs from 'fs';

/**
 * Exporter for TanzoLang profiles
 */
export class TanzoExporter {
  private profile: TanzoProfileType;

  /**
   * Initialize the exporter with a profile
   * 
   * @param profile TanzoProfile instance
   */
  constructor(profile: TanzoProfileType) {
    this.profile = profile;
  }

  /**
   * Export the profile to a plain object
   * Removes undefined/null values
   * 
   * @returns Object representation of the profile
   */
  public toObject(): Record<string, any> {
    return this.removeEmpty(JSON.parse(JSON.stringify(this.profile)));
  }

  /**
   * Export the profile to a JSON string
   * 
   * @param indent Number of spaces for indentation
   * @returns JSON string representation of the profile
   */
  public toJson(indent: number = 2): string {
    return JSON.stringify(this.toObject(), null, indent);
  }

  /**
   * Export the profile to a YAML string
   * 
   * @returns YAML string representation of the profile
   */
  public toYaml(): string {
    try {
      const yaml = require('js-yaml');
      return yaml.dump(this.toObject(), { sortKeys: false });
    } catch (error) {
      console.error('js-yaml is required to generate YAML. Please install it with: npm install js-yaml');
      throw new Error('js-yaml is required to generate YAML');
    }
  }

  /**
   * Export the profile to a shorthand string format
   * This is a compact representation for quick reference
   * 
   * @returns Shorthand string representation of the profile
   */
  public toShorthand(): string {
    const da = this.profile.digital_archetype;
    const attributes = this.profile.attributes;
    
    // Name, category and top traits
    const parts: string[] = [
      `${da.name} (${da.category})`,
      'Traits:',
      Object.entries(attributes.personality.traits)
        .map(([k, v]) => `${k.charAt(0).toUpperCase() + k.slice(1)}: ${v}`)
        .join(', '),
    ];
    
    // Top 3 skills
    const capabilities = attributes.abilities.core_capabilities;
    if (capabilities && capabilities.length > 0) {
      const skills = capabilities.slice(0, 3);
      if (capabilities.length > 3) {
        skills.push('...');
      }
      parts.push('Skills: ' + skills.join(', '));
    }
    
    // Knowledge domains
    const domains = attributes.knowledge.domains;
    if (domains && domains.length > 0) {
      const domainList = domains.slice(0, 3);
      if (domains.length > 3) {
        domainList.push('...');
      }
      parts.push(
        `Knowledge (${attributes.knowledge.expertise_level}): ` + 
        domainList.join(', ')
      );
    }
    
    // Basic metadata
    if (this.profile.metadata && this.profile.metadata.author) {
      parts.push(`By: ${this.profile.metadata.author}`);
    }
    
    parts.push(`Version: ${this.profile.profile_version}`);
    
    return parts.join(' | ');
  }

  /**
   * Save the profile to a JSON file
   * 
   * @param filePath Path to save the file
   * @param indent Number of spaces for indentation
   */
  public saveJson(filePath: string, indent: number = 2): void {
    fs.writeFileSync(filePath, this.toJson(indent), 'utf8');
  }

  /**
   * Save the profile to a YAML file
   * 
   * @param filePath Path to save the file
   */
  public saveYaml(filePath: string): void {
    fs.writeFileSync(filePath, this.toYaml(), 'utf8');
  }

  /**
   * Recursively remove empty values (null, undefined) from an object
   * 
   * @param obj Object to clean
   * @returns Cleaned object without empty values
   */
  private removeEmpty(obj: any): any {
    if (Array.isArray(obj)) {
      return obj
        .map(v => this.removeEmpty(v))
        .filter(v => v !== undefined && v !== null);
    } else if (obj !== null && typeof obj === 'object') {
      return Object.entries(obj)
        .map(([k, v]) => [k, this.removeEmpty(v)])
        .filter(([_, v]) => v !== undefined && v !== null)
        .reduce((a, [k, v]) => ({ ...a, [k]: v }), {});
    }
    return obj;
  }
}
