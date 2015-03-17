import tkinter as tk
import random

class Element:
    _int = -1
    def __init__(self, name):
        self._name = name
    def int(self):
        # Element's numeric value representation according to the global moves list
        return self._int
    def name(self):
        return self._name
    def compareTo(self, element):
        # Element is the element object to compare this object to
        raise NotImplementedError("Not yet implemented")

class Rock(Element):
    _int = 0
    def compareTo(self, element):
        if "Rock" in element.name():
            return "Rock equals Rock", "Tie"
        if "Paper" in element.name():
            return "Paper covers Rock", "Lose"
        if "Scissors" in element.name():
            return "Rock crushes Scissors", "Win"
        if "Lizard" in element.name():
            return "Rock crushes Lizard", "Win"
        if "Spock" in element.name():
            return "Spock vaporizes Rock", "Lose"

class Paper(Element):
    _int = 1
    def compareTo(self, element):
        if "Rock" in element.name():
            return "Paper covers Rock", "Win"
        if "Paper" in element.name():
            return "Paper equals Paper", "Tie"
        if "Scissors" in element.name():
            return "Scissors cut Paper", "Lose"
        if "Lizard" in element.name():
            return "Lizard eats Paper", "Lose"
        if "Spock" in element.name():
            return "Paper disproves Spock", "Win"

class Scissors(Element):
    _int = 2
    def compareTo(self, element):
        if "Rock" in element.name():
            return "Rock crushes Scissors", "Lose"
        if "Paper" in element.name():
            return "Scissors cut Paper", "Win"
        if "Scissors" in element.name():
            return "Scissors equals Scissors", "Tie"
        if "Lizard" in element.name():
            return "Scissors decapitate Lizard", "Win"
        if "Spock" in element.name():
            return "Spock smashes Scissors", "Lose"

class Lizard(Element):
    _int = 3
    def compareTo(self, element):
        if "Rock" in element.name():
            return "Rock crushes Lizard", "Lose"
        if "Paper" in element.name():
            return "Lizard eats Paper", "Win"
        if "Scissors" in element.name():
            return "Scissors decapitate Lizard", "Lose"
        if "Lizard" in element.name():
            return "Lizard equals Lizard", "Tie"
        if "Spock" in element.name():
            return "Lizard poisons Spock", "Win"

class Spock(Element):
    _int = 4
    def compareTo(self, element):
        if "Rock" in element.name():
            return "Spock vaporizes Rock", "Win"
        if "Paper" in element.name():
            return "Paper disproves Spock", "Lose"
        if "Scissors" in element.name():
            return "Spock smashes Scissors", "Win"
        if "Lizard" in element.name():
            return "Lizard poisons Spock", "Lose"
        if "Spock" in element.name():
            return "Spock equals Spock", "Tie"

moves = [Rock('Rock'), Paper('Paper'), Scissors('Scissors'), Lizard('Lizard'), Spock('Spock')] # Global moves list

class Player:
    def __init__(self):
        self._name = "Base Player Class"
        
    def name(self):
        return self._name
        
    def play(self):
        raise NotImplementedError("Not yet implemented")
        
    def update(self, opponentMove):
        # Called after play() with the opponent's move for this round.
        # Update any strategies that rely on previous moves here
        # There is no need to implement this method
        # opponentMove is an integer, 0-4 corresponding to the moves list
        pass

class StupidBot(Player):
    def __init__(self):
        self._name = "StupidBot"
        
    def play(self):
        return moves[0]

class RandomBot(Player):
    def __init__(self):
        self._name = "RandomBot"
        
    def play(self):
        return random.choice(moves)

class IterativeBot(Player):
    def __init__(self):
        self._name = "IterativeBot"
        self.move = 0 # start at Rock
        
    def play(self):
        result = moves[self.move]
        self.move = (self.move + 1) % 5 # Go through each move in the moves list
        return result

class LastPlayBot(Player):
    def __init__(self):
        self._name = "LastPlayBot"
        self.lastMove = 0
        
    def play(self):
        return moves[self.lastMove]
        
    def update(self, opponentMove):
        self.lastMove = opponentMove # Get opponent's last move

class Human(Player):
        def __init__(self):
                self._name = "HumanBot"
        
        def play(self):
                print("(1) : Rock\n(2) : Paper\n(3) : Scissors\n(4) : Lizard\n(5) : Spock")
                return self.getMove()
        
        def getMove(self):
                moveInt = int(input("Enter your move: "))
                try:
                        return moves[(moveInt-1)]
                except IndexError:
                        print("Invalid move. Please try again.")
                        return self.getMove()

class MyBot(Player):
    def __init__(self):
        self._name = "MyBot"
        self.bestMoves = [0]*5 # Initialize an empty list with 0s
    
    def play(self):
        return moves[self.bestMove()]
    
    def update(self,opponentMove):
        # Updates the best moves list to +1 to each move that would have won against this opponent's move
        for i,move in enumerate(moves):
            if "Win" in move.compareTo(moves[opponentMove])[1]:
                self.bestMoves[i] += 1
    
    def bestMove(self):
        # Gets the "Best move"
        # Selects the move that would have won the most times
        best = -1
        bestMove = 0
        for i,move in enumerate(self.bestMoves):
            if move > best:
                best = move
                bestMove = i
        return bestMove

def create_bot(number):
        if number == 1:
                return Human()
        elif number == 2:
                return StupidBot()
        elif number == 3:
                return RandomBot()
        elif number == 4:
                return IterativeBot()
        elif number == 5:
                return LastPlayBot()
        elif number == 6:
                return MyBot() #mybot
        else:
                print("Error in bot selection")
                exit(0)

print("Welcome to Rock, Paper, Scissors, Lizard, Spock, implemented by Kraig and Coltran.")

print("Please choose two players:\n(1) Human\n(2) StupidBot\n(3) RandomBot\n(4) IterativeBot\n(5) LastPlayBot\n(6) MyBot\n")

player1 = create_bot(int(input("Select player 1: ")))
player2 = create_bot(int(input("Select player 2: ")))

p1score = 0
p2score = 0

for x in range (1,6):
        p1move = player1.play()
        p2move = player2.play()
        
        player1.update(p2move.int())
        player2.update(p1move.int())
        
        result = p1move.compareTo(p2move)
        
        print("\nRound " + str(x) + ":")
        print("    Player 1 chose " + p1move.name())
        print("    Player 2 chose " + p2move.name())
        
        print("    " + result[0])
        if "Win" in result[1]:
                print("    Player 1 won the round")
                p1score += 1
        elif "Tie" in result[1]:
                print("    Round was a tie")
        else:
                print("    Player 2 won the round")
                p2score += 1

print("The score is " + str(p1score) + " to " + str(p2score) + ".")

if p1score > p2score:
        print("Player 1 won the game")
elif p1score == p2score:
        print("Game was a draw")
else:
        print("Player 2 won the game")