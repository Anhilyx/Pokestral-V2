from pydantic import BaseModel, Field, field_validator


class Move(BaseModel):
    """
    A move that a pokemon can use in battle.
    """

    name: str = Field(...,
        description="The name of the move in english.")
    pp: int | None = Field(None,
        description="The current PP of the move, or None if the PP is not known.")


class PokemonSummary(BaseModel):
    """
    A summary of a pokemon's most useful informations for battle.
    """

    name: str = Field(...,
        description="The name of the pokemon in english.")
    
    health: float = Field(default=100.0,
        description="The current health of the pokemon as a percentage (0-100).")

    ability: str | None = Field(default=None,
        description="The name of the pokemon's ability, or None if the ability is not known.")
    item: str | None = Field(default=None,
        description="The name of the pokemon's held item, or None if the item is not known.")
    moves: list[Move] = Field(default_factory=list,
        description="A list of the known pokemon's moves.")


class PokemonDetails(BaseModel):
    """
    A detailed summary of all pokemon's informations for battle.
    """

    @field_validator('mega_evolved', mode='before')
    @classmethod
    def avoid_none_mega_evolve(cls, value):
        return value or False

    name: str = Field(...,
        description="The name of the pokemon in english.")
    level: int = Field(100,
        description="The current level of the pokemon.")

    active: bool = Field(default=False,
        description="Whether the pokemon is currently active in the battle.")
    fainted: bool = Field(default=False,
        description="Whether the pokemon is fainted.")
    mega_evolved: bool = Field(default=False,
        description="Whether the pokemon is mega evolved.")
    dynamaxed: bool = Field(default=False,
        description="Whether the pokemon is dynamaxed.")
    terastallized: bool = Field(default=False,
        description="Whether the pokemon is terastallized.")

    hp: int | None = Field(None,
        description="The current HP of the pokemon, or None if the exact HP is not known.")
    health: float = Field(default=100.0,
        description="The current health of the pokemon as a percentage (0-100).")

    ability: str | None = Field(default=None,
        description="The name of the pokemon's ability, or None if the ability is not known.")
    item: str | None = Field(default=None,
        description="The name of the pokemon's held item, or None if the item is not known.")
    moves: list[Move] = Field(default_factory=list,
        description="A list of the known pokemon's moves.")

    stats: dict[str, int] = Field(default={
        "hp": 0,
        "atk": 0,
        "def": 0,
        "spa": 0,
        "spd": 0,
        "spe": 0
    }, description="A dictionary of the pokemon's stat changes, where the keys are the stat names and the values are the stat changes. A +n means the stats will be multiplied by (2+n)/2, while a -n means the stats will be multiplied by 2/(2+n).")
    statuses: list[str] = Field(default_factory=list,
        description="A list of the pokemon's status conditions.")
    types: list[str] | None = Field(default=None,
        description="A list of the pokemon's types, or None if the types are not acquireable.")