#!/usr/bin/env python3
"""Write one debugging haiku (5-7-5, 17 syllables) to /output/entry.txt.

The haiku is fixed text: a git-blame joke with a turn in the last line.
The program validates its own shape before writing anything, so a bad
edit fails loudly here instead of shipping an invalid entry.
"""

import os
import sys

HAIKU = (
    "git blame points at me\n"
    "the bug I swore was not mine\n"
    "my name, six months back"
)

# Hand-counted syllables per line: git(1) blame(1) points(1) at(1) me(1) = 5;
# the(1) bug(1) I(1) swore(1) was(1) not(1) mine(1) = 7;
# my(1) name(1) six(1) months(1) back(1) = 5.
EXPECTED_SYLLABLES = (5, 7, 5)

SYLLABLES = {
    "git": 1, "blame": 1, "points": 1, "at": 1, "me": 1,
    "the": 1, "bug": 1, "i": 1, "swore": 1, "was": 1, "not": 1, "mine": 1,
    "my": 1, "name": 1, "six": 1, "months": 1, "back": 1,
}


def count_syllables(line):
    words = line.replace(",", "").split()
    return sum(SYLLABLES[w.lower()] for w in words)


def main():
    lines = HAIKU.split("\n")
    assert len(lines) == 3, "haiku must have exactly 3 lines"
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        got = count_syllables(line)
        assert got == expected, f"{line!r}: {got} syllables, expected {expected}"
    assert 1 <= len(HAIKU) <= 200, f"haiku is {len(HAIKU)} chars, must be 1-200"
    assert HAIKU.strip(), "haiku must not be only whitespace"

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    os.chmod(out_path, 0o644)
    # Read back and prove the file on disk is exactly what we validated.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == HAIKU, "output on disk differs from validated haiku"
    print(HAIKU)
    return 0


if __name__ == "__main__":
    sys.exit(main())
