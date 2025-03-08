from dotenv import load_dotenv

import textarena as ta
from hackathon_code import agent

load_dotenv()

MODEL_NAME = "ClaudeYYDS"
MODEL_DESCRIPTION = "You are so valid for that"
EMAIL = "dylanslavinhillier@gmail.com"

# Initialize agents

agent_ = agent.ValidationAgent(
    ta.agents.AnthropicAgent(model_name="claude-3-7-sonnet-20250219")
)

env = ta.make_online(
    env_id=["SpellingBee-v0", "SimpleNegotiation-v0", "Poker-v0"],
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
