"""
Sudoku Game

In this game, a single player fills a 9x9 grid with numbers from 1 to 9, ensuring that each number appears only once in each row, column, and 3x3 subgrid.

Gameplay:

    The game is played on a 9x9 grid, divided into nine 3x3 subgrids.
    The player fills the empty cells with numbers from 1 to 9.
    Each row, column, and 3x3 subgrid must contain the numbers 1 through 9 with no repetition.
    The player wins when the entire grid is correctly filled according to the rules.

Key Rules:

    The player must fill each empty cell with a number from 1 to 9.
    A number cannot repeat in any row, column, or 3x3 subgrid.
    The game can be played with hints enabled or disabled:
        Hints Enabled: The player can receive guidance on whether a number placement is correct.
        Hints Disabled: The player must solve the puzzle without any assistance.

Parameters:

    difficulty: Sets the number of pre-filled cells and the overall complexity of the puzzle (easy, medium, hard).
    hints_enabled: If True, the player can receive feedback on their moves.

Game Outcomes:

    The player wins by successfully completing the grid according to the Sudoku rules.
    The player can restart if they make an error and wish to try again.
    
"""

from typing import Any, Dict, Optional, Tuple, List
import random, re
import copy
import textarena as ta
import time

class SudokuEnv(ta.Env):
    """
    Sudoku Game Environment
    """

    def __init__(
        self, 
        difficulty: Optional[str] = "easy",
        max_turns: Optional[int] = 5,
    ):
        """
        Initialise the Sudoku Environment.
        
        Args:
            difficulty (str): The difficulty level of the game (easy, medium, hard).
            max_turns (int): The maximum number of moves allowed.
            time_limit (int): The time limit for the game.
        """
        self.environment_name = "Sudoku"
        self.difficulty = difficulty
        self.max_turns = max_turns

        ## initialise the game state
        self.state = ta.State(
            num_players=1,
            max_turns=max_turns,
            render_keys=["rendered_board"], ## ensure that the rendered board is in the game state
        )

    def _generate_board(self, difficulty: str) -> List[List[int]]:
        """
        Generate a Sudoku puzzle based on the difficulty level.
        
        Args:
            difficulty (str): The difficulty level of the game (easy, medium, hard).
            
        Returns:
            List[List[int]]: The Sudoku puzzle grid.
        """
        ## define the number of clues based on difficulty
        difficulty_levels = {
            "easy": 30, # 51 clues
            "medium": 40, # 41 clues
            "hard": 50 # 31 clues
        }
        clues = difficulty_levels.get(difficulty, 30) # default to easy

        ## generate a full grid
        full_grid = self._generate_full_grid()

        ## remove cells to create puzzle
        puzzle_grid = self._remove_cells(full_grid, clues)

        return puzzle_grid
    
    def _generate_full_grid(self) -> List[List[int]]:
        """
        Generate a fully solvable Sudiku grid using backtracking.
        
        Returns:
            List[List[int]]: The Sudoku grid.
        """
        grid = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_grid(grid)
        return grid

    def _fill_grid(self, grid: List[List[int]]) -> bool:
        """
        Recursively fills the Sudoku grid using backtracking.

        Args:
            grid (List[List[int]]): The Sudoku grid to fill.

        Returns:
            bool: True if the grid is successfully filled, False otherwise.
        """
        empty = self._find_empty(grid)
        if not empty:
            return True  # Grid is complete
        row, col = empty

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self._fill_grid(grid):
                    return True
                grid[row][col] = 0
        return False
    
    def _find_empty(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """
        Finds an empty cell in the grid.

        Args:
            grid (List[List[int]]): The Sudoku grid.

        Returns:
            Optional[Tuple[int, int]]: The row and column of an empty cell, or None if full.
        """
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """
        Checks if it's safe to place a number in a given cell.

        Args:
            grid (List[List[int]]): The Sudoku grid.
            row (int): Row index.
            col (int): Column index.
            num (int): Number to place.

        Returns:
            bool: True if safe, False otherwise.
        """
        # Check row
        if num in grid[row]:
            return False
        # Check column
        if num in [grid[i][col] for i in range(9)]:
            return False
        # Check subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def _remove_cells(self, grid: List[List[int]], clues: int) -> List[List[int]]:
        """
        Removes cells from the full grid to create a puzzle, ensuring a unique solution.

        Args:
            grid (List[List[int]]): A fully solved Sudoku grid.
            clues (int): Number of clues (filled cells) to retain.

        Returns:
            List[List[int]]: The resulting Sudoku puzzle grid.
        """
        puzzle = copy.deepcopy(grid)
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        while len(cells) > (81 - clues):
            row, col = cells.pop()
            removed = puzzle[row][col]
            puzzle[row][col] = 0

            # Make a copy to check for uniqueness
            grid_copy = copy.deepcopy(puzzle)
            solutions = []
            self._count_solutions(grid_copy, solutions)
            if len(solutions) != 1:
                # Not unique, revert the removal
                puzzle[row][col] = removed

        return puzzle

    def _solve_sudoku(self, grid: List[List[int]]) -> bool:
        """
        Solves the Sudoku puzzle using backtracking. Modifies the grid in-place.

        Args:
            grid (List[List[int]]): The Sudoku grid to solve.

        Returns:
            bool: True if solvable, False otherwise.
        """
        empty = self._find_empty(grid)
        if not empty:
            return True  # Solved
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self._solve_sudoku(grid):
                    return True
                grid[row][col] = 0
        return False

    def _count_solutions(self, grid: List[List[int]], solutions: List[List[List[int]]], limit: int = 2) -> int:
        """
        Counts the number of solutions for a given Sudoku puzzle.

        Args:
            grid (List[List[int]]): The Sudoku grid.
            solutions (List[List[List[int]]]): A list to store found solutions.
            limit (int): The maximum number of solutions to find.

        Returns:
            int: The number of solutions found.
        """
        if len(solutions) >= limit:
            return len(solutions)

        empty = self._find_empty(grid)
        if not empty:
            solutions.append(copy.deepcopy(grid))
            return len(solutions)
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                self._count_solutions(grid, solutions, limit)
                grid[row][col] = 0
        return len(solutions)
    
    def reset(
        self, 
        seed: Optional[int] = None 
    ) -> Optional[ta.Observations]:
        """
        Reset the game environment.
        
        Args:
            seed (int): The random seed for the game.
            
        Returns:
            Tuple containing:
                - observations (Optional[Dict[int, str]]): Initial observations for the player.
                - info (Dict[str, Any]): Additional information.
        """
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        ## load the puzzle
        self.game_board = self._generate_board(self.difficulty)

        return self.state.reset(
            game_state={
                "board": copy.deepcopy(self.game_board),
                "rendered_board": self._get_grid_string_with_indices(self.game_board),
                "start_time": time.time(),
                "completed": False,
            },
            player_prompt_function=self._generate_player_prompt,
        )
    
    def _generate_player_prompt(self, player_id: int) -> str:
        """
        Generate the initial prompt for the player, providing them with the Sudoku grid and instructions.

        Returns:
            str: Initial prompt for the player.
        """
        prompt = (
            f"You are Player {player_id}. You are playing Sudoku ({self.difficulty}).\n"
            "Here is the current state of the Sudoku grid. Each row is numbered from 1 to 9, and each column is also numbered from 1 to 9.\n"
            "Empty cells are represented by '.', and pre-filled cells contain digits from 1 to 9.\n\n"
            "Current Sudoku Grid:\n"
        )
        
        # Include the grid with row and column indices for clarity
        grid_str = self._get_grid_string_with_indices()
        prompt += f"{grid_str}\n\n"
        
        prompt += (
            "Your objective is to fill the empty cells in the 9x9 grid with digits from 1 to 9 such that:\n"
            "1. Each row contains all digits from 1 to 9 without repetition.\n"
            "2. Each column contains all digits from 1 to 9 without repetition.\n"
            "3. Each of the nine 3x3 subgrids contains all digits from 1 to 9 without repetition.\n\n"
            "Rules and Instructions:\n"
            "1. **Do not overwrite** the initial numbers provided in the grid.\n"
            "2. **Only fill** empty cells represented by '.'.\n"
            "3. You may respond in any manner you prefer, but ensure that your response includes the format of '[row column number]'.\n"
            # "3. **Respond only** with a single move at a time in the following format: 'row column number'.\n"
            # "   - Example: To place the number 7 in row 5, column 3, respond with '5 3 7'.\n"
            "4. **Ensure** that your move does not violate Sudoku rules. Invalid moves will result in penalties.\n"
            # "5. **Do not** include any additional text or explanations in your response.\n\n"
            "Examples:\n"
            "- **Valid Move**:\n"
            "  - Grid Snippet Before Move:\n"
            "  \n"
            "  - Move: `[5 3 7]`\n"
            "  - Explanation: Placing 7 at row 5, column 3 does not violate any Sudoku rules.\n\n"
            "- **Invalid Move** (Overwriting a pre-filled cell):\n"
            "  - Grid Snippet Before Move:\n"
            "  \n"
            "  - Move: `[1 1 9]`\n"
            "  - Explanation: Cell (1,1) is already filled with 5. You cannot overwrite it.\n\n"
            "- **Invalid Move** (Violating Sudoku rules):\n"
            "  - Grid Snippet Before Move:\n"
            "  \n"
            "  - Move: `[1 3 5]`\n"
            "  - Explanation: Placing 5 in row 1, column 3 violates the rule since 5 already exists in row 1.\n\n"
            "The history of your moves and thoughts will be appended as you play more rounds. Use the history of your move to improve your decision making by avoiding the moves you have tried. Good luck!\n\n"
        )
        
        # if self.time_limit:
        #     prompt += f"You have {self.time_limit} seconds to complete the puzzle.\n"
        
        return (-1, prompt)


    def step(
        self, 
        player_id: int, 
        action: str
    ) -> Tuple[
        Optional[ta.Observations], # observations
        Optional[ta.Rewards], # reward
        bool, # truncated
        bool, # terminated
        ta.Info # info
    ]:
        """
        Take a step in the game environment given an action from a player.
        
        Args:
            player_id (int): The ID of the player taking the action.
            action (str): The action taken by the player.
            
        Returns:
            Tuple containing:
                - observations (Optional[Dict[int, str]]): Observations for the players after the step.
                - info (Dict[str, Any]): Additional information.
        """
        ## TODO - add a regex for the action string that you're extracting. Would help to add in a [ ].
        ## TODO - Use the regex to then extract out the row, column, and number from the action string


        ## update the observations
        self.state.add_observation(
            from_id=player_id,
            to_id=-1, # this means send observation to all players (presumably, all players can see the board)
            message=action,
            for_logging=True
        )

        ## validate the actions
        ## extract the format [row column number] from the action
        print("ACTION\n", action)
        action_search_pattern = re.compile(r"\[(\d+)\s(\d+)\s(\d+)\]")
        match = action_search_pattern.search(action)

        if not match:
            self.state.set_invalid_move(
                player_ids=[player_id],
                reasons=[f"Invalid move format. Player {player_id} did not respond with valid 'row column number'."]
            )
        else:
            row, col, num = map(int, match.groups())

            row_idx, col_idx = row - 1, col - 1

            ## check if the cell is already filled in the initial grid
            if self.game_board[row_idx][col_idx] != 0:
                self.state.set_invalid_move(
                    player_ids=[player_id],
                    reasons=[f"Invalid move. Player {player_id} attempted to overwrite a pre-filled cell ({row}, {col})."]
                )
            elif self._is_move_correct(row_idx, col_idx, num):
                ## update the grid
                self.state.game_state["board"][row_idx][col_idx] = num
                self.state.add_observation(
                    from_id=ta.GAME_ID,
                    to_id=-1,
                    message=f"Board state: {self._get_grid_string_with_indices()}",
                    for_logging=False
                )
            else:
                self.state.set_invalid_move(
                    player_ids=[player_id],
                    reasons=[f"Invalid move. Player {player_id} attempted to place {num} at ({row}, {col}), which violates Sudoku rules."]
                )

            ## check if the game is completed
            if self._is_puzzle_complete():
                self.state.game_state["completed"] = True
                self.state.set_winners(
                    player_ids=[player_id],
                    reason=f"Congratulations! Player {player_id} completed the Sudoku puzzle."
                )

            ## update game board
            self.state.game_state["rendered_board"] = self._get_grid_string_with_indices(self.state.game_state["board"])

        ## step the state
        return self.state.step()
            
    def render(self):
        """
        Renders the current state of the Sudoku grid.
        """
        grid_str = self._get_grid_string_with_indices()
        print("Board State\n", grid_str)
        print(f"Turn Number {self.state.turn} of {self.max_turns}")
    
    def _get_grid_string_with_indices(self, game_board: Optional[List[int]] = None) -> str:
        """
        Converts the current grid to a formatted string with row and column indices.

        Returns:
            str: Formatted grid string with indices.
        """
        if game_board is None:
            game_board = self.state.game_state["board"]
        header = "   " + " ".join([f"C{j+1}" + ("  " if (j + 1) % 3 == 0 else "") for j in range(9)])  # Column headers
        lines = [header]
        for i, row in enumerate(game_board):
            row_str = f"R{i+1} "  # Row header
            for j, num in enumerate(row):
                cell = str(num) if num != 0 else "."
                row_str += f" {cell} "
                if (j + 1) % 3 == 0 and j < 8:
                    row_str += "| "
            lines.append(row_str.strip())
            if (i + 1) % 3 == 0 and i < 8:
                lines.append("   " + "- " * 16)

        return "\n".join(lines)
    
    def _is_move_correct(self, row: int, col: int, num: int) -> bool:
        """
        Checks if placing a number at the given position is correct.

        Args:
            row (int): Row index (0-based).
            col (int): Column index (0-based).
            num (int): Number to place.

        Returns:
            bool: True if the move is correct, False otherwise.
        """
        # Check row
        if num in self.state.game_state["board"][row]:
            return False
        # Check column
        if num in [self.state.game_state["board"][i][col] for i in range(9)]:
            return False
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.state.game_state["board"][i][j] == num:
                    return False
        return True
    
    def _is_puzzle_complete(self) -> bool:
        """
        Checks if the puzzle is completely and correctly filled.

        Returns:
            bool: True if complete, False otherwise.
        """
        for i in range(9):
            for j in range(9):
                num = self.state.game_state["board"][i][j]
                if num == 0 or not self._is_move_correct_complete(i, j, num):
                    return False
        return True
    
    def _is_move_correct_complete(self, row: int, col: int, num: int) -> bool:
        """
        Checks if the current move is still valid in the completed puzzle.

        Args:
            row (int): Row index (0-based).
            col (int): Column index (0-based).
            num (int): Number to place.

        Returns:
            bool: True if the move is correct, False otherwise.
        """
        # Temporarily remove the number to check for duplicates
        self.state.game_state["board"][row][col] = 0
        correct = self._is_move_correct(row, col, num)
        self.state.game_state["board"][row][col] = num
        return correct
