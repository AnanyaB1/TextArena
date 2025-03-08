import asyncio
from typing import Optional
import anthropic
import aiohttp

STANDARD_GAME_PROMPT = "You are a competitive game player. Make sure you read the game instructions carefully, and always follow the required format."


class AsyncAgent:
    """Base class for agents that generate responses asynchronously."""

    async def __call__(self, observation: str, tools: list) -> str:
        """
        Process the observation and return the generated response.

        Args:
            observation (str): The input string to process.

        Returns:
            str: The generated response.
        """
        raise NotImplementedError("Agents must implement the __call__ method.")


class OpenRouterAgent(AsyncAgent):
    async def __call__(self, observation: str) -> str:
        aiohttp_client = aiohttp.ClientSession()


class AsyncAnthropicAgent(AsyncAgent):
    """Agent class using the Anthropic Claude API to generate responses asynchronously."""

    def __init__(
        self,
        model_name: str,
        system_prompt: Optional[str] = STANDARD_GAME_PROMPT,
        max_tokens: int = 1000,
        temperature: float = 0.9,
        verbose: bool = False,
    ):
        """
        Initialize the Anthropic agent.

        Args:
            model_name (str): The name of the Claude model (e.g., "claude-3-5-sonnet-20241022").
            system_prompt (Optional[str]): The system prompt to use (default: STANDARD_GAME_PROMPT).
            max_tokens (int): The maximum number of tokens to generate.
            temperature (float): The temperature for randomness in response generation.
            verbose (bool): If True, additional debug info will be printed.
        """
        super().__init__()
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.verbose = verbose
        self.client = anthropic.AsyncAnthropic()

    async def _make_request(self, observation: str, tools: list) -> str:
        """Make a single API request to Anthropic and return the generated message."""
        response = await self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": observation}]}
            ],
            tools=[],
        )

        return response.content[0].text.strip()

    async def _retry_request(
        self, observation: str, retries: int = 3, delay: int = 5, tools: list = []
    ) -> str:
        """
        Attempt to make an API request with retries.

        Args:
            observation (str): The input to process.
            retries (int): The number of attempts to try.
            delay (int): Seconds to wait between attempts.

        Raises:
            Exception: The last exception caught if all retries fail.
        """
        last_exception = None
        for attempt in range(1, retries + 1):
            try:
                response = await self._make_request(observation, tools)
                if self.verbose:
                    print(f"\nObservation: {observation}\nResponse: {response}")
                return response
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt} failed with error: {e}")
                if attempt < retries:
                    await asyncio.sleep(delay)
        raise last_exception

    async def __call__(self, observation: str, tools: list) -> str:
        """
        Process the observation using the Anthropic API and return the generated response.

        Args:
            observation (str): The input string to process.

        Returns:
            str: The generated response.
        """
        if not isinstance(observation, str):
            raise ValueError(
                f"Observation must be a string. Received type: {type(observation)}"
            )
        return await self._retry_request(observation, tools=[])
