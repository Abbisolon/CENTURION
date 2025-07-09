# File: centurion/deck.py
"""
Day 1 Task 3: Implement the Deck class
"""

from .card import Card
import random

class Deck:
    """
    Represents a standard 52-card deck.
    """
    def __init__(self):
        """Create all 52 cards (values 1–13 × 4 suits)."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        # List comprehension builds Card instances for each suit and value
        self.cards = [Card(value, suit) for suit in suits for value in range(1, 14)]

    def shuffle(self):
        """Randomize the order of cards in the deck."""
        random.shuffle(self.cards)

    def deal(self, count: int):
        """Remove `count` cards from the top and return them."""
        # Split the list: first `count` cards as dealt, remainder stays in deck
        dealt_cards = self.cards[:count]
        self.cards = self.cards[count:]
        return dealt_cards
