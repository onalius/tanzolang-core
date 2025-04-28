/**
 * Validation functions for TanzoLang profiles.
 */

import * as fs from 'fs';
import * as path from 'path';
import { z } from 'zod';
import { parse, stringify } from 'yaml';
import { ProfileSchema, Profile } from './types';

/**
 * Load the TanzoLang JSON Schema
 * @returns The schema as an object
 */
export function loadSchema(): any {
  // Try to find the schema file in a few common locations
  const possiblePaths = [
    path.resolve(process.cwd(), 'spec/tanzo-schema.json'),
    path.resolve(__dirname, '../../../spec/tanzo-schema.json'),
    '/spec/tanzo-schema.json'
  ];

  for (const schemaPath of possiblePaths) {
    if (fs.existsSync(schemaPath)) {
      const schemaContent = fs.readFileSync(schemaPath, 'utf8');
      return JSON.parse(schemaContent);
    }
  }

  // If schema not found, throw an error
  throw new Error(
    'Could not find tanzo-schema.json. Make sure it exists in the spec directory.'
  );
}

/**
 * Validate a profile against the TanzoLang schema
 * @param profileData The profile data to validate
 * @returns True if valid, throws error if invalid
 */
export function validateProfile(profileData: any): boolean {
  try {
    // Validate with Zod schema
    ProfileSchema.parse(profileData);
    return true;
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(`Profile validation failed: ${error.message}`);
    }
    throw error;
  }
}

/**
 * Load and validate a profile from a file
 * @param filePath Path to the profile file (YAML or JSON)
 * @returns A validated profile object
 */
export function loadProfile(filePath: string): Profile {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Profile file not found: ${filePath}`);
  }

  const fileContent = fs.readFileSync(filePath, 'utf8');
  let profileData: any;

  // Load file based on extension
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.yaml' || ext === '.yml') {
    profileData = parse(fileContent);
  } else if (ext === '.json') {
    profileData = JSON.parse(fileContent);
  } else {
    throw new Error(`Unsupported file format: ${ext}`);
  }

  // Validate with Zod schema
  return ProfileSchema.parse(profileData);
}

/**
 * Save a profile to a file
 * @param profile The profile to save
 * @param filePath Path where to save the file
 * @param format Format to save as ('yaml' or 'json')
 */
export function saveProfile(
  profile: Profile,
  filePath: string,
  format: 'yaml' | 'json' = 'yaml'
): void {
  // Remove undefined properties
  const cleanProfile = JSON.parse(JSON.stringify(profile));

  // Save in requested format
  if (format === 'yaml') {
    fs.writeFileSync(filePath, stringify(cleanProfile));
  } else if (format === 'json') {
    fs.writeFileSync(filePath, JSON.stringify(cleanProfile, null, 2));
  } else {
    throw new Error(`Unsupported format: ${format}. Use 'yaml' or 'json'.`);
  }
}
