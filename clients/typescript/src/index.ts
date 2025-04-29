/**
 * Tanzo Schema TypeScript SDK
 */

import fs from 'fs';
import path from 'path';
import * as yaml from 'js-yaml';
import { ZodError } from 'zod';

import { 
  TanzoProfile, 
  TanzoProfileSchema, 
  ArchetypeSchema,
  TraitScoreSchema,
  SkillSchema,
  SimulationParametersSchema,
  MetadataSchema,
  ProfileType,
  DistributionType
} from './schema';

export { 
  TanzoProfile, 
  TanzoProfileSchema,
  ArchetypeSchema,
  TraitScoreSchema,
  SkillSchema,
  SimulationParametersSchema,
  MetadataSchema,
  ProfileType,
  DistributionType
};

/**
 * Custom error class for schema validation errors
 */
export class SchemaValidationError extends Error {
  details: Array<{ path: string; message: string }>;

  constructor(message: string, details: Array<{ path: string; message: string }> = []) {
    super(message);
    this.name = 'SchemaValidationError';
    this.details = details;
  }
}

/**
 * Get the path to the canonical schema file
 */
export function getSchemaPath(): string {
  // Try to find the schema in a few common locations
  const possiblePaths = [
    // From the project root
    path.join(process.cwd(), 'spec', 'tanzo-schema.json'),
    // From the package directory
    path.join(__dirname, '..', 'schema', 'tanzo-schema.json'),
    // From the parent project if used as a dependency
    path.join(process.cwd(), 'node_modules', 'tanzo-schema', 'schema', 'tanzo-schema.json'),
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      return p;
    }
  }

  throw new Error('Could not find tanzo-schema.json. Please ensure the schema file is accessible.');
}

/**
 * Load and parse a profile from a file path
 */
export function loadProfileFromFile(filePath: string): any {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  
  if (filePath.endsWith('.json')) {
    return JSON.parse(content);
  } else if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
    return yaml.load(content);
  } else {
    throw new Error('Unsupported file format. Expected .json, .yaml, or .yml');
  }
}

/**
 * Validate a Tanzo profile against the schema
 */
export function validateProfile(
  profileData: TanzoProfile | string | object
): TanzoProfile {
  // Handle different input types
  let profileObject: any;

  if (typeof profileData === 'string') {
    // Check if it's a file path
    if (fs.existsSync(profileData)) {
      profileObject = loadProfileFromFile(profileData);
    } else {
      // Try to parse as JSON or YAML
      try {
        if (profileData.trim().startsWith('{') || profileData.trim().startsWith('[')) {
          profileObject = JSON.parse(profileData);
        } else {
          profileObject = yaml.load(profileData);
        }
      } catch (error) {
        throw new SchemaValidationError(`Failed to parse profile data: ${(error as Error).message}`);
      }
    }
  } else {
    profileObject = profileData;
  }

  // Validate with Zod schema
  try {
    return TanzoProfileSchema.parse(profileObject);
  } catch (error) {
    if (error instanceof ZodError) {
      const details = error.errors.map(err => ({
        path: err.path.join('/'),
        message: err.message
      }));
      throw new SchemaValidationError('Profile validation failed', details);
    }
    throw new SchemaValidationError(`Validation error: ${(error as Error).message}`);
  }
}

/**
 * Create a new profile with defaults for required fields
 */
export function createProfile(partial: Partial<TanzoProfile> = {}): TanzoProfile {
  const defaults: TanzoProfile = {
    version: '0.1.0',
    profile_type: 'archetype_only',
    archetype: {
      name: 'New Archetype',
      core_traits: {
        intelligence: { base: 5.0 },
        creativity: { base: 5.0 },
        sociability: { base: 5.0 }
      },
      skills: [
        {
          name: 'Default Skill',
          proficiency: { base: 5.0 }
        }
      ]
    }
  };

  return { ...defaults, ...partial };
}
