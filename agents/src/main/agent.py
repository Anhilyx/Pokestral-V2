import httpx
from langchain_openai import ChatOpenAI
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langchain_classic.agents.agent import AgentExecutor
from langchain_classic.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from main.models.response import Action
from planning.agent import Agent as PlanningAgent
from thinking.agent import Agent as ThinkingAgent
from time import sleep
import traceback
from utils.logging import LOGGER


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
        self.planning_agent = PlanningAgent(uuid, model_name, api_token)
        self.thinking_agent = ThinkingAgent(uuid, model_name, api_token)
        
        # Bind the available tools
        self.tools = [
            StructuredTool.from_function(
                func=self.plan,
                name="ask_planning",
                description="Ask the agent to plan the best action to take based on the current game context, and to give strategic advices. " + \
                            "This tool will give a natural language response explaining its chain of thought for how will the match evolve in the future and what to take into account."
            ),
            StructuredTool.from_function(
                func=self.think,
                name="ask_thoughts",
                description="Ask the agent to think about the best action to take based on the current game context, and to explain its reasoning. " + \
                            "This tool will give a natural language response explaining its chain of thought for why its answer might be the best action to take."
            )
        ]

        # Create the agent and its executor (the thinking loop)
        self.agent = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, self.tools, ChatPromptTemplate.from_messages([
                ("system", """
                    You are a professional Pokemon competitive player, and you are currently playing a match.
                    You must carefully analyze the game state before making any decision.
                """.replace("    ", "")),
                ("human", """
                    ---
                 
                    ### Response from the 'planning' agent:
                 
                    {initial_planning}
                 
                    ### Response from the 'thinking' agent:
                 
                    {initial_thoughts}
                 
                    ---
                """.replace("    ", "")),
                ("placeholder", "{agent_scratchpad}"),
            ])),
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )
    
    def run(self):
        """
        Run the agent's main loop, where it will continuously think and decide on the best action to take until the game is over.
        """

        try:
            # Ask the sub-agents a first time before starting
            LOGGER.info(f"🔄 Asking for thoughts...")
            initial_planning = self.planning_agent.think()
            sleep(1)
            initial_thoughts = self.thinking_agent.think(initial_planning)
            sleep(1)
            LOGGER.info("✅ Done.")

            # Invoke the agent to get the best action to take
            response = self.agent.invoke({
                "initial_planning": initial_planning,
                "initial_thoughts": initial_thoughts
            })["output"]
            LOGGER.info(response)

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

    #=======#
    # Tools #
    #=======#


    def plan(self, additional_context: str = "") -> str:
        """
        Ask the planning Agent to plan the best action to take, in a strategic way, based on the current game context.

        Args:
            additional_context (str, optional): Any additional context to give to the planning agent. Defaults to "".

        Returns:
            str: The final decision of the agent with its strategic advices.
        """

        LOGGER.info(f"🔄 Asking for a plan...")
        reasoning = self.planning_agent.think(additional_context)
        LOGGER.info(f"""
        ==============================

        {reasoning}

        ==============================
        """.replace("    ", ""))

        LOGGER.info("✅ Done.")
        return reasoning

    
    def think(self, additional_context: str = "") -> str:
        """
        Ask the thinking Agent to think about the best action to take, in a logical and reasoned way, based on the current game context.

        Args:
            additional_context (str, optional): Any additional context to give to the thinking agent. Defaults to "".

        Returns:
            str: The final decision of the agent with its reasoning.
        """

        LOGGER.info(f"🔄 Asking for thoughts...")
        # if comments: LOGGER.debug(f"ℹ️ Comments: {comments}")

        reasoning = self.thinking_agent.think(additional_context)
        LOGGER.info(f"""
        ==============================

        {reasoning}

        ==============================
        """.replace("    ", ""))

        LOGGER.info("✅ Done.")
        return reasoning