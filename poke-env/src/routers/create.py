from fastapi import APIRouter, FastAPI, HTTPException
from game import Instance
from models.instance import Instanciator as InstanceModel, UUIDModel


app = FastAPI()
router = APIRouter(
    prefix="/create",
    tags=["Instantiate"]
)


@router.post("/fighter")
async def create_fighter(data: InstanceModel) -> UUIDModel:
    """
    Create a game instance that challenges an opponent.

    Args:
        data (InstanceModel): An object containing the informations to create a game instance as a fighter.

    Returns:
        UUID: An object containing the UUID of the created instance.

    Raises:
        HTTPException (400): If the opponent field is not provided in the request body.
    """

    # Opponent is required for a fighter
    if data.opponent is None:
        raise HTTPException(status_code=400, detail="Opponent is required to create a fighter instance")

    _, uuid = await Instance.fighter(data.opponent, data.username, data.password)
    return UUIDModel(uuid=uuid)


@router.post("/waiter")
async def create_waiter(data: InstanceModel) -> UUIDModel:
    """
    Create a game instance that waits for an opponent.

    Args:
        data (InstanceModel): An object containing the informations to create a game instance as a waiter.

    Returns:
        UUID: An object containing the UUID of the created instance.
    """

    _, uuid = await Instance.waiter(data.opponent, data.username, data.password)
    return UUIDModel(uuid=uuid)