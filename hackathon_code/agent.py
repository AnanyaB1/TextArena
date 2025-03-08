import mcp
from mcp.client.stdio import stdio_client
from mcp.client import session as mcp_session
import json
from hackathon_code import negotiation
from textarena.core import Agent

VALIDATION_PROMPT = """I am playing a game. Here was the prompt:
"{PROMPT}"

Here is the answer I gave:
"{ANSWER}"

Please ensure that the answer I gave was valid and actually fit the format required by the game.
If the answer was invalid, please provide a valid answer.

If the answer was valid, please return [VALID]
If the answer was invalid please return [INVALID]
"""


import asyncio
from typing import Optional

STANDARD_GAME_PROMPT = "You are a competitive game player. Make sure you read the game instructions carefully, and always follow the required format."


class AsyncAnthropicAgent(Agent):
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

        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Anthropic package is required for AsyncAnthropicAgent. "
                "Install it with: pip install anthropic"
            )

        self.client = anthropic.AsyncAnthropic()

    async def _make_request(self, observation: str) -> str:
        """Make a single API request to Anthropic and return the generated message."""
        response = await self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": observation}]}
            ],
        )

        return response.content[0].text.strip()

    async def _retry_request(
        self, observation: str, retries: int = 3, delay: int = 5
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
                response = await self._make_request(observation)
                if self.verbose:
                    print(f"\nObservation: {observation}\nResponse: {response}")
                return response
            except Exception as e:
                last_exception = e
                print(f"Attempt {attempt} failed with error: {e}")
                if attempt < retries:
                    await asyncio.sleep(delay)
        raise last_exception

    async def __call__(self, observation: str) -> str:
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
        return await self._retry_request(observation)


server_params = mcp.StdioServerParameters(
    command="python",  # Executable
    args=["hackathon_code/server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


class MCPAgent(AsyncAnthropicAgent):
    def __init__(self, server_params: mcp.StdioServerParameters, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.server_params = server_params

    async def _make_request(self, observation: str) -> str:
        """Make a single API request to Anthropic and return the generated message."""
        async with stdio_client(self.server_params) as streams:
            async with mcp_session.ClientSession(*streams) as session:

                try:
                    tools_result = await session.list_tools()
                    tools = tools_result.model_dump()["tools"]

                    tools = [
                        {"input_schema": tool.pop("inputSchema"), **tool}
                        for tool in tools
                        if "inputSchema" in tool
                    ]

                    print("Available tools:", tools)

                    final_response_text = ""
                    is_tool_call_pending = True
                    messages = [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": observation}],
                        }
                    ]

                    # Loop to handle multiple tool calls in a conversation
                    while is_tool_call_pending:
                        response = await self.client.messages.create(
                            model=self.model_name,
                            max_tokens=self.max_tokens,
                            temperature=self.temperature,
                            system=self.system_prompt,
                            messages=messages,
                            tools=tools,
                        )

                        print("Response:", response)

                        # Check if there's a tool_use in the response
                        is_tool_call_pending = False
                        for content_block in response.content:
                            if content_block.type == "tool_use":
                                is_tool_call_pending = True

                                tool_name = content_block.name
                                tool_input = content_block.input
                                tool_id = content_block.id

                                print(f"Tool called: {tool_name}")
                                print(f"Tool input: {json.dumps(tool_input, indent=2)}")

                                # Execute the tool using MCP session
                                try:
                                    tool_result = await session.call_tool(
                                        tool_name, tool_input
                                    )

                                    # Convert tool result to string format for Anthropic
                                    # The content must be a string, not an object
                                    tool_result_dict = tool_result.model_dump()
                                except Exception as e:
                                    if "MCP error" in str(e):
                                        tool_result_dict = {"error": str(e)}

                                result_str = json.dumps(tool_result_dict)
                                print(f"Tool result: {result_str}")

                                # Add tool call and result to messages
                                messages.append(
                                    {
                                        "role": "assistant",
                                        "content": [content_block.model_dump()],
                                    }
                                )

                                # Add tool response to messages - content must be a string
                                messages.append(
                                    {
                                        "role": "user",
                                        "content": [
                                            {
                                                "type": "tool_result",
                                                "tool_use_id": tool_id,
                                                "content": result_str,  # Now it's a string
                                            }
                                        ],
                                    }
                                )
                            elif content_block.type == "text":
                                # Accumulate text responses
                                final_response_text += content_block.text

                        # If no tool calls were made, we use the text response
                        if not is_tool_call_pending and not final_response_text:
                            final_response_text = response.content[0].text

                except Exception as e:

                    print(f"Error: {e}")
                    raise e

            return final_response_text.strip()


class ValidationAgent(Agent):
    def __init__(self, claude_agent: AsyncAnthropicAgent, num_tries: int = 5):
        self.agent = claude_agent
        self.num_tries = num_tries

    def __call__(self, observation):
        for _ in range(self.num_tries):
            print(negotiation.get_trade_value(observation, incoming=True))
            initial_answer = self.agent(observation)
            validation_prompt = VALIDATION_PROMPT.format(
                PROMPT=observation, ANSWER=initial_answer
            )
            validation_response = asyncio.run(self.agent(validation_prompt))
            if "[VALID]" in validation_response:
                return initial_answer
        return initial_answer
