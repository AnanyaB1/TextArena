import nltk, random 
from nltk import pos_tag
from nltk.corpus import words
from nltk.corpus import wordnet
nltk.download('wordnet')
import re
from typing import Optional, Tuple, List, Dict, Any
import textarena as ta


class WordleEnv(ta.Env):
    """
    Environment for Wordle game.
    """
    def __init__(self,hardcore: Optional[bool] = False, max_turns: Optional[int] = None):
        """
        Initializes the Wordle environment.
        
        Args:
            hardcore (bool): If True, use the full English word set; otherwise, use a simplified word set.
            max_turns (int): Maximum number of turns before the game ends in a draw.
        """
        super().__init__()
        self.word_length = 5
        self._load_word_list(hardcore=hardcore)
        self.max_turns = max_turns


    @property
    def terminal_render_keys(self):
        return ["rendered_board"]
    
    def _check_word(self, word: str) -> bool:
        return len(wordnet.synsets(word)) > 0
    
    def _load_word_list(self, hardcore: bool = False) -> None:
        """
        Load the word list based on the 'hardcore' parameter.

        Args:
            hardcore (bool): Determines whether to load the full or simplified word list.
        """
        # Get word list
        if hardcore:
            word_list = words.words("en")
        else:
            word_list = words.words("en-basic")

        # Filter words based on POS tags
        self.word_list = [
            word for word in word_list if pos_tag([word])[0][1] in ["NN"] and len(word) == self.word_length
        ]

    def reset(self, num_players: int = 1, seed: Optional[int] = None):
        """
        Resets the Wordle environment to its initial state.
        """
        self.state = ta.State(num_players=num_players, min_players=1, max_players=1, max_turns=self.max_turns)
        secret_word = random.choice(self.word_list)
        game_state = {
            "secret_word": secret_word,
            "guess_history": []
        }
        self.state.reset(seed=seed, game_state=game_state, player_prompt_function=self._generate_player_prompt)
    
    def _generate_player_prompt(self, player_id: int, game_state: Dict[int, Any]) -> str:
        """
        Generates the initial prompt for the player.
        """
        prompt = (
            f"You are Player {player_id} in Wordle.\n"
            f"A secret {self.word_length}-letter word has been chosen. You have {self.max_turns} attempts to guess it.\n"
            "For each guess, wrap your word in square brackets (e.g., [apple]).\n"
            "Feedback for each letter will be given as follows:\n"
            "  - G (green): correct letter in the correct position\n"
            "  - Y (yellow): letter exists in the word but in the wrong position\n"
            "  - X (wrong): letter is not in the word\n"
            "Enter your guess to begin.\n"
        )
        return prompt

    def step(self, action: str) -> Tuple[bool, ta.Info]:
        """
        Processes the player's guess and updates the game state.

        Args:
            action (str): The player's guess in the format [word].

        Returns:
            Tuple[bool, ta.Info]: (done, info)
        """
        player_id = self.state.current_player_id

        # Log the player's action
        self.state.add_observation(
            from_id=player_id,
            to_id=-1,  # broadcast to all
            message=action,
            for_logging=True
        )


        # Extract the guess using regex
        match = re.search(r"\[(\w+)\]", action)

        if match is None:
            print(f"input missing brackets")
            reason = f"Player {self.state.current_player_id} tried submitting a word in the wrong format. Please make sure to use squared brackets."
            self.state.set_invalid_move(player_id=player_id, reason=reason)
            return self.state.step()
        
        else:
            word = match.group(1).lower()
        
        if len(word) != self.word_length:
            reason = f"Player {player_id}, your word must be exactly {self.word_length} letters."
            self.state.set_invalid_move(player_id=player_id, reason=reason)
            return self.state.step()
        
        elif not self._check_word(word):
            reason = f"Player {player_id}, '{word}' is not an English word."
            self.state.set_invalid_move(player_id=player_id, reason=reason)
            return self.state.step()

        # Evaluate the word
        feedback = self._evaluate_guess(word)

        # Save the guess and feedback
        self.state.game_state["guess_history"].append((word, feedback))

        # Update board views
        self.state.game_state["rendered_board"] = self._render_board()
        self.state.game_state["player_view"] = self._render_player_view(player_id)

        # Check for win condition (all letters green)
        if all(f == "G" for f in feedback):
            self.state.set_winners([player_id], reason=f"Player {player_id} guessed the word correctly!")
        else:
            message = f"Player {player_id} submitted [{word}].\nFeedback:\n{self._render_player_view(player_id)}\nYou have {self.max_turns - self.state.turn - 1} turns left."
           
            self.state.add_observation(
                from_id=ta.GAME_ID,
                to_id=-1,
                message=message,
                for_logging=False
            )

        return self.state.step()

    def _evaluate_guess(self, guess: str) -> List[str]:
        """
        Evaluates the player's guess against the secret word and returns feedback for each letter.
        
        Feedback:
            - "green": correct letter in the correct position.
            - "yellow": letter is in the word but in the wrong position.
            - "wrong": letter is not in the word.
        
        Args:
            guess (str): The player's guess.
        
        Returns:
            List[str]: A list of feedback tokens for each letter.
        """
        secret_word = self.state.game_state["secret_word"]
        feedback = [None] * self.word_length
        secret_list = list(secret_word)
        guess_list = list(guess)

        # First pass: mark correct letters in the correct position (green)
        for i in range(self.word_length):
            if guess_list[i] == secret_list[i]:
                feedback[i] = "G"
                secret_list[i] = None  # Mark this letter as accounted for

        # Second pass: mark correct letters in the wrong position (yellow) or wrong letters
        for i in range(self.word_length):
            if feedback[i] is None:
                if guess_list[i] in secret_list:
                    feedback[i] = "Y"
                    # Remove the first occurrence of guess_list[i] from secret_list
                    index = secret_list.index(guess_list[i])
                    secret_list[index] = None
                else:
                    feedback[i] = "X"

        return feedback
    
    def _render_board(self) -> str:
        """ Renders the board in full Wordle format. """
        history = self.state.game_state["guess_history"]
        if not history:
            return "No guesses yet."

        output = []
        for word, feedback in history:
            letters_row = "| Letter  | " + " ".join(word.upper()) + " |"
            divider_row = "|---------|" + "--" * self.word_length + "--"
            status_row = "| Status  | " + " ".join(feedback) + " |"
            output.append(f"{letters_row}\n{divider_row}\n{status_row}\n")

        return "\n".join(output)
    
    def _render_player_view(self, player_id: int) -> str:
        """ Renders a simplified player view (letters and feedback only). """
        history = self.state.game_state["guess_history"]
        if not history:
            return "No guesses yet."

        output = []
        for word, feedback in history:
            word_row = " ".join(word.upper())
            feedback_row = " ".join(feedback)
            output.append(f"{word_row}\n{feedback_row}\n")

        return "\n".join(output)
