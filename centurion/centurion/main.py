# File: centurion/main.py
"""
Day 5 Task a: Add restart/exit prompt after game over
"""
from centurion.game import Game


def run_game():
    """
    Runs one full game (all rounds) and returns when game over.
    """
    game = Game(["Player 1", "Player 2"])
    game.start_new_game()

    # Round loop
    while True:
        # Draw detection at start of round
        if all(len(p.hand) == 0 for p in game.players):
            print(f"\nDraw — no scoring. Multiplier is now x{game.multiplier}.")
            input("Press [Enter] to start the next round...")
            game.start_round()
            continue

        print(f"\n🔁 Round {game.round_number}")
        print(f"Counters: {game.counters} | Total: {game.current_total}\n")

        # Show hands
        for player in game.players:
            print(f"{player.name}'s hand:")
            for idx, card in enumerate(player.hand):
                print(f"  [{idx}] {card}")
            print()

        current = game.players[game.current_player_idx]
        print(f"{current.name}, it's your turn.")
        while True:
            try:
                choice = int(input(f"Select card index (0-{len(current.hand)-1}): "))
                if 0 <= choice < len(current.hand):
                    break
                print("Invalid index, try again.")
            except ValueError:
                print("Enter a number.")

        # Show and record
        played_card = current.hand[choice]
        before_scores = [p.score for p in game.players]
        before_counters = game.counters

        result = game.play_turn(choice)
        print(f"\n{current.name} played {played_card}!")
        print(f"New total: {game.current_total}")

        # Scoring outcome
        if result is None:
            print(f"Draw — no scoring. Multiplier is now x{game.multiplier}.")
            input("Press [Enter] to start the next round...")
            continue

        if game.current_total >= 100 and game.current_total % 10 == 0:
            winner = result
            idx = game.players.index(winner)
            delta_score = winner.score - before_scores[idx]

            if delta_score > 0:
                print(f"{winner.name} scores {delta_score} point(s)!")
            else:
                print(f"{winner.name} loses {abs(delta_score)} point(s)!")

            print("\nScores:")
            for p in game.players:
                print(f"- {p.name}: {p.score}")
            print(f"\nCounters remaining: {game.counters}")

            if game.is_game_over():
                champion = game.declare_winner()
                print(f"\n🎉 Game over! {champion.name} wins the game! 🎉")
                return

            input("Press [Enter] to start the next round...")
            game.start_round()
            continue

        # Next turn
        next_player = game.players[game.current_player_idx]
        print(f"Next turn: {next_player.name}")


def main():
    print("🎉 Welcome to Centurion! 🎉")
    while True:
        input("Press [Enter] to start a new game...")
        run_game()
        # Prompt for restart
        choice = input("\nPlay again? (Y/N): ").strip().lower()
        if not choice.startswith('y'):
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
