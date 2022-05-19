from GameData import *
from GameState import *
from Memory import *

import os.path
import random
import logging


filename = "Rumpel_Matrix.txt"

class Brain:
    def __init__(self, memory):

        self.memory = memory
        #self.Q = [[random.random() for x in range(24)] for y in range(len(Round) * len(Position))]
        self.Q = [[0.5 for x in range(24)] for y in range(len(Round) * len(Position))]   
        
        self.learningRate = 0.1
        self.discountFactor = 0.9


        if os.path.isfile(filename):
            f = open(filename, "r")
            line = f.readline()
            stateIndex = 0
            while line:
                values = line.strip().split(" ")
                for i in range(len(values)):
                    self.Q[stateIndex][i] = float(values[i])
                line = f.readline()
                stateIndex += 1
            f.close()

    

    def suggestCard(self, gameState):
        cardIndex = 0
    
        if len(gameState.playableCards) != 1:
            # sample card according to weight

            #weights = []

            #output = "Weights: \n"

            #for card in gameState.playableCards:
            #    weights.append(brain.Q[gameState.state.getInt()][cardToInt[card]])
            #    output += str(weights[-1]) + ", "


            #output += "\n Normalized weights: \n"

            # softmax function to map weights to range (0,1) with sum = 1
            #summedE = 0.0

            #for i in range(len(weights)):
            #    summedE += math.exp(weights[i])

            #for i in range(len(weights)):            
            #    weights[i] = math.exp(weights[i]) / summedE   
            
            #    output += str(weights[i]) + ", "
           
            # accumulate weights to sample cdf

            #output += "\n CDF: \n"

            #for i in range(1, len(weights)):   
            #    weights[i] += weights[i - 1]

            #for i in range(len(weights)): 
            #    output += str(weights[i]) + ", "
        

            #randomNr = random.random()    

            #output += "\n Random: " + str(randomNr) + "\n"

            #for i in range(len(weights)):
            #    if randomNr < weights[i]:
            #        cardIndex = i
            #        output += "CardIndex: " + str(cardIndex)
            #        break

            #logging.debug(output)

            randomCard = random.randint(0, len(gameState.playableCards) - 1)    
            randomNr = random.random()

            # do proper exploration / exploitation with diminishing epsilon over nr of games played
            if (randomNr < 0.025):
                cardIndex = randomCard
            else:        
                #output = ""
                maxWeight = float("-inf")
                for i in range(len(gameState.playableCards)):
                    weight = self.Q[gameState.state.getInt()][cardToInt[gameState.playableCards[i]]]
                    #output += gameState.playableCards[i] + ": " + str(weight) + "\n"
                    if weight > maxWeight:
                        maxWeight = weight
                        cardIndex = i

                #output += "Max weight: " + str(maxWeight) + ", card: " + gameState.playableCards[cardIndex] + "\n"
                #logging.debug(output)

            
        card = gameState.playableCards[cardIndex]
        self.memory.setLastAction(cardToInt[card])
            
        restHand = list(gameState.hand)
        restHand.remove(card)
        self.memory.setLastRestHand(list(gameState.hand))
        return card



    def learn(self, gameState, points):

        for i in range(11,-1,-1):
            maxCard = float("-inf")
            if i < 11:                
                nextState = self.memory.tricks[i + 1].state

                #State(Round.ONE, Position.FIRST)
                #for p in range(4):
                #    if self.memory.tricks[i].winner == gameState.players[p]:
                #        nextState.round = Round(i + 1)
                #        nextState.position = Position(gameState.playerPosition - p)
                
                for card in self.memory.tricks[i].restHand:
                    weight = self.Q[nextState.getInt()][cardToInt[card]]
                    if weight > maxCard:
                        maxCard = weight
            else:
                maxCard = 0

                #newState = State(Round.ONE, Position.FIRST)
                #newState.round = Round(i + 1)
                #minState = float("inf")

                #for pos in Position:
                #    newState.position = pos
                #    maxCard = float("-inf")
                #    for card in self.memory.tricks[i].restHand:
                #        weight = self.Q[newState.getInt()][cardToInt[card]]
                #        if weight > maxCard:
                #            maxCard = weight
                #    if maxCard < minState:
                #        minState = maxCard
            #else:
            #    minState = 0
                
            #reward = points
            #if i != 11:
            #    reward = 0.0

            
            reward = self.memory.tricks[i].evaluateTrick() / 44.0

            # logging.debug("Trick " + str(i) + ": " + \
            #    str((1 - self.learningRate) * self.Q[self.memory.tricks[i].state.getInt()][self.memory.tricks[i].action]) + \
            #    " + " + str(self.learningRate) + " * (" + str(reward) + " + " + str(self.discountFactor) + " * " + \
            #    str(maxCard) + " = " + \
            #    str((1 - self.learningRate) * self.Q[self.memory.tricks[i].state.getInt()][self.memory.tricks[i].action] + \
            #    self.learningRate * (reward + self.discountFactor * maxCard)))

            self.Q[self.memory.tricks[i].state.getInt()][self.memory.tricks[i].action] = \
                (1 - self.learningRate) * self.Q[self.memory.tricks[i].state.getInt()][self.memory.tricks[i].action] + \
                self.learningRate * (reward + self.discountFactor * maxCard)

    
    def saveToDisk(self):
        f = open(filename, "w")

        for i in range (len(Round) * len(Position)):
            output = ""
            for j in range (24):
                output += str(self.Q[i][j]) + " "
            f.write(output + "\n")

        f.close()


