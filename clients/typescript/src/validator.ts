/**
 * Validation utilities for TanzoLang profiles
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import Ajv from 'ajv';
import { TanzoProfile } from './models';
import { z } from 'zod';

/**
 * Load the TanzoLang JSON schema
 * 
 * @returns The JSON schema as an object
 */
export function loadSchema(): object {
  try {
    // Try to load from standard location relative to this file
    const schemaPath = path.resolve(__dirname, '../../../spec/tanzo-schema.json');
    if (fs.existsSync(schemaPath)) {
      return JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
    }

    // If not found, try to load from the package
    const packageSchemaPath = path.resolve(__dirname, '../schema/tanzo-schema.json');
    if (fs.existsSync(packageSchemaPath)) {
      return JSON.parse(fs.readFileSync(packageSchemaPath, 'utf-8'));
    }

    throw new Error('Cannot find the TanzoLang schema file');
  } catch (error) {
    throw new Error(`Failed to load schema: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * Load a YAML file into an object
 * 
 * @param filePath Path to the YAML file
 * @returns The parsed YAML content
 */
export function loadYamlFile(filePath: string): object {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return yaml.load(content) as object;
  } catch (error) {
    throw new Error(`Failed to load YAML file: ${error instanceof Error ? error.message : String(error)}`);
  }
}

/**
 * Validate a TanzoLang profile file against the JSON schema
 * 
 * @param filePath Path to the YAML or JSON file
 * @returns The validated profile as an object
 */
export function validateFile(filePath: string): object {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  // Load the file based on extension
  let data: object;
  const extension = path.extname(filePath).toLowerCase();
  
  if (extension === '.yaml' || extension === '.yml') {
    data = loadYamlFile(filePath);
  } else if (extension === '.json') {
    data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } else {
    throw new Error(`Unsupported file format: ${extension}`);
  }

  // Validate against schema
  const schema = loadSchema();
  const ajv = new Ajv();
  const validate = ajv.compile(schema);
  
  if (!validate(data)) {
    const errors = validate.errors?.map(e => `${e.instancePath} ${e.message}`).join(', ');
    throw new Error(`Schema validation failed: ${errors}`);
  }

  return data;
}

/**
 * Validate a TanzoLang profile and return a typed object
 * 
 * @param profilePath Path to the profile file
 * @returns A validated TanzoProfile object
 */
export function validateProfile(profilePath: string): TanzoProfile {
  // First validate using JSON Schema
  const data = validateFile(profilePath);
  
  // Then validate using Zod for stronger typing
  try {
    return TanzoProfile.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      const formattedErrors = error.errors.map(e => `${e.path.join('.')} ${e.message}`).join(', ');
      throw new Error(`Zod validation failed: ${formattedErrors}`);
    }
    throw error;
  }
}
