import builtins
import pytest
import centurion.main as cm


def test_restart_exit_flow(monkeypatch, capsys):
    # Stub run_game to simulate a game that ends immediately
    calls = []
    def fake_run_game():
        calls.append(True)
        print("Game over stub")
        return
    monkeypatch.setattr(cm, 'run_game', fake_run_game)

    # Simulate user inputs: Enter to start, then 'n' to exit
    inputs = iter(['', 'n'])
    def fake_input(prompt=''):
        # print prompt so tests can capture it
        print(prompt, end='')
        return next(inputs)
    monkeypatch.setattr(builtins, 'input', fake_input)

    cm.main()

    out = capsys.readouterr().out
    assert "Play again? (Y/N):" in out
    assert "Thanks for playing!" in out
    assert calls == [True]


def test_restart_keep_playing_flow(monkeypatch, capsys):
    # Stub run_game to simulate a game that ends immediately
    calls = []
    def fake_run_game():
        calls.append(True)
        print("Game over stub")
        return
    monkeypatch.setattr(cm, 'run_game', fake_run_game)

    # Inputs: Enter to start, 'y' to restart, Enter to start again, 'n' to exit
    inputs = iter(['', 'y', '', 'n'])
    def fake_input(prompt=''):
        print(prompt, end='')
        return next(inputs)
    monkeypatch.setattr(builtins, 'input', fake_input)

    cm.main()

    out = capsys.readouterr().out
    # run_game called twice
    assert calls == [True, True]
    # Prompt appeared twice
    assert out.count("Play again? (Y/N):") == 2
    assert "Thanks for playing!" in out
