import { calculate, Generations, Pokemon, Move } from '@smogon/calc';
import { parseSmogonSet } from '../utils/parser.js';

/**
 * Calculate damage from attacker to defender using a move in a given generation
 * @param {object} attackerSet - The Smogon set string for the attacker
 * @param {string} defenderName - The name of the defender Pokemon
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
export function calculateDamage(attackerSet, defenderName, genId=9) {

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

    // Create options variants
    const options = {
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
        
        //                 🟢 HP        🟢 DEF/SPD                    🔴 Nature
        "max-phys":       {maxHP: true,  maxDef: true,  maxSpd: false, nature: true },
        "max-spec":       {maxHP: true,  maxDef: false, maxSpd: true,  nature: true },
    };

    // Calculate damages for each option set
    for (const [key, opts] of Object.entries(options)) {
        // Initialize data container
        data[key] = {};

        // Create defender Pokemon
        const defender = new Pokemon(gen, defenderName, {
            // Define stats based on options
            evs: {
                hp: opts.maxHP ? 252 : 0,
                def: opts.maxDef ? 252 : 0,
                spd: opts.maxSpd ? 252 : 0,
            },
            nature: (opts.nature && opts.maxDef) ? 'Impish' :
                    (opts.nature && opts.maxSpd) ? 'Calm'   :
                                                   'Quirky'
        });

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