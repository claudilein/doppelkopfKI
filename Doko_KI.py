import sys
import re
from enum import Enum
from dataclasses import dataclass
import logging
import time
import math

from Constants import *
from Brain import *
from Randy import *
from GameState import *
from GameData import *
from Memory import *
from Statistics import *


            
        

# Utility functions

def eprint(input):
    sys.stderr.write(input + "\n")
    sys.stderr.flush()

def printf(input):
    print(input, flush = True)

# Communication

def outputHello():
    printf("Hallo, ich bin " + me)

def outputAnnouncement():
    printf("Ansage Keine")

def outputCard(gameState):
    memory.storeState(State(gameState.state.round, gameState.state.position))    
    card = brain.suggestCard(gameState)
    memory.storeMyCard(card)
    gameState.hand.remove(card)
    printf("Karte " + card)   
   


def recognizePartner(gameState, player):   
    
    # DEPRECATE

    if gameState.players[0].alias == player:
        gameState.players[0].isRe = True
    elif gameState.players[1].alias == player:
        gameState.players[1].isRe = True
    elif gameState.players[2].alias == player:
        gameState.players[2].isRe = True
                        
    # if someone revealed their team and it's my team
    for player in gameState.players:
        if player.team != Team.NONE and player.team == gameState.team:
            gameState.partner = player
            break

        


    if gameState.DxSeen == True:
        if gameState.players[0].isRe == False:
            gameState.partner = gameState.players[0]
        elif gameState.players[1].isRe == False:
            gameState.partner = gameState.players[1]
        elif gameState.players[1].isRe == False:
            gameState.partner = gameState.players[1]
    else:
        gameState.DxSeen = True
        if gameState.isRe == True:
            gameState.partner = player

# inputCard - player : string, card : string
def inputCard(player, card):    
    memory.storeCard(card)
    memory.storePlayer(player)
    if card == "Dx":
        recognizePartner(gameState, player)

# inputTrick - trickNumber : int
def inputTrick(trickNumber):    
    gameState.state.round = Round(trickNumber - 1)
    memory.addNewEmptyTrick()

# inputPlayable - cards : string[]
def inputPlayable(cards):        
    gameState.playableCards.clear()
    for card in cards:
        gameState.playableCards.append(card)   

# inputPlayer - player1 : string, player2 : string, player3 : string, player4 : string
def inputPlayers(player1, player2, player3, player4):
    gameState.setPlayers(Player(player1, False, 0, Team.NONE),
                        Player(player2, False, 0, Team.NONE),
                        Player(player3, False, 0, Team.NONE),
                        Player(player4, False, 0, Team.NONE))
    
# inputHand - cards : string[]
def inputHand(cards):
    for card in cards:
        if card == "Dx":
            # deprecate isRe
            gameState.isRe = True
            gameState.team = Team.RE
            gameState.getMyPlayer().team = Team.RE
            break

    if gameState.team == Team.NONE:
        gameState.team = Team.KONTRA
        gameState.getMyPlayer().team = Team.KONTRA

    gameState.hand = cards

# inputPips - pips : [player : string, pips : int]
def inputPips(pips):

    return
    #for player in pips:
    #    for j in range(4):
    #        if gameState.players[j].alias == player[0]:
    #            # Ermittelt Spieler, der den letzten Stich gewonnen hat
    #            if player[1] > gameState.players[j].points:
    #                if len(memory.tricks) > 0:
    #                    # Setzte Gewinner vom letzten Stich
    #                    memory.storeWinner(gameState.players[j].alias)
    #                gameState.players[j].points = player[1]
    #                
    #                gameState.setPosition(gameState.players[j].alias)

# inputMatch - matchNumber : int
def inputMatch(matchNumber):    
    gameState.reset()
    if matchNumber > 1:                
        memory.resetMemory()
        if matchNumber % 100 == 0:
            brain.saveToDisk()
            statistics.computeExpectedValues()
            statistics.computePipsToPoints()
            statistics.save()

# inputPoints - points: [player : string, points : int]
def inputPoints(points):
    myPoints = 0
    for player in points:
        if player[0] == me:
            myPoints = player[1]

    for player in gameState.players:
        if player.alias == me:
            statistics.addGame(Game(player.pips, myPoints, player.team))            
                    
    brain.learn(gameState, myPoints)
    statistics.analyze(memory)
    


# inputAnnouncement - player : string, announcement : string
def inputAnnouncement(player, announcement):
    if announcement == "Re":
        gameState.setPlayerTeam(player, Team.RE)
    else:
        gameState.setPlayerTeam(player, Team.KONTRA)

def inputTakes(player, pips):    
    memory.storeWinner(player)
    for j in range(4):
        if gameState.players[j].alias == player:
            gameState.setPosition(gameState.players[j].alias)
            gameState.players[j].pips += pips


def readInput(gameState):
    input = sys.stdin.readline()
    params = re.split(' |\n', input)

    if len(params) > 0:
        if params[0] == "Karte":
            inputCard(params[1], params[2])

        elif params[0] == "Karte?":
            outputCard(gameState)

        elif params[0] == "Stich":
            inputTrick(int(params[1]))

        elif params[0] == "Spielbar":
            inputPlayable(params[2:-1])

        elif params[0] == "Hallo?":
            outputHello()

        elif params[0] == "Ansage?":
            outputAnnouncement()

        elif params[0] == "Spieler":
            inputPlayers(params[1], params[2], params[3], params[4])
            
        elif params[0] == "Hand":
            inputHand(params[2:-1])

        elif params[0] == "Augen":
            pips = []
            for i in range(1,8,2):                
                pips.append([params[i], int(params[i + 1])])
                
            inputPips(pips)
            
        elif params[0] == "Partie":
            inputMatch(int(params[1]))

        elif params[0] == "Punkte":
            points = []
            for i in range(1,8,2):                
                points.append([params[i], int(params[i + 1])])

            inputPoints(points)

        elif params[0] == "Ansage":
            inputAnnouncement(params[1], params[2])

        elif params[0] == "Nimmt":
            inputTakes(params[1], int(params[2]))
            
        elif params[0] == "Feierabend":
            exit()


### MAIN ###
            
random.seed()
memory = Memory()
# brain = Brain(memory)
brain = Randy()
gameState = GameState()
statistics = Statistics()
logging.basicConfig(filename='debug.log',level=logging.DEBUG)


with open('debug.log', 'w'):
    pass


while True:
    readInput(gameState)



 