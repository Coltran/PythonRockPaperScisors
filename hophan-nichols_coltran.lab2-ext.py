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
    def __init__(self, modal, root):
        self._name = "HumanBot"
        self.modal = modal
        self.root = root
    
    def play(self):
        self.modal.setUp()
        self.root.wait_window(self.modal.top) # wait for the user to input their move
        
        
        return moves[self.modal.choice]

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



class HumanModal():
    # Modal window that asks the human to input their move
    def __init__(self, parent, player):
        self.parent = parent # parent window
        self.player = player # player number[0-1]
    def setUp(self):
        top = self.top = tk.Toplevel(self.parent)
        self.label = tk.Label(top, text="Pick a move player " + str(self.player+1) + ":")
        self.label.pack()
        self.humanButtons = [0]*5
        self.humanButtons[0] = tk.Button(top, text="Rock", command=lambda: self.setChoice(0))
        self.humanButtons[0].number = 0
        self.humanButtons[1] = tk.Button(top, text="Paper", command=lambda: self.setChoice(1))
        self.humanButtons[1].number = 1
        self.humanButtons[2] = tk.Button(top, text="Scissors", command=lambda: self.setChoice(2))
        self.humanButtons[2].number = 2
        self.humanButtons[3] = tk.Button(top, text="Lizard", command=lambda: self.setChoice(3))
        self.humanButtons[3].number = 3
        self.humanButtons[4] = tk.Button(top, text="Spock", command=lambda: self.setChoice(4))
        self.humanButtons[4].number = 4
        for button in self.humanButtons:
            button.pack()

    def setChoice(self, choice):
        # Set the users choice and return to the parent window
        self.choice = choice
        self.top.destroy()

class Application(tk.Frame):
    # Base application frame
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="white")
        
        self.parent = parent
        
        self.initUI()
        self.players = [None,None]
        self.currentPlayer = 0
    
    def initUI(self):
        titleLabel = tk.Label(self, text="Pick player 1")
        titleLabel.pack()
        self.titleLabel = titleLabel
        
        # Each bot button will call botButtonPressed with their bot number
        self.botButton1 = tk.Button(self, text="Human", command=lambda: self.botButtonPressed(1))
        self.botButton1.pack()
        
        self.botButton2 = tk.Button(self, text="StupidBot", command=lambda: self.botButtonPressed(2))
        self.botButton2.pack()
        
        self.botButton3 = tk.Button(self, text="RandomBot", command=lambda: self.botButtonPressed(3))
        self.botButton3.pack()
        
        self.botButton4 = tk.Button(self, text="IterativeBot", command=lambda: self.botButtonPressed(4))
        self.botButton4.pack()
        
        self.botButton5 = tk.Button(self, text="LastPlayBot", command=lambda: self.botButtonPressed(5))
        self.botButton5.pack()
        
        self.botButton6 = tk.Button(self, text="MyBot", command=lambda: self.botButtonPressed(6))
        self.botButton6.pack()
    
        self.textArea = tk.Label(self, justify=tk.LEFT)
        
        self.parent.title("Rock, Paper, Scissors, Lizard, Spock")
        self.pack(fill=tk.BOTH, expand=1)
    

    def botButtonPressed(self, bot):
        if bot == 1:
            self.players[self.currentPlayer] = Human(HumanModal(self.parent,self.currentPlayer), self.parent)
        elif bot == 2:
            self.players[self.currentPlayer] = StupidBot()
        elif bot == 3:
            self.players[self.currentPlayer] = RandomBot()
        elif bot == 4:
            self.players[self.currentPlayer] = IterativeBot()
        elif bot == 5:
            self.players[self.currentPlayer] = LastPlayBot()
        elif bot == 6:
            self.players[self.currentPlayer] = MyBot()
        else:
            print("Error in bot selection")
            exit(0)
        
        if self.currentPlayer == 0:
            # Pick second player
            self.nextPick()
        else:
            # Both players picked
            self.playGame()

    def nextPick(self):
        self.titleLabel["text"] = "Pick Player 2"
        self.currentPlayer += 1

    def removeButtons(self):
        # Remove the bot buttons from the UI
        self.botButton1.pack_forget()
        self.botButton2.pack_forget()
        self.botButton3.pack_forget()
        self.botButton4.pack_forget()
        self.botButton5.pack_forget()
        self.botButton6.pack_forget()

    def addTextToTextArea(self, text):
        self.textArea["text"] = self.textArea["text"] + text + "\n"
    
    def playGame(self):
        self.removeButtons()

        self.titleLabel["text"] = "Rock, Paper, Scissors, Lizard, Spock!"
        self.textArea.pack()

        p1score = 0
        p2score = 0

        for x in range (1,6):
            p1move = self.players[0].play()
            p2move = self.players[1].play()
            
            

            
            result = p1move.compareTo(p2move)
            
            self.addTextToTextArea("\nRound " + str(x) + ":")
            self.addTextToTextArea("    Player 1 chose " + p1move.name())
            self.addTextToTextArea("    Player 2 chose " + p2move.name())
            
            self.addTextToTextArea("    " + result[0])
            if "Win" in result[1]:
                self.addTextToTextArea("    Player 1 won the round")
                p1score += 1
            elif "Tie" in result[1]:
                self.addTextToTextArea("    Round was a tie")
            else:
                self.addTextToTextArea("    Player 2 won the round")
                p2score += 1
            self.players[1].update(p1move.int())
            self.players[0].update(p2move.int())

        self.addTextToTextArea("\nThe score is " + str(p1score) + " to " + str(p2score) + ".")


        if p1score > p2score:
            self.addTextToTextArea("Player 1 won the game")
        elif p1score == p2score:
            self.addTextToTextArea("Game was a draw")
        else:
            self.addTextToTextArea("Player 2 won the game")




root = tk.Tk()
root.geometry("400x600+300+300")
app = Application(root)
root.mainloop()
