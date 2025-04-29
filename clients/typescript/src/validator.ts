/**
 * Validator functions for TanzoLang profiles.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { TanzoProfile, TanzoProfileSchema } from './models';
import { z } from 'zod';

/**
 * File formats supported for loading profiles.
 */
export type FileFormat = 'json' | 'yaml' | 'yml';

/**
 * Result of a profile validation.
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Load a profile from a file.
 *
 * @param filePath - The path to the profile file.
 * @returns The loaded profile data.
 * @throws Error if the file format is not supported or if the file cannot be read.
 */
export function loadProfile(filePath: string): any {
  // Check if file exists
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  // Read file content
  const content = fs.readFileSync(filePath, 'utf8');
  const extension = path.extname(filePath).toLowerCase();

  // Parse based on file extension
  if (extension === '.json') {
    return JSON.parse(content);
  } else if (extension === '.yaml' || extension === '.yml') {
    return yaml.load(content);
  } else {
    throw new Error(`Unsupported file format: ${extension}`);
  }
}

/**
 * Validate a profile using Zod schema.
 *
 * @param profile - The profile data to validate.
 * @returns Validation result with a list of errors if any.
 */
export function validateProfile(profile: any): ValidationResult {
  try {
    TanzoProfileSchema.parse(profile);
    return { valid: true, errors: [] };
  } catch (error) {
    if (error instanceof z.ZodError) {
      // Format Zod validation errors
      const errors = error.errors.map(
        (err) => `${err.path.join('.')}: ${err.message}`
      );
      return { valid: false, errors };
    }
    // Handle unexpected errors
    return {
      valid: false,
      errors: [`Unexpected validation error: ${String(error)}`],
    };
  }
}

/**
 * Validate a profile file.
 *
 * @param filePath - The path to the profile file.
 * @returns Validation result with a list of errors if any.
 * @throws Error if the file format is not supported or if the file cannot be read.
 */
export function validateProfileFile(filePath: string): ValidationResult {
  const profile = loadProfile(filePath);
  return validateProfile(profile);
}

/**
 * Check if a profile is valid.
 *
 * @param profile - The profile data to validate.
 * @returns True if the profile is valid, false otherwise.
 */
export function isValidProfile(profile: any): boolean {
  return validateProfile(profile).valid;
}

/**
 * Export a profile to a JSON string.
 *
 * @param profile - The profile to export.
 * @returns The profile as a JSON string.
 */
export function exportProfileToJson(profile: TanzoProfile): string {
  return JSON.stringify(profile, null, 2);
}

/**
 * Export a profile to a YAML string.
 *
 * @param profile - The profile to export.
 * @returns The profile as a YAML string.
 */
export function exportProfileToYaml(profile: TanzoProfile): string {
  return yaml.dump(profile, { indent: 2 });
}
