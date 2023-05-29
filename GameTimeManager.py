import time, random


class GameManager:

    def __init__(self, code, guess_time):
        self.cards = {}
        self.usedCards = []
        self.players = []
        self.code = code
        self.current_round = 0
        self.scores = {}
        self.locked = False
        self.current_difficulty = 0
        self.roundTimes = [0, 5, 60, guess_time, 20]
        self.roundState = 0
        self.votes = [[], [], [], [], []]

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
        self.votes[self.roundState] += (player1, score)
        self.locked = False

    def get_leaderboard(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        leaderboard = []
        for player in self.players:
            leaderboard.append((player, self.scores[player]))
        # sort leaderboard by score
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        self.locked = False
        return leaderboard

    def start_round(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.roundStartTime = time.time()
        self.roundState = 1
        self.locked = False

    def next_state(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.roundState += 1
        self.votes[self.roundState] = []
        self.locked = False

    def get_state(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        state = self.roundState
        self.locked = False
        return state

    def get_remaining_time(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        remaining_time = self.roundTimes[self.roundState] - (time.time() - self.roundStartTime)
        self.locked = False
        return remaining_time

    def get_round(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        round = self.current_round
        self.locked = False
        return round

    def vote_on_difficulty(self, player, difficulty):
        while self.locked:
            time.sleep(1)
        self.locked = True
        self.votes[-1].append((player, difficulty))
        self.locked = False

    def vote_to_start(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if self.roundState == 0:
            self.votes[0].append((player, 1))

        self.locked = False

    def unvote_to_start(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        if self.roundState == 0:
            self.votes[0].remove((player, 1))

        self.locked = False

    def get_votes_to_start(self):
        while self.locked:
            time.sleep(1)
        self.locked = True
        votes = self.votes[0]
        self.locked = False
        return votes, min(2, len(self.players) / 2)

    def game_manager(self):
        # tick every 1 second
        while True:
            time.sleep(1)
            if self.roundState == 0:
                #if enough players have voted to start, begin drawing
                if len(self.votes[0]) > min(2, len(self.players) / 2) and len(self.players) > 3:
                    self.start_round()
            elif self.roundState == 1:
                # if time is up, begin guessing
                if self.get_remaining_time() <= 0:
                    self.next_state()
            elif self.roundState == 2:
                if len(self.votes[2]) == len(self.players) or self.get_remaining_time() <= 0:
                    self.next_state()
            elif self.roundState == 3:
                if len(self.votes[3]) == len(self.players):
                    self.next_state()
            elif self.roundState == 4:
                if len(self.votes[4]) == len(self.players):
                    self.next_state()
            elif self.roundState == 5:
                if len(self.votes[5]) == len(self.players):
                    self.next_state()
                    self.current_round += 1
                    self.roundState = 0
                    self.current_difficulty = 0
                    self.votes = [[], [], [], [], []]
                    for player in self.players:
                        self.scores[player] = 0
                    self.roundStartTime = time.time()
