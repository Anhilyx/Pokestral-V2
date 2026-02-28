import { Generations, Pokemon } from '@smogon/calc';

// TODO: use a type table that changes based on the generation
const TYPES = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy'];
const TYPES_TABLE = [  // ⬇️ Attacker types  |  ➡️ Defender types
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 1.0, 0.5, 1.0],
    [1.0, 0.5, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 1.0, 2.0, 1.0],
    [1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0],
    [1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 0.5, 1.0],
    [1.0, 1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0],
    [1.0, 0.5, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0],
    [2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.0, 1.0, 2.0, 2.0, 0.5],
    [1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 0.0, 2.0],
    [1.0, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0],
    [1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.5, 1.0],
    [1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 0.5, 0.5],
    [1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0],
    [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.5, 0.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 0.5],
    [1.0, 0.5, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0],
    [1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0]
];

/**
 * Get the entire types table for a given generation (or the latest if not specified).
 * @param {number} gen - The generation number (1 to 9) or null/undefined for the latest generation. Currently unused.
 * @returns {object} An object containing the types table, where each key is an attacker type and its value is an object mapping defender types to their effectiveness multiplier.
 */
export function getTypesTable(gen = 9) {
    const typesTable = {};

    for (let i = 0; i < TYPES_TABLE.length; i++) {
        typesTable[TYPES[i]] = {};

        for (let j = 0; j < TYPES_TABLE[i].length; j++) {
            typesTable[TYPES[i]][TYPES[j]] = TYPES_TABLE[i][j];
        }
    }

    return typesTable;
}

/**
 * Get the type table of a specific type for a given generation (or the latest if not specified)
 * @param {string} type - The name of the type (e.g., "Fire")
 * @param {number} gen - The generation number (1 to 9) or null/undefined for the latest generation. Currently unused.
 * @return {object} An object mapping defender types to their effectiveness multiplier against the specified attacker type.
 * @throws {Error} If the type name is invalid or not found.
 */
export function getSpecificTypeTable(type, gen = 9) {
    type = type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();  // Normalize type name

    if (!TYPES.includes(type)) {
        throw new Error(`Invalid type "${type}". Valid types are: ${TYPES.join(', ')}`);
    }

    const typeIndex = TYPES.indexOf(type);
    const mapping = {
        "attacking": {},
        "defending": {}
    };

    for (let i = 0; i < TYPES.length; i++) {
        mapping["attacking"][TYPES[i]] = TYPES_TABLE[typeIndex][i];
        mapping["defending"][TYPES[i]] = TYPES_TABLE[i][typeIndex];
    }

    return mapping;
}

/**
 * Get the type table of a specific pokemon for a given generation (or the latest if not specified)
 * @param {string} pokemon - The name of the pokemon (e.g., "Pikachu")
 * @param {number} gen - The generation number (1 to 9) or null/undefined for the latest generation. Currently unused.
 * @return {object} An object mapping attacking types to their effectiveness multiplier against the specified pokemon.
 * @throws {Error} If the pokemon name is invalid or not found.
 */
export function getPokemonTypeTable(pokemon, gen = 9) {
    try {
        // Retrieve the types of the specified pokemon using the @smogon/calc library
        gen = Generations.get(gen);
        const poke = new Pokemon(gen, pokemon);
        const rawTypes = poke.types;
        const types = rawTypes.map(t => t.charAt(0).toUpperCase() + t.slice(1).toLowerCase());  // Normalize type names

        if (types.length === 0) {
            throw new Error(`No types found for pokemon "${pokemon}".`);
        }
        if (types.some(t => !TYPES.includes(t))) {
            throw new Error(`Invalid type(s) "${types.filter(t => !TYPES.includes(t)).join(', ')}" found for pokemon "${pokemon}". Valid types are: ${TYPES.join(', ')}`);
        }

        // Build the type table for the pokemon by combining the effectiveness of its types against all attacking types
        let mapping = {
            "attacking": {},
            "defending": {}
        };
        const typesIndices = types.map(t => TYPES.indexOf(t));

        for (let i = 0; i < TYPES.length; i++) {
            for (const typeIndex of typesIndices) {
                mapping["attacking"][TYPES[typeIndex]] = mapping["attacking"][TYPES[typeIndex]] || {};
                mapping["attacking"][TYPES[typeIndex]][TYPES[i]] = TYPES_TABLE[typeIndex][i];
            }
        }

        for (let i = 0; i < TYPES.length; i++) {
            let multiplier = 1.0;
            for (const typeIndex of typesIndices) {
                multiplier *= TYPES_TABLE[i][typeIndex];
            }
            mapping["defending"][TYPES[i]] = multiplier;
        }

        return mapping;

    } catch (err) {
        throw new Error(`Error retrieving types for pokemon "${pokemon}": ${err.message}`);
    }
}
