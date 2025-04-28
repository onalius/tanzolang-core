/**
 * Validation functions for Tanzo profiles
 */

import { z } from 'zod';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { TanzoProfile } from './models';

/**
 * Result of a validation operation
 */
export interface ValidationResult {
  isValid: boolean;
  errors?: string[];
}

/**
 * Load a YAML file into a JavaScript object
 * 
 * @param filePath Path to the YAML file
 * @returns The parsed YAML content
 */
export function loadYamlFile(filePath: string): any {
  const content = fs.readFileSync(filePath, 'utf8');
  return yaml.load(content);
}

/**
 * Validate a Tanzo profile against the schema
 * 
 * @param data Either a JavaScript object containing profile data, a file path to a YAML file,
 *             or a string containing YAML content
 * @returns A ValidationResult object with validation status and any errors
 */
export function validateTanzoProfile(data: any | string): ValidationResult {
  let profileData: any;
  
  // Process the input data
  if (typeof data === 'object' && data !== null) {
    profileData = data;
  } else if (typeof data === 'string') {
    // Check if it's a file path
    if (fs.existsSync(data) && fs.statSync(data).isFile()) {
      try {
        profileData = loadYamlFile(data);
      } catch (error) {
        return {
          isValid: false,
          errors: [`Failed to load YAML file: ${(error as Error).message}`]
        };
      }
    } else {
      // Assume it's YAML content
      try {
        profileData = yaml.load(data);
        if (typeof profileData !== 'object' || profileData === null) {
          return {
            isValid: false,
            errors: ['YAML content does not represent an object']
          };
        }
      } catch (error) {
        return {
          isValid: false,
          errors: [`Invalid YAML content: ${(error as Error).message}`]
        };
      }
    }
  } else {
    return {
      isValid: false,
      errors: ['Input must be an object, file path, or YAML string']
    };
  }

  // Validate with Zod
  const result = TanzoProfile.safeParse(profileData);
  
  if (!result.success) {
    // Format Zod errors
    const formattedErrors = result.error.errors.map(err => {
      const path = err.path.join('.');
      return `${path ? path + ': ' : ''}${err.message}`;
    });
    
    return {
      isValid: false,
      errors: formattedErrors
    };
  }
  
  return { isValid: true };
}
