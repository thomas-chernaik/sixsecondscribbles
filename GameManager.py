import random
import string
import time


class Game:
    def __init__(self, code, socket):
        self.socket = socket
        self.cards = {0: [["items beginning with c",
                           ["cucumber", "carrot", "candy", "candle", "cactus", "cage", "cake", "cars", "cow",
                            "court"]]] * 10}
        self.usedCards = []
        self.players = []
        self.code = code
        self.rounds = 0
        self.current_round = 0
        self.scores = {}
        self.locked = False
        self.current_difficulty = 0
        self.difficulty_votes = {}
        self.roundStartTime = 0
        self.drawLeadTime = 5
        self.drawTime = 60
        self.displayLeaderboardTime = 20
        self.startVotes = 0
        self.numToPass = 0
        self.numScored = 0
        self.players_cards = {}
        self.startVotesPlayers = set()

    def add_player(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.players.append(player)
        self.scores[player] = 0
        self.locked = False

    def get_card(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if len(self.usedCards) == len(self.cards):
            self.usedCards = []
        card = random.choice(self.cards[self.current_difficulty])
        while card in self.usedCards:
            card = random.choice(self.cards[self.current_difficulty])
        self.usedCards.append(card)
        self.players_cards[player] = card[0]
        self.locked = False
        return card

    def get_players_card(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        playerNum = self.players.index(player) + self.numToPass
        if playerNum >= len(self.players):
            playerNum -= len(self.players)
        card = self.players_cards[self.players[playerNum]]
        self.locked = False
        return self.players[playerNum]  # return card

    def add_score(self, player1, player2, score):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.numScored += 1
        self.scores[player1] += score
        self.scores[player2] += score
        if self.numScored == len(self.players):
            self.socket.emit('displayLeaderboard', self.code)
        self.locked = False

    def get_leaderboard(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        leaderboard = []
        for player in self.players:
            leaderboard.append((player, self.scores[player]))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        # add the rank to the leaderboard
        for i in range(len(leaderboard)):
            leaderboard[i] = (leaderboard[i][0], leaderboard[i][1], i + 1)
        self.locked = False
        return leaderboard

    def vote_on_difficulty(self, player, difficulty):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if player not in self.difficulty_votes:
            self.difficulty_votes[player] = difficulty
        self.locked = False

    def set_difficulty(self):
        # get the most popular vote for difficulty
        while self.locked:
            time.sleep(1)
        self.locked = True
        difficulties = {}
        for player in self.difficulty_votes:
            if self.difficulty_votes[player] not in difficulties:
                difficulties[self.difficulty_votes[player]] = 0
            difficulties[self.difficulty_votes[player]] += 1
        max_difficulty = 0
        max_votes = 0
        for difficulty in difficulties:
            if difficulties[difficulty] > max_votes:
                max_votes = difficulties[difficulty]
                max_difficulty = difficulty
        self.current_difficulty = max_difficulty
        self.locked = False

    def start_round(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.current_round += 1
        self.locked = False
        self.set_difficulty()
        self.locked = True
        self.roundStartTime = time.time()
        self.numToPass += 1
        self.numToPass %= len(self.players)
        if self.numToPass == 0:
            self.numToPass = 1
        self.numScored = 0
        self.locked = False

    def vote_to_start(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if player not in self.start_votes:
            self.start_votes.add(player)
        else:
            self.locked = False
            return # already voted
        self.startVotes += 1
        if self.startVotes > len(self.players) / 2:  # and len(self.players) > 3:
            self.startVotes = 0
            self.locked = False
            self.start_round()
            self.socket.emit("startRound", self.code)
        self.locked = False

    def getPlayers(self):
        return self.players

    def submit_card(self, player, score):
        while self.locked:
            time.sleep(1)
        self.locked = True
        otherPlayer = self.players.index(player) + self.numToPass
        otherPlayer %= len(self.players)
        self.locked = False
        self.add_score(player, self.players[otherPlayer], score)

    def get_other_player_name(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        otherPlayer = self.players.index(player) + self.numToPass
        otherPlayer %= len(self.players)
        self.locked = False
        return self.players[otherPlayer]

    @staticmethod
    def generateCode():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
