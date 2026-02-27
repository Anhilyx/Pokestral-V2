import asyncio
import httpx
from thinking.models.information import Damage, Definition
from thinking.models.overview import AvailableActions, Overview, Teams


HTTPX_CLIENT = httpx.Client()
POKE_ENV_URL = "http://pokestral-poke-env:8000/api/poke-env"
TOOLS_URL = "http://pokestral-tools:8000/api/tools"


def get_match_overview(game_uuid: str) -> Overview:
    """
    Get a quick overview of the game state, including the active pokemons (with their known details) and the state of the field.

    Args:
        game_uuid (str): The UUID of the game to get the overview for.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the poke-env API.

    Returns:
        Overview: An Overview object containing the overview of the game state.
    """

    # Fetch all required data
    responses = [
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/turn",
            params={"uuid": game_uuid}
        ),
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/active-pokemons",
            params={"uuid": game_uuid}
        ),
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/terrain",
            params={"uuid": game_uuid}
        )
    ]

    # Check for HTTP errors or invalid responses and parse the results
    results = []
    for response in responses:
        response.raise_for_status()
        results.append(response.json())
    
    # Construct the Overview object
    return Overview(
        turn=results[0]["turn"],
        player_pokemons=results[1]["player"],
        opponent_pokemons=results[1]["opponent"],
        player_field=results[2]["player"],
        opponent_field=results[2]["opponent"],
        global_field=results[2]["field"]
    )


def get_available_actions(game_uuid: str) -> AvailableActions:
    """
    Get the list of available actions for the current turn (every usable move and every switch available).

    Args:
        game_uuid (str): The UUID of the game to get the available actions for.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the poke-env API.

    Returns:
        AvailableActions: An AvailableActions object containing the list of available actions for the current turn.
    """

    # Fetch all required data
    responses = [
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/available-moves",
            params={"uuid": game_uuid}
        ),
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/available-switches",
            params={"uuid": game_uuid}
        ),
        HTTPX_CLIENT.get(
            f"{POKE_ENV_URL}/look/available-mechanics",
            params={"uuid": game_uuid}
        )
    ]

    # Check for HTTP errors or invalid responses and parse the results
    results = []
    for response in responses:
        response.raise_for_status()
        results.append(response.json())
    
    # Construct the AvailableActions object
    return AvailableActions(
        moves=[
            move["name"]
            for move in results[0]
            if move["pp"] > 0
        ],
        switches=[
            pokemon["name"]
            for pokemon in results[1]
        ],
        mega_evolve=results[2]["mega_evolve"],
        z_move=results[2]["z_move"],
        dynamax=results[2]["dynamax"],
        terastallize=results[2]["terastallize"]

    )


def get_teams(game_uuid: str) -> Teams:
    """
    Get the teams of both players, with all the known details of each pokemon.

    Args:
        game_uuid (str): The UUID of the game to get the teams for.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the poke-env API.

    Returns:
        Teams: A Teams object containing the teams of both players, with all the known details of each pokemon.
    """

    # Fetch all required data
    response = HTTPX_CLIENT.get(
        f"{POKE_ENV_URL}/look/teams",
        params={"uuid": game_uuid}
    )

    # Check for HTTP errors or invalid responses and parse the results
    response.raise_for_status()
    data = response.json()

    # Construct the Teams object
    return Teams(
        player_team=data["player"],
        opponent_team=data["opponent"]
    )


def get_damages(move: str, attacker: str, defender: str) -> Damage:
    """
    Get the estimated damage range of a move used by an attacker on a defender.

    Args:
        move (str): The name of the move in english.
        attacker (str): The name of the attacking pokemon in english.
        defender (str): The name of the defending pokemon in english.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the tools API.

    Returns:
        Damage: A Damage object containing the estimated damage range of the move in different scenarios.
    """

    # Fetch all required data
    # TODO: Here, the known informations should be given (pokemons levels, player's pokemon set, ...)
    response = HTTPX_CLIENT.get(
        f"{TOOLS_URL}/damage-calculator/known-none",
        params={
            "moves": [move],
            "attacker": attacker,
            "defender": defender
        }
    )

    # Check for HTTP errors or invalid responses and parse the results
    response.raise_for_status()
    data = response.json()

    # Construct the Damage object
    return Damage(
        atk_vs_atk={
            "min": max(
                data["max-atk|default"][0]["min"],
                data["max-spa|default"][0]["min"],
            ),
            "max": max(
                data["max-atk|default"][0]["max"],
                data["max-spa|default"][0]["max"],
            )
        },
        atk_vs_def={
            "min": max(
                min(
                    data["max-atk|max-phys"][0]["min"],
                    data["max-atk|max-spec"][0]["min"],
                ),
                min(
                    data["max-spa|max-phys"][0]["min"],
                    data["max-spa|max-spec"][0]["min"],
                )
            ),
            "max": max(
                min(
                    data["max-atk|max-phys"][0]["max"],
                    data["max-atk|max-spec"][0]["max"],
                ),
                min(
                    data["max-spa|max-phys"][0]["max"],
                    data["max-spa|max-spec"][0]["max"],
                )
            )
        },
        def_vs_atk={
            "min": data["default|default"][0]["min"],
            "max": data["default|default"][0]["max"]
        },
        def_vs_def={
            "min": min(
                data["default|max-phys"][0]["min"],
                data["default|max-spec"][0]["min"],
            ),
            "max": max(
                data["default|max-phys"][0]["max"],
                data["default|max-spec"][0]["max"],
            )
        }
    )


def get_definition(term: str) -> Definition:
    """
    Get the precise definition of a term related to pokemon battles (a move, an ability or an item).

    Args:
        term (str): The term to get the definition for.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the tools API.

    Returns:
        Definition: A Definition object containing the definition of the term.
    """

    # Fetch all required data
    response = HTTPX_CLIENT.get(
        f"{TOOLS_URL}/dictionnary",
        params={"term": term}
    )

    # Check for HTTP errors or invalid responses and parse the results
    response.raise_for_status()
    data = response.json()

    # Construct the Definition object
    return Definition(
        name=term,
        description=data
    )


def get_log(game_uuid: str) -> list[str]:
    """
    Get the log of the battle, which is a list of strings describing the events that happened during the battle.

    Args:
        game_uuid (str): The UUID of the game to get the log for.

    Raises:
        httpx.HTTPError: If there is an error while fetching the data from the poke-env API.

    Returns:
        list[str]: The log of the battle, which is a list of strings describing the events that happened during the battle.
    """

    # Fetch all required data
    response = HTTPX_CLIENT.get(
        f"{POKE_ENV_URL}/look/log",
        params={"uuid": game_uuid}
    )

    # Check for HTTP errors or invalid responses and parse the results
    response.raise_for_status()
    data = response.json()

    return data