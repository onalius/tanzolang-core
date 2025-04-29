/**
 * Validation functions for TanzoLang profiles.
 * 
 * This module provides functions to validate TanzoLang profiles against
 * the schema and load profiles from various formats.
 */

import fs from 'fs';
import path from 'path';
import { ZodError } from 'zod';
import Ajv from 'ajv';
import YAML from 'yaml';

import { TanzoProfileSchema, TanzoProfile } from './schema';

/**
 * Load and parse the TanzoLang JSON schema
 * 
 * @returns The JSON schema as an object
 */
export function loadJsonSchema(): Record<string, any> {
  // Try to locate the schema in a few different places
  const possibleLocations = [
    path.resolve(process.cwd(), 'spec/tanzo-schema.json'),
    path.resolve(__dirname, '../../..', 'spec/tanzo-schema.json'),
    path.resolve(process.env.HOME || '', '.tanzo/tanzo-schema.json'),
  ];
  
  for (const location of possibleLocations) {
    try {
      const schema = JSON.parse(fs.readFileSync(location, 'utf-8'));
      return schema;
    } catch (error) {
      // Continue to the next location
    }
  }
  
  throw new Error(
    'Could not find tanzo-schema.json. Please ensure the tanzo-lang-core ' +
    'repository is properly installed or provide a path to the schema file.'
  );
}

/**
 * Validate data against the TanzoLang JSON schema using Ajv
 * 
 * @param data - The data to validate
 * @param schema - Optional schema to use instead of the default
 * @returns True if validation succeeds, throws exception otherwise
 */
export function validateWithAjv(
  data: Record<string, any>,
  schema?: Record<string, any>
): boolean {
  const ajv = new Ajv();
  const actualSchema = schema || loadJsonSchema();
  
  const validate = ajv.compile(actualSchema);
  const valid = validate(data);
  
  if (!valid && validate.errors) {
    throw new Error(`Validation failed: ${ajv.errorsText(validate.errors)}`);
  }
  
  return true;
}

/**
 * Validate data using Zod schema
 * 
 * @param data - The data to validate
 * @returns A validated TanzoProfile object
 */
export function validateWithZod(data: Record<string, any>): TanzoProfile {
  return TanzoProfileSchema.parse(data);
}

/**
 * Validate a TanzoLang profile using both Ajv and Zod
 * 
 * @param data - The profile data to validate
 * @param options - Validation options
 * @returns A validated TanzoProfile object
 */
export function validateTanzoProfile(
  data: Record<string, any>,
  options: {
    useAjv?: boolean;
    useZod?: boolean;
  } = { useAjv: true, useZod: true }
): TanzoProfile {
  const { useAjv = true, useZod = true } = options;
  
  if (useAjv) {
    validateWithAjv(data);
  }
  
  if (useZod) {
    return validateWithZod(data);
  }
  
  // If we don't use Zod validation but need to return a TanzoProfile
  return data as TanzoProfile;
}

/**
 * Load and validate a TanzoLang profile from a YAML file
 * 
 * @param filePath - Path to the YAML file
 * @returns A validated TanzoProfile object
 */
export function loadProfileFromYaml(filePath: string): TanzoProfile {
  const yamlContent = fs.readFileSync(filePath, 'utf-8');
  const data = YAML.parse(yamlContent);
  
  return validateTanzoProfile(data);
}

/**
 * Load and validate a TanzoLang profile from a JSON file
 * 
 * @param filePath - Path to the JSON file
 * @returns A validated TanzoProfile object
 */
export function loadProfileFromJson(filePath: string): TanzoProfile {
  const jsonContent = fs.readFileSync(filePath, 'utf-8');
  const data = JSON.parse(jsonContent);
  
  return validateTanzoProfile(data);
}
