import re
import random
from itertools import combinations

# Define card ranks and suits
RANKS = '23456789TJQKA'
SUITS = 'cdhs'

# Generate a deck of 52 cards
DECK = [r + s for r in RANKS for s in SUITS]

def poker_decision(game_text):
    """Decides on a poker action based on game text sent"""
    hole_cards, community_cards, my_chips, opponent_chips, opponent_last_bet, opponent_prev_bet,current_round = extract_game_info(observation)
    print(f"Extracted Hole Cards: {hole_cards}, Community Cards: {community_cards}")
    # print(f"My Chips: {my_chips}, Opponent Chips: {opponent_chips}")
    # print(f"Opponent Last Bet: {opponent_last_bet}, Previous Bet: {opponent_prev_bet}")

    win_probability = simulate_win_probability(hole_cards, community_cards if community_cards else None)
    print(f"Estimated Win Probability: {win_probability * 100:.2f}%")

    # Example decision-making
    decision = poker_decision_strategy(hole_cards, win_probability, "Small Blind", opponent_last_bet, opponent_prev_bet, my_chips,current_round)
    # print(f"Recommended Action: {decision}")

    if current_round == 1:
        upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"+f"Recommended Action: {decision}"
    else:
        upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"
        # upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"+f"Recommended Action: {decision}"

    # upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"

    action = agents[player_id](upaded_observation)

    return action



def extract_game_info(game_text):
    """Extracts hole cards, community cards, and player chip counts from game text."""
    hole_cards_match = re.search(r'Your hole cards: \[(.*?)\]', game_text)
    community_cards_match = re.search(r'Visible Community Cards: \[(.*?)\]', game_text)
    player_chips_match = re.search(r'Player 1 .*?: (\d+) chips', game_text)
    opponent_chips_match = re.search(r'Player 0 .*?: (\d+) chips', game_text)
    opponent_bet_match = re.findall(r'Player 0 .*?bet=(\d+)', game_text)
    round_match = re.search(r'Round (\d+) of 10', game_text)
    
    hole_cards = hole_cards_match.group(1).split(', ') if hole_cards_match else []
    community_cards = community_cards_match.group(1).split(', ') if community_cards_match and community_cards_match.group(1) else []
    my_chips = int(player_chips_match.group(1)) if player_chips_match else 1000
    opponent_chips = int(opponent_chips_match.group(1)) if opponent_chips_match else 1000
    opponent_last_bet = int(opponent_bet_match[-1]) if opponent_bet_match else 0
    opponent_prev_bet = int(opponent_bet_match[-2]) if len(opponent_bet_match) > 1 else 0
    current_round = int(round_match.group(1)) if round_match else 1
    
    return hole_cards, community_cards, my_chips, opponent_chips, opponent_last_bet, opponent_prev_bet, current_round

def remove_used_cards(deck, used_cards):
    """Removes used cards from the deck."""
    return [card for card in deck if card not in used_cards]

def simulate_win_probability(hole_cards, community_cards=None, num_simulations=100000):
    """Simulates win probability by playing random hands."""
    wins = 0
    community_cards = community_cards if community_cards else []
    
    for _ in range(num_simulations):
        deck = remove_used_cards(DECK, hole_cards + community_cards)
        random.shuffle(deck)
        
        # Generate random opponent hole cards
        opponent_hole = deck[:2]
        remaining_deck = deck[2:]
        
        # Generate remaining community cards if none exist
        remaining_community = remaining_deck[:(5 - len(community_cards))]
        full_community = community_cards + remaining_community
        
        # Evaluate hand strengths
        player_strength = evaluate_hand_strength(hole_cards, full_community)
        opponent_strength = evaluate_hand_strength(opponent_hole, full_community)
        
        if player_strength > opponent_strength:
            wins += 1
    
    return wins / num_simulations

def evaluate_hand_strength(hole_cards, community_cards):
    """A placeholder function for hand strength evaluation (to be replaced with a real evaluator)."""
    all_cards = hole_cards + community_cards
    try:
        return sum(RANKS.index(card[0]) for card in all_cards if card)
    except ValueError:
        print("Error: Invalid card format detected.")
        return 0  # Default to lowest strength on error

def poker_decision_strategy(hole_cards, win_probability, position, opponent_last_bet, opponent_prev_bet, my_chips, current_round):
    """Decision-making strategy for a two-player Texas Hold'em game."""
    opponent_tendency = "aggressive" if opponent_last_bet > 2 * opponent_prev_bet else "normal"
    
    if current_round <=1:
        return "[Bet 50]"
    
    if my_chips > 1010:
        return "[Fold]" if win_probability < 0.9 else "[Call]"
    else:
        if win_probability < 0.2:
            return "[Fold]" if opponent_tendency == "aggressive" else "[Call]"
        else:
            # return "[Call]"
            return f'{win_probability}'




# Example Usage
game_text = """[GAME] You are Player 1 in a 2-player Texas Hold'em Poker game.
Game Information:
- This is a 10-round game
- Each player starts with 1000 chips
- Small blind is 10 chips
- Big blind is 20 chips
- Players must call the current bet to stay in the hand

Available Actions:
  '[Check]' - When there's no bet to call
  '[Call]' - Match the current bet
  '[Fold]' - Give up your hand
  '[Bet <amount>]' - Make a new bet, e.g. '[Bet 100]'
  '[Raise <amount>]' - Increase the current bet, e.g. '[Raise 200]'

The Player with the most chips at the end wins
[GAME] Your hole cards: [K♦, 3♦]
[GAME] ----- Round 1 of 10 - Turn: Pre-flop -----
Visible Community Cards: []
Pot: 30
Player 0 (Dealer/Big Blind): 980 chips, bet=20, status=active
Player 1 (Small Blind): 990 chips, bet=10, status=active
Your hole cards: K♦, 3♦"""

hole_cards, community_cards, my_chips, opponent_chips, opponent_last_bet, opponent_prev_bet, current_round = extract_game_info(game_text)
print(f"Extracted Hole Cards: {hole_cards}, Community Cards: {community_cards}")
print(f"My Chips: {my_chips}, Opponent Chips: {opponent_chips}")
print(f"Opponent Last Bet: {opponent_last_bet}, Previous Bet: {opponent_prev_bet}")
print(f"Current Round: {current_round}")

win_probability = simulate_win_probability(hole_cards, community_cards if community_cards else None)
print(f"Estimated Win Probability: {win_probability * 100:.2f}%")

# Example decision-making
decision = poker_decision_strategy(hole_cards, win_probability, "Small Blind", opponent_last_bet, opponent_prev_bet, my_chips, current_round)
print(f"Recommended Action: {decision}")


from dotenv import load_dotenv

import textarena as ta
from hackathon_code import agent

load_dotenv()

# Initialize agents
# agents = {
#     0: agent.ValidationAgent(
#         ta.agents.AnthropicAgent(model_name="claude-3-7-sonnet-20250219")
#     ),
#     1: ta.agents.AnthropicAgent(model_name="claude-3-7-sonnet-20250219"),
# }


def get_agents():
    agents = {
        0: agent.ValidationAgent(
            ta.agents.AnthropicAgent(model_name="claude-3-5-haiku-20241022")
        ),
        1: ta.agents.AnthropicAgent(model_name="claude-3-5-haiku-20241022"),
    }
    return agents


agents = {
    0: agent.ValidationAgent(
        ta.agents.AnthropicAgent(model_name="claude-3-5-haiku-20241022")
    ),
    1: ta.agents.AnthropicAgent(model_name="claude-3-5-haiku-20241022"),
}


# Initialize environment from subset and wrap it
env = ta.make(env_id="Poker-v0")
env = ta.wrappers.LLMObservationWrapper(env=env)
# Optional render wrapper
env = ta.wrappers.SimpleRenderWrapper(
    env=env,
    player_names={0: "GPT-4o-mini", 1: "claude-3.5-haiku"},
)

env.reset(num_players=len(agents))
done = False
while not done:
    player_id, observation = env.get_observation()
    print(observation)
    # hole_cards, community_cards = extract_game_info(observation)


    hole_cards, community_cards, my_chips, opponent_chips, opponent_last_bet, opponent_prev_bet,current_round = extract_game_info(observation)
    print(f"Extracted Hole Cards: {hole_cards}, Community Cards: {community_cards}")
    # print(f"My Chips: {my_chips}, Opponent Chips: {opponent_chips}")
    # print(f"Opponent Last Bet: {opponent_last_bet}, Previous Bet: {opponent_prev_bet}")

    win_probability = simulate_win_probability(hole_cards, community_cards if community_cards else None)
    print(f"Estimated Win Probability: {win_probability * 100:.2f}%")

    # Example decision-making
    decision = poker_decision_strategy(hole_cards, win_probability, "Small Blind", opponent_last_bet, opponent_prev_bet, my_chips,current_round)
    # print(f"Recommended Action: {decision}")



    # win_probability = simulate_win_probability(hole_cards, community_cards if community_cards else None)
    # print(f"Estimated Win Probability: {win_probability * 100:.2f}%")

    # advice= f"The winning probability is {win_probability * 100:.2f}%"
    # # hole_cards, community_cards = extract_game_info(observation)
    # # win_probability = simulate_win_probability(hole_cards, community_cards)
    # print(f"Estimated Win Probability: {win_probability * 100:.2f}%")

    if current_round == 1:
        upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"+f"Recommended Action: {decision}"
    else:
        upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"
        # upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"+f"Recommended Action: {decision}"

    # upaded_observation=observation+f"Estimated Win Probability: {win_probability * 100:.2f}%"

    action = agents[player_id](upaded_observation)
    # action = asyncio.get_event_loop().run_until_complete(agents[player_id](upaded_observation))

    done, info = env.step(action=action)
rewards = env.close()