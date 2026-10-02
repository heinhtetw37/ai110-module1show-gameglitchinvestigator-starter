from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_hard_is_harder_than_normal():
    assert get_range_for_difficulty("Hard")[1] > get_range_for_difficulty("Normal")[1]


def test_parse_guess():
    assert parse_guess("42") == (True, 42, None)
    assert parse_guess("3.7") == (True, 3, None)
    assert parse_guess("")[0] is False
    assert parse_guess("abc")[0] is False


def test_first_attempt_win_score():
    assert update_score(0, "Win", 1) == 90
    assert update_score(10, "Too High", 2) == 5


# --- Regression: invalid input must not consume an attempt (app.py) ---
import os

from streamlit.testing.v1 import AppTest

APP_PATH = os.path.join(os.path.dirname(__file__), "..", "app.py")


def _submit(at, text):
    at.text_input[0].set_value(text)
    at.button[0].click()  # "Submit Guess"
    at.run()


def test_invalid_guess_does_not_use_attempt():
    at = AppTest.from_file(APP_PATH).run()
    assert at.session_state.attempts == 0

    _submit(at, "")      # blank
    _submit(at, "abc")   # not a number
    assert at.session_state.attempts == 0

    _submit(at, "5")     # valid guess counts
    assert at.session_state.attempts == 1
