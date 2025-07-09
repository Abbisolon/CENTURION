# File: tests/test_game_flow.py
import pytest
from centurion.game import Game
from centurion.card import Card


def test_exact_100_scoring():
    g = Game(["A","B"])
    g.start_new_game()
    g.cards_played_count = [3,2]
    g.current_total = 80
    g.players[0].hand = [Card(10,"Hearts")]  # 10×2=20 -> 100
    winner = g.play_turn(0)
    assert winner == g.players[0]
    assert g.players[0].score == 6  # total cards=5? Actually cards_played_count increment -> [4,2]=6
    assert g.counters == 21-6


def test_overshoot_scoring_net_cards():
    g = Game(["A","B"])
    g.start_new_game()
    g.cards_played_count = [4,3]
    g.current_total = 90
    g.players[0].hand = [Card(10,"Hearts")]  # 10×2=20 -> 110
    winner = g.play_turn(0)
    assert winner == g.players[0]
    # raw cards_played_count after increment [5,3]=8; excess=(110-100)//10=1; net=7
    assert g.players[0].score == 7
    assert g.counters == 21-7


def test_consecutive_draws_multiplier_progression():
    g = Game(["A","B"])
    g.start_new_game()
    # simulate first draw
    g.players[0].hand.clear(); g.players[1].hand.clear()
    result = g.play_turn(0)
    assert result is None
    assert g.multiplier == 2
    # simulate second draw
    g.players[0].hand.clear(); g.players[1].hand.clear()
    result = g.play_turn(0)
    assert result is None
    assert g.multiplier == 3


def test_multiplier_resets_after_score():
    g = Game(["A","B"])
    g.start_new_game()
    # cause a draw then score
    g.players[0].hand.clear(); g.players[1].hand.clear()
    g.play_turn(0)
    assert g.multiplier == 2
    # now exact 100 next round
    g.players[0].hand = [Card(50,"Hearts")]  # 100
    winner = g.play_turn(0)
    assert winner == g.players[0]
    assert g.multiplier == 1


def test_full_game_runs_without_error():
    g = Game(["A","B"])
    g.start_new_game()
    # simulate playing first available card each turn until game over
    while not g.is_game_over():
        # if draw, next round started internally
        if all(len(p.hand)==0 for p in g.players):
            g.play_turn(0)
        else:
            # always play first card
            active_idx = g.current_player_idx
            g.play_turn(0)
    # after game over, declare_winner should not error
    champ = g.declare_winner()
    assert champ in g.players

if __name__ == "__main__":
    pytest.main()
