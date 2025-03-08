"""Gets the trade value

Observation format:
'''
Current observations:
You have some resources, and your task is to trade such that the total value of your resources increases.
The resources and associated values you currently have are:
        + [Wheat]   Qty: 24   Value: 6
        + [Wood]    Qty: 20   Value: 11
        + [Sheep]   Qty: 10   Value: 14
        + [Brick]   Qty: 11   Value: 23
        + [Ore]     Qty: 14   Value: 36

You can broadcast messages, privately message someone, or make trade offers.
You can also accept or deny any offers you received previously.
Your personal valuations are shown above; your goal is to maximize your total resource value.
Available actions:
  '[Broadcast: Some message]' - Send a message to all players
  '[Whisper to X: Some message]' - Send a private message to a specific player
  '[Offer to X: 2 Wheat -> 3 Wood]' - Make a trade offer to a specific player
  '[Accept <x>]' or '[Deny <x>]' - Accept or Deny a trade offer
You may combine multiple tokens in a single turn if you like.
Game ends after 16 turns.
'''
"""

import re


def get_resource_value(observation: str) -> dict:
    """Gets the value of each resource type"""
    resources = re.findall(r"\[(\w+)\]\s+Qty:\s+(\d+)\s+Value:\s+(\d+)", observation)
    return {resource: int(value) for resource, _, value in resources}


def get_trade_value(resource_table: str, offer_text: str, incoming: bool) -> int:
    """Gets the value of a trade given by self (format: [Offer: 2 Wheat -> 3 Wood])
    Args:
        The big string of the observation"""
    resource_value_dict = get_resource_value(resource_table)
    trade = re.findall(r"\[(?:Offer: )?([\d\s\w,]+) -> ([\d\s\w,]+)\]", offer_text)
    # get last trade
    trade = trade[-1] if trade else None
    if trade:
        print(trade)

        def parse_resources(resource_text):
            resource_pattern = r"(\d+)\s+(\w+)"
            return [
                (int(quantity), resource)
                for quantity, resource in re.findall(resource_pattern, resource_text)
            ]

        resource1, resource2 = trade
        count1, resource1 = parse_resources(resource1)[0]
        count2, resource2 = parse_resources(resource2)[0]

        trade_value = (
            int(count1) * resource_value_dict[resource1]
            - int(count2) * resource_value_dict[resource2]
        )
        if incoming:
            return -trade_value
        return trade_value
    return 0
