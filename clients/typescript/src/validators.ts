/**
 * Validation utilities for TanzoLang profiles
 */
import { z } from 'zod';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { TanzoProfileSchema, TanzoProfile } from './schema';

/**
 * Validate a TanzoLang profile against the schema
 * 
 * @param profileData - Either a JSON/YAML string or an object containing the profile data
 * @returns A validated profile object
 * @throws Error if validation fails
 */
export function validateTanzoProfile(profileData: string | object): TanzoProfile {
  try {
    // Convert string to object if needed
    let profileObj: object;
    
    if (typeof profileData === 'string') {
      try {
        // Try JSON first
        profileObj = JSON.parse(profileData);
      } catch (jsonError) {
        // Try YAML next
        try {
          profileObj = yaml.load(profileData) as object;
          if (typeof profileObj !== 'object' || profileObj === null) {
            throw new Error('Invalid YAML: did not result in an object');
          }
        } catch (yamlError) {
          throw new Error(`Invalid profile format (not valid JSON or YAML): ${yamlError}`);
        }
      }
    } else {
      profileObj = profileData;
    }
    
    // Validate using Zod
    const result = TanzoProfileSchema.parse(profileObj);
    return result;
  } catch (error) {
    if (error instanceof z.ZodError) {
      const issues = error.issues.map(issue => 
        `${issue.path.join('.')}: ${issue.message}`
      ).join('\n');
      throw new Error(`Profile validation failed:\n${issues}`);
    }
    throw error;
  }
}

/**
 * Load and validate a TanzoLang profile from a YAML file
 * 
 * @param yamlPath - Path to the YAML file
 * @returns A validated profile object
 * @throws Error if the file cannot be found or validation fails
 */
export function loadProfileFromYaml(yamlPath: string): TanzoProfile {
  try {
    const yamlContent = fs.readFileSync(yamlPath, 'utf8');
    return validateTanzoProfile(yamlContent);
  } catch (error) {
    if (error instanceof Error && 'code' in error && error.code === 'ENOENT') {
      throw new Error(`Profile file not found: ${yamlPath}`);
    }
    throw error;
  }
}
