import json
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from thinking.instance import Instance


class Agent:
    """
    Reflexion Agent for Pokemon Competitive Battles using LangChain and Ollama.
    """

    def __init__(self, uuid: str, model_name: str):
        """
        Initialize the Agent with a game UUID and the name of the Ollama model to use.

        Args:
            uuid (str): Unique identifier for the game instance.
            model_name (str): The name of the Ollama model to use for the agent's reasoning.
        """

        # Initialize the game instance
        self.uuid = uuid
        self.game_instance = Instance(uuid)
        
        # Connect to the Ollama model
        self.llm = ChatOllama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
            format="json"
        )
        
        # Bind the available tools
        self.tools = [
            StructuredTool.from_function(
                func=self.game_instance.get_teams,
                name="get_teams",
                description="This tool allows you to get all the known informations about both teams. Use it if you need to check details about either team."
            ),
            StructuredTool.from_function(
                func=self.game_instance.get_definition,
                name="get_definition",
                description=(
                    "This tool allows you to get the exact definition of any move, ability or item. Use it if you're not 100% sure about any move, ability or item mentioned in the context. **Never try to guess the effect of a move, ability or item if you don't know it perfectly.**"
                )
            ),
            StructuredTool.from_function(
                func=self.game_instance.get_damage_calculation,
                name="get_damage_calculation",
                description="This tool allows you to estimate the damage of an attack, based on different stats repartition of both the attacker and the defender. Use it to estimate the damage of either your or your opponent's attacks, in order to make informed decisions about the action to take."
            ),
            StructuredTool.from_function(
                func=self.game_instance.get_log,
                name="get_log",
                description="This tool allows you to get the complete log of the battle, which is a list of strings describing the events that happened during the battle. You can use this tool to get an history of the entire match, and potentially analyse patterns in the opponent's playstyle, or reflect on your own previous actions."
            )
        ]

        # Create the agent and its executor (the thinking loop)
        self.agent = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, self.tools, ChatPromptTemplate.from_messages([
                ("system", """
                    You are a professional Pokemon competitive player, and you are currently playing a match.
                    Your goal is to select the best possible action for the current turn, and to explain why this one and not another.
                    You have access to several tools that can help you make informed decisions.

                    THINKING PROCESS :
                    1. Analyse the current game state based on the provided context, and identify the key factors that should influence your decision (e.g. the health of your Pokemon, the possible threats from the opponent, the available moves, etc...).
                    2. If you see a move, ability or item that you are not 100% sure about, use the 'get_definition' tool. Never try to guess the effect of a move, ability or item if you don't know it perfectly.
                    3. Think about the possible actions you can take (e.g. which move to use, whether to switch, etc...) and their potential consequences.
                    4. Use the 'get_damage_calculation' tool to estimate the damage of either your or your opponent's attacks, in order to make informed decisions about the action to take.
                    5. Make your decision, and explain why this one is better, and why the other options are less good.
                """.replace("    ", "")),
                ("human", """
                    Here is the current game context in JSON format:
                    {match_context}
                    
                    What's the best action to take for this turn, and why?
                """.replace("    ", "")),
                ("placeholder", "{agent_scratchpad}"),
            ])),
            tools=self.tools,
            verbose=True,
            max_iterations=50,
            handle_parsing_errors=True
        )

    def think(self, event_type: str = "new_turn") -> str:
        """
        Main thinking loop of the agent. It retrieves the current game context, feeds it to the LLM, and processes the response.

        Args:
            event_type (str): The type of event that triggered the thinking process. It can be "start", "new_turn", "player_fainted", or "opponent_fainted". This allows the agent to adapt its context retrieval based on the game state.

        Returns:
            str: The final decision of the agent with its reasoning.
        """

        # Retrieve the current game context based on the event type
        context_data = {}
        if event_type == "start":
            context_data = self.game_instance.on_game_start()
        elif event_type == "new_turn":
            context_data = self.game_instance.on_new_turn()
        elif event_type == "player_fainted":
            context_data = self.game_instance.on_player_fainted()
        elif event_type == "opponent_fainted":
            context_data = self.game_instance.on_opponent_fainted()
        context_str = json.dumps(context_data, default=lambda o: o.__dict__, indent=2)

        # Thinking loop
        response = self.agent.invoke({
            "match_context": context_str
        })

        # Return the final decision (the "output" field of the response)
        return response["output"]