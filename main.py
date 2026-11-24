#!/usr/bin/env python3
"""One Word From Grandma - make.fun entry.

Writes exactly one word to /output/entry.txt: the word a grandma
would type about AI. Deterministic, Python 3.13 standard library only.
"""

import os
import sys
import tempfile

WORD = "Dearbot"


def is_single_word(word: str) -> bool:
    """True when the entry is exactly one token: no internal whitespace."""
    return len(word.split()) == 1


def validate(word: str) -> None:
    """Gate: UTF-8, 1-30 characters, not only whitespace."""
    if not word or len(word) > 30 or not word.strip():
        print("error: word must be 1-30 non-whitespace characters",
              file=sys.stderr)
        sys.exit(1)
    if not is_single_word(word):
        print("error: entry must be exactly one word", file=sys.stderr)
        sys.exit(1)
    word.encode("utf-8")


def resolve_output_dir() -> str:
    """Fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> repo output/ -> tmp."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    candidates = ["/output",
                  os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "output")]
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write_probe")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return tempfile.mkdtemp(prefix="grandma-entry-")


def main() -> int:
    validate(WORD)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: exactly one word, nothing else.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(WORD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
