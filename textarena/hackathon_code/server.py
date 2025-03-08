from mcp.server.fastmcp import FastMCP
from textarena.hackathon_code.negotiation import get_trade_value
from textarena.hackathon_code.spelling_bee import get_longest_word

mcp = FastMCP("Tools")


# @mcp.resource("echo://{message}")
# def echo_resource(message: str) -> str:
#     """Echo a message as a resource"""
#     return f"Resource echo: {message}"


@mcp.tool()
def negotiation_get_trade_value(
    resource_table: str, offer_text: str, incoming: bool
) -> int:
    """
    FOR THE GAME NEGOTIATION
    Gets the value of a trade given by self (format: [Offer: 2 Wheat -> 3 Wood])
    Args:
        Input resource_table: the resource table
            e.g.         + [Wheat]   Qty: 21   Value: 5
                + [Wood]    Qty: 6    Value: 12
                + [Sheep]   Qty: 20   Value: 14
                + [Brick]   Qty: 20   Value: 27
                + [Ore]     Qty: 14   Value: 35
            Quoted exactly as in the game!
        Input observation: the trade you want to evaluate
            e.g. [Offer: 2 Wheat -> 3 Wood]
            [Offer: 100 Sheep, 2 Wheat -> 3 Wood]
        Input incoming: whether the trade is given by the other player,
        or you are evaluating your own trade
    Returns:
        The value of the trade to you
    """
    return get_trade_value(resource_table, offer_text, incoming)

@mcp.tool()
def spelling_bee_get_word(observation: str) -> str:
    """
    FOR THE GAME SPELLING BEE
    Gets the longest possible word to submit given the allowed letters and the word history
    Args:
        The big string of the observation
    Returns:
        The word to submit
    """
    return get_longest_word(observation)



# @mcp.prompt()
# def echo_prompt(message: str) -> str:
#     """Create an echo prompt"""
#     return f"Please process this message: {message}"

if __name__ == "__main__":
    mcp.run()
