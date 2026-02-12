/**
 * Get the definition of a move/ability by its name and, optionally, its category.
 * @param {string} name - The name of the move/ability/item to look up.
 * @param {string|null} category - The category ('move', 'ability', 'item') to search in. If null, the function will automatically search across all categories.
 */
export async function getDefinition(name, category) {

    // ===== 1. Search through all categories (if necessary) =====
    if (!category) {
        
        // Loop through all categories
        const categories = ['move', 'ability', 'item'];
        for (const cat of categories) {

            // Fetch the list of items in the current category
            const response = await fetch(`https://pokeapi.co/api/v2/${cat}?limit=10000`);
            const items = (await response.json()).results;

            // If the item is found, set the category and break out of the loop
            for (const item of items) {
                if (item.name.toLowerCase() === name.toLowerCase()) {
                    category = cat;
                    break;
                }
            }
            if (category) break;
        }

        // Check that a category was found
        if (!category)
            throw new Error(`Could not find '${name}' in any categories.`);
    }

    // ===== 2. Fetch the definition from the identified category =====

    // Fetch all the informations for the specified name in its category
    const response = await fetch(`https://pokeapi.co/api/v2/${category}/${name.toLowerCase()}`);

    // If the item isn't found in the specified category, throw an error
    if (!response.ok)
        throw new Error(`Failed to fetch definition for ${name} in category ${category}.`);

    // Extract the definition from the response
    const definitions = (await response.json()).effect_entries;
    for (const entry of definitions) {
        if (entry.language.name === 'en') {
            return entry.effect;
        }
    }

    // If no English definition is found, throw an error
    throw new Error(`No definition found for ${name} in category ${category}.`);
}