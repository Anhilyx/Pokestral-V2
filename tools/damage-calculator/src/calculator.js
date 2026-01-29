const { calculate, Generations, Pokemon, Move } = require('@smogon/calc');
const { Dex } = require('@pkmn/dex');

/**
 * Parse a Smogon set string into a data object
 * @param {string} setString - The Smogon set string
 * @returns {object} Parsed data object
 */
function parseSmogonSet(setString) {

    // Prepare data container
    let data = {};

    // Split by lines
    const lines = setString.split('\n').map(line => line.trim());
    
    // Extract from first line
    const name = lines[0].match(/^\S+/)?.[0];
    const item = lines[0].match(/@(.*)$/)?.[1].trim();
    // Store to data
    data.name = name;
    if (item) data.item = item;

    // Extract from subsequent lines
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i];

        // Ability
        if (line.startsWith('Ability:')) {
            data.ability = line.replace('Ability:', '').trim();
        }

        // Level
        else if (line.startsWith('Level:')) {
            data.level = parseInt(line.replace('Level:', '').trim());
        }

        // Happiness
        else if (line.startsWith('Happiness:')) {
            data.happiness = parseInt(line.replace('Happiness:', '').trim());
        }

        // Hidden Power Type
        else if (line.startsWith('Hidden Power:')) {
            data.hiddenPower = line.replace('Hidden Power:', '').trim();
        }

        // Tera Type
        else if (line.startsWith('Tera Type:')) {
            data.teraType = line.replace('Tera Type:', '').trim();
        }

        // EVs
        else if (line.includes('EVs:')) {
            const evs = line.replace('EVs:', '').trim().split('/');
            data.evs = {};
            for (const ev of evs) {
                const [value, stat] = ev.trim().split(' ');
                data.evs[stat.toLowerCase()] = parseInt(value);
            }
        }

        // IVs
        else if (line.includes('IVs:')) {
            const ivs = line.replace('IVs:', '').trim().split('/');
            data.ivs = {};
            for (const iv of ivs) {
                const [value, stat] = iv.trim().split(' ');
                data.ivs[stat.toLowerCase()] = parseInt(value);
            }
        }

        // Nature
        else if (line.endsWith('Nature')) {
            data.nature = line.replace('Nature', '').trim();
        }

        // Moves
        else if (line.startsWith('-')) {
            if (!data.moves) data.moves = [];
            const move = line.replace('-', '').trim();
            data.moves.push(move);
        }
    }

    // Check for invalid data
    if (!data.name)  // Missing Pokemon name
        throw new Error("Invalid set: Missing Pokemon name.");
    else if (!Dex.species.get(data.name).exists)  // Pokemon not found
        throw new Error (`Invalid set: Pokemon ${data.name} not found.`);
    else if (data.level && (data.level < 1 || data.level > 100))  // Level validity
        throw new Error("Invalid set: Level must be between 1 and 100.");
    else if (data.happiness && (data.happiness < 0 || data.happiness > 255))  // Happiness validity
        throw new Error("Invalid set: Happiness must be between 0 and 255.");
    else if (data.evs  && Object.values(data.evs).find(ev => ev < 0 || ev > 252))  // EVs validity
        throw new Error("Invalid set: EVs must be between 0 and 252.");
    else if (data.ivs && Object.values(data.ivs).find(iv => iv < 0 || iv > 31))  // IVs validity
        throw new Error("Invalid set: IVs must be between 0 and 31.");
    else if (!data.moves || data.moves.length < 1 || data.moves.length > 4)  // Invalid number of moves
        throw new Error("Invalid set: Pokemons must have between 1 and 4.");

    return data;
}

/**
 * Calculate damage from attacker to defender using a move in a given generation
 * @param {object} attackerSet - The Smogon set string for the attacker
 * @param {string} defenderName - The name of the defender Pokemon
 * @param {number} genId - The generation number (default: 9)
 * @returns {object} Damage calculation results for various stat configurations
 */
function calc(attackerSet, defenderName, genId=9) {

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

module.exports = { calc };