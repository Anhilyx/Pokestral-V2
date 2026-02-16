from poke_env.battle import AbstractBattle as PokeEnvBattle
from poke_env.battle.field import Field as PokeEnvField
from poke_env.battle.pokemon import Pokemon as PokeEnvPokemon
from poke_env.battle.side_condition import SideCondition as PokeEnvSideCondition
from poke_env.battle.weather import Weather as PokeEnvWeather
from poke_env.battle.move import Move as PokeEnvMove
from poke_env.data import GenData
from pydantic import BaseModel, ConfigDict
from typing import ClassVar


class Terrain(BaseModel):
    """
    Represents the terrain information of a battle, including global conditions (weather and fields) and side conditions (hazards, walls, ...) for both players.

    Attributes:
        field (dict[str, int]): The global conditions of the battle, such as weather and fields, and how many turns they have been active for.
        player (dict[str, int]): The side conditions of the player's side, such as hazards and walls, and how many turns they have been active for.
        opponent (dict[str, int]): The side conditions of the opponent's side, such as hazards and walls, and how many turns they have been active for.
    """

    field: dict[str, int]
    player: dict[str, int]
    opponent: dict[str, int]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "field": {
                    "Electric Terrain": 3,
                    "Trick Room": 4,
                    "Rain": 1
                },
                "player": {
                    "Spikes": 8,
                    "Stealth Rock": 9
                },
                "opponent": {
                    "Aurora Veil": 6
                }
            }
        }
    )

    POKE_ENV_FIELDS: ClassVar[dict] = {
        PokeEnvField.ELECTRIC_TERRAIN: "Electric Terrain",
        PokeEnvField.FAIRY_LOCK:       "Fairy Lock",
        PokeEnvField.GRASSY_TERRAIN:   "Grassy Terrain",
        PokeEnvField.GRAVITY:          "Gravity",
        PokeEnvField.HEAL_BLOCK:       "Heal Block",
        PokeEnvField.MISTY_TERRAIN:    "Misty Terrain",
        PokeEnvField.MUD_SPORT:        "Mud Sport",
        PokeEnvField.MUD_SPOT:         "Mud Spot",
        PokeEnvField.PSYCHIC_TERRAIN:  "Psychic Terrain",
        PokeEnvField.TRICK_ROOM:       "Trick Room",
        PokeEnvField.WATER_SPORT:      "Water Sport",
        PokeEnvField.WONDER_ROOM:      "Wonder Room"
    }
    
    POKE_ENV_WEATHERS: ClassVar[dict] = {
        PokeEnvWeather.DELTASTREAM:   "Delta Stream",
        PokeEnvWeather.DESOLATELAND:  "Desolate Land",
        PokeEnvWeather.HAIL:          "Hail",
        PokeEnvWeather.PRIMORDIALSEA: "Primordial Sea",
        PokeEnvWeather.RAINDANCE:     "Rain Dance",
        PokeEnvWeather.SANDSTORM:     "Sandstorm",
        PokeEnvWeather.SNOW:          "Snow",
        PokeEnvWeather.SNOWSCAPE:     "Snowscape",
        PokeEnvWeather.SUNNYDAY:      "Sunny Day",
    }

    POKE_ENV_SIDED: ClassVar[dict] = {
        PokeEnvSideCondition.AURORA_VEIL:      "Aurora Veil",
        PokeEnvSideCondition.CRAFTY_SHIELD:    "Crafty Shield",
        PokeEnvSideCondition.FIRE_PLEDGE:      "Fire Pledge",
        PokeEnvSideCondition.G_MAX_CANNONADE:  "G-Max Cannonade",
        PokeEnvSideCondition.G_MAX_STEELSURGE: "G-Max Steelsurge",
        PokeEnvSideCondition.G_MAX_VINE_LASH:  "G-Max Vine Lash",
        PokeEnvSideCondition.G_MAX_VOLCALITH:  "G-Max Volcalith",
        PokeEnvSideCondition.G_MAX_WILDFIRE:   "G-Max Wildfire",
        PokeEnvSideCondition.GRASS_PLEDGE:     "Grass Pledge",
        PokeEnvSideCondition.LIGHT_SCREEN:     "Light Screen",
        PokeEnvSideCondition.LUCKY_CHANT:      "Lucky Chant",
        PokeEnvSideCondition.MATBLOCK:         "Mat Block",
        PokeEnvSideCondition.MIST:             "Mist",
        PokeEnvSideCondition.QUICK_GUARD:      "Quick Guard",
        PokeEnvSideCondition.REFLECT:          "Reflect",
        PokeEnvSideCondition.SAFEGUARD:        "Safeguard",
        PokeEnvSideCondition.SPIKES:           "Spikes",
        PokeEnvSideCondition.STEALTH_ROCK:     "Stealth Rock",
        PokeEnvSideCondition.STICKY_WEB:       "Sticky Web",
        PokeEnvSideCondition.TAILWIND:         "Tailwind",
        PokeEnvSideCondition.TOXIC_SPIKES:     "Toxic Spikes",
        PokeEnvSideCondition.WATER_PLEDGE:     "Water Pledge",
        PokeEnvSideCondition.WIDE_GUARD:       "Wide Guard",
    }

    @staticmethod
    def from_poke_env(battle: PokeEnvBattle) -> "Terrain":
        """
        Create a Terrain object from a poke_env Battle object.

        Args:
            battle (PokeEnvBattle): The poke_env Battle object to create the Terrain object from.

        Returns:
            Terrain: The created Terrain object.
        """

        field = {}
        player = {}
        opponent = {}

        # Extract fields
        for key, value in battle.fields.items():
            key = Terrain.POKE_ENV_FIELDS.get(key)
            if key is not None:
                field[key] = battle.turn - value
        
        # Extract weather
        for key, value in battle.weather.items():
            key = Terrain.POKE_ENV_WEATHERS.get(key)
            if key is not None:
                field[key] = battle.turn - value

        # Extract one-sided effects
        for key, value in battle.side_conditions.items():
            key = Terrain.POKE_ENV_SIDED.get(key)
            if key is not None:
                player[key] = battle.turn - value
        for key, value in battle.opponent_side_conditions.items():
            key = Terrain.POKE_ENV_SIDED.get(key)
            if key is not None:
                opponent[key] = battle.turn - value
        
        return Terrain(
            field=field,
            player=player,
            opponent=opponent
        )


class Move(BaseModel):
    """
    Represents a move from a pokemon during a battle.

    Attributes:
        name (str): The name of the move.
        pp (int): The current PP of the move.
    """

    name: str
    pp: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Judgement",
                "pp": 7
            }
        }
    )

    POKE_ENV_MOVES: ClassVar[dict] = GenData.from_gen(9).load_moves(9)

    @staticmethod
    def from_poke_env(move: PokeEnvMove) -> "Move":
        """
        Create a Move object from a poke_env Move object.

        Args:
            move (poke_env.battle.move.Move): The poke_env Move object to create the Move object from.

        Returns:
            Move: The created Move object.
        """

        raw_move = Move.POKE_ENV_MOVES.get(move.id)
        if raw_move is None:
            raise ValueError(f"Move with id {move.id} not found in Gen 9 moves data")

        name = raw_move["name"]
        pp = move.current_pp

        return Move(
            name=name,
            pp=pp
        )


class Pokemon(BaseModel):
    """
    Represents the information of a Pokemon during a battle.

    Attributes:
        name (str): The name of the Pokemon.
        level (int): The level of the Pokemon.

        active (bool): Whether the Pokemon is currently active in the battle or not.
        fainted (bool): Whether the Pokemon is fainted or not.
        mega_evolved (None): Whether the Pokemon is currently Mega Evolved or not.  # TODO: Not implemented yet.
        dynamaxed (bool): Whether the Pokemon is currently Dynamaxed or not.
        terastallized (bool): Whether the Pokemon is currently Terastallized or not.

        hp (int|None): The current HP of the Pokemon. If None, it means the raw HP is not known.
        health (float): The percentage of current HP to maximum HP of the Pokemon.
        
        ability (str|None): The ability of the Pokemon, if known.
        item (str|None): The held item of the Pokemon, if known.
        moves (list[Move]): The known moves of the Pokemon, with their current PP.
        
        stats (dict[str, int]): The stat changes of the Pokemon, such as attack, defense, speed, etc.
        statuses (list[str]): The status conditions of the Pokemon, if any.
        types (list[str]|None): The types of the Pokemon, if altered.
    """

    name: str
    level: int = 100

    active: bool = False
    fainted: bool = False
    mega_evolved: None = None  # TODO: Not implemented yet
    dynamaxed: bool = False
    terastallized: bool = False

    hp: int|None = None
    health: float = 100.0

    ability: str|None = None
    item: str|None = None
    moves: list[Move] = []

    stats: dict[str, int] = {
        "hp": 0,
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0
    }
    statuses: list[str] = []
    types: list[str]|None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Arceus",
                "level": 100,
                
                "active": True,
                "fainted": False,
                "mega_evolved": None,
                "dynamaxed": False,
                "terastallized": False,

                "hp": 215,
                "health": 53.5,

                "ability": "Multitype",
                "item": "Silk Scarf",
                "stats": {
                    "hp": 0,
                    "atk": 2,
                    "def": 0,
                    "spa": 0,
                    "spd": 0,
                    "spe": 1
                },
                "statuses": ["paralyzed", "encore"],
                "moves": [
                    Move(name="Extreme Speed", pp=4).model_dump(),
                    Move(name="Shadow Claw", pp=24).model_dump(),
                    Move(name="Swords Dance", pp=30).model_dump(),
                    Move(name="Recover",  pp=11).model_dump()
                ]
            }
        }
    )

    POKE_ENV_POKEMONS: ClassVar[dict] = GenData.from_gen(9).load_pokedex(9)

    @staticmethod
    def from_poke_env(pokemon: PokeEnvPokemon) -> "Pokemon":
        """
        Create a Pokemon object from a poke_env Pokemon object.

        Args:
            pokemon (poke_env.battle.pokemon.Pokemon): The poke_env Pokemon object to create the Pokemon object from.

        Returns:
            Pokemon: The created Pokemon object.
        """
        
        raw_pokemon = Pokemon.POKE_ENV_POKEMONS.get(pokemon.base_species)
        if raw_pokemon is None:
            raise ValueError(f"Pokemon with base species {pokemon.base_species} not found in Gen 9 pokedex data")

        name = raw_pokemon["name"]
        level = pokemon.level

        active = pokemon.active if pokemon.active is not None else False
        fainted = pokemon.fainted
        mega_evolved = None  # TODO: Not implemented yet
        dynamaxed = pokemon.is_dynamaxed
        terastallized = pokemon.is_terastallized

        hp = pokemon.current_hp
        health = pokemon.current_hp_fraction * 100

        ability = pokemon.ability  # TODO: Format ability name
        item = pokemon.item  # TODO: Format item name
        moves = [Move.from_poke_env(move) for move in pokemon.moves.values()]

        stats = pokemon.boosts
        statuses = [pokemon.status.name] if pokemon.status else []
        if pokemon.must_recharge: statuses.append("recharging")
        # TODO: Add other possible statuses such as "confused", "encored", "trapped", ...
        has_base_types = True
        base_types = [ type.name for type in pokemon.original_types ]
        current_types = [ type.name for type in pokemon.types ]
        for type in base_types:
            if type not in current_types:
                has_base_types = False
                break
        for type in current_types:
            if type not in base_types:
                has_base_types = False
                break
        types = current_types if has_base_types else None

        return Pokemon(
            name=name,
            level=level,
            active=active,
            fainted=fainted,
            mega_evolved=mega_evolved,
            dynamaxed=dynamaxed,
            terastallized=terastallized,
            hp=hp,
            health=health,
            ability=ability,
            item=item,
            moves=moves,
            stats=stats,
            statuses=statuses,
            types=types
        )


class Teams(BaseModel):
    """
    Represents the teams information of a battle, including the player's team and the opponent's team.

    Attributes:
        player (list[Pokemon]): The player's Pokemons.
        opponent (list[Pokemon]): The opponent's Pokemons.
    """

    player: list[Pokemon]
    opponent: list[Pokemon]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player": [
                    Pokemon(name="Ditto", active=True, ability="Imposter").model_dump(),
                    Pokemon(name="Arceus", ability="Multitype").model_dump()
                ],
                "opponent": [
                    Pokemon(name="Pikachu", active=True).model_dump(),
                    Pokemon(name="Charizard").model_dump()
                ]
            }
        }
    )


class ActionMove(BaseModel):
    """
    Represents the details of a move action taken by a player during a battle.

    Attributes:
        move (str): The name of the move used in the action.
        use_mega_evolution (bool): Whether to mega evolve the Pokemon when using the move or not.
        use_z_move (bool): Whether to use the move as a Z-move or not.
        use_dynamax (bool): Whether to dynamax the Pokemon when using the move or not.
        use_terastallization (bool): Whether to terastallize the Pokemon when using the move or not.
    """

    move: str
    use_mega_evolution: bool = False
    use_z_move: bool = False
    use_dynamax: bool = False
    use_terastallization: bool = False

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "move": "Extreme Speed",
                "use_mega_evolution": False,
                "use_z_move": False,
                "use_dynamax": False,
                "use_terastallization": False
            }
        }
    )


class ActionSwitch(BaseModel):
    """
    Represents the details of a switch action taken by a player during a battle.

    Attributes:
        pokemon (str): The name of the Pokemon to switch to.
    """

    pokemon: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pokemon": "Ditto"
            }
        }
    )


class Action(BaseModel):
    """
    Represents an action taken by a player during a battle.

    Attributes:
        type (str): The type of the action. Must be equal to one of the Action.ACTION_??? constants.
        details (ActionMove|ActionSwitch): The details of the action. The content depends on the type of action.
    """

    type: str
    details: ActionMove|ActionSwitch

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "move",
                "details": ActionMove(move="Extreme Speed").model_dump()
            }
        }
    )

    ACTION_MOVE: ClassVar[str] = "move"
    ACTION_SWITCH: ClassVar[str] = "switch"