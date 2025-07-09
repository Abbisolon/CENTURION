# File: centurion/card.py
"""
Day 4 Task 1: Add suit-value mapping and computed property
"""

class Card:
    """
    Represents a playing card with a numeric face value and suit,
    and computes its counting value (face × suit multiplier).
    """
    # Map suit names to their multipliers
    SUIT_VALUES = {
        "Spades": 1,
        "Hearts": 2,
        "Clubs": 3,
        "Diamonds": 4,
    }

    def __init__(self, value: int, suit: str):
        """Store face value (1–13) and suit name."""
        self.value = value
        self.suit = suit

    @property
    def suit_value(self) -> int:
        """Return the numeric multiplier for this card's suit."""
        return Card.SUIT_VALUES.get(self.suit, 0)

    @property
    def count_value(self) -> int:
        """Counting value = face value × suit multiplier."""
        return self.value * self.suit_value

    def __repr__(self) -> str:
        """Show face, suit, and computed counting value."""
        return (f"Card(face={self.value}, suit='{self.suit}', "
                f"count_value={self.count_value})")
