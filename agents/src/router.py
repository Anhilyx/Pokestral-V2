from os import environ as env
from fastapi import APIRouter, FastAPI
import httpx
from main.agent import Agent
from threading import Thread
from time import sleep
from utils.logging import LOGGER

# MODEL_NAME = "Mistral Nemo"
# MODEL_NAME = "Mistral Small"
# MODEL_NAME = "Qwen 2.5"
# MODEL_NAME = "Qwen 3.5 4B"
# MODEL_NAME = "Mistral Large (Web)"
MODEL_NAME = env.get("MODEL_NAME", "Mistral Large (Web)")
MODEL_TOKEN = env.get("MODEL_TOKEN", "")

if MODEL_NAME == "" or MODEL_TOKEN == "":
    LOGGER.error("❌ MODEL_NAME and MODEL_TOKEN environment variables must be set!")
    exit(1)

# Warmup the model
while True:
    LOGGER.info(f"🧠 Warming up '{MODEL_NAME}'...")
    try:

        response = httpx.post(
            "https://ollama.ai.anhilyx.fr/api/generate",
            headers={
                "Authorization": f"Bearer {MODEL_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "prompt": "",
                "stream": False,
                "keep_alive": 300
            },
            timeout=300
        )
        response.raise_for_status()

        LOGGER.info(f"✅ Model '{MODEL_NAME}' loaded successfully!")
        break

    except Exception as e:
        LOGGER.error(f"❌ Error while warming up the model: {e}")
        sleep(10)
    

app = FastAPI()
router = APIRouter()


@router.get("/challenge")
async def challenge(username: str):
    """
    Endpoint to challenge a player on Pokestral's Showdown. This will create a new game against the specified opponent.

    Args:
        username (str): The username of the opponent to challenge.
    """

    LOGGER.info(f"⚔️ Challenging player '{username}'...")

    # Create the game
    res = httpx.post(
        "https://pokestral.anhilyx.fr/api/poke-env/create/fighter",
        json={
            "username": "Pokestral1",
            "password": "password",
            "opponent": username,
        }
    )
    res.raise_for_status()
    uuid = res.json()["uuid"]
    agent = Agent(uuid, MODEL_NAME, MODEL_TOKEN)
    LOGGER.info(f"🎮 Game created with UUID: {uuid}")

    # Start the agent in a separate thread
    Thread(target=start, args=(uuid, agent)).start()
    return True


def start(uuid: str, agent: Agent):
    """
    Function to start the agent. This will run in a separate thread and will continuously check for actions to perform in the game.

    Args:
        uuid (str): The UUID of the game to play.
        agent (Agent): The agent to run in the game.
    """

    # Loop forever
    while True is True:

        # Wait for an action to be required
        while False is False:
            res = httpx.get(
                "https://pokestral.anhilyx.fr/api/poke-env/look/turn",
                params={"uuid": uuid}
            )
            if res.status_code == 200:
                LOGGER.info("🎮 Action is available!")
                break
            sleep(1)

        # Run the main agent
        try:
            agent.run()
            print("\n" * 4)
        except Exception as e:
            LOGGER.error(f"❌ Error while running the agent: {e}")
            # traceback.print_exc()
        finally:
            sleep(1)