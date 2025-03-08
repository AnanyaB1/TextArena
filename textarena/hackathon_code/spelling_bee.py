import itertools
import re
from textarena.utils.word_lists import EnglishDictionary

dictionary = EnglishDictionary()

def get_longest_word(observation: str) -> str:
    """
    FOR THE GAME SPELLING BEE
    Gets the longest possible word to submit given the allowed letters and the word history.
    
    Args:
        observation (str): The big string of the game observation.
    
    Returns:
        str: The best valid word to submit.
    """

    print("in function call for spelling bee=====================")

    # Extract allowed letters
    match = re.search(r"Allowed Letters:\s*([a-z]+)", observation, re.IGNORECASE)
    allowed_letters = set(match.group(1)) if match else set()

    # Extract used words
    used_words = set(re.findall(r"\[([a-zA-Z]+)\]", observation))

    if not allowed_letters:
        return "[pass]"

    # Generate valid words
    valid_words = set()
    for length in range(4, len(allowed_letters) + 1):
        for combo in itertools.combinations(allowed_letters, length):
            for perm in itertools.permutations(combo):
                word = "".join(perm)
                if word not in used_words and dictionary.is_english_word(word):
                    valid_words.add(word)
    
    print(f"valid words: {valid_words}")

    # Return the longest valid word, or pass if none found
    return f"[{max(valid_words, key=len)}]" if valid_words else "[pass]"

# class SpellingBeeAgent:
#     def init(self, dictionary: EnglishDictionary, num_tries: int = 1):
#         self.dictionary = dictionary
#         self.num_tries = num_tries

#     def extract_allowed_letters(self, observation):
#         """
#         Extracts the allowed letters from the Spelling Bee game observation.
#         """
#         match = re.search(r"Allowed Letters:\s*([a-z]+)", observation, re.IGNORECASE)
#         if match:
#             return set(match.group(1))
#         return set()

#     def generate_valid_words(self, letters, used_words):
#         """
#         Generate valid words using the allowed letters, avoiding already used words.
#         """
#         if not letters:
#             return []
        
#         valid_words = set()
#         for length in range(4, len(letters) + 1):
#             for combo in itertools.combinations(letters, length):
#                 for perm in itertools.permutations(combo):
#                     word = "".join(perm)
#                     if word not in used_words and self.dictionary.is_english_word(word):
#                         valid_words.add(word)
        
#         return sorted(valid_words, key=len, reverse=True)  # Longest words first

#     def extract_used_words(self, observation):
#         """
#         Extracts used words from the observation.
#         """
#         words = re.findall(r"\[([a-zA-Z]+)\]", observation)
#         return set(re.findall(r"\[([a-zA-Z]+)\]", observation))

#     def call(self, observation):
#         """
#         Processes the game observation and returns the best valid word.
#         """
#         letters = self.extract_allowed_letters(observation)
#         used_words = self.extract_used_words(observation)
#         valid_words = self.generate_valid_words(letters, used_words)
        
#         return f"[{valid_words[0]}]" if valid_words else "[pass]"