/**
 * TanzoLang TypeScript SDK
 * 
 * This package provides tools for working with TanzoLang profiles including:
 * - Zod schemas for type-safe access to profile data
 * - Validation against the official TanzoLang JSON Schema
 * - Simulation utilities for Monte Carlo trials
 * - Export functionality for serialization
 */

import * as schemas from './schemas';
import Ajv from 'ajv';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

/**
 * Load the TanzoLang JSON Schema
 */
export function loadSchema(): object {
  const schemaPath = path.resolve(__dirname, '../../../spec/tanzo-schema.json');
  try {
    const schemaContent = fs.readFileSync(schemaPath, 'utf-8');
    return JSON.parse(schemaContent);
  } catch (error) {
    throw new Error(`Failed to load schema: ${error}`);
  }
}

/**
 * Load a TanzoLang document from a file path
 * 
 * Supports both JSON and YAML formats
 */
export function loadDocument(filePath: string): object {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const extension = path.extname(filePath).toLowerCase();
    
    if (extension === '.yaml' || extension === '.yml') {
      return yaml.load(content) as object;
    } else {
      return JSON.parse(content);
    }
  } catch (error) {
    throw new Error(`Failed to load document: ${error}`);
  }
}

/**
 * Validate a TanzoLang document against the schema
 * 
 * @param document The document to validate
 * @param schema Optional schema to validate against
 * @returns A list of validation errors
 */
export function validateDocument(
  document: object,
  schema: object = loadSchema()
): string[] {
  const ajv = new Ajv();
  const validate = ajv.compile(schema);
  const valid = validate(document);
  
  if (valid) {
    return [];
  } else {
    return validate.errors?.map(error => 
      `${error.instancePath}: ${error.message}`
    ) || [];
  }
}

/**
 * Parse a document into a type-safe TanzoDocument
 * 
 * @param document The document to parse
 * @returns A parsed TanzoDocument
 * @throws Error if the document is invalid
 */
export function parseDocument(document: object): schemas.TanzoDocument {
  const errors = validateDocument(document);
  
  if (errors.length > 0) {
    throw new Error(`Invalid TanzoLang document: ${errors.join('; ')}`);
  }
  
  // Parse using Zod schema
  return schemas.tanzoDocumentSchema.parse(document);
}

/**
 * Run a Monte Carlo simulation on a TanzoLang profile
 * 
 * @param document The document to simulate
 * @param iterations The number of simulation iterations to run
 * @returns Simulation results
 */
export function runSimulation(
  document: object | schemas.TanzoDocument,
  iterations: number = 100
): schemas.SimulationResult {
  // Parse the document if it's not already a TanzoDocument
  const tanzoDoc = 'profile' in document ? 
    document as schemas.TanzoDocument : 
    parseDocument(document);
  
  // Implementation of simulation logic
  // This is a simplified version compared to the Python implementation
  const profile = tanzoDoc.profile;
  const results: schemas.SimulationResult = {
    traitMeans: {},
    traitStdDevs: {},
    archetypeWeights: {},
    numIterations: iterations
  };
  
  // Record original archetype weights
  for (const archetype of profile.archetypes) {
    results.archetypeWeights[archetype.type] = archetype.weight;
    results.traitMeans[archetype.type] = {};
    results.traitStdDevs[archetype.type] = {};
    
    if (archetype.traits) {
      // Collect trait values over all iterations
      const traitValues: Record<string, number[]> = {};
      
      for (const trait of archetype.traits) {
        traitValues[trait.name] = [];
        
        // Simulate trait values across iterations
        for (let i = 0; i < iterations; i++) {
          const variance = trait.variance || 0.1;
          // Generate random value using normal distribution
          let value = trait.value + 
            (Math.random() + Math.random() + Math.random() + Math.random() + 
             Math.random() + Math.random() - 3) * variance;
          // Clamp to [0, 1]
          value = Math.max(0, Math.min(1, value));
          traitValues[trait.name].push(value);
        }
        
        // Calculate mean
        const mean = traitValues[trait.name].reduce((a, b) => a + b, 0) / iterations;
        results.traitMeans[archetype.type][trait.name] = mean;
        
        // Calculate standard deviation
        const variance = traitValues[trait.name].reduce(
          (sum, val) => sum + Math.pow(val - mean, 2), 0
        ) / iterations;
        results.traitStdDevs[archetype.type][trait.name] = Math.sqrt(variance);
      }
    }
  }
  
  return results;
}

/**
 * Export a TanzoLang document to a shorthand string representation
 * 
 * @param document The document to export
 * @returns A shorthand string representation
 */
export function exportShorthand(
  document: object | schemas.TanzoDocument
): string {
  // Parse the document if it's not already a TanzoDocument
  const tanzoDoc = 'profile' in document ? 
    document as schemas.TanzoDocument : 
    parseDocument(document);
  
  const profile = tanzoDoc.profile;
  
  // Start with profile name
  const parts: string[] = [profile.name];
  
  // Add archetypes
  const archetypeParts: string[] = [];
  for (const archetype of profile.archetypes) {
    let aPart = `${archetype.type.substring(0, 3)}:${archetype.weight.toFixed(1)}`;
    
    // Add traits if available
    if (archetype.traits && archetype.traits.length > 0) {
      const traitParts = archetype.traits.map(
        trait => `${trait.name}:${trait.value.toFixed(1)}`
      );
      
      if (traitParts.length > 0) {
        aPart += `(${traitParts.join(',')})`;
      }
    }
    
    archetypeParts.push(aPart);
  }
  
  parts.push(archetypeParts.join('|'));
  
  return parts.join(' - ');
}

// Export the schemas
export { schemas };
