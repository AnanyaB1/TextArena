from dotenv import load_dotenv

import textarena as ta
from textarena.hackathon_code import agent

load_dotenv()

# Initialize agents
agents = {
    0: agent.ValidationAgent(agent.MCPAgent(model_name="claude-3-5-haiku-20241022")),
    1: ta.agents.HumanAgent(),
}

# Initialize environment from subset and wrap it
env = ta.make(env_id="SimpleNegotiation-v0")
env = ta.wrappers.LLMObservationWrapper(env=env)
# Optional render wrapper
# env = ta.wrappers.SimpleRenderWrapper(
#     env=env,
#     player_names={0: "claude 3.5", 1: "human"},
# )

env.reset(num_players=len(agents))
done = False
while not done:
    player_id, observation = env.get_observation()
    action = agents[player_id](observation)
    done, info = env.step(action=action)
rewards = env.close()
