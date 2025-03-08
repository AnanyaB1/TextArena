"""Lets go"""

import time

from dotenv import load_dotenv

import textarena as ta
from textarena.hackathon_code import agent

load_dotenv()

MODEL_NAME = "ClaudeYYDS"
MODEL_DESCRIPTION = "You are so valid for that"
EMAIL = "dylanslavinhillier@gmail.com"

# Initialize agents

for _ in range(5):
    try:
        agent_ = agent.NormalAgent(
            agent.MCPAgent(model_name="claude-3-7-sonnet-20250219"),
            # num_tries=2,
        )

        env = ta.make_online(
            env_id=["SimpleNegotiation-v0"],
            model_name=MODEL_NAME,
            model_description=MODEL_DESCRIPTION,
            email=EMAIL,
        )
        env = ta.wrappers.LLMObservationWrapper(env=env)

        env.reset(num_players=1)

        done = False
        while not done:
            player_id, observation = env.get_observation()
            action = agent_(observation)
            done, info = env.step(action=action)
        env.close()
        print(info)
        print(f"DONE - sleeping")
        time.sleep(10)
    except Exception as e:
        print(f"EXCEPTION: {e}")
        time.sleep(30)
