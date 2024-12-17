import random
from collections import defaultdict, Counter

# Define a Tile class to represent each Mahjong tile
class Tile:
    def __init__(self, suit, value):
        self.suit = suit  # "Man", "Pin", "Sou", "Honor"
        self.value = value  # 1-9 for suits, or "East", "South", etc. for Honors

    def __repr__(self):
        return f"{self.value}{self.suit}"

# Generate a standard set of Mahjong tiles
def generate_tiles():
    suits = ["Man", "Pin", "Sou"]
    honors = ["East", "South", "West", "North", "White", "Green", "Red"]
    tiles = []

    for suit in suits:
        tiles.extend([Tile(suit, i) for i in range(1, 10)] * 4)  # 4 copies of 1-9 for suits
    for honor in honors:
        tiles.extend([Tile("Honor", honor)] * 4)  # 4 copies of each honor tile

    return tiles

# Define a Player class to manage each player's hand
class Player:
    def __init__(self, name, is_bot=True):
        self.name = name
        self.hand = []
        self.discards = []
        self.is_bot = is_bot  # Determines if player is a bot or human
        self.riichi = False  # Track if player declared Riichi
        self.wind = None  # Player's wind
        self.points = 25000  # Standard starting points

    def draw_tile(self, tile):
        self.hand.append(tile)

    def discard_tile(self):
        if self.is_bot:
            tile = BotStrategy.analyze_hand(self.hand)  # Choose smarter discard
        else:
            self.show_hand()
            tile_index = int(input(f"{self.name}, choose a tile to discard (0-{len(self.hand)-1}): "))
            tile = self.hand[tile_index]
        self.hand.remove(tile)
        self.discards.append(tile)
        return tile


    def show_hand(self):
        print(f"{self.name}'s hand: {[f'{i}: {tile}' for i, tile in enumerate(self.hand)]}")

    def declare_riichi(self):
        if not self.riichi:
            print(f"{self.name} declares Riichi!")
            self.riichi = True
            return True
        return False

    def check_win(self):
        """Check if the hand is a winning hand (simplified Riichi Mahjong)."""
        counts = defaultdict(int)
        for tile in self.hand:
            counts[(tile.suit, tile.value)] += 1
        
        pairs = 0
        triples = 0
        sequences = 0

        # Count triples and pairs
        for _, count in counts.items():
            while count >= 3:
                triples += 1
                count -= 3
            while count >= 2:
                pairs += 1
                count -= 2

        # Winning hand: Must have 4 melds (triples/sequences) and 1 pair
        return triples + sequences >= 4 and pairs >= 1

    def has_yaku(self):
        """Check for simplified Yaku. This includes hands like Tanyao, Yakuhai, etc."""
        all_simples = all(tile.value not in [1, 9] and tile.suit != "Honor" for tile in self.hand)
        all_honors = all(tile.suit == "Honor" for tile in self.hand)
        yakuhai = any(tile.suit == "Honor" and tile.value in ["East", "South", "West", "North"] for tile in self.hand)
        
        yaku_list = []
        if all_simples:
            yaku_list.append("Tanyao (All Simples)")
        if all_honors:
            yaku_list.append("Honors Only")
        if yakuhai:
            yaku_list.append("Yakuhai (Value Honor)")

        return yaku_list

# Define the Bot Strategy
class BotStrategy:
    @staticmethod
    def analyze_hand(hand):
        """
        Analyze hand and rank tiles based on their usefulness.
        Tiles that are isolated or cannot form sets are prioritized for discard.
        """
        tile_counts = Counter((tile.suit, tile.value) for tile in hand)
        tile_ranks = {}

        for tile in hand:
            key = (tile.suit, tile.value)
            count = tile_counts[key]
            
            # Rank: Higher rank = less useful
            if tile.suit == "Honor":
                tile_ranks[tile] = 10 - count  # Isolated honors are bad
            else:
                neighbors = [
                    (tile.suit, tile.value - 1),
                    (tile.suit, tile.value + 1)
                ]
                useful_neighbors = sum(1 for n in neighbors if tile_counts.get(n, 0) > 0)
                tile_ranks[tile] = 5 - (count + useful_neighbors)  # Prefer tiles with fewer neighbors

        # Return the least useful tile
        return sorted(tile_ranks.items(), key=lambda x: x[1], reverse=True)[0][0]


# Define the game class
class RiichiMahjong:
    def __init__(self, num_players=4, num_bots=3):
        self.players = []
        self.setup_players(num_players, num_bots)
        self.tiles = generate_tiles()
        self.discard_pile = []
        self.current_player_index = 0
        self.round_wind = "East"  # Starting round wind
        self.dealer_index = 0  # Tracks the current dealer

    def setup_players(self, num_players, num_bots):
        winds = ["East", "South", "West", "North"]
        for i in range(num_players):
            if i < num_bots:
                player = Player(f"Bot {i+1}", is_bot=True)
            else:
                name = input(f"Enter name for Player {i+1}: ")
                player = Player(name, is_bot=False)
            player.wind = winds[i % 4]  # Assign player winds
            self.players.append(player)

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def deal_tiles(self):
        hand_size = 13
        for _ in range(hand_size):
            for player in self.players:
                if self.tiles:
                    player.draw_tile(self.tiles.pop())

    def play_turn(self, player):
        print(f"\n{player.name}'s turn ({player.wind} wind)")
        if self.tiles:
            drawn_tile = self.tiles.pop()
            player.draw_tile(drawn_tile)
            print(f"{player.name} drew {drawn_tile}")
        else:
            print("No more tiles to draw!")
            return False

        if not player.is_bot:
            player.show_hand()
        
        # Riichi Declaration
        if not player.is_bot and not player.riichi:
            if input(f"{player.name}, do you want to declare Riichi? (y/n): ").lower() == "y":
                player.declare_riichi()

        discarded_tile = player.discard_tile()
        self.discard_pile.append(discarded_tile)
        print(f"{player.name} discarded {discarded_tile}")

        # Check for win condition
        if player.check_win():
            yaku = player.has_yaku()
            if yaku:
                print(f"{player.name} wins with Yaku: {', '.join(yaku)}")
            else:
                print(f"{player.name} wins with no Yaku!")
            print(f"Winning hand: {player.hand}")
            return True
        return False

    def start_game(self):
        self.shuffle_tiles()
        self.deal_tiles()
        print(f"Starting Riichi Mahjong - Round Wind: {self.round_wind}\n")

        while self.tiles:
            player = self.players[self.current_player_index]
            if self.play_turn(player):
                print("Game Over!")
                return
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

        print("Game over! No more tiles left.")

# Run the game
num_players = int(input("Enter total number of players (including bots, max 4): "))
num_bots = int(input(f"Enter number of bots (0-{num_players}): "))
game = RiichiMahjong(num_players=num_players, num_bots=num_bots)
game.start_game()
