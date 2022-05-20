import logging
from GameData import *

# At the beginning of the trick, memory space for it is reserved. 
# While other players (and myself) play the cards, I fill the space with information about that trick,
# e.g. who played what card, what action did I choose and what did my rest hand look like at that point in time.
class Memory:
    def __init__(self):             
        self.tricks = []
        

    def resetMemory(self):
        self.tricks.clear()

    def addNewEmptyTrick(self):
        self.tricks.append(Trick())

    def isValid(self):
        if len(self.tricks) > 0:
             return True
        else:
            logging.debug("Memory :: isValid : Trick array is empty.")
            return False

    def storeMyCard(self, card):
        if self.isValid():
            self.tricks[-1].myCard = card

    def storeCard(self, card):
        if self.isValid():
             self.tricks[-1].addCard(card)

    def storePlayer(self, player):
        if self.isValid():
             self.tricks[-1].addPlayer(player)
       
    def storeWinner(self, winner):
        if self.isValid():
            self.tricks[-1].winner = winner

    def storeAction(self, action):
        if self.isValid():
            self.tricks[-1].action = action

    def storeState(self, state):
        if self.isValid():
            self.tricks[-1].state = state

    def storeRestHand(self, restHand):
        if self.isValid():
            self.tricks[-1].restHand = restHand
         


