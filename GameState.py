from GameData import *
from dataclasses import dataclass
import logging

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        #deprecate isRe
        self.isRe = False
        self.playableCards = []
        self.state = State(Round.ONE, Position.FIRST)
        self.partner = ""
        self.players = []
        self.DxSeen = False
        self.hand = []
        # static position over all games, not per trick
        self.playerPosition = 0
        self.team = Team.NONE
        self.myPlayerIndex = 0

    # reduce to 3, don't need myself in this
    def setPlayers(self, player1, player2, player3, player4):
        self.players.append(player1)
        self.players.append(player2)
        self.players.append(player3)
        self.players.append(player4)

        for i in range(4):
            if self.players[i].alias == me:
                self.myPlayerIndex = i
                self.playerPosition = i
                self.state.position = Position(i)
                break

    def getMyPlayer(self):
        return self.players[self.myPlayerIndex]

    # set position given winner of last round (winner : string)
    def setPosition(self, winner):        
        for i in range(4):
            if self.players[i].alias == winner:
                position = self.playerPosition - i
                if position < 0:
                    position += 4
                self.state.position = Position(position)
                break


    def setPlayerTeam(self, player, team):
        playerIndex = self.players.index(player)
        if team == Team.RE:
            self.players[playerIndex].team = Team.RE
        else:
            self.players[playerIndex].team = Team.KONTRA

        
        # hingehackt, das kann man sicher noch schöner machen
        countTeamKnown = 0
        countRe = 0
        playerUnknown = ""

        for player in self.players:
            if player.team != Team.NONE:
                countTeamKnown += 1
            else:
                playerUnknown = player.alias

            if player.team == Team.RE:
                countRe += 1

        if countTeamKnown > 2:
            if countRe == 2:
                self.setPlayerTeam(playerUnknown, Team.KONTRA)
            else:
                self.setPlayerTeam(playerUnknown, Team.RE)



    def __str__(self):
        return f'''
        Round: {self.round.name}
        Position: {self.position.name}
        isRe: {str(self.isRe)}
        playableCards: {self.playableCards}        
        partner: {self.partner}
        players: {self.players}
        DxSeen: {str(self.DxSeen)}
        '''
