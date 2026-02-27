import traceback

import httpx
from thinking.agent import Agent
from time import sleep


MODEL_NAME = "mistral-nemo"
MODEL_TOKEN = "your_ollama_api_token_here"



if __name__ == "__main__":

    # Warmup the model
    print(f"Warming up '{MODEL_NAME}'...")
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
        print(f"✅ Model '{MODEL_NAME}' loaded successfully!")
    except Exception as e:
        print(f"❌ Error while warming up the model: {e}")
    
    # Create the game
    res = httpx.post(
        "https://pokestral.anhilyx.fr/api/poke-env/create/fighter",
        json={
            "username": "Pokestral1",
            "password": "password",
            "opponent": "Anhilyx",
        }
    )
    res.raise_for_status()
    uuid = res.json()["uuid"]
    print(f"Game created with UUID: {uuid}")

    # Wait for the game to start
    while True:
        res = httpx.get(
            "https://pokestral.anhilyx.fr/api/poke-env/look/turn",
            params={"uuid": uuid}
        )
        if res.status_code == 200:
            print("Game is ready!")
            break
        sleep(1)

    # Create the agent and start thinking
    try:
        agent = Agent(uuid, MODEL_NAME, MODEL_TOKEN)
        print(f"""
            ==============================
                    
            {agent.think()}

            ==============================
        """.replace("    ", ""))
    except Exception as e:
        traceback.print_exc()
    finally:
        while True:
            sleep(60)