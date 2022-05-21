from Memory import *
from GameData import *
from Constants import *
import time


import os.path

class Statistics:
    def __init__(self):
        self.filenameCardValues = "Statistics_CardValues.txt"
        self.filenameGames = "Statistics_Games.txt"
        self.expectedValues = [0] * 24
        self.cardValueSum = [0] * 24
        self.cardCount = [0] * 24
        self.games = []

        if os.path.isfile(self.filenameCardValues):
            f = open(self.filenameCardValues, "r")
            line = f.readline()
            lineNumber = 0
            for i in range(24):
                values = line.strip().split(" ")
                self.cardValueSum[lineNumber] = int(values[0])
                self.cardCount[lineNumber] = int(values[1])
                line = f.readline()
                lineNumber += 1
            f.close()

        if os.path.isfile(self.filenameGames):
            f = open(self.filenameGames, "r")
            line = f.readline()
            while line:
                values = line.strip().split(" ")
                self.games.append(Game(int(values[0]), int(values[1]), Team(int(values[2]))))
                line = f.readline()
            f.close()

    def rateHand(cards):
        self.computeExpectedValues()
        expectedPips = 0
        for card in cards:
            expectedPips += self.expectedValues[cardToInt[card]]
        return expectedPips

    def analyze(self, memory):
        for trick in memory.tricks:
            trick.evaluateTrick()
            # logging.debug(trick.toString())
            self.cardCount[cardToInt[trick.myCard]] += 1

            if trick.winner == me:
                self.cardValueSum[cardToInt[trick.myCard]] += trick.pips

    def addGame(self, game):
        self.games.append(game)
        
        #f = open(self.filenameGames, "a")
        #f.write(str(game.pips) + " " + str(game.points) + " " + str(game.team.value) + "\n")
        #f.close()

    def computeExpectedValues(self):                
        output = "Expected Values: \n"
        for i in range(len(self.cardValueSum)):
            self.expectedValues[i] = self.cardValueSum[i] / self.cardCount[i]
            output += intToCard[i] + ": " + str(self.expectedValues[i]) + "\n"
        logging.debug(output)

    def computePipsToPoints(self):
        startTime = time.time()

        numberOfBuckets = 24 
        bucketRange = 240 / numberOfBuckets

        bucketsRe = [0] * numberOfBuckets 
        countRe = [0] * numberOfBuckets 

        bucketsContra = [0] * numberOfBuckets 
        countContra = [0] * numberOfBuckets         

        for game in self.games:
            won = 0
            if game.points > 0:
                won = 1
            if game.team == Team.RE:                
                bucketsRe[int(game.pips / bucketRange)] += won
                countRe[int(game.pips / bucketRange)] += 1
            elif game.team == Team.KONTRA:
                bucketsContra[int(game.pips / bucketRange)] += won
                countContra[int(game.pips / bucketRange)] += 1

        output = "Expected values (Pips to points): \n"
        output += "--- RE --- \n"

        for bucket in range(numberOfBuckets):
            output += "[" + str(bucket * bucketRange) + " - " + str((bucket + 1) * bucketRange) + "]: "
            winPercentage = 0
            if countRe[bucket] > 0:
                winPercentage = bucketsRe[bucket] * 100 / countRe[bucket]
            output += str(winPercentage) + "\n"

        output += "--- CONTRA --- \n"

        for bucket in range(numberOfBuckets):
            output += "[" + str(bucket * bucketRange) + " - " + str((bucket + 1) * bucketRange) + "]: "
            winPercentage = 0
            if countContra[bucket] > 0:
                winPercentage = bucketsContra[bucket] * 100 / countContra[bucket]
            output += str(winPercentage) + "\n"


        stopTime = time.time()
        logging.debug("Time elapsed: " + str(stopTime - startTime))

        logging.debug(output)



    def save(self):
        f = open(self.filenameCardValues, "w")
        for i in range (24):
            f.write(str(self.cardValueSum[i]) + " " + str(self.cardCount[i]) + "\n")
        f.close()







