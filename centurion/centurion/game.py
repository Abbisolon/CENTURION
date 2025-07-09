# File: centurion/game.py
"""
Centurion game logic: face × suit counting, exact-100 wins by cards played,
overshoot scoring by net cards, draw increments multiplier.
"""
from .player import Player
from .deck import Deck
from typing import List, Optional

class Game:
    """
    Core game logic for Centurion.
    """
    def __init__(self, player_names: List[str]):
        self.players = [Player(name) for name in player_names]
        self.counters = 21
        self.multiplier = 1
        self.current_total = 0
        self.current_player_idx = 0
        self.round_number = 0
        self.cards_played_count: List[int] = []
        self.deck: Optional[Deck] = None

    def start_new_game(self):
        """
        Reset counters, scores, and start first round.
        """
        self.counters = 21
        self.multiplier = 1
        for p in self.players:
            p.score = 0
        self.start_round()

    def start_round(self):
        """
        Shuffle deck, deal 7 cards each, and reset round state.
        """
        self.round_number += 1
        self.deck = Deck()
        self.deck.shuffle()
        for p in self.players:
            p.hand.clear()
            p.receive_cards(self.deck.deal(7))
        self.current_total = 0
        self.current_player_idx = 0
        self.cards_played_count = [0] * len(self.players)

    def play_turn(self, card_idx: int) -> Optional[Player]:
        """
        Execute a player's turn or handle draw:
        - On draw (all hands empty), increment multiplier, start next round, return None
        - On scoring stop (multiple of 10 >=100), apply scoring or penalties, return scoring player
        - Otherwise switch turn and continue, return the player who just played
        """
        # Draw check before playing
        if all(len(p.hand) == 0 for p in self.players):
            # Increment multiplier on consecutive draws: 1→2, 2→3, etc.
            self.multiplier += 1
            self.start_round()
            return None

        player = self.players[self.current_player_idx]
        # Track cards played this round
        self.cards_played_count[self.current_player_idx] += 1
        card = player.play_card(card_idx)
        self.current_total += card.count_value

        # Stop on first multiple of ten >= 100
        if self.current_total >= 100 and self.current_total % 10 == 0:
            # Exact 100: award cards played
            if self.current_total == 100:
                total_cards = sum(self.cards_played_count)
                points = total_cards * self.multiplier
                player.score += points
                self.counters -= points
                winner = player
            else:
                # Overshoot: award net cards (cards played minus excess tens)
                excess_tens = (self.current_total - 100) // 10
                total_cards = sum(self.cards_played_count)
                net_cards = total_cards - excess_tens
                points = net_cards * self.multiplier
                player.score += points
                self.counters -= points
                winner = player
            # Reset multiplier after scoring
            self.multiplier = 1
            return winner

        # Continue round: switch to next player
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return player

    def is_game_over(self) -> bool:
        """Return True if shared counters are exhausted."""
        return self.counters <= 0

    def declare_winner(self) -> Player:
        """Return the player with the highest personal score."""
        return max(self.players, key=lambda p: p.score)
