from fastapi import APIRouter, FastAPI, HTTPException
from game import Instance
from models.battle import Action as ActionModel, ActionMove, ActionSwitch


app = FastAPI()
router = APIRouter(
    prefix="/act",
    tags=["Actions"]
)


@router.post("/")
async def act(uuid: str, data: ActionModel):
    """
    Send an action to the instance.

    Args:
        uuid (str): The UUID of the instance to send the action to.
        data (ActionModel): The action to send.
    
    Raises:
        HTTPException (404): If the provided UUID is invalid.
        HTTPException (403): If the required action is impossible to perform (e.g. trying to switch a fainted Pokémon, trying to use a move that is not available, trying to use a mechanic that isn't available, ...).
    """

    # Retrieve the instance
    instance = Instance.get(uuid)
    if instance is None:
        raise HTTPException(status_code=404, detail="Invalid instance UUID")
    
    # Validate the request
    if data.type == ActionModel.ACTION_MOVE and not isinstance(data.details, ActionMove):
        raise HTTPException(status_code=422, detail="Invalid action data for move action")
    if data.type == ActionModel.ACTION_SWITCH and not isinstance(data.details, ActionSwitch):
        raise HTTPException(status_code=422, detail="Invalid action data for switch action")

    # Send the action
    try:
        instance.set_action(data)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    # Return a success, just for the sake of it
    return True