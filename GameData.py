from dataclasses import dataclass, field
from Constants import *
from typing import List

@dataclass
class Player:
    alias : str
    # deprecated
    isRe : bool 
    pips : int
    team : Team

    def reset(self):
        pips = 0
        team = Team.NONE

   
@dataclass
class State:
    round : Round
    position : Position

    def getInt(self):
        return self.round.value * len(Position) + self.position.value

@dataclass
class Game:
    pips : int
    points : int
    team : Team

@dataclass
class Trick:
    cards : [str] = field(default_factory=list)
    players : [str] = field(default_factory=list)
    winner : str = ""
    highestCard : str = ""
    pips : int = 0
    restHand : [str] = field(default_factory=list)
    state : State = State(Round.ONE, Position.FIRST)
    action : int = 0
    myCard : str = ""   

    def addCard(self, card):
        self.cards.append(card)

    def addPlayer(self, player):
        self.players.append(player)

    def evaluateTrick(self):
        self.pips = 0
        for i in range(4):
            self.pips += cardPoints[self.cards[i]]
            if self.players[i] == self.winner:
                self.highestCard = self.cards[i]

        #return (1 if (self.winner == gameState.partner or self.winner == me) else -1) * points 
        return (1 if (self.winner == me) else -1) * self.pips

    def toString(self):
        output = ""
        for i in range(4):
            output += self.players[i] + ": " + self.cards[i] + "\n"
        output += "Winner: " + self.winner + "\n"
        output += "Highest card: " + self.highestCard + "\n"
        output += "My card: " + self.myCard + "\n"
        output += "Pips: " + str(self.pips) + "\n"
        output += "\n"

        return output
        
