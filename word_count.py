#!/usr/bin/env python3
"""Count lines, words and characters in text files.

Usage:
    python word_count.py file1.txt file2.txt
    python word_count.py --top 10 notes.txt
    python word_count.py --json report.md
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9_]+(?:['-][A-Za-z0-9_]+)*")


def count_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    words = WORD_RE.findall(text)
    return {
        "file": str(path),
        "lines": len(lines),
        "words": len(words),
        "characters": len(text),
        "top_words": Counter(w.lower() for w in words),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Count lines, words and characters in text files."
    )
    parser.add_argument("files", nargs="+", type=Path, help="text files to count")
    parser.add_argument("--top", type=int, default=0,
                        help="show the N most common words")
    parser.add_argument("--json", action="store_true",
                        help="print results as JSON instead of a table")
    args = parser.parse_args(argv)

    results = []
    for path in args.files:
        if not path.is_file():
            print(f"word_count: {path}: no such file", file=sys.stderr)
            return 1
        results.append(count_file(path))

    total = {"lines": 0, "words": 0, "characters": 0}
    for r in results:
        for key in total:
            total[key] += r[key]

    if args.json:
        out = [{k: r[k] for k in ("file", "lines", "words", "characters")}
               for r in results]
        out.append({"file": "TOTAL", **total})
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    print(f"{'file':<30} {'lines':>7} {'words':>7} {'chars':>7}")
    for r in results:
        print(f"{r['file']:<30} {r['lines']:>7} {r['words']:>7} "
              f"{r['characters']:>7}")
    print(f"{'TOTAL':<30} {total['lines']:>7} {total['words']:>7} "
          f"{total['characters']:>7}")

    if args.top > 0:
        merged = Counter()
        for r in results:
            merged.update(r["top_words"])
        print(f"\nTop {args.top} words:")
        for word, n in merged.most_common(args.top):
            print(f"  {word:<20} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
