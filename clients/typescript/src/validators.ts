/**
 * Validation utilities for TanzoLang schema.
 */

import { readFileSync } from 'fs';
import { parse } from 'yaml';
import { TanzoProfile, TanzoProfileSchema } from './models';

/**
 * Validate a profile object against the TanzoLang schema.
 * 
 * @param profile Profile object to validate
 * @returns The validated profile
 * @throws If validation fails
 */
export const validateProfile = (profile: TanzoProfile): TanzoProfile => {
  return TanzoProfileSchema.parse(profile);
};

/**
 * Load a profile from a YAML or JSON file.
 * 
 * @param filePath Path to YAML or JSON file
 * @returns Validated TanzoProfile object
 * @throws If the file format is not supported or validation fails
 */
export const loadProfile = (filePath: string): TanzoProfile => {
  const content = readFileSync(filePath, 'utf-8');
  
  let data: any;
  if (filePath.endsWith('.json')) {
    data = JSON.parse(content);
  } else if (filePath.endsWith('.yml') || filePath.endsWith('.yaml')) {
    data = parse(content);
  } else {
    throw new Error(`Unsupported file format: ${filePath}`);
  }
  
  return validateProfile(data);
};

/**
 * Save a profile to a YAML file.
 * 
 * @param profile TanzoProfile object
 * @param filePath Output file path
 */
export const saveProfileToYaml = (profile: TanzoProfile, filePath: string): void => {
  const yaml = require('yaml');
  const fs = require('fs');
  
  const validated = validateProfile(profile);
  const yamlStr = yaml.stringify(validated);
  
  fs.writeFileSync(filePath, yamlStr, 'utf-8');
};

/**
 * Save a profile to a JSON file.
 * 
 * @param profile TanzoProfile object
 * @param filePath Output file path
 */
export const saveProfileToJson = (profile: TanzoProfile, filePath: string): void => {
  const fs = require('fs');
  
  const validated = validateProfile(profile);
  const jsonStr = JSON.stringify(validated, null, 2);
  
  fs.writeFileSync(filePath, jsonStr, 'utf-8');
};
