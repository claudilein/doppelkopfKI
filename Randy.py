from GameState import *
import random

class Randy:
    def __init__(self):
        return

    def suggestCard(self, gameState):
        numberOfCards = len(gameState.playableCards)
        randomCardIndex = random.randint(0, numberOfCards - 1)   
        return gameState.playableCards[randomCardIndex]

    def learn(self, gameState, points):
        return

    def saveToDisk(self):
        return