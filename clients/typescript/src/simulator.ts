/**
 * Simulator for Tanzo profiles
 */

import { 
  Archetype, 
  Attribute, 
  ComparisonOperator,
  Effect, 
  Modifier, 
  OperationType, 
  TanzoProfile 
} from './schema';

/**
 * State tracked during a simulation run
 */
interface SimulationState {
  archetypeValues: Record<string, number>;
  attributeValues: Record<string, number>;
  activeModifiers: Modifier[];
}

/**
 * Apply a modifier effect to the simulation state
 */
function applyEffect(
  effect: Effect, 
  state: SimulationState, 
  archetypesByName: Record<string, Archetype>
): void {
  // Check if condition is met (if any)
  if (effect.condition) {
    const attrName = effect.condition.attribute;
    if (!(attrName in state.attributeValues)) {
      return; // Attribute not found, can't apply condition
    }
    
    const attrVal = state.attributeValues[attrName];
    const condVal = effect.condition.value;
    
    // Evaluate the condition
    switch (effect.condition.operator) {
      case 'eq':
        if (attrVal !== condVal) return;
        break;
      case 'neq':
        if (attrVal === condVal) return;
        break;
      case 'gt':
        if (attrVal <= condVal) return;
        break;
      case 'lt':
        if (attrVal >= condVal) return;
        break;
      case 'gte':
        if (attrVal < condVal) return;
        break;
      case 'lte':
        if (attrVal > condVal) return;
        break;
    }
  }
  
  // Apply the effect
  const target = effect.target;
  const value = effect.value;
  
  // Check if target is an archetype
  if (target in archetypesByName) {
    const current = state.archetypeValues[target] || 0.0;
    let newVal = current;
    
    switch (effect.operation) {
      case 'add':
        newVal = current + value;
        break;
      case 'multiply':
        newVal = current * value;
        break;
      case 'set':
        newVal = value;
        break;
      case 'min':
        newVal = Math.min(current, value);
        break;
      case 'max':
        newVal = Math.max(current, value);
        break;
    }
    
    // Clamp value to [0, 1]
    state.archetypeValues[target] = Math.max(0.0, Math.min(1.0, newVal));
  }
  // Otherwise assume it's an attribute
  else if (target in state.attributeValues) {
    const current = state.attributeValues[target];
    let newVal = current;
    
    switch (effect.operation) {
      case 'add':
        newVal = current + value;
        break;
      case 'multiply':
        newVal = current * value;
        break;
      case 'set':
        newVal = value;
        break;
      case 'min':
        newVal = Math.min(current, value);
        break;
      case 'max':
        newVal = Math.max(current, value);
        break;
    }
    
    // Clamp value to [0, 1]
    state.attributeValues[target] = Math.max(0.0, Math.min(1.0, newVal));
  }
}

/**
 * Simulate a single run of a Tanzo profile
 */
export function simulateProfile(
  profile: TanzoProfile,
  options: {
    randomize?: boolean;
    seed?: number;
  } = {}
): Record<string, number> {
  const { randomize = false, seed } = options;
  
  // Set random seed if provided
  if (seed !== undefined) {
    // Simple seeded random function 
    // This is a basic implementation - a real library would use a more robust method
    Math.random = (() => {
      let s = seed;
      return () => {
        s = Math.sin(s) * 10000;
        return s - Math.floor(s);
      };
    })();
  }
  
  // Initialize state
  const state: SimulationState = {
    archetypeValues: {},
    attributeValues: {},
    activeModifiers: []
  };
  
  // Get all archetypes by name for easy lookup
  const archetypesByName: Record<string, Archetype> = {};
  for (const archetype of profile.profile.archetypes) {
    archetypesByName[archetype.name] = archetype;
  }
  
  // Initialize attribute values
  for (const archetype of profile.profile.archetypes) {
    // Store base archetype value from weight
    state.archetypeValues[archetype.name] = archetype.weight;
    
    if (archetype.attributes) {
      for (const attr of archetype.attributes) {
        // Apply variance if randomize is enabled
        let value = attr.value;
        if (randomize && attr.variance) {
          // Use normal distribution centered on value with variance as std dev
          // Box-Muller transform for normal distribution
          const u1 = Math.random();
          const u2 = Math.random();
          const z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
          value = value + z * attr.variance;
          // Clamp to [0, 1]
          value = Math.max(0.0, Math.min(1.0, value));
        }
        
        state.attributeValues[attr.name] = value;
      }
    }
  }
  
  // Apply global modifiers
  if (profile.profile.modifiers) {
    for (const modifier of profile.profile.modifiers) {
      applyEffect(modifier.effect, state, archetypesByName);
      state.activeModifiers.push(modifier);
    }
  }
  
  // Apply archetype-specific modifiers
  for (const archetype of profile.profile.archetypes) {
    if (archetype.modifiers) {
      for (const modifier of archetype.modifiers) {
        applyEffect(modifier.effect, state, archetypesByName);
        state.activeModifiers.push(modifier);
      }
    }
  }
  
  // Merge results
  return {
    ...state.attributeValues,
    ...state.archetypeValues
  };
}

/**
 * Run a Monte Carlo simulation with many iterations
 */
export function runMonteCarlo(
  profile: TanzoProfile,
  iterations: number = 100
): {
  means: Record<string, number>;
  stdevs: Record<string, number>;
} {
  // Track results across iterations
  const results: Record<string, number>[] = [];
  
  for (let i = 0; i < iterations; i++) {
    // Use a different seed for each iteration for reproducibility
    const simResult = simulateProfile(profile, { 
      randomize: true, 
      seed: i 
    });
    results.push(simResult);
  }
  
  // Calculate statistics
  const allKeys = new Set<string>();
  for (const result of results) {
    Object.keys(result).forEach(key => allKeys.add(key));
  }
  
  const means: Record<string, number> = {};
  const stdevs: Record<string, number> = {};
  
  for (const key of allKeys) {
    const values = results.map(r => r[key] || 0.0);
    // Calculate mean
    means[key] = values.reduce((sum, val) => sum + val, 0) / values.length;
    
    // Calculate standard deviation
    const variance = values.reduce(
      (sum, val) => sum + Math.pow(val - means[key], 2), 
      0
    ) / values.length;
    stdevs[key] = Math.sqrt(variance);
  }
  
  return { means, stdevs };
}
