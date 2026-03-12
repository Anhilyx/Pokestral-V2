import traceback

import httpx
from main.agent import Agent
from time import sleep


# MODEL_NAME = "Mistral Nemo"
# MODEL_NAME = "Mistral Small"
# MODEL_NAME = "Qwen 2.5"
# MODEL_NAME = "Qwen 3.5 4B"
MODEL_NAME = "Mistral Large (Web)"
MODEL_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


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
    sleep(10)
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
    agent = Agent(uuid, MODEL_NAME, MODEL_TOKEN)
    print(f"Game created with UUID: {uuid}")

    # Loop forever
    while True is True:

        # Wait for an action to be required
        while False is False:
            res = httpx.get(
                "https://pokestral.anhilyx.fr/api/poke-env/look/turn",
                params={"uuid": uuid}
            )
            if res.status_code == 200:
                print("Action is available!")
                break
            sleep(1)

        # Run the main agent
        try:
            agent.run()
            print("\n" * 4)
        except Exception as e:
            traceback.print_exc()
        finally:
            sleep(1)