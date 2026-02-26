import { calculate, Generations, Pokemon, Move } from '@smogon/calc';
import { parseSmogonSet } from '../utils/parser.js';

// List attacker options variants
const ATTACKER_REPARTS = {
    //                 🔴 ATK/SPA                    🔴 Nature
    "default":        {maxAtk: false, maxSpa: false, nature: false},

    //                 🟢 ATK/SPA                    🔴 Nature
    "max-stats-atk":  {maxAtk: true,  maxSpa: false, nature: false},
    "max-stats-spa":  {maxAtk: false, maxSpa: true,  nature: false},

    //                 🟢 ATK/SPA                    🟢 Nature
    "max-atk":        {maxAtk: true,  maxSpa: false, nature: true },
    "max-spa":        {maxAtk: false, maxSpa: true,  nature: true },
};

// List defender options variants
const DEFENDER_REPARTS = {
    //                 🔴 HP        🔴 DEF/SPD                    🔴 Nature
    "default":        {maxHP: false, maxDef: false, maxSpd: false, nature: false},

    //                 🔴 HP        🟢 DEF/SPD                    🔴 Nature
    "max-stats-def":  {maxHP: false, maxDef: true,  maxSpd: false, nature: false},
    "max-stats-spd":  {maxHP: false, maxDef: false, maxSpd: true,  nature: false},

    //                 🔴 HP        🟢 DEF/SPD                    🟢 Nature
    "max-def":        {maxHP: false, maxDef: true,  maxSpd: false, nature: true},
    "max-spd":        {maxHP: false, maxDef: false, maxSpd: true,  nature: true },

    //                 🟢 HP        🔴 DEF/SPD                    🔴 Nature
    "max-hp":         {maxHP: true,  maxDef: false, maxSpd: false, nature: false},

    //                 🟢 HP        🟢 DEF/SPD                    🔴 Nature
    "max-stats-phys": {maxHP: true,  maxDef: true,  maxSpd: false, nature: false},
    "max-stats-spec": {maxHP: true,  maxDef: false, maxSpd: true,  nature: false},
   
    //                 🟢 HP        🟢 DEF/SPD                    🟢 Nature
    "max-phys":       {maxHP: true,  maxDef: true,  maxSpd: false, nature: true },
    "max-spec":       {maxHP: true,  maxDef: false, maxSpd: true,  nature: true },
};

/**
 * Create a pokemon based on its repart
 * @param {string} name - The name of the Pokemon
 * @param {object} repart - The specific repart for the Pokemon
 * @param {object} gen - The generation object
 */
function fromRepart(name, repart, gen) {
    return new Pokemon(gen, name, {
        // Define stats based on options
        evs: {
            hp:  repart.maxHP  ? 252 : 0,
            atk: repart.maxAtk ? 252 : 0,
            def: repart.maxDef ? 252 : 0,
            spa: repart.maxSpa ? 252 : 0,
            spd: repart.maxSpd ? 252 : 0,
        },
        nature: (repart.nature && repart.maxAtk) ? 'Lonely' :
                (repart.nature && repart.maxDef) ? 'Impish' :
                (repart.nature && repart.maxSpa) ? 'Rash'   :
                (repart.nature && repart.maxSpd) ? 'Calm'   :
                                                   'Quirky'
    });
}

/**
 * Calculate damage from a known attacker set to a defender whose set is unknown
 * @param {object} attackerSet - The Smogon set string for the attacker
 * @param {string} defenderName - The name of the defender Pokemon
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
export function calculateDamage_knownAttacker(attackerSet, defenderName, genId=9) {

    // Create generation object
    const gen = Generations.get(genId);
   
    // Create attacker Pokemon
    const attackerData = parseSmogonSet(attackerSet);
    const attacker = new Pokemon(gen, attackerData.name, {
        ...attackerData
    });

    // Create moves
    const moves = [];
    for (const moveName of attackerData.moves)
        moves.push(new Move(gen, moveName));

    // Prepare data container
    let data = {};

    // Calculate damages for each defender possible reparts
    for (const [key, opts] of Object.entries(DEFENDER_REPARTS)) {
        // Initialize data container
        data[key] = {};

        // Create defender Pokemon
        const defender = fromRepart(defenderName, opts, gen)

        for (const move of moves) {
            // Perform calculation
            const result = calculate(gen, attacker, defender, move);

            // Store parsed result
            data[key][move.name] = {
                min: result.damage.length ?
                     result.damage[0] :
                     result.damage,
                max: result.damage.length ?
                     result.damage[result.damage.length - 1] :
                     result.damage
            }
        }
    }
   
    return data;
}

/**
 * Calculate damage from an attacker whose set is unknown to a known defender set
 * @param {object} attackerName - The name of the attacker Pokemon
 * @param {string} defenderSet - The Smogon set string for the defender
 * @param {string} moveNames - The list of moves usable by the attacker to calculate damage for
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
export function calculateDamage_knownDefender(attackerName, defenderSet, moveNames, genId=9) {

    // Create generation object
    const gen = Generations.get(genId);
   
    // Create defender Pokemon
    const defenderData = parseSmogonSet(defenderSet);
    const defender = new Pokemon(gen, defenderData.name, {
        ...defenderData
    });

    // Create moves
    const moves = [];
    for (const moveName of moveNames)
        moves.push(new Move(gen, moveName));

    // Prepare data container
    let data = {};

    // Calculate damages for each attacker possible reparts
    for (const [key, opts] of Object.entries(ATTACKER_REPARTS)) {
        // Initialize data container
        data[key] = {};

        // Create attacker Pokemon
        const attacker = fromRepart(attackerName, opts, gen);

        for (const move of moves) {
            // Perform calculation
            const result = calculate(gen, attacker, defender, move);

            // Store parsed result
            data[key][move.name] = {
                min: result.damage.length ?
                     result.damage[0] :
                     result.damage,
                max: result.damage.length ?
                     result.damage[result.damage.length - 1] :
                     result.damage
            }
        }
    }
   
    return data;
}

/**
 * Calculate damage from a known attacker set to a known defender set
 * @param {object} attackerSet - The Smogon set string for the attacker
 * @param {string} defenderSet - The Smogon set string for the defender
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
export function calculateDamage_knownBoth(attackerSet, defenderSet, genId=9) {

    // Create generation object
    const gen = Generations.get(genId);
   
    // Create attacker Pokemon
    const attackerData = parseSmogonSet(attackerSet);
    const attacker = new Pokemon(gen, attackerData.name, {
        ...attackerData
    });

    // Create defender Pokemon
    const defenderData = parseSmogonSet(defenderSet);
    const defender = new Pokemon(gen, defenderData.name, {
        ...attackerData
    });


    // Create moves
    const moves = [];
    for (const moveName of attackerData.moves)
        moves.push(new Move(gen, moveName));

    // Prepare data container
    let data = {
        'default': {}
    };

    for (const move of moves) {
        // Perform calculation
        const result = calculate(gen, attacker, defender, move);

        // Store parsed result
        data.default[move.name] = {
            min: result.damage.length ?
                    result.damage[0] :
                    result.damage,
            max: result.damage.length ?
                    result.damage[result.damage.length - 1] :
                    result.damage
        }
    }
   
    return data;
}

/**
 * Calculate damage from an attacker whose set is unknown to a defender whose set is unknown
 * @param {object} attackerName - The name of the attacker Pokemon
 * @param {string} defenderName - The name of the defender Pokemon
 * @param {string} moveNames - The list of moves usable by the attacker to calculate damage for
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
export function calculateDamage_knownNone(attackerName, defenderName, moveNames, genId=9) {

    // Create generation object
    const gen = Generations.get(genId);

    // Create moves
    const moves = [];
    for (const moveName of moveNames)
        moves.push(new Move(gen, moveName));

    // Prepare data container
    let data = {};

    // Calculate damages for each attacker possible reparts
    for (const [keyAtk, optsAtk] of Object.entries(ATTACKER_REPARTS)) {

        // Create attacker Pokemon
        const attacker = fromRepart(attackerName, optsAtk, gen);

        // Calculate damages for each defender possible reparts
        for (const [keyDef, optsDef] of Object.entries(DEFENDER_REPARTS)) {

            // Create defender Pokemon
            const defender = fromRepart(defenderName, optsDef, gen);

            // Initialize data container
            const key = keyAtk === keyDef ?
                        keyAtk :
                        `${keyAtk}|${keyDef}`;
            data[key] = {};

            for (const move of moves) {
                // Perform calculation
                const result = calculate(gen, attacker, defender, move);

                // Store parsed result
                data[key][move.name] = {
                    min: result.damage.length ?
                        result.damage[0] :
                        result.damage,
                    max: result.damage.length ?
                        result.damage[result.damage.length - 1] :
                        result.damage
                }
            }
        }
    }
   
    return data;
}