import random
import string
import time


class Game:
    def __init__(self, code, socket):
        self.lastTimeNewRound = time.time()
        self.socket = socket
        self.cards = self.get_all_cards()
        self.usedCards = set()
        self.players = []
        self.code = code
        self.scores = {}
        self.locked = False
        self.current_difficulty = 0
        self.difficulty_votes = {}
        self.startVotes = 0
        self.numToPass = 0
        self.numScored = 0
        self.players_cards = {}
        self.startVotesPlayers = set()

    def get_time_since_last_round(self):
        return time.time() - self.lastTimeNewRound

    def get_all_cards(self):
        cards = {}
        with (open("cards.txt", "r") as cards_file):
            for card in cards_file.readlines():
                #strip the newline character
                card = card.strip()
                #get the card difficulty
                card_difficulty = card.split(',')[1]
                #map the card difficulty to an index
                if card_difficulty == 'normal':
                    card_difficulty = 0
                elif card_difficulty == 'difficult':
                    card_difficulty = 1
                else:
                    card_difficulty = 2
                #add the card to the dictionary, without the difficulty
                if card_difficulty in cards:
                    cards[card_difficulty].append(tuple(card.split(',')[0:1] + card.split(',')[2:]))
                else:
                    cards[card_difficulty] = list()
                    cards[card_difficulty].append(tuple(card.split(',')[0:1] + card.split(',')[2:]))
        print(cards)
        print(".")
        return cards


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
        #check if the player already has a card
        if player in self.players_cards:
            self.locked = False
            return self.players_cards[player]
        if len(self.usedCards) == len(self.cards):
            self.usedCards = set()
        card = random.choice(self.cards[self.current_difficulty])
        while card in self.usedCards:
            card = random.choice(self.cards[self.current_difficulty])
        self.usedCards.add(card)
        self.players_cards[player] = card
        self.locked = False
        return card

    def get_players_card(self, player):
        while self.locked:
            time.sleep(1)
        self.locked = True
        playerNum = self.players.index(player) + self.numToPass
        if playerNum >= len(self.players):
            playerNum -= len(self.players)
        card = self.players_cards[self.players[playerNum]][0]
        self.locked = False
        return self.players[playerNum] + ";" + card # return card and player name

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
        self.lastTimeNewRound = time.time()
        #clean up the card titles
        self.players_cards = {}
        self.locked = False
        self.set_difficulty()
        self.locked = True
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
        if player not in self.startVotesPlayers:
            self.startVotesPlayers.add(player)
        else:
            self.locked = False
            return # already voted
        self.startVotes += 1
        if self.startVotes > len(self.players) / 2 and len(self.players) >= 1:
            self.startVotesPlayers = set()
            self.startVotes = 0
            self.locked = False
            self.start_round()
            print("hi")
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
        return ''.join(random.choice(string.ascii_uppercase + "123456789") for _ in range(4))
