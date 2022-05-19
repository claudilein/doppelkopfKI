import logging
from GameData import *

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
         


