class BoardClass():
    """A class to store and handle a tic tac toe game

        Attributes:
            player_move (str): The move the player makes (X or O)
            user_name (str): The username of the player
            last_turn_name (str): The name of the last player to make a move
            num_wins (int): The number of times the player has won
            num_ties (int): The number of games the player has tied
            num_losses (int): The number of games the player has lost
            num_games (int): The number of total games the player has played
    """
    def __init__(self, player_move: str, user_name: str, last_turn_name: str, num_wins: int = 0, num_ties: int = 0, num_losses: int = 0, num_games: int = 0):
        """Make a BoardClass

        Args:
            player_move (str): The move the player makes (X or O)
            user_name (str): The username of the player
            last_turn_name (str): The name of the last player to make a move
            num_wins (int): The number of times the player has won
            num_ties (int): The number of games the player has tied
            num_losses (int): The number of games the player has lost
            num_games (int): The number of total games the player has played
        """
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.player_move = player_move

        self.user_name = user_name
        self.last_turn_name = last_turn_name
        self.num_wins = num_wins
        self.num_ties = num_ties
        self.num_losses = num_losses
        self.num_games = num_games
        

    def updateGamesPlayed(self) -> None:
        """Increment the number of games played

        """
        self.num_games += 1

    def updateWins(self) -> None:
        """Increment the number of wins
        
        """
        self.num_wins += 1

    def updateTies(self) -> None:
        """Increment the number of ties
        
        """
        self.num_ties += 1

    def updateLosses(self) -> None:
        """Increment the number of losses
        
        """
        self.num_losses += 1

    def lastTurnName(self, user_name) -> None:
        """Change the name of the user who made the last move

        Args:
            user_name: The username of the player who made the last turn.
        
        """
        self.last_turn_name = user_name

    def resetGameBoard(self) -> None:
        """Reset the game board to be empty list

        """
        for i in range(9):
            self.board[i] = " "

    def updateGameBoard(self, updated_board) -> None:
        """Replace the current gameboard with a new gameboard

            Args:
            updated_board: The board which will replace the current one

        """
        for i in range(9):
            self.board[i] = updated_board[i]

    def isWinner(self, player_move) -> bool:
        """Determine if any win conditions of tic tac toe have been met

        Args:
            player_move: The character that the player has been playing with (X or O)

        Returns:
            Returns True if the board is a winning board, False otherwise

        """
        # row 1
        if self.board[0] == player_move and self.board[1] == player_move and self.board[2] == player_move:
            return True
        
        # row 2
        elif self.board[3] == player_move and self.board[4] == player_move and self.board[5] == player_move:
            return True

        # row 3
        elif self.board[6] == player_move and self.board[7] == player_move and self.board[8] == player_move:
            return True

        # column 1
        elif self.board[0] == player_move and self.board[3] == player_move and self.board[6] == player_move:
            return True

        # column 2
        elif self.board[1] == player_move and self.board[4] == player_move and self.board[7] == player_move:
            return True

        # column 3
        elif self.board[2] == player_move and self.board[5] == player_move and self.board[8] == player_move:
            return True

        # diagonal 1
        elif self.board[0] == player_move and self.board[4] == player_move and self.board[8] == player_move:
            return True

        # diagonal 2
        elif self.board[2] == player_move and self.board[4] == player_move and self.board[6] == player_move:
            return True

        return False

    def boardIsFull(self) -> bool:
        """Determine if the board is full, signifying a tie game.

        Returns: 
            True if the board is full, False if not
        """
        spaces = 0

        for i in self.board:
            if i == " ":
                spaces += 1

        if self.isWinner(self.player_move) == False and spaces == 0:
            return True
        else:
            return False


    def printStats(self) -> None:
        """Print out all of the statistics for the player

        """
        print("\nThe stats for", self.user_name + " are: ")
        print("Last player to make a move: ", self.last_turn_name)
        print("Number of games: ", self.num_games)
        print("Number of wins: ", self.num_wins)
        print("Number of ties: ", self.num_ties)
        print("Number of losses: ", self.num_losses)

    def edit_board(self, keypad) -> None:
        """Edit the board to reflect the player's choice of where they want to make a move if the position is empty

            Args:
            keypad: The position of the board the player would like to make a move on

        """
        if self.board[int(keypad)] == " ":
            self.board[int(keypad)] = self.player_move

    def print_board(self) -> None:
        """Print out the game board so that the player can see the status of the game and decide where to make their next move

        """
        print(" %s | %s | %s " %(self.board[0], self.board[1], self.board[2]))
        print("===========")
        print(" %s | %s | %s " %(self.board[3], self.board[4], self.board[5]))
        print("===========")
        print(" %s | %s | %s " %(self.board[6], self.board[7], self.board[8]))
