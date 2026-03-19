import json
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from thinking.models.overview import Teams
from thinking.tools import get_available_actions, get_damages, get_definition, get_log, get_match_overview, get_pokemon_type_table, get_teams, get_types_table
from threading import Thread
from utils.json_to_markdown import to_table as json_to_table
from utils.logging import LOGGER


class Agent:
    """
    Reflexion Agent for Pokemon Competitive Battles using LangChain and Ollama.
    """

    def __init__(self, uuid: str, model_name: str, api_token: str):
        """
        Initialize the Agent with a game UUID, the name of the OpenAI model to use, and an API token.

        Args:
            uuid (str): Unique identifier for the game instance.
            model_name (str): The name of the OpenAI model to use for the agent's reasoning.
            api_token (str): API token for authenticating with the OpenAI API.
        """

        # Initialize the game instance
        self.uuid = uuid
        
        def get_api_token():
            return api_token
        
        ratel_limiter = InMemoryRateLimiter(
            requests_per_second=1.0,
            check_every_n_seconds=0.1,
            max_bucket_size=1
        )

        # Connect to the OpenAI model
        self.llm = ChatOpenAI(
            model=model_name,
            base_url="https://llm.ai.anhilyx.fr",
            api_key=get_api_token,
            rate_limiter=ratel_limiter,

            temperature=0
        )

        # Retrieve and format the types table
        types_table_json = get_types_table()
        for typeAtk in types_table_json:
            for typeDef in types_table_json[typeAtk]:
                types_table_json[typeAtk][typeDef] = round(types_table_json[typeAtk][typeDef], 1)
        types_table = json_to_table(types_table_json)
        
        # Bind the available tools
        self.tools = [
            StructuredTool.from_function(
                func=self.get_detailed_teams,
                name="get_detailed_teams",
                description="Tool to get **all** the *known* information about both teams, including the stats, moves, abilities, items, etc... of each pokemon. " + \
                            "You can use it if you need to check details about pokemons that aren't currently on the field, usually to anticipate a switch."
            ),
            StructuredTool.from_function(
                func=self.get_combat_log,
                name="get_combat_log",
                description="Tool to get the complete log of the battle. Each line of the log is represented as a structured string. " + \
                            "You can use it to get an history of the entire match, and potentially analyse patterns in the opponent's playstyle or reflect on your own previous actions."
            ),
            StructuredTool.from_function(
                func=self.get_definitions,
                name="get_definitions",
                description="Tool to get the exact definition of moves, abilities and items. " + \
                            "You **must** use it whenever you see a moves/abilities/items you're not perfectly familiar with. " + \
                            "Do not try to guess the effect of a move, ability or item."
            ),
            StructuredTool.from_function(
                func=self.get_types_tables,
                name="get_types_tables",
                description="Tool to get the type effectiveness table against every pokemon in the battle, in a markdown format. " + \
                            "You **must** use it to know the precise weaknesses and resistances of each pokemon. " + \
                            "Do not try to guess the weaknesses and resistances of any pokemon."
            ),
            # StructuredTool.from_function(
            #     func=self.game_instance.get_damage_calculation,
            #     name="get_damage_calculation",
            #     description="This tool allows you to estimate the damage of an attack, based on different stats repartition of both the attacker and the defender. " + \
            #                 "Use it whenever you think about using an attack, or whenever you think the opponent might use an attack against you. " + \
            #                 "Never try to guess the damage of an attack, and never advise using a damaging move without checking its damages first."
            # ),
        ]

        # Create the agent and its executor (the thinking loop)
        self.agent = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, self.tools, ChatPromptTemplate.from_messages([
                ("system", f"""
                    You are a professional Pokemon competitive player, and you are currently playing a match.
                    Your goal is to select the best possible action for the current turn, and to explain why this one and not another.
                    You have access to several tools that can/must help you make informed decisions.
                
                    STRATEGIC ADVICES:
                    - You can switch OR use a move. Always take this into account, and don't instantly overshadow one possibility over the other.
                    - You must think about what will your opponent do on the current turn, but also try to think about their next turns (their game-plan), and include this in your reasoning.
                
                    ADDITIONAL INFORMATIONS:
                    - The item 'unknown_item' means that you don't know if and which item the pokemon is holding. So no need to ask the definition of 'unknown_item'.
                    - If a tool fails, stop using it and try to make due without it, as best as you can. However, you must take this failure into account in your reasoning, considering the result 'unknown'.

                    TYPES TABLE:
                    {types_table}
                """.replace("    ", "")),
                ("human", """
                    Here is the current game context in JSON format:
                    {match_context}
                """.replace("    ", "")),
                ("human", """
                    {comments}
                    What's the best action to take for this turn, and why?
                """),
                ("placeholder", "{agent_scratchpad}"),
            ])),
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )

    def think(self, comments: str = "") -> str:
        """
        Main thinking loop of the agent. It retrieves the current game context, feeds it to the LLM, and processes the response.

        Args:
            comments (str, optional): Additional comments or instructions to guide the agent's reasoning. Defaults to "".

        Returns:
            str: The final decision of the agent with its reasoning.
        """

        # Retrieve the current game context based on the event type
        overview = get_match_overview(self.uuid)
        teams = get_teams(self.uuid)
        actions = get_available_actions(self.uuid)

        # Format the data into a string
        context_str = f"""
            ### Your team

            Active Pokemon: {json.dumps(overview.player_pokemons[0].model_dump(), indent=2)}
            Team: {json.dumps([pokemon.name for pokemon in teams.player_team], indent=2)}

            ### Opponent's team

            Active Pokemon: {json.dumps(overview.opponent_pokemons[0].model_dump(), indent=2)}
            Team: {json.dumps([pokemon.name for pokemon in teams.opponent_team], indent=2)}

            ### Field

            Affecting your side: {json.dumps(overview.player_field, indent=2)}
            Affecting opponent's side: {json.dumps(overview.opponent_field, indent=2)}
            Affecting both sides: {json.dumps(overview.global_field, indent=2)}

            ---

            ### The actions you can choose for this turn

            Moves: {json.dumps(actions.moves, indent=2)}
            Switches: {json.dumps(actions.switches, indent=2)}
        """.replace("    ", "")

        # Thinking loop
        response = self.agent.invoke({
            "match_context": context_str,
            "comments": comments
        })

        # Return the final decision (the "output" field of the response)
        return response["output"]
    
    #=======#
    # Tools #
    #=======#

    def get_detailed_teams(self) -> Teams:
        """
        Tool to get **all** the *known* information about both teams, including the stats, moves, abilities, items, etc... of each pokemon.

        Returns:
            Teams: A dataclass containing detailed information about both teams.
        """

        LOGGER.info("🔄 Fetching detailed teams information...")
        LOGGER.info("✅ Done.")

        return get_teams(self.uuid)
    
    def get_combat_log(self) -> list[str]:
        """
        Tool to get the complete log of the battle. Each line of the log is represented as a structured string.

        Returns:
            list[str]: The combat log of the battle.
        """

        LOGGER.info("🔄 Fetching combat log...")
        LOGGER.info("✅ Done.")

        return get_log(self.uuid)

    def get_definitions(self, names: list[str]) -> dict[str, str]:
        """
        Tool to get the exact definition of moves, abilities and items.

        Args:
            names (list[str]): A list of names of moves, abilities and/or items to get the definitions of.

        Returns:
            dict[str, str]: A dictionary mapping each name to its definition.
        """

        LOGGER.info(f"🔄 Fetching definitions for {len(names)} names...")
        LOGGER.debug(f"ℹ️ Names: {names}")

        # Prepare values
        threads = []
        definitions = { name: "???" for name in names }
        def get_definition_thread(name):
            definitions[name] = get_definition(name).description

        # Fetch definitions in parallel
        for name in names:
            thread = Thread(target=get_definition_thread, args=(name,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        # Return the definitions
        LOGGER.info("✅ Done.")
        return definitions
    
    def get_types_tables(self) -> str:
        """
        Tool to get the type effectiveness table against every pokemon in the battle, in a markdown format.

        Returns:
            str: A markdown table showing the type effectiveness of each type against every pokemon in the battle.
        """

        LOGGER.info("🔄 Fetching type tables...")

        # Retrieve the current teams to get the types of each pokemon
        teams = get_teams(self.uuid)
        pokemons = set([ pokemon.name for pokemon in teams.player_team + teams.opponent_team ])

        # Retrieve the list of types
        types = get_types_table().keys()

        # Prepare values
        types_tables = { pokemon: { type: "???" for type in types } for pokemon in pokemons }
        def get_types_table_thread(pokemon):
            data: dict[str, float] = get_pokemon_type_table(pokemon)["defending"] # type: ignore
            for typeAtk in data.keys():
                data[typeAtk] = round(data[typeAtk], 1)
            types_tables[pokemon] = { type: str(data[type]) for type in types }

        # Fetch types tables in parallel
        threads = []
        for pokemon in pokemons:
            thread = Thread(target=get_types_table_thread, args=(pokemon,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        # Return the types tables
        LOGGER.info("✅ Done.")
        return json_to_table(types_tables)
        