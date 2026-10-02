def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # Wider range than Normal so Hard is actually harder
        return 1, 200
    # Unknown difficulty: fall back to the Normal range
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # Treat missing, empty and whitespace-only input the same way
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()
    try:
        if "." in raw:
            # Decimals are truncated toward zero, e.g. "3.7" -> 3
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Hint tells the player which direction to move
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # Earlier wins earn more: 90 on attempt 1, dropping 10 per attempt
        points = 100 - 10 * attempt_number
        # Always award at least 10 points for a win
        if points < 10:
            points = 10
        return current_score + points

    # Wrong guesses cost 5 points, whether too high or too low
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    # Any other outcome leaves the score unchanged
    return current_score
