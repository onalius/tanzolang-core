/**
 * Validator for TanzoLang profiles.
 * 
 * This module provides functionality to validate TanzoLang profiles against the schema.
 */

import * as fs from 'fs';
import * as path from 'path';
import { YAML } from 'yaml';
import { z } from 'zod';
import { tanzoProfileSchema, TanzoProfile } from './schema';

export class TanzoValidator {
  private schema: any;

  /**
   * Initialize the validator with the schema.
   * 
   * @param schemaPath - Path to the schema file. If undefined, the default schema is used.
   */
  constructor(schemaPath?: string) {
    if (schemaPath) {
      this.schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
    } else {
      // Try to find the schema in the package
      try {
        // First, check if we're running from within the repository
        const repoSchemaPath = path.resolve(__dirname, '../../../spec/tanzo-schema.json');
        if (fs.existsSync(repoSchemaPath)) {
          this.schema = JSON.parse(fs.readFileSync(repoSchemaPath, 'utf8'));
        } else {
          // Then check for a bundled schema
          const bundledSchemaPath = path.resolve(__dirname, '../tanzo-schema.json');
          if (fs.existsSync(bundledSchemaPath)) {
            this.schema = JSON.parse(fs.readFileSync(bundledSchemaPath, 'utf8'));
          } else {
            throw new Error('Could not find the TanzoLang schema file.');
          }
        }
      } catch (error) {
        throw new Error(`Failed to load the TanzoLang schema: ${error}`);
      }
    }
  }

  /**
   * Validate a TanzoLang profile file against the schema.
   * 
   * @param filePath - Path to the profile file (JSON or YAML).
   * @returns True if the profile is valid.
   * @throws {Error} If the file cannot be found or if the profile is invalid.
   */
  public validateFile(filePath: string): boolean {
    if (!fs.existsSync(filePath)) {
      throw new Error(`Profile file not found: ${filePath}`);
    }

    // Load the profile from the file
    const fileContent = fs.readFileSync(filePath, 'utf8');
    let profileData: any;

    if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
      profileData = YAML.parse(fileContent);
    } else if (filePath.endsWith('.json')) {
      profileData = JSON.parse(fileContent);
    } else {
      throw new Error(`Unsupported file format: ${filePath}`);
    }

    return this.validate(profileData);
  }

  /**
   * Validate a TanzoLang profile against the schema.
   * 
   * @param profileData - The profile data to validate.
   * @returns True if the profile is valid.
   * @throws {Error} If the profile is invalid.
   */
  public validate(profileData: any): boolean {
    try {
      // Validate using Zod schema
      tanzoProfileSchema.parse(profileData);
      return true;
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new Error(`Profile validation failed: ${JSON.stringify(error.errors)}`);
      }
      throw new Error(`Profile validation failed: ${error}`);
    }
  }

  /**
   * Parse and validate a TanzoLang profile.
   * 
   * @param profileData - The profile data to parse and validate.
   * @returns The parsed and validated TanzoProfile.
   * @throws {Error} If the profile is invalid.
   */
  public parseProfile(profileData: any): TanzoProfile {
    try {
      return tanzoProfileSchema.parse(profileData);
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new Error(`Profile parsing failed: ${JSON.stringify(error.errors)}`);
      }
      throw new Error(`Profile parsing failed: ${error}`);
    }
  }
}
