import asyncio
from models.battle import Action as ActionModel, ActionMove, ActionSwitch, Move as MoveModel, Pokemon as PokemonModel, Teams as TeamsModel, Terrain as TerrainModel
from os import getenv as env
from poke_env import ServerConfiguration, AccountConfiguration
from poke_env.battle import AbstractBattle
from poke_env.data import to_id_str
from poke_env.player import Player
from poke_env.player.battle_order import BattleOrder
from uuid import uuid4

SERVER_CONFIGURATION = ServerConfiguration(
    f"wss://{env('SHOWDOWN_URL', 'localhost:8000')}/showdown/websocket",
    "https://play.pokemonshowdown.com/action.php?"
)


class Instance(Player):
    """
    A game instance. Each instance allows one player to communicate to Pokemon Showdown from an API.
    """

    def __init__(self, *args, **kwargs):
        # Instance attributes
        self.task = None
        self.next_move = None
        self.battle = None
        self.ready = False

        # Default initialization
        super().__init__(*args, **kwargs)

    #========#
    # Static #
    #========#

    __INSTANCES = {}

    @staticmethod
    def get(uuid: str) -> "Instance":
        """
        Get an instance from its uuid.

        Args:
            uuid (str): The uuid of the instance to get.
        
        Returns:
            Instance: The instance corresponding to the given uuid.
        """

        return Instance.__INSTANCES[uuid]

    @staticmethod
    async def fighter(
        opponent: str,
        username: str|None = None,
        password: str|None = None
    ) -> tuple["Instance", str]:
        """
        Create a game instance that challenges an opponent.

        Args:
            opponent (str): The name of the opponent to challenge.
            username (str|None, optional): Username for authentication. If none is provided, will be logged as a guest. Defaults to None.
            password (str|None, optional): Password for authentication. If none is provided, a non-registered account will be used. If no username is provided, it will be ignored. Defaults to None.

        Returns:
            tuple[Instance, str]: The game instance that has been created and its uuid.
        """
    
        # Setup account configuration
        if username is not None:
            account_configuration = AccountConfiguration(username=username, password=password)
        else:
            account_configuration = None

        # Initialize the instance
        instance = Instance(
            server_configuration=SERVER_CONFIGURATION,
            account_configuration=account_configuration
        )
        uuid = uuid4().hex
        Instance.__INSTANCES[uuid] = instance

        # Start the instance
        await instance.send_challenges(opponent, n_challenges=1)

        # Return the instance
        return (instance, uuid)

    @staticmethod
    async def waiter(
        opponent: str|None = None,
        username: str|None = None,
        password: str|None = None
    ) -> tuple["Instance", str]:
        """
        Create a game instance that waits for an opponent.

        Args:
            opponent (str|None): The name of the opponent to wait for. If None, will wait for any opponent. Defaults to None.
            username (str|None, optional): Username for authentication. If none is provided, will be logged as a guest. Defaults to None.
            password (str|None, optional): Password for authentication. If none is provided, a non-registered account will be used. If no username is provided, it will be ignored. Defaults to None.

        Returns:
            tuple[Instance, str]: The game instance that has been created and its uuid.
        """
    
        # Setup account configuration
        if username is not None:
            account_configuration = AccountConfiguration(username=username, password=password)
        else:
            account_configuration = None

        # Initialize the instance
        instance = Instance(
            server_configuration=SERVER_CONFIGURATION,
            account_configuration=account_configuration
        )
        uuid = uuid4().hex
        Instance.__INSTANCES[uuid] = instance

        # Start the instance
        await instance.accept_challenges(opponent, n_challenges=1)

        # Return the instance
        return (instance, uuid)
    
    #============#
    # Properties #
    #============#

    def is_ready(self) -> bool:
        """
        Check if the instance is ready to receive commands (and also to send data).

        Returns:
            bool: True if the instance is ready, False otherwise.
        """

        return self.ready

    def get_turn(self) -> int:
        """
        Get the current turn of the battle.

        Returns:
            int: The current turn of the battle.

        Raises:
            ValueError: If the battle information is not available yet.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return self.battle.turn

    def get_terrain(self) -> TerrainModel:
        """
        Get the current status of the terrain (weather, field(s), hazards, ...).

        Returns:
            TerrainModel: The current status of the terrain. This include global conditions (weather and fields) and side conditions (hazards, walls, ...) for both players.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return TerrainModel.from_poke_env(self.battle)
    
    def get_active_pokemons(self) -> TeamsModel:
        """
        Get the list of the active pokemons in the battle.

        Returns:
            TeamsModel: A TeamsModel object containing the details of the active pokemons of each players in the battle.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")

        # Retrieve the active pokemons of the players
        player_pokemon = self.battle.active_pokemon
        opponent_pokemon = self.battle.opponent_active_pokemon

        # Format the pokemons information as a TeamsModel object
        return TeamsModel(
            player=[PokemonModel.from_poke_env(player_pokemon)] if player_pokemon is not None else [],
            opponent=[PokemonModel.from_poke_env(opponent_pokemon)] if opponent_pokemon is not None else []
        )

    def get_teams(self) -> TeamsModel:
        """
        Get the list of all pokemons in the teams of both players.

        Returns:
            TeamsModel: A TeamsModel object containing the details of all pokemons in the teams of both players in the battle.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")

        # Retrieve the pokemons in the teams of both players
        player_team = self.battle.team.values()
        opponent_team = self.battle.opponent_team.values()

        # Format the pokemons information as a TeamsModel object
        return TeamsModel(
            player=[PokemonModel.from_poke_env(pokemon) for pokemon in player_team],
            opponent=[PokemonModel.from_poke_env(pokemon) for pokemon in opponent_team]
        )
    
    def get_available_moves(self) -> list[MoveModel]:
        """
        Get the list of available moves for the active pokemon.

        Returns:
            list[MoveModel]: The list of available moves for the active pokemon.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return [MoveModel.from_poke_env(move) for move in self.battle.available_moves]

    def get_available_switches(self) -> list[PokemonModel]:
        """
        Get the list of available pokemons to switch to for the active pokemon.

        Returns:
            list[PokemonModel]: The list of available pokemons to switch to for the active pokemon.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return [PokemonModel.from_poke_env(pokemon) for pokemon in self.battle.available_switches]
    
    def get_available_mechanics(self) -> dict[str, bool]:
        """
        Get the list of available mechanics (e.g. mega evolution, z-move, ...) for the active pokemon.

        Returns:
            dict[str, bool]: A dictionary containing the available mechanics for the active pokemon, with the name of the mechanic as key and whether it is available or not as value.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return {
            "mega_evolve": self.battle.can_mega_evolve,
            "z_move": self.battle.can_z_move,
            "dynamax": self.battle.can_dynamax,
            "terastallize": self.battle.can_tera
        }
    
    def get_log(self) -> list[str]:
        """
        Get the battle log, which is a list of strings describing the events that happened in the battle so far.

        Returns:
            list[str]: The battle log.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")
        
        return [
            "|".join(event)
            for value in self.battle.observations.values()
            for event in value.events
        ]

    def set_action(self, action: ActionModel):
        """
        Define the next move to play in the battle.

        Args:
            action (ActionModel): The action to play in the battle.
        
        Raises:
            ValueError: If the provided action is invalid or impossible to perform in the current battle state.
        """

        if self.battle is None:
            raise ValueError("Error while retrieving battle information")

        # Handle move action
        if action.type == ActionModel.ACTION_MOVE:
            move_details: ActionMove = action.details # type: ignore

            # Find the corresponding move
            move = None
            move_id = to_id_str(move_details.move)
            for available_move in self.battle.available_moves:
                if available_move.id == move_id:
                    import logging
                    logging.error(f"{move_id} == {available_move.id}")
                    move = available_move
                    break
            if move is None:
                raise ValueError("The provided move is not usable in the current battle state, or not available at all on this pokemon.")
            
            # Handle mechanics (e.g. terastallize)
            if move_details.use_mega_evolution:
                if not self.battle.can_mega_evolve:
                    raise ValueError("Mega Evolution has already been used or is not available in the current format.")
                if (
                    not self.battle.active_pokemon.item.name.startswith("mega")
                    and not self.battle.active_pokemon.name == "rayquaza"
                ):  # TODO: Improve this check
                    raise ValueError("The active pokemon is not holding the required item to mega-evolve.")
            if move_details.use_z_move:
                if not self.battle.can_z_move:
                    raise ValueError("Z-Move has already been used or is not available in the current format.")
                if not self.battle.active_pokemon.item.name.endswith("z"):  # TODO: Improve this check
                    raise ValueError("The active pokemon is not holding the required item to use a Z-Move.")
            if move_details.use_dynamax:
                if not self.battle.can_dynamax:
                    raise ValueError("Dynamax has already been used or is not available in the current format.")
            if move_details.use_terastallization:
                if not self.battle.can_tera:
                    raise ValueError("Terastallization has already been used or is not available in the current format.")

            # Create the battle order
            self.next_move = self.create_order(
                move,
                mega=move_details.use_mega_evolution,
                z_move=move_details.use_z_move,
                dynamax=move_details.use_dynamax,
                terastallize=move_details.use_terastallization
            )
            
        # Handle switch action
        elif action.type == ActionModel.ACTION_SWITCH:
            switch_details: ActionSwitch = action.details # type: ignore

            # Find the corresponding pokemon
            pokemon = None
            pokemon_id = to_id_str(switch_details.pokemon)
            for available_pokemon in self.battle.available_switches:
                if available_pokemon.base_species == pokemon_id:
                    pokemon = available_pokemon
                    break
            if pokemon is None:
                raise ValueError("The provided pokemon is not switchable in the current battle state, or not available at all in the team.")
            
            # Create the battle order
            self.next_move = self.create_order(pokemon)
        
        else:
            raise ValueError("Invalid action type")

    #===========#
    # Overrides #
    #===========#

    async def accept_challenges(self, *args, **kwargs):
        """
        Override the accept_challenges method to:
        - Make the accept_challenges method non-blocking
        - Prevent running multiple times the same instance
        """

        # Prevent running multiple times the same instance
        if self.task is not None:
            raise ValueError("This instance has already been started")
        
        # Make the accept_challenges method non-blocking
        self.task = asyncio.create_task(super().accept_challenges(*args, **kwargs))
    
    async def send_challenges(self, *args, **kwargs):
        """
        Override the send_challenges method to:
        - Make the send_challenges method non-blocking
        - Prevent running multiple times the same instance
        """

        # Prevent running multiple times the same instance
        if self.task is not None:
            raise ValueError("This instance has already been started")
        
        # Make the send_challenges method non-blocking
        self.task = asyncio.create_task(super().send_challenges(*args, **kwargs))
    
    async def choose_move(self, battle: AbstractBattle) -> BattleOrder:
        """
        This method is called by the engine at each turn to get the move to play.

        Args:
            battle (AbstractBattle): The current battle state.

        Returns:
            BattleOrder | Awaitable[BattleOrder]: The move to play, or an awaitable that will resolve to the move to play.
        """

        self.next_move = None
        self.battle = battle
        self.ready = True

        while self.next_move is None:
            await asyncio.sleep(0.1)

        self.ready = False

        return self.next_move