from fastapi import APIRouter, FastAPI, HTTPException
from game import Instance
from models.battle import Pokemon as PokemonModel, Teams as TeamsModel, Terrain as TerrainModel


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