from thinking.models.information import Damage, Definition
from thinking.models.overview import Overview, AvailableActions, Teams
from thinking.tools import get_match_overview, get_available_actions, get_teams, get_damages, get_definition, get_log, get_types_table, get_pokemon_type_table


class Instance:
    """
    A class representing an instance of a battle in poke-env.
    This class is meant to be used as an interface between the AI and the API.
    It provides methods to retrieve information about the battle state, such as the active pokemons and the teams of both players, but without having to give additional informations.
    It also automate some info retrieval.
    """

    #============#
    # Initialize #
    #============#

    def __init__(self, uuid: str):
        """
        Initialize the instance with the given UUID.

        Args:
            uuid (str): The UUID of the instance.
        """

        self.uuid = uuid
        
    #===========#
    # Raw Infos #
    #===========#

    def get_overview(self) -> Overview | str:
        """
        Get an overview of the current game state, including the turn number, the active pokemons (with their known details) and the state of the field.

        Returns:
            Overview | str: An Overview object containing the overview of the game state, or an error message if the overview could not be retrieved.
        """

        try:
            return get_match_overview(self.uuid)
        except Exception as e:
            return f"Error while fetching overview: {str(e)}"
    
    def get_available_actions(self) -> AvailableActions | str:
        """
        Get the list of available actions for the current turn, with all the known details of each action.

        Returns:
            AvailableActions | str: An AvailableActions object containing the list of available actions for the current turn, or an error message if the available actions could not be retrieved.
        """

        try:
            return get_available_actions(self.uuid)
        except Exception as e:
            return f"Error while fetching available actions: {str(e)}"
    
    def get_teams(self) -> Teams | str:
        """
        Get the list of all pokemons in the teams of both players, with all the known details of each pokemon.

        Returns:
            Teams | str: A Teams object containing the teams of both players, or an error message if the teams could not be retrieved.
        """

        try:
            return get_teams(self.uuid)
        except Exception as e:
            return f"Error while fetching teams: {str(e)}"
    
    def get_damage_calculation(self, move: str, attacker: str, defender: str) -> Damage | str:
        """
        Get the damage calculation estimation for a given move, attacker and defender.

        Args:
            move (str): The name of the move in english.
            attacker (str): The name of the attacking pokemon in english.
            defender (str): The name of the defending pokemon in english.

        Returns:
            Damage | str: A Damage object containing the damage calculation for the given move, attacker and defender, or an error message if the damage calculation could not be retrieved.
        """
    
        try:
            return get_damages(move, attacker, defender)
        except Exception as e:
            return f"Error while fetching damage calculation: {str(e)}"
    
    def get_definition(self, term: str) -> Definition | str:
        """
        Get the precise definition of a given term.

        Args:
            term (str): The term to get the definition of.

        Returns:
            Definition | str: A Definition object containing the definition of the given term, or an error message if the definition could not be retrieved.
        """

        try:
            return get_definition(term)
        except Exception as e:
            return f"Error while fetching definition: {str(e)}"
    
    def get_log(self) -> list[str] | str:
        """
        Get the log of the battle, which is a list of strings describing the events that happened during the battle.

        Returns:
            list[str] | str: The log of the battle, or an error message if the log could not be retrieved.
        """

        try:
            return get_log(self.uuid)
        except Exception as e:
            return f"Error while fetching log: {str(e)}"
    
    def get_types_table(self) -> dict[str, dict[str, float]] | str:
        """
        Get the type effectiveness table, which is a dictionary containing, for each types, the effectiveness of an attack of this type against each types.

        Returns:
            dict[str, dict[str, float]] | str: The type effectiveness table, which is a dictionary containing, for each types, the effectiveness of an attack of this type against each types, or an error message if the table could not be retrieved.
        """
    
        try:
            return get_types_table()
        except Exception as e:
            return f"Error while fetching types table: {str(e)}"
    
    def get_pokemon_type_table(self, pokemon_name: str) -> dict[str, list[str]] | str:
        """
        Get the type table of a pokemon, which is a dictionary containing the efficiency of the attacks of the type(s) of the pokemon against each types, as well as the effectiveness of attacks against this pokemon.

        Args:
            pokemon_name (str): The name of the pokemon in english.

        Raises:
            httpx.HTTPError: If there is an error while fetching the data from the tools API or if the pokemon is not found in the tools database.

        Returns:
            dict[str, list[str]] | str: The type table of the pokemon, which is a dictionary containing the efficiency of the attacks of the type(s) of the pokemon against each types, as well as the effectiveness of attacks against this pokemon, or an error message if the table could not be retrieved.
        """
    
        try:
            return get_pokemon_type_table(pokemon_name)
        except Exception as e:
            return f"Error while fetching pokemon type table: {str(e)}"
    
    #======================#
    # Automated Retrievals #
    #======================#

    def on_game_start(self) -> dict:
        """
        Helper method to be called at the start of the game.
        """

        actions = self.get_available_actions()
        teams = self.get_teams()

        return {
            "available_actions": actions,
            "teams": teams
        }

    def on_new_turn(self) -> dict:
        """
        Helper method to be called at the beginning of each turn.
        """

        overview = self.get_overview()
        actions = self.get_available_actions()

        return {
            "overview": overview,
            "available_actions": actions
        }
    
    def on_player_fainted(self) -> dict:
        """
        Helper method to be called when one of the player's pokemons fainted.
        """

        overview = self.get_overview()
        actions = self.get_available_actions()
        teams = self.get_teams()

        return {
            "overview": overview,
            "available_actions": actions,
            "teams": teams
        }
    
    def on_opponent_fainted(self) -> dict:
        """
        Helper method to be called when one of the opponent's pokemons fainted.
        """

        overview = self.get_overview()
        teams = self.get_teams()

        return {
            "overview": overview,
            "teams": teams
        }