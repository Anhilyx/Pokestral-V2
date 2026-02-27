from thinking.models.pokemon import PokemonDetails
from pydantic import BaseModel, Field


class Overview(BaseModel):
    """
    Overview of the current game state, including the turn number, the active pokemons (with their known details) and the state of the field.
    """

    turn: int

    player_pokemons: list[PokemonDetails] = Field(default_factory=list,
        description="A list of the player's active pokemons with all their details.")
    player_field: dict[str, int] = Field(default_factory=dict,
        description="A dictionary representing the state of the player's field, with the name of the field condition as key and how many turns it has been active as value.")
    
    opponent_pokemons: list[PokemonDetails] = Field(default_factory=list,
        description="A list of the opponent's active pokemons with their known details.")
    opponent_field: dict[str, int] = Field(default_factory=dict,
        description="A dictionary representing the state of the opponent's field, with the name of the field condition as key and how many turns it has been active as value.")
    
    global_field: dict[str, int] = Field(default_factory=dict,
        description="A dictionary representing the state of the field conditions that affect both players, with the name of the field condition as key and how many turns it has been active as value.")
    

class Teams(BaseModel):
    """
    The teams of both players, with all the known details of each pokemon.
    """

    player_team: list[PokemonDetails] = Field(default_factory=list,
        description="A list of the player's team pokemons with all their details.")
    opponent_team: list[PokemonDetails] = Field(default_factory=list,
        description="A list of the opponent's team pokemons with all their details.")
    

class AvailableActions(BaseModel):
    """
    The list of available actions for the current turn, with all the known details of each action.
    """

    moves: list[str] = Field(default_factory=list,
        description="A list of the available moves for the active pokemon, with their names in english.")
    switches: list[str] = Field(default_factory=list,
        description="A list of the available switches for the active pokemon, with the names of the pokemons in english.")
    
    mega_evolve: bool = Field(default=False,
        description="Whether the active pokemon can mega evolve or not.")
    z_move: bool = Field(default=False,
        description="Whether the active pokemon can use a Z-move or not.")
    dynamax: bool = Field(default=False,
        description="Whether the active pokemon can dynamax or not.")
    terastallize: bool = Field(default=False,
        description="Whether the active pokemon can terastallize or not.")