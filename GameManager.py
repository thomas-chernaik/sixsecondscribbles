import random
import string
import time


class Game:
    def __init__(self, code, guess_time, socket):
        self.socket = socket
        self.cards = {}
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
        self.guessTime = guess_time
        self.displayLeaderboardTime = 20
        self.startVotes = 0

    def add_player(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.players.append(player)
        self.scores[player] = 0
        self.locked = False

    def get_card(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if len(self.usedCards) == len(self.cards):
            self.usedCards = []
        card = random.choice(self.cards[self.current_difficulty])
        while card in self.usedCards:
            card = random.choice(self.cards[self.current_difficulty])
        self.usedCards.append(card)
        self.locked = False
        return card

    def add_score(self, player1, player2, score):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.scores[player1] += score
        self.scores[player2] += score
        self.locked = False

    def get_leaderboard(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        leaderboard = []
        for player in self.players:
            leaderboard.append((player, self.scores[player]))
        leaderboard.sort(key=lambda x: x[1], reverse=True)
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
        self.locked = False

    def getCurrentSection(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if time.time() - self.roundStartTime < self.drawLeadTime:
            self.locked = False
            return "drawLead"
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime:
            self.locked = False
            return "draw"
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime + self.guessTime:
            self.locked = False
            return "guess"
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime + self.guessTime + self.displayLeaderboardTime:
            self.locked = False
            return "displayLeaderboard"
        else:
            self.start_round()
            self.locked = False
            return "drawLead"

    def getTimeLeftInSection(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if time.time() - self.roundStartTime < self.drawLeadTime:
            self.locked = False
            return self.drawLeadTime - (time.time() - self.roundStartTime)
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime:
            self.locked = False
            return self.drawLeadTime + self.drawTime - (time.time() - self.roundStartTime)
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime + self.guessTime:
            self.locked = False
            return self.drawLeadTime + self.drawTime + self.guessTime - (time.time() - self.roundStartTime)
        elif time.time() - self.roundStartTime < self.drawLeadTime + self.drawTime + self.guessTime + self.displayLeaderboardTime:
            self.locked = False
            return self.drawLeadTime + self.drawTime + self.guessTime + self.displayLeaderboardTime - (
                        time.time() - self.roundStartTime)
        else:
            self.start_round()
            self.locked = False
            return self.drawLeadTime - (time.time() - self.roundStartTime)

    def vote_to_start(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.startVotes += 1
        if self.startVotes > len(self.players) / 2:# and len(self.players) > 3:
            self.locked = False
            self.start_round()
            self.socket.emit("startRound", room=self.code)
        self.locked = False

    def getPlayers(self):
        return self.players

    @staticmethod
    def generateCode():
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
