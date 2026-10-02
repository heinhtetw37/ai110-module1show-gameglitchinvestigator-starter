# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game looked fine at first: a number guessing game with a difficulty picker, a hint checkbox, an attempts counter and a score. It stopped making sense once I played it. The hints sent me the wrong way, Hard mode was easier than Normal, and typing junk into the box used up my attempts. I found these by playing and by reading the debug panel, which shows the secret number.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess higher than the secret (e.g. 60 when the secret is 50) | Hint says "Go LOWER!" | Hint said to go higher, so the hints were backwards | None, it was a logic bug |
| Select "Hard" difficulty | Largest range and fewest attempts | Range was narrower than Normal, so Hard was easier | None |
| Blank input or "abc", then Submit | Show an error and keep the attempt count unchanged | The invalid guess cost an attempt and was added to the history | None. The "Attempts left" counter dropped |
| Guess "3.7" or whitespace-only input | Handled predictably | Inconsistent handling, so I made decimals truncate and blank input return "Enter a guess." | None |

---

## 2. How did you use AI as a teammate?

I used Claude Code in VS Code as my main AI tool. I used it to read the code, find bugs and write fixes and tests.

**Correct suggestion:** Claude pointed out that the hint messages in `check_guess` were swapped. A guess above the secret said "Go HIGHER!", and it should say "Go LOWER!". I checked this by reading the code and by running `test_guess_too_high` and `test_guess_too_low`. Both pass now. I also played a round with the debug panel open and confirmed the hints pointed the right way.

**Suggestion I changed:** For the invalid-input bug, the AI's first idea was a larger rewrite of how submissions are handled. That was more than the bug needed. I kept the change small. Bad input now shows an error and returns before `attempts` goes up. I moved the parsing and scoring into `logic_utils.py`, where I could test them. I checked the result with a regression test that submits "", "abc" and then "5", and asserts that attempts only reaches 1 on the valid guess.

---

## 3. Debugging and testing your fixes

I called a bug fixed only when I could reproduce it before the fix and see it gone afterward. That meant both a manual replay in the app and an automated test. The test I found most useful was `test_invalid_guess_does_not_use_attempt`. It uses Streamlit's `AppTest` to run the real app, submit a blank guess, then "abc", then "5", and check the attempts counter. It showed me the bug was in the app's flow and not in the helper functions, because the unit tests on `parse_guess` alone had passed while the app still wasted attempts. The AI helped me write the `AppTest` regression test, which I hadn't used before, and it explained how `session_state` can be read from inside the test.

---

## 4. What did you learn about Streamlit and state?

Every time you click a button or type in a box, Streamlit re-runs the whole Python script from top to bottom. Ordinary variables are reset on each run, so a plain `secret = random.randint(...)` would pick a new number on every click. `st.session_state` is a dictionary that survives reruns, so it's where the secret, attempts, score and history are kept. In this app I only create the secret when the difficulty changes or on "New Game". That's why the game stays consistent between guesses.

---

## 5. Looking ahead: your developer habits

**Habit to reuse:** I'll write a failing regression test before I fix a bug, then fix it and watch the test go green. It gave me proof that each fix worked, and it will catch the bug if it returns.

**What I'd do differently:** I'd give the AI a narrower task. Something like "fix only the invalid-input attempt bug" gets a smaller and easier-to-review change than "fix the game". I'd also read every diff before accepting it.

**How my thinking changed:** AI-generated code can look polished and still be wrong. The app's footer even says it was "production-ready", and it had backwards hints. I now treat AI output as a draft from a teammate, and I want tests before I trust it.
