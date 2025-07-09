# File: centurion/player.py
"""
Day 1 Task 4: Implement the Player class
"""
from typing import List
from .card import Card

class Player:
    """
    Represents a game player with a hand of cards and a score.
    """
    def __init__(self, name: str):
        """Initialize with player name, empty hand, and zero score."""
        self.name = name
        self.hand: List[Card] = []
        self.score: int = 0

    def receive_cards(self, cards: List[Card]):
        """Add a list of Card objects to this player's hand."""
        self.hand.extend(cards)

    def play_card(self, index: int) -> Card:
        """Remove and return the Card at the given hand index."""
        return self.hand.pop(index)
