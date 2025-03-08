from textarena.core import Agent
from textarena.agents import AnthropicAgent

VALIDATION_PROMPT = """I am playing a game. Here was the prompt:
"{PROMPT}"

Here is the answer I gave:
"{ANSWER}"

Please ensure that the answer I gave was valid and actually fit the format required by the game.
If the answer was invalid, please provide a valid answer.

If the answer was valid, please return [VALID]
If the answer was invalid please return [INVALID]
"""


class ValidationAgent(Agent):
    def __init__(self, claude_agent: AnthropicAgent, num_tries: int = 5):
        self.agent = claude_agent
        self.num_tries = num_tries

    def __call__(self, observation):
        for _ in range(self.num_tries):
            initial_answer = self.agent(observation)
            validation_prompt = VALIDATION_PROMPT.format(
                PROMPT=observation, ANSWER=initial_answer
            )
            validation_response = self.agent(validation_prompt)
            if "[VALID]" in validation_response:
                return initial_answer
        return initial_answer
