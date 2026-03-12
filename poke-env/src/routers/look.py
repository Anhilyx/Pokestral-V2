from fastapi import APIRouter, FastAPI, HTTPException
from game import Instance
from models.battle import Move as MoveModel, Pokemon as PokemonModel, Teams as TeamsModel, Terrain as TerrainModel, Turn as TurnModel


app = FastAPI()
router = APIRouter(
    prefix="/look",
    tags=["Lookup"]
)


@router.get("/ready")
async def is_ready(uuid: str) -> bool:
    """
    Check if the instance is ready to receive commands (and also to send data).

    Args:
        uuid (str): The UUID of the instance to check.

    Returns:
        bool: True if the instance is ready, False otherwise.

    Raises:
        HTTPException (404): If the provided UUID is invalid.
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Check if the instance is ready
    return instance.is_ready()


@router.get("/turn")
async def get_turn(uuid: str) -> TurnModel:
    """
    Get the current turn number in the battle.

    Args:
        uuid (str): The UUID of the instance to get the turn number from.
    
    Returns:
        TurnModel: The current turn number in the battle.
    
    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the turn information is not available yet.
        HTTPException (500): If there is an internal error with the turn information retrieval function.
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the turn information
    try:
        turn = instance.get_turn()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if turn is None:
        raise HTTPException(status_code=425, detail="Turn information is not available yet")
    
    return TurnModel(turn=turn)


@router.get("/terrain")
async def get_terrain(uuid: str) -> TerrainModel:
    """
    Get the current status of the terrain, both global (weather and fields) and side conditions (hazards, walls, ...).

    Args:
        uuid (str): The UUID of the instance to get the terrain information from.
    
    Returns:
        TerrainModel: The current status of the terrain. This include global conditions (weather and fields) and side conditions (hazards, walls, ...) for both players.
    
    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the terrain information is not available yet.
        HTTPException (500): If there is an internal error with the terrain informations retrieval function.
    """
    
    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the terrain information
    try:
        terrain = instance.get_terrain()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if terrain is None:
        raise HTTPException(status_code=425, detail="Terrain information is not available yet")
    
    # Return the formatted terrain information as JSON
    return terrain


@router.get("/active-pokemons")
async def get_active_pokemons(uuid: str) -> TeamsModel:
    """
    Get the list of the active pokemons in the battle.

    Args:
        uuid (str): The UUID of the instance to get the active pokemons from.
    
    Returns:
        TeamsModel: The active pokemons information in the battle.
    
    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the active pokemons information is not available yet.
        HTTPException (500): If there is an internal error with the active pokemons informations retrieval function.
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the active pokemons information
    try:
        active_pokemons = instance.get_active_pokemons()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if active_pokemons is None:
        raise HTTPException(status_code=425, detail="Active pokemons information is not available yet")

    return active_pokemons


@router.get("/teams")
async def get_teams(uuid: str) -> TeamsModel:
    """
    Get the list of all pokemons in the teams of both players.

    Args:
        uuid (str): The UUID of the instance to get the teams from.
    
    Returns:
        TeamsModel: The teams information in the battle.
    
    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the teams information is not available yet.
        HTTPException (500): If there is an internal error with the teams informations retrieval function.
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the teams information
    try:
        teams = instance.get_teams()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if teams is None:
        raise HTTPException(status_code=425, detail="Teams information is not available yet")

    return teams


@router.get("/available-moves")
async def get_available_moves(uuid: str) -> list[MoveModel]:
    """
    Get the list of the available moves for the active pokemon of the player.

    Args:
        uuid (str): The UUID of the instance to get the available moves from.
    
    Returns:
        list[MoveModel]: The list of the available moves for the active pokemon of the player.

    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the available moves information is not available yet.
        HTTPException (500): If there is an internal error with the available moves informations retrieval function
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the available moves information
    try:
        available_moves = instance.get_available_moves()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if available_moves is None:
        raise HTTPException(status_code=425, detail="Available moves information is not available yet")

    return available_moves


@router.get("/available-switches")
async def get_available_switches(uuid: str) -> list[PokemonModel]:
    """
    Get the list of the available pokemons to switch to for the player.

    Args:
        uuid (str): The UUID of the instance to get the available switches from.
    
    Returns:
        list[PokemonModel]: The list of the available pokemons to switch to for the player.

    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the available switches information is not available yet.
        HTTPException (500): If there is an internal error with the available switches informations retrieval function
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the available switches information
    try:
        available_switches = instance.get_available_switches()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if available_switches is None:
        raise HTTPException(status_code=425, detail="Available switches information is not available yet")

    return available_switches


@router.get("/available-mechanics")
async def get_available_mechanics(uuid: str) -> dict[str, bool]:
    """
    Get the list of the available mechanics for the current turn.

    Args:
        uuid (str): The UUID of the instance to get the available mechanics from.
    
    Returns:
        dict[str, bool]: The available mechanics for the current turn.

    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the available mechanics information is not available yet.
        HTTPException (500): If there is an internal error with the available mechanics informations retrieval function
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the available mechanics information
    try:
        available_mechanics = instance.get_available_mechanics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if available_mechanics is None:
        raise HTTPException(status_code=425, detail="Available mechanics information is not available yet")

    return available_mechanics


@router.get("/log")
async def get_log(uuid: str) -> list[str]:
    """
    Get the battle log, which is a list of strings describing the events that happened during the battle.

    Args:
        uuid (str): The UUID of the instance to get the battle log from.
    
    Returns:
        list[str]: The battle log, which is a list of strings describing the events that happened during the battle.

    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (425): If the battle log information is not available yet.
        HTTPException (500): If there is an internal error with the battle log informations retrieval function
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")

    # Get the battle log information
    try:
        battle_log = instance.get_log()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    if battle_log is None:
        raise HTTPException(status_code=425, detail="Battle log information is not available yet")

    return battle_log