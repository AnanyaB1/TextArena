""" Register all environments """

from textarena.envs.registration import register
from textarena.envs.utils.jury import OpenRouterJury


# Mastermind (single-player)
register(id="Mastermind-v0", entry_point="textarena.envs.Mastermind.env:MastermindEnv", code_length=4, num_numbers=6, max_turns=20, duplicate_numbers=False)
register(id="Mastermind-v0-hard", entry_point="textarena.envs.Mastermind.env:MastermindEnv", code_length=4, num_numbers=8, max_turns=30, duplicate_numbers=False)
register(id="Mastermind-v0-extreme", entry_point="textarena.envs.Mastermind.env:MastermindEnv", code_length=6, num_numbers=12, max_turns=50, duplicate_numbers=True)

# Crosswords (single-player)
register(id="Crosswords-v0", entry_point="textarena.envs.Crosswords.env:CrosswordsEnv", hardcore=False, max_turns=30, num_words=3)
register(id="Crosswords-v0-hardcore", entry_point="textarena.envs.Crosswords.env:CrosswordsEnv", hardcore=True, max_turns=30, num_words=3)

# FifteenPuzzle (single-player)
register(id="FifteenPuzzle-v0", entry_point="textarena.envs.FifteenPuzzle.env:FifteenPuzzleEnv", max_turns=50)

# GuessTheNumber (single-player)
register(id="GuessTheNumber-v0", entry_point="textarena.envs.GuessTheNumber.env:GuessTheNumberEnv", min_number=1, max_number=20, max_turns=10)
register(id="GuessTheNumber-v0-hardcore", entry_point="textarena.envs.GuessTheNumber.env:GuessTheNumberEnv", min_number=1, max_number=50, max_turns=7)

# GuessWho (single-player)
register(id="GuessWho-v0", entry_point="textarena.envs.GuessWho.env:GuessWhoEnv", max_turns=20)

# Hangman (single-player)
register(id="Hangman-v0", entry_point="textarena.envs.Hangman.env:HangmanEnv", hardcore=False)
register(id="Hangman-v0-hardcore", entry_point="textarena.envs.Hangman.env:HangmanEnv", hardcore=True)

# LogicPuzzle (single-player)
register(id="LogicPuzzle-v0", entry_point="textarena.envs.LogicPuzzle.env:LogicPuzzleEnv", difficulty="easy")
register(id="LogicPuzzle-v0-hard", entry_point="textarena.envs.LogicPuzzle.env:LogicPuzzleEnv", difficulty="hard")

# Minesweeper (single-player)
register(id="Minesweeper-v0", entry_point="textarena.envs.Minesweeper.env:MinesweeperEnv", rows=8, cols=8, num_mines=10, max_turns=100)
register(id="Minesweeper-v0-medium", entry_point="textarena.envs.Minesweeper.env:MinesweeperEnv", rows=10, cols=10, num_mines=20, max_turns=100)
register(id="Minesweeper-v0-hard", entry_point="textarena.envs.Minesweeper.env:MinesweeperEnv", rows=12, cols=12, num_mines=30, max_turns=100)

# Sudoku (single-player)
register(id="Sudoku-v0", entry_point="textarena.envs.Sudoku.env:SudokuEnv", clues=30, max_turns=100)
register(id="Sudoku-v0-medium", entry_point="textarena.envs.Sudoku.env:SudokuEnv", clues=40, max_turns=100)
register(id="Sudoku-v0-hard", entry_point="textarena.envs.Sudoku.env:SudokuEnv", clues=50, max_turns=100)

# TowerOfHanoi (single-player)
register(id="TowerOfHanoi-v0", entry_point="textarena.envs.TowerOfHanoi.env:TowerOfHanoiEnv", num_disks=3, max_turns=100)
register(id="TowerOfHanoi-v0-medium", entry_point="textarena.envs.TowerOfHanoi.env:TowerOfHanoiEnv", num_disks=4, max_turns=100)
register(id="TowerOfHanoi-v0-hard", entry_point="textarena.envs.TowerOfHanoi.env:TowerOfHanoiEnv", num_disks=5, max_turns=100)
register(id="TowerOfHanoi-v0-extreme", entry_point="textarena.envs.TowerOfHanoi.env:TowerOfHanoiEnv", num_disks=7, max_turns=100)

# TwentyQuestions (single-player)
register(id="TwentyQuestions-v0", entry_point="textarena.envs.TwentyQuestions.env:TwentyQuestionsEnv", hardcore=False)
register(id="TwentyQuestions-v0-hardcore", entry_point="textarena.envs.TwentyQuestions.env:TwentyQuestionsEnv", hardcore=True)

# WordLadder (single-player)
register(id="WordLadder-v0", entry_point="textarena.envs.WordLadder.env:WordLadderEnv", min_distance=5, max_distance=7, max_turns=100)
register(id="WordLadder-v0-medium", entry_point="textarena.envs.WordLadder.env:WordLadderEnv", min_distance=8, max_distance=12, max_turns=100)
register(id="WordLadder-v0-hard", entry_point="textarena.envs.WordLadder.env:WordLadderEnv", min_distance=13, max_distance=15, max_turns=100)

# WordSearch (single-player)
register(id="WordSearch-v0", entry_point="textarena.envs.WordSearch.env:WordSearchEnv", hardcore=False)
register(id="WordSearch-v0-hardcore", entry_point="textarena.envs.WordSearch.env:WordSearchEnv", hardcore=True)

# Battleship (two-player)
register(id="Battleship-v0", entry_point="textarena.envs.Battleship.env:BattleshipEnv", grid_size=10)
register(id="Battleship-v0-large", entry_point="textarena.envs.Battleship.env:BattleshipEnv", grid_size=14)
register(id="Battleship-v0-extreme", entry_point="textarena.envs.Battleship.env:BattleshipEnv", grid_size=20)

# Chess (two-player)
register(id="Chess-v0", entry_point="textarena.envs.Chess.env:ChessEnv", is_open=True, max_turns=100, show_valid=True)
register(id="Chess-v0-long", entry_point="textarena.envs.Chess.env:ChessEnv", is_open=False, max_turns=250, show_valid=True)
register(id="Chess-v0-blind", entry_point="textarena.envs.Chess.env:ChessEnv", is_open=False, max_turns=150, show_valid=False)

# ConnectFour (two-player)
register(id="ConnectFour-v0", entry_point="textarena.envs.ConnectFour.env:ConnectFourEnv", is_open=True, num_rows=6, num_cols=7)
register(id="ConnectFour-v0-blind", entry_point="textarena.envs.ConnectFour.env:ConnectFourEnv", is_open=False, num_rows=6, num_cols=7)
register(id="ConnectFour-v0-large", entry_point="textarena.envs.ConnectFour.env:ConnectFourEnv", is_open=True, num_rows=12, num_cols=15)
 
# DontSayIt (two-player)
register(id="DontSayIt-v0", entry_point="textarena.envs.DontSayIt.env:DontSayItEnv", hardcore=False, max_turns=20)
register(id="DontSayIt-v0-hardcore", entry_point="textarena.envs.DontSayIt.env:DontSayItEnv", hardcore=True, max_turns=30)
register(id="DontSayIt-v0-unlimited", entry_point="textarena.envs.DontSayIt.env:DontSayItEnv", hardcore=False, max_turns=None)

# LetterAuction (two-player)
register("LetterAuction-v0", entry_point="textarena.envs.LetterAuction.env:LetterAuctionEnv", starting_coins=100)
register("LetterAuction-v0-medium", entry_point="textarena.envs.LetterAuction.env:LetterAuctionEnv", starting_coins=50)
register("LetterAuction-v0-hard", entry_point="textarena.envs.LetterAuction.env:LetterAuctionEnv", starting_coins=25)

# MemoryGame (two-player)
register("MemoryGame-v0", entry_point="textarena.envs.MemoryGame.env:MemoryGameEnv", grid_size=4)
register("MemoryGame-v0-medium", entry_point="textarena.envs.MemoryGame.env:MemoryGameEnv", grid_size=6)
register("MemoryGame-v0-hard", entry_point="textarena.envs.MemoryGame.env:MemoryGameEnv", grid_size=8)

# ScenarioPlanning (two-player)
register(id="ScenarioPlanning-v0", entry_point="textarena.envs.ScenarioPlanning.env:ScenarioPlanningEnv", jury_class=OpenRouterJury, jury_size=11)

# SpellingBee (two-player)
register(id="SpellingBee-v0", entry_point="textarena.envs.SpellingBee.env:SpellingBeeEnv", num_letters=7)
register(id="SpellingBee-v0-small", entry_point="textarena.envs.SpellingBee.env:SpellingBeeEnv", num_letters=4)
register(id="SpellingBee-v0-large", entry_point="textarena.envs.SpellingBee.env:SpellingBeeEnv", num_letters=10)

# Taboo (two-player)
register(id="Taboo-v0", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["things"])
register(id="Taboo-v0-animals", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["animals"])
register(id="Taboo-v0-cars", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["cars"])
register(id="Taboo-v0-city/country", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["city/country"])
register(id="Taboo-v0-food", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["food"])
register(id="Taboo-v0-literature", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["literature"])
register(id="Taboo-v0-people", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["people"])
register(id="Taboo-v0-tv", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["tv"])
register(id="Taboo-v0-long", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=24, categories=["things"])
register(id="Taboo-v0-full", entry_point="textarena.envs.Taboo.env:TabooEnv", max_turns=6, categories=["animals", "cars", "city/country", "food", "literature", "people", "things", "tv"])

# TicTacToe (two-player)
register(id="TicTacToe-v0", entry_point="textarena.envs.TicTacToe.env:TicTacToeEnv")

# IteratedPrisonersDilemma (two-player)
register(id="IteratedPrisonersDilemma-v0", entry_point="textarena.envs.IteratedPrisonersDilemma.env:IteratedPrisonersDilemmaEnv", num_rounds=10, communication_turns=3, cooperate_reward=3, defect_reward=5, sucker_reward=0, mutual_defect_reward=1)

# Stratego (two-player)
register(id="Stratego-v0", entry_point="textarena.envs.Stratego.env:StrategoEnv")

# SpiteAndMalice (two-player)
register(id="SpiteAndMalice-v0", entry_point="textarena.envs.SpiteAndMalice.env:SpiteAndMaliceEnv")

# TruthAndDeception (two-player) [TODO can extend to more players]
register(id="TruthAndDeception-v0", entry_point="textarena.envs.TruthAndDeception.env:TruthAndDeceptionEnv", max_turns=6)
register(id="TruthAndDeception-v0-long", entry_point="textarena.envs.TruthAndDeception.env:TruthAndDeceptionEnv", max_turns=12)
register(id="TruthAndDeception-v0-extreme", entry_point="textarena.envs.TruthAndDeception.env:TruthAndDeceptionEnv", max_turns=50)

# UltimateTicTacToe (two-player)
register(id="UltimateTicTacToe-v0", entry_point="textarena.envs.UltimateTicTacToe.env:UltimateTicTacToeEnv")

# WordChains (two-player)
register(id="WordChains-v0", entry_point="textarena.envs.WordChains.env:WordChainsEnv")

# Debate (two-player)
register(id="Debate-v0", entry_point="textarena.envs.Debate.env:DebateEnv", max_turns=6, jury_class=OpenRouterJury, jury_size=7)
register(id="Debate-v0-medium", entry_point="textarena.envs.Debate.env:DebateEnv", max_turns=12, jury_class=OpenRouterJury, jury_size=9)
register(id="Debate-v0-long", entry_point="textarena.envs.Debate.env:DebateEnv", max_turns=30, jury_class=OpenRouterJury, jury_size=13)

# SimpleNegotiation (two-player)
register(id="SimpleNegotiation-v0", entry_point="textarena.envs.SimpleNegotiation.env:SimpleNegotiationEnv", max_turns=10)
register(id="SimpleNegotiation-v0-short", entry_point="textarena.envs.SimpleNegotiation.env:SimpleNegotiationEnv", max_turns=6)
register(id="SimpleNegotiation-v0-long", entry_point="textarena.envs.SimpleNegotiation.env:SimpleNegotiationEnv", max_turns=30)

# Negotiation (2-15 players)
register(id="Negotiation-v0", entry_point="textarena.envs.Negotiation.env:NegotiationEnv", turn_multiple=8)
register(id="Negotiation-v0-long", entry_point="textarena.envs.Negotiation.env:NegotiationEnv", turn_multiple=15)

# Snake (2-15 players)
register(id="Snake-v0", entry_point="textarena.envs.Snake.env:SnakeEnv", width=5, height=5, num_apples=2, max_turns=40)
register(id="Snake-v0-standard", entry_point="textarena.envs.Snake.env:SnakeEnv", width=10, height=10, num_apples=3, max_turns=100)
register(id="Snake-v0-large", entry_point="textarena.envs.Snake.env:SnakeEnv", width=15, height=15, num_apples=5, max_turns=10)

# LiarsDice (2-15 players)
register(id="LiarsDice-v0", entry_point="textarena.envs.LiarsDice.env:LiarsDiceEnv", num_dice=5)
register(id="LiarsDice-v0-large", entry_point="textarena.envs.LiarsDice.env:LiarsDiceEnv", num_dice=12)

# Poker (2-15 players)
register(id="Poker-v0", entry_point="textarena.envs.Poker.env:PokerEnv", num_rounds=10, starting_chips=1_000, small_blind=10, big_blind=20)
register(id="Poker-v0-long", entry_point="textarena.envs.Poker.env:PokerEnv", num_rounds=15, starting_chips=1_000, small_blind=10, big_blind=20)
register(id="Poker-v0-extreme", entry_point="textarena.envs.Poker.env:PokerEnv", num_rounds=50, starting_chips=1_000, small_blind=10, big_blind=20)

# Character Conclave (3-15 players)
register(id="CharacterConclave-v0", entry_point="textarena.envs.CharacterConclave.env:CharacterConclaveEnv", character_budget=1_000)
register(id="CharacterConclave-v0-long", entry_point="textarena.envs.CharacterConclave.env:CharacterConclaveEnv", character_budget=5_000)
register(id="CharacterConclave-v0-extreme", entry_point="textarena.envs.CharacterConclave.env:CharacterConclaveEnv", character_budget=10_000)