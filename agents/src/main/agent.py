import httpx
import json
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import logging
from main.models.response import Action
import re
from thinking.agent import Agent as ThinkingAgent
import traceback


class Agent:
    """
    Main agent that have the final word on the actions to take.
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
            timeout=300,

            temperature=0
        )

        # Initialize the Thinking Agent
        self.thinking_agent = ThinkingAgent(uuid, model_name, api_token)
        
        # Bind the available tools
        self.tools = [
            StructuredTool.from_function(
                func=self.think,
                name="ask_thoughts",
                description="Ask the agent to think about the best action to take based on the current game context, and to explain its reasoning. " + \
                            "**This tool must be asked every time**, and will give a natural language response explaining its chain of thought for why its answer might be the best action to take."
            )
        ]

        # Create the agent and its executor (the thinking loop)
        self.agent = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, self.tools, ChatPromptTemplate.from_messages([
                # ("system", """
                #     You are a professional Pokemon competitive player, and you are currently playing a match.
                #     You have access to other agents that are going to help you choose the best action to take.
                #     Your goal is to centralize these advices, and then choose the best action to take based on them.

                #     RULES:
                #     - You **MUST** call every agents at least once.
                 
                #     STRUCTURE:
                #     You **MUST** answer using one of the following structures:
                #     1. If you want to use a move:
                #     ```json
                #     {{
                #         "move": "move_name",
                #         "use_mega_evolution": true/false,
                #         "use_z_move": true/false,
                #         "use_dynamax": true/false,
                #         "use_terastallization": true/false
                #     }}
                #     ```
                #     2. If you want to switch:
                #     ```json
                #     {{
                #         "pokemon": "pokemon_name"
                #     }}
                #     ```
                # """.replace("    ", "")),
                ("system", """
                    You are a professional Pokemon competitive player, and you are currently playing a match.
                    You must carefully analyze the game state before making any decision.

                    RULES:
                    - You **MUST** use the `ask_thoughts` tool to analyze the situation before taking any action.
                    - Once you have the results from the `ask_thoughts` tool, you must output your final decision strictly in JSON format. Do not add any conversational text.
                    
                    STRUCTURE:
                    You **MUST** answer using ONE of the following JSON structures enclosed in a json markdown block:
                    
                    1. If you want to use a move:
                    ```json
                    {{
                        "move": "move_name",
                        "use_mega_evolution": true/false,
                        "use_z_move": true/false,
                        "use_dynamax": true/false,
                        "use_terastallization": true/false
                    }}
                    ```
                    2. If you want to switch:
                    ```json
                    {{
                        "pokemon": "pokemon_name"
                    }}
                    ```
                """.replace("    ", "")),
                ("placeholder", "{agent_scratchpad}"),
            ])),
            tools=self.tools,
            verbose=True,
            max_iterations=50,
            handle_parsing_errors=True
        )

    def think(self) -> str:
        """
        Ask the thinking Agent to think about the best action to take, in a logical and reasoned way, based on the current game context.

        Returns:
            str: The final decision of the agent with its reasoning.
        """

        return self.thinking_agent.think()
    
    def run(self):
        """
        Run the agent's main loop, where it will continuously think and decide on the best action to take until the game is over.
        """

        try:
            # Invoke the agent to get the best action to take
            response = self.agent.invoke({})["output"]
            logging.info(response)

            # Convert the response to a JSON object
            structured_llm = self.llm.with_structured_output(Action)
            structured_response = structured_llm.invoke(
                f"Based on the following analysis, extract the final move or switch action: {response}"
            )

            # Send the action
            if structured_response:
                res = httpx.post(
                    "https://pokestral.anhilyx.fr/api/poke-env/act/",
                    params={
                        "uuid": self.uuid
                    },
                    json=structured_response.model_dump() # type: ignore
                )
                res.raise_for_status()

            # If the response is not valid, log an error
            else:
                raise ValueError(f"Invalid response from the agent: {response}")

        except Exception as e:
            traceback.print_exc()