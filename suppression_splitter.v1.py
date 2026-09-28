#!/usr/bin/env python3
"""
Sentence splitter implementing suppression-spec.md v1.0 (SANIUL-blackdragon/sentence-splitting-research).

Every function cites the spec ID it implements. Where the spec contradicts itself,
the choice made is listed in SPEC_DEVIATIONS and printed by `--deviations`.

Usage:
    python suppression_splitter.py input.txt            # one sentence per line
    python suppression_splitter.py input.txt --trace    # show every candidate + deciding rule
    python suppression_splitter.py input.txt --json
    python suppression_splitter.py --html page.html
    cat text | python suppression_splitter.py -
    python suppression_splitter.py --test               # run the 24 worked rulings (§7)
    python suppression_splitter.py --deviations
"""
import argparse
import html as htmllib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, asdict
from typing import List, Optional

# --------------------------------------------------------------------------- #
# D3 / D8 / D9 / D16 constants
# --------------------------------------------------------------------------- #
PUNCT_SINGLE = set('.!?,;:()[]{}"“”„»«–…')      # D3 (single-char members)
PUNCT_MULTI = ["--"]                            # D3 (two-char member, matched first)
TERMINATORS = set(".!?…")                       # D8
DECORATION = set("\"”')]}»")                    # D9 (note: ' is unreachable, see deviations)
QUOTE_CHARS = set('"“”„«»')                     # D16

LAMBDA = 3                                      # D15

# --------------------------------------------------------------------------- #
# Lexicons (§5). Static, lowercase, no periods (L1).
# --------------------------------------------------------------------------- #
# Set P as printed in R2.1, minus entries that can never match a period-free
# single token (e.g, ie, nb, "et al", the literal "…" placeholder) -- see deviations.
# `etc` and `inc` carry an asterisk in the spec pointing at a nonexistent R2.2;
# ruling 7.12 and the closing note of §4 say `etc.` splits by DL1, so they are
# excluded from P. Toggle with --strict-asterisks to put them back in.
SET_P_BASE = {
    "dr", "mr", "mrs", "ms", "prof", "gen", "sen", "capt", "sgt", "lt", "col",
    "rev", "hon", "st", "mt", "ft", "vs", "ca", "cf", "pp", "fig", "eq", "ch",
    "sec", "no", "approx", "dept", "univ", "assn", "bros",
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "sept",
    "oct", "nov", "dec", "mon", "tue", "tues", "wed", "thu", "thur", "thurs",
    "fri", "sat", "sun",
}
SET_P_ASTERISKED = {"inc", "etc"}

SPEECH_VERBS = {
    "said", "asked", "replied", "answered", "shouted", "whispered", "muttered",
    "exclaimed", "cried", "continued", "began", "added", "wrote", "noted",
    "explained",
}
PRONOUNS = {"he", "she", "it", "they", "we", "you", "i"}   # lowercase only (R3.2 ii)

SPEC_DEVIATIONS = [
    "D3 vs D5: `--` (2 chars) and D5's 'exactly one character'. Implemented `--` as one punctuation token.",
    "D3: em dash (U+2014) and left single quote (U+2018) are NOT in the Punctuation Set, so `word—Next` is ONE word token.",
    "D9 lists `'` as Decoration but D3 says `'` is a word character, so it can never be a punctuation token. Decoration therefore never contains `'`.",
    "R1.1 is dead: a candidate requires whitespace/end after Decoration (D10/R0.1), so the token after the terminator can never be an adjacent word token. Implemented anyway, never fires.",
    "R2.1 lists `e.g, i.e, n.b, et al, …`: dotted entries contradict L1 (periods are tokenized away) and can never match; `…` is a literal placeholder. Dropped.",
    "R2.1 asterisks `inc*`/`etc*` refer to a nonexistent 'R2.2 note'; ruling 7.12 says `etc.` splits. Excluded from P (use --strict-asterisks to include).",
    "R3.2(i) and (ii): all listed triggers are lowercase, so R3.1 always fires first; R3.2 only differs for capitalised speech verbs (lexicon match is case-insensitive per 0.3).",
    "T3 'effective initial': implemented as the first letter-or-digit character in the following word token (scan), not strict prefix-skipping.",
    "D16: parity counted over the whole stream (across blocks), before the terminator cluster (closing quote of the decoration NOT counted).",
    "D12: blank line = `\\n{2,}` after normalising CRLF/CR to LF. Whitespace-only lines are NOT blank lines.",
    "R3.2 guard cites 'ruling 7.13' but the relevant ruling is 7.10.",
]


# --------------------------------------------------------------------------- #
# Character classes (D2)
# --------------------------------------------------------------------------- #
def is_ws(ch: str) -> bool:
    return ch.isspace()


def is_letter(ch: str) -> bool:
    return unicodedata.category(ch).startswith("L")


def is_digit(ch: str) -> bool:
    return unicodedata.category(ch) == "Nd"


def is_upper_letter(ch: str) -> bool:
    return is_letter(ch) and ch.isupper()


def is_lower_letter(ch: str) -> bool:
    return is_letter(ch) and not ch.isupper()


# --------------------------------------------------------------------------- #
# Tokenization (T1, T2, D4, D5)
# --------------------------------------------------------------------------- #
@dataclass
class Tok:
    kind: str   # 'W' word, 'P' punctuation
    text: str
    start: int
    end: int


def tokenize(s: str) -> List[Tok]:
    toks: List[Tok] = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if is_ws(ch):
            i += 1
            continue
        matched = False
        for m in PUNCT_MULTI:
            if s.startswith(m, i):
                toks.append(Tok("P", m, i, i + len(m)))
                i += len(m)
                matched = True
                break
        if matched:
            continue
        if ch in PUNCT_SINGLE:
            toks.append(Tok("P", ch, i, i + 1))
            i += 1
            continue
        j = i
        while j < n and not is_ws(s[j]) and s[j] not in PUNCT_SINGLE and not s.startswith("--", j):
            j += 1
        toks.append(Tok("W", s[i:j], i, j))
        i = j
    return toks


# --------------------------------------------------------------------------- #
# Shape helpers (D6, D7, T3)
# --------------------------------------------------------------------------- #
def is_single_char_token(t: Tok) -> bool:                       # D6
    return t.kind == "W" and len(t.text) == 1


def is_all_caps_run(t: Tok) -> bool:                            # D7
    if t.kind != "W":
        return False
    letters = [c for c in t.text if is_letter(c)]
    return (len(letters) >= 2
            and not any(is_lower_letter(c) for c in letters)
            and any(is_upper_letter(c) for c in letters))


def effective_initial(t: Optional[Tok]) -> str:                 # T3
    if t is None:
        return "none"
    for c in t.text:
        if is_letter(c) or is_digit(c):
            return c
    return "none"


# --------------------------------------------------------------------------- #
# Decision record
# --------------------------------------------------------------------------- #
@dataclass
class Decision:
    pos: int            # absolute offset of the split point (end of decoration)
    decision: str       # SPLIT | KEEP
    rule: str           # deciding rule ID
    context: str


# --------------------------------------------------------------------------- #
# Blocks (D12)
# --------------------------------------------------------------------------- #
BLOCK_TAGS = re.compile(r"</?(?:h[1-6]|li|td|p|div)\b[^>]*>", re.I)
ANY_TAG = re.compile(r"<[^>]+>")


def strip_html(src: str) -> str:
    src = BLOCK_TAGS.sub("\n\n", src)
    src = ANY_TAG.sub("", src)
    return htmllib.unescape(src)


def find_blocks(text: str):
    """Yield (start, end) of blocks; blank line = 2+ consecutive newlines."""
    pos = 0
    for m in re.finditer(r"\n{2,}", text):
        if m.start() > pos:
            yield pos, m.start()
        pos = m.end()
    if pos < len(text):
        yield pos, len(text)


# --------------------------------------------------------------------------- #
# The splitter
# --------------------------------------------------------------------------- #
def split_text(text: str, html: bool = False, strict_asterisks: bool = False,
               trace: Optional[List[Decision]] = None) -> List[str]:
    if html:
        text = strip_html(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    set_p = SET_P_BASE | (SET_P_ASTERISKED if strict_asterisks else set())

    # prefix count of quote characters over the whole stream (D16)
    prefix = [0] * (len(text) + 1)
    for i, ch in enumerate(text):
        prefix[i + 1] = prefix[i] + (1 if ch in QUOTE_CHARS else 0)

    chunks: List[str] = []

    for b_start, b_end in find_blocks(text):
        block = text[b_start:b_end]
        toks = tokenize(block)
        if not toks:
            continue
        chunk_start = 0
        i = 0
        while i < len(toks):
            t = toks[i]
            if not (t.kind == "P" and t.text in TERMINATORS):
                i += 1
                continue

            # --- D11 terminator cluster
            j = i
            while (j + 1 < len(toks) and toks[j + 1].kind == "P"
                   and toks[j + 1].text in TERMINATORS
                   and toks[j + 1].start == toks[j].end):
                j += 1
            cluster = toks[i:j + 1]
            # --- D9 decoration
            k = j
            while (k + 1 < len(toks) and toks[k + 1].kind == "P"
                   and toks[k + 1].text in DECORATION
                   and toks[k + 1].start == toks[k].end):
                k += 1
            end_pos = toks[k].end

            # --- D10 / R0.1 candidacy
            is_candidate = end_pos >= len(block) or block[end_pos].isspace()
            if not is_candidate:
                i = k + 1
                continue

            ctx = block[max(0, toks[i].start - 25): min(len(block), end_pos + 25)].replace("\n", " ")
            abs_pos = b_start + end_pos

            # --- DL3 block-edge override
            if k == len(toks) - 1:
                if trace is not None:
                    trace.append(Decision(abs_pos, "SPLIT", "DL3", ctx))
                i = k + 1
                continue

            decision, rule = decide(toks, i, j, k, block, b_start, prefix, set_p)
            if trace is not None:
                trace.append(Decision(abs_pos, decision, rule, ctx))
            if decision == "SPLIT":
                piece = block[chunk_start:end_pos].strip()
                if piece:
                    chunks.append(piece)
                chunk_start = end_pos
            i = k + 1

        tail = block[chunk_start:].strip()
        if tail:
            chunks.append(tail)

    return chunks


def decide(toks, i, j, k, block, b_start, prefix, set_p):
    """Apply DL1/DL2/DL5. Returns (decision, rule_id). Rules only ever suppress."""
    cluster_toks = toks[i:j + 1]
    pre = toks[i - 1] if i > 0 else None
    nxt_adjacent = toks[k + 1] if k + 1 < len(toks) and toks[k + 1].start == toks[k].end else None
    words_after = [t for t in toks[k + 1:] if t.kind == "W"]
    following = words_after[0] if words_after else None
    initial = effective_initial(following)

    # R0.2 classification
    cluster_str = "".join(c.text for c in cluster_toks)
    is_ellipsis = "…" in cluster_str or cluster_str.count(".") >= 2

    # R1.1 internal period (adjacent)  -- dead in practice, see deviations
    if (pre is not None and pre.kind == "W" and pre.end == toks[i].start
            and nxt_adjacent is not None and nxt_adjacent.kind == "W" and k == j):
        return "KEEP", "R1.1"
    # R1.2 single-character pre-token
    if pre is not None and is_single_char_token(pre):
        return "KEEP", "R1.2"
    # R1.3 all-caps run
    if pre is not None and is_all_caps_run(pre):
        return "KEEP", "R1.3"
    # R2.1 set P
    if pre is not None and pre.kind == "W" and pre.text.lower() in set_p:
        return "KEEP", "R2.1"
    # R3.1 lowercase continuation
    if initial != "none" and is_lower_letter(initial):
        return "KEEP", "R3.1"
    # R3.2 attribution pattern
    parity_open = prefix[b_start + toks[i].start] % 2 == 1
    if parity_open:
        w = [x.text for x in words_after[:LAMBDA]]
        if w and w[0].lower() in SPEECH_VERBS:
            return "KEEP", "R3.2(i)"
        if len(w) >= 2 and w[0] in PRONOUNS and w[1].lower() in SPEECH_VERBS:
            return "KEEP", "R3.2(ii)"
    # R4.2 ellipsis
    if is_ellipsis:
        return "KEEP", "R4.2"
    # DL5 capital condition / DL1 default
    if initial != "none" and is_upper_letter(initial):
        return "SPLIT", "DL1+DL5"
    return "KEEP", "DL5"


# --------------------------------------------------------------------------- #
# Tests: the 24 worked rulings of §7 (expected chunk lists)
# --------------------------------------------------------------------------- #
RULINGS = [
    ("7.1", "The value is 9.81 m/s². The test passed.", ["The value is 9.81 m/s².", "The test passed."]),
    ("7.2", "See example.com for details. We left.", ["See example.com for details.", "We left."]),
    ("7.3", "She earned her Ph.D. The committee met.", ["She earned her Ph.D. The committee met."]),
    ("7.4", "Dr. Smith arrived. He sat.", ["Dr. Smith arrived.", "He sat."]),
    ("7.5", "St. James's Park is old. It is nice.", ["St. James's Park is old.", "It is nice."]),
    ("7.6", "J. K. Rowling wrote it. More followed.", ["J. K. Rowling wrote it.", "More followed."]),
    ("7.7", "I don't. You do.", ["I don't.", "You do."]),
    ("7.8", '"Stop!" he said. Then it ended.', ['"Stop!" he said.', "Then it ended."]),
    ("7.9", '"Stop!" He left.', ['"Stop!"', "He left."]),
    ("7.10", '"It is over." He said nothing.', ['"It is over."', "He said nothing."]),
    ("7.11", '"What?" asked the teacher. Nobody answered.', ['"What?" asked the teacher.', "Nobody answered."]),
    ("7.12", "We bought bread, etc. Then we left.", ["We bought bread, etc.", "Then we left."]),
    ("7.13", "We bought bread, etc. and milk.", ["We bought bread, etc. and milk."]),
    ("7.14", "The treaty followed in 1995. It held.", ["The treaty followed in 1995.", "It held."]),
    ("7.15", "The current reached 5 A. The voltage rose.", ["The current reached 5 A. The voltage rose."]),
    ("7.16", "Chapter IV. The next chapter began.", ["Chapter IV. The next chapter began."]),
    ("7.17", "It was over… A new era began.", ["It was over… A new era began."]),
    ("7.18", "It uses natural language processing (NLP). We tried it.",
     ["It uses natural language processing (NLP).", "We tried it."]),
    ("7.19", "It was signed in the U.S. The Senate adjourned.", ["It was signed in the U.S. The Senate adjourned."]),
    ("7.20", "It was in the U.S. Senate adjourned early.", ["It was in the U.S. Senate adjourned early."]),
    ("7.21", "Wait… what happened next. Nobody knows.", ["Wait… what happened next.", "Nobody knows."]),
    ("7.22", "NASA was founded. Later it grew.", ["NASA was founded.", "Later it grew."]),
    ("7.23", "He is taller than I. Others disagree.", ["He is taller than I. Others disagree."]),
    ("7.24", "Prices rose 5. The next year fell.", ["Prices rose 5. The next year fell."]),
]


def run_tests(strict_asterisks=False) -> int:
    failed = 0
    for rid, text, expected in RULINGS:
        got = split_text(text, strict_asterisks=strict_asterisks)
        ok = got == expected
        failed += (not ok)
        print(f"[{'PASS' if ok else 'FAIL'}] {rid}: {text}")
        if not ok:
            print(f"        expected: {expected}\n        got:      {got}")
    print(f"\n{len(RULINGS) - failed}/{len(RULINGS)} rulings pass")
    return failed


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Suppression-spec v1.0 sentence splitter")
    ap.add_argument("file", nargs="?", help="input file, or - for stdin")
    ap.add_argument("--html", action="store_true", help="treat input as HTML (D12)")
    ap.add_argument("--trace", action="store_true", help="print every candidate and the rule that decided it")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--raw", action="store_true", help="keep internal newlines/spacing in output chunks")
    ap.add_argument("--strict-asterisks", action="store_true", help="put etc/inc into set P")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--deviations", action="store_true")
    a = ap.parse_args()

    if a.deviations:
        for d in SPEC_DEVIATIONS:
            print("-", d)
        return
    if a.test:
        sys.exit(1 if run_tests(a.strict_asterisks) else 0)
    if not a.file:
        ap.error("give a file, '-' for stdin, --test, or --deviations")

    src = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    tr: List[Decision] = []
    chunks = split_text(src, html=a.html, strict_asterisks=a.strict_asterisks, trace=tr)

    if a.trace:
        for d in tr:
            print(f"{d.decision:5} {d.rule:8} @{d.pos:<6} ...{d.context}...", file=sys.stderr)
    if a.json:
        print(json.dumps({"chunks": chunks, "trace": [asdict(d) for d in tr]}, ensure_ascii=False, indent=2))
    else:
        for c in chunks:
            print(c if a.raw else " ".join(c.split()))


if __name__ == "__main__":
    main()
