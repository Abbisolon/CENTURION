# File: centurion/gui.py
"""
Fully functional Tkinter GUI for Centurion, mirroring CLI gameplay exactly.
Supports rounds, exact-100 wins, overshoot scoring, draw handling (multiplier progression),
and game-over restart.
"""
import tkinter as tk
import tkinter.messagebox as mb
from centurion.game import Game

class CenturionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Centurion")

        # Start Game button
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        # Info frame (counters, total, turn, multiplier, deck) hidden until start
        self.info_frame = tk.Frame(root)
        self.counters_label = tk.Label(self.info_frame, text="Counters: 0", font=('Arial', 12))
        self.total_label    = tk.Label(self.info_frame, text="Total: 0",    font=('Arial', 12))
        self.turn_label     = tk.Label(self.info_frame, text="",           font=('Arial', 12, 'bold'))
        self.multiplier_label = tk.Label(self.info_frame, text="Multiplier: x1", font=('Arial', 12))
        self.deck_frame     = tk.LabelFrame(self.info_frame, text="Deck", font=('Arial', 10, 'bold'))
        self.deck_label     = tk.Label(self.deck_frame, text="🂠", font=('Arial', 14), width=4)
        self.deck_label.pack()

        # Score frame hidden until start
        self.score_frame = tk.Frame(root)
        self.score_labels = [tk.Label(self.score_frame, text="", font=('Arial', 12)) for _ in range(2)]

        # Hands frame hidden until start
        self.hands_frame = tk.Frame(root)

    def start_game(self):
        # Initialize game logic
        self.game = Game(["Player 1", "Player 2"])
        self.game.start_new_game()

        # Disable start button and show UI components
        self.start_button.config(state=tk.DISABLED)
        self.info_frame.pack(pady=5)
        for widget in (self.counters_label, self.total_label, self.turn_label, self.multiplier_label):
            widget.pack(side=tk.LEFT, padx=5)
        self.deck_frame.pack(side=tk.LEFT, padx=10)

        self.score_frame.pack(pady=5)
        for lbl in self.score_labels:
            lbl.pack(side=tk.LEFT, padx=10)

        self.hands_frame.pack(pady=10)
        self.update_info()
        self.render_hands()

    def update_info(self):
        # Update counters, total, turn, multiplier, and player scores
        self.counters_label.config(text=f"Counters: {self.game.counters}")
        self.total_label.config(text=f"Total: {self.game.current_total}")
        current = self.game.players[self.game.current_player_idx].name
        self.turn_label.config(text=f"Turn: {current}")
        self.multiplier_label.config(text=f"Multiplier: x{self.game.multiplier}")
        for idx, player in enumerate(self.game.players):
            self.score_labels[idx].config(text=f"{player.name} Score: {player.score}")

    def format_card(self, card):
        # Face mapping and suit symbols
        face_map = {1:'A', 11:'J', 12:'Q', 13:'K'}
        face = face_map.get(card.value, str(card.value))
        suit_symbols = {'Spades':'♠','Hearts':'♥','Clubs':'♣','Diamonds':'♦'}
        symbol = suit_symbols.get(card.suit, '')
        color = 'red' if card.suit in ['Hearts','Diamonds'] else 'black'
        return f"{face}{symbol}", color

    def render_hands(self):
        # Draw detection: if no cards left, increment multiplier and start next round
        if all(len(p.hand) == 0 for p in self.game.players):
            self.game.multiplier += 1
            mb.showinfo("Draw", f"Round draw. Multiplier now x{self.game.multiplier}.")
            self.game.start_round()
            self.update_info()

        # Clear existing hand buttons
        for w in self.hands_frame.winfo_children():
            w.destroy()

        # Render each player's hand with clickable cards
        current_idx = self.game.current_player_idx
        for p_idx, player in enumerate(self.game.players):
            frame = tk.LabelFrame(self.hands_frame, text=player.name, font=('Arial', 10, 'bold'))
            frame.pack(fill=tk.X, padx=5, pady=5)
            for c_idx, card in enumerate(player.hand):
                text, color = self.format_card(card)
                state = tk.NORMAL if p_idx == current_idx else tk.DISABLED
                btn = tk.Button(
                    frame, text=text, fg=color, font=('Arial', 12), width=4,
                    state=state, command=lambda ci=c_idx: self.handle_click(ci)
                )
                btn.pack(side=tk.LEFT, padx=2)

    def handle_click(self, card_idx):
        # Play a card and handle results
        winner = self.game.play_turn(card_idx)

        # If scoring occurs
        if winner is None:
            # Draw already handled in render_hands
            pass
        elif self.game.current_total >= 100 and self.game.current_total % 10 == 0:
            mb.showinfo("Round Over", f"{winner.name} wins this round!")
            if self.game.is_game_over():
                again = mb.askyesno("Game Over", "Game over! Play again?")
                if again:
                    self.game.start_new_game()
                else:
                    self.root.destroy()
                    return
            else:
                self.game.start_round()

        # Update UI
        self.update_info()
        self.render_hands()

if __name__ == "__main__":
    root = tk.Tk()
    CenturionGUI(root)
    root.mainloop()
