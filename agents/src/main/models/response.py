from pydantic import BaseModel, Field


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

    move: str = Field(...,
        description="The name of the move used in the action.")
    use_mega_evolution: bool = Field(False,
        description="Whether to mega evolve the Pokemon when using the move or not.")
    use_z_move: bool = Field(False,
        description="Whether to use the move as a Z-move or not.")
    use_dynamax: bool = Field(False,
        description="Whether to dynamax the Pokemon when using the move or not.")
    use_terastallization: bool = Field(False,
        description="Whether to terastallize the Pokemon when using the move or not.")


class ActionSwitch(BaseModel):
    """
    Represents the details of a switch action taken by a player during a battle.

    Attributes:
        pokemon (str): The name of the Pokemon to switch to.
    """

    pokemon: str = Field(...,
        description="The name of the Pokemon to switch to.")


class Action(BaseModel):
    """
    Represents an action taken by a player during a battle.

    Attributes:
        type (str): The type of the action. Must be equal to one of the Action.ACTION_??? constants.
        details (ActionMove|ActionSwitch): The details of the action. The content depends on the type of action.
    """

    type: str = Field(...,
        description="The type of the action. Must be equal to 'move' or 'switch'.")
    details: ActionMove|ActionSwitch = Field(...,
        description="The details of the action. The content depends on the type of action.")