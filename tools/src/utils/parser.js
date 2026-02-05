import { Dex } from '@pkmn/dex';

/**
 * Parse a Smogon set string into a data object
 * @param {string} setString - The Smogon set string
 * @returns {object} Parsed data object
 */
export function parseSmogonSet(setString) {

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
        throw new Error("Invalid set: Pokemons must have between 1 and 4 moves.");

    return data;
}