import random
from collections import defaultdict

# Define a Tile class to represent each Mahjong tile
class Tile:
    def __init__(self, suit, value):
        self.suit = suit  # "Man", "Pin", "Sou", "Honor"
        self.value = value  # 1-9 for suits, or "East", "South", etc. for Honors

    def __repr__(self):
        return f"{self.value}{self.suit}"

# Generate a large set of Mahjong tiles (2+ sets)
def generate_tiles(num_sets=2):
    suits = ["Man", "Pin", "Sou"]
    honors = ["East", "South", "West", "North", "White", "Green", "Red"]
    tiles = []

    for _ in range(num_sets):
        for suit in suits:
            tiles.extend([Tile(suit, i) for i in range(1, 10)])  # 1-9 for suits
        tiles.extend([Tile("Honor", h) for h in honors])  # Honor tiles

    return tiles

# Define a Player class to manage each player's hand
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.discards = []

    def draw_tile(self, tile):
        self.hand.append(tile)

    def discard_tile(self, tile):
        self.hand.remove(tile)
        self.discards.append(tile)
        return tile

    def show_hand(self):
        return self.hand

    def check_win(self):
        """Check if the hand is a winning hand (simplified for this version)."""
        counts = defaultdict(int)
        for tile in self.hand:
            counts[(tile.suit, tile.value)] += 1
        
        pairs = 0
        triples = 0

        for _, count in counts.items():
            if count >= 3:
                triples += 1
                count -= 3
            if count >= 2:
                pairs += 1

        # Simple win condition: at least 1 pair and enough triples for a full hand
        return pairs >= 1 and triples >= 4

# Define the game class
class SuperLargeMahjong:
    def __init__(self, num_players=4, num_sets=2):
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.tiles = generate_tiles(num_sets)
        self.discard_pile = []
        self.special_rules = []  # Placeholder for custom rules
        self.current_player_index = 0

    def shuffle_tiles(self):
        random.shuffle(self.tiles)

    def deal_tiles(self):
        # Deal 13 tiles per player (standard starting hand)
        hand_size = 13
        for _ in range(hand_size):
            for player in self.players:
                if self.tiles:
                    player.draw_tile(self.tiles.pop())

    def add_special_rule(self, rule_name, rule_func):
        """Add a custom rule to the game. Rule must be a callable."""
        self.special_rules.append((rule_name, rule_func))

    def apply_special_rules(self, player):
        """Apply all custom rules to a player's hand."""
        for rule_name, rule_func in self.special_rules:
            rule_func(player)

    def play_turn(self, player):
        """Player's turn: Draw a tile, discard a tile, and check for win."""
        print(f"\n{player.name}'s turn")
        if self.tiles:
            drawn_tile = self.tiles.pop()
            player.draw_tile(drawn_tile)
            print(f"{player.name} drew {drawn_tile}")
        else:
            print("No more tiles to draw!")
            return False

        print(f"{player.name}'s hand: {player.show_hand()}")

        # Player discards a tile (simplified: discard the last tile)
        discarded_tile = player.discard_tile(player.hand[-1])
        self.discard_pile.append(discarded_tile)
        print(f"{player.name} discarded {discarded_tile}")

        # Check for win condition
        if player.check_win():
            print(f"{player.name} wins with hand: {player.show_hand()}!")
            return True
        return False

    def start_game(self):
        self.shuffle_tiles()
        self.deal_tiles()

        print("Starting Super Large Mahjong!\n")
        
        # Game loop
        while self.tiles:
            player = self.players[self.current_player_index]
            if self.play_turn(player):
                print("Game Over!")
                return

            # Move to next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

        print("Game over! No more tiles left.")

# Example of a custom rule
def example_special_rule(player):
    """Example: Print the player's hand size if over 16."""
    if len(player.hand) > 16:
        print(f"{player.name} has an oversized hand with {len(player.hand)} tiles!")

# Run the game
game = SuperLargeMahjong(num_players=4, num_sets=3)
game.add_special_rule("Example Rule", example_special_rule)
game.start_game()
