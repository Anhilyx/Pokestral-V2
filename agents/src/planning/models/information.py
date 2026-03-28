from pydantic import BaseModel, Field


class Damage(BaseModel):
    """
    The estimated damage ranges that a move would deal to a defending pokemon.
    This damage is calculated not knowing the exact sets of the pokemons. It uses general assumptions, so it may not be accurate in all cases, but it should give a good estimation of the damage that a move would deal in most different cases.
    """

    atk_vs_atk: dict = Field(...,
        description="The estimated damage range that the move would deal if the attacker and the defender have an offensive set.")
    atk_vs_def: dict = Field(...,
        description="The estimated damage range that the move would deal if the attacker has an offensive set and the defender has a defensive set.")
    def_vs_atk: dict = Field(...,
        description="The estimated damage range that the move would deal if the attacker has a defensive set and the defender has an offensive set.")
    def_vs_def: dict = Field(...,
        description="The estimated damage range that the move would deal if the attacker and the defender have a defensive set.")
    

class Definition(BaseModel):
    """
    The precise definition of a term related to pokemon battles (a move, an ability or an item).
    """

    name: str = Field(...,
        description="The name of the term in english.")
    description: str = Field(...,
        description="The precise definition of the term.")