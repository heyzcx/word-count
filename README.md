# word-count

Count lines, words and characters in text files — zero-dependency Python CLI.

## Install

Requires Python 3.8+. No dependencies. Just download `word_count.py`:

```bash
curl -O https://raw.githubusercontent.com/heyzcx/word-count/main/word_count.py
```

## Usage

```bash
# Count one or more files
python word_count.py notes.txt draft.md

# Show the 10 most common words
python word_count.py --top 10 notes.txt

# Machine-readable output
python word_count.py --json notes.txt
```

Example output:

```
file                             lines   words   chars
notes.txt                            3      27     124
TOTAL                                3      27     124

Top 3 words:
  the                  5
  fox                  4
  quick                2
```

Word matching is case-insensitive and keeps hyphenated words and
contractions together (`well-known`, `don't` each count as one word).

## License

MIT
