from mcp.server.fastmcp import FastMCP
from hackathon_code.negotiation import get_trade_value

mcp = FastMCP("Echo")


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"


@mcp.tool()
def negotiation_get_trade_value(observation: str, incoming: bool) -> int:
    """
    FOR THE GAME NEGOTIATION
    Gets the value of a trade given by self (format: [Offer: 2 Wheat -> 3 Wood])
    Args:
        The big string of the observation"""
    return get_trade_value(observation, incoming)


@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"
