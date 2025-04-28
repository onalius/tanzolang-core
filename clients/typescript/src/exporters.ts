/**
 * Export utilities for TanzoLang profiles
 */
import * as fs from 'fs';
import * as yaml from 'js-yaml';
import { TanzoProfile } from './schema';

/**
 * Export a profile as a shorthand string representation
 * 
 * @param profile - The profile to export
 * @returns A shorthand string representation of the profile
 */
export function exportProfileShorthand(profile: TanzoProfile): string {
  const p = profile.profile;
  const archetype = p.archetype;
  
  // Start with name and primary archetype
  let shorthand = `${p.name} [${archetype.primary}`;
  
  // Add secondary archetype if present
  if (archetype.secondary) {
    shorthand += `/${archetype.secondary}`;
  }
  
  shorthand += "]";
  
  // Add personality traits if present
  if (p.personality?.traits) {
    const traits = p.personality.traits;
    shorthand += ` | O:${traits.openness?.toFixed(1) ?? '?'} C:${traits.conscientiousness?.toFixed(1) ?? '?'} `;
    shorthand += `E:${traits.extraversion?.toFixed(1) ?? '?'} A:${traits.agreeableness?.toFixed(1) ?? '?'} N:${traits.neuroticism?.toFixed(1) ?? '?'}`;
  }
  
  // Add communication style if present
  if (p.communication?.style) {
    shorthand += ` | ${p.communication.style}`;
    
    if (p.communication.tone) {
      shorthand += `, ${p.communication.tone}`;
    }
  }
  
  return shorthand;
}

/**
 * Export a profile as a JSON string or to a JSON file
 * 
 * @param profile - The profile to export
 * @param path - If provided, write the JSON to this file path
 * @returns The JSON string representation of the profile
 */
export function exportProfileJson(profile: TanzoProfile, path?: string): string {
  const jsonStr = JSON.stringify(profile, null, 2);
  
  if (path) {
    fs.writeFileSync(path, jsonStr, 'utf8');
  }
  
  return jsonStr;
}

/**
 * Export a profile as a YAML string or to a YAML file
 * 
 * @param profile - The profile to export
 * @param path - If provided, write the YAML to this file path
 * @returns The YAML string representation of the profile
 */
export function exportProfileYaml(profile: TanzoProfile, path?: string): string {
  const yamlStr = yaml.dump(profile, {
    sortKeys: false,
    lineWidth: 100
  });
  
  if (path) {
    fs.writeFileSync(path, yamlStr, 'utf8');
  }
  
  return yamlStr;
}
