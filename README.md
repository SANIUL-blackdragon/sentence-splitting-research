# Sentence Splitting Research

A lightweight, rule-based sentence splitting research archive — built for real-time TTS streaming on low-end hardware.

---

## Why This Exists

This repo is a **public research archive** for a narrow problem: **how to split prose into sentences with algorithms**, without ML models.

I'm building a project (to be open-sourced later) with an **English TTS feature**. The TTS layer needs to split prose **per sentence only**, so that:

- Sentence *N* can be spoken while *N+1* (and onward) is being generated as audio **in parallel**.
- The result is a **streaming-like UX** instead of waiting for an entire paragraph.

My current splitting layer has bugs — it doesn't split exactly where it should in some cases. ML models exist for this, but they're too heavy and too slow for users on **trash machines**. So the goal here is:

> **As light as possible. As fast as possible. Good enough for a smoother streaming UX.**

I'm keeping this public in case it helps someone else. No promises for the future.

---

## Current Status

**Test 1: Fail (as of commit `5e53df2`).**

| Artifact | Purpose | Result |
|---|---|---|
| [`suppression-spec.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/suppression-spec.md) | The suppression-based splitting spec (v1.2) | — |
| [`suppression_splitter.v1.py`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/suppression_splitter.v1.py) | Reference implementation of the spec | ❌ |
| [`corpus_trace.v1.txt`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/corpus_trace.v1.txt) | Trace output (12,862 decisions, 9,089 logged splits) | ❌ |
| [`trace-analysis.1.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/trace-analysis.1.md) | **Test 1 post-mortem, deep edition** — supersedes v1; measurement-only | 📊 |
| [`structural-report.1.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/structural-report.1.md) | **unslop lens** — the same trace read as prose, from the listener's side | 📊 |

The v1 splitter does **not** split correctly against the current corpus. Two independent audits — one decision-level, one reading-level — reach the same verdict from opposite directions.

---

## Test 1 Post-Mortem — The Short Version

Two companions to the trace, both measurement-only, both regenerating the trace byte-identically. Read together they agree on three culprits.

**Verdict: the architecture did its job. The accepted-miss schedule was calibrated for the wrong genre, and nine tenths of the visible damage happens before any rule fires.**

### 1. W1 holds — now as a measurement, not a doctrine

Split-side precision: **8,918 / 9,089 = 98.12%**. All 171 false splits pass through doors §6 already declares: **159 through Door A(ii)** (enumerator/label orphans), **12 through Door A(i)** (one family: `conc.` before a chemical formula). Doors B and C: zero violations.

### 2. The suppression stack is mis-calibrated, rule by rule

| Rule | Keeps | Wrong | Precision |
|---|---:|---:|---:|
| R1.2 (single-char veto) | 2,686 | 2,021 | **24.8%** |
| R3.1 (lowercase continuation) | 206 | 177 | 14.1% |
| R1.3 (all-caps/formula) | 155 | 154 | 0.6% |
| R2.1 (Set P) | 7 | 4 | 42.9% |
| R4.2 (ellipsis) | 19 | 10 | 47.4% |
| KEEP-DL5 (fall-through) | 700 | sampled ≈33% precision | — |

R1.2 is the modal suppressor and the worst offender. The mass is **digits and units**: `2`×309, `1`×305, `3`×279 … within the 1,556 digit keeps, **1,107 are line-start enumerators** and **449 are math/number sentence-ends**. The correct keeps are almost entirely the six dotted-abbreviation families (`p.d.`, `e.g.`, `e.m.f.`, `s.f.`, `b.p.`, `i.e.`). A tail-whitelist limited to those families preserves ~97% of R1.2's correct work while licensing splits for ~1,976 false merges.

### 3. The largest pathology is upstream of every rule

Of 10,492 terminator-less output chunks, **89.6% are manufactured by the blank-line block layer alone** (D12). The spec has no ingestion layer — the block layer adjudicates 100% of the corpus as prose, but only **66.1% of input blocks are prose**. DL3, the most numerous split license (4,367 decisions), is at output level a no-op: it certifies tails the block layer cuts anyway.

### What held

W1 (precision, now measured), DL3 (all 4,367 block-edge splits are clean), R0.1 (decimal/domain/scientific-notation absorption), and dotted-abbreviation absorption. R1.1 and R3.2 never fire. The em-dash concern from v1 measured benign: 99.3% of the 3,184 em dashes are spaced, and the 21 word-adjacent ones are chemistry bond notation where fusion is desirable.

### Recall

v1 had no recall number. v2 measures it: **pooled expert-reader recall 0.837** (95% CI [0.727, 0.948]); per-genre 1.000 study-guide / 0.714 exam-readiness / 0.857 reference. Misses concentrate at part-label glue (R3.1) and at boundaries the candidate machinery never sees.

---

## The unslop Lens

[`structural-report.1.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/structural-report.1.md) reads the 22,257 output chunks as prose and applies unslop's 30 rules as a detection instrument. The corpus passes every **lexical** rule (2 AI-vocab hits in 22,257 chunks; zero sycophancy, hedging, filler, fancy synonyms) and fails the **structural** ones:

| Lens | Measured | Reading consequence |
|---|---|---|
| Run-on sentences | 3,052 glued boundaries in 1,788 chunks | two or three sentences spoken as one breath |
| Verbless fragments | 13,193 chunks (59.3%) end without a terminator | no prosodic close on roughly every other utterance |
| Heading markers | 2,071 chunks open on `#` | the listener hears "hash hash hash" |
| UI glyph debris | 117 chunks carry `☰ ✕ ☽ ✓ □`; 39 are one character | syllables of noise |

Attribution of the 3,052 run-on boundaries: **70.6% to R1.2**, 19.0% to the DL5 fall-through, 4.8% to R1.3, 4.7% to R3.1. The reading lens and the decision lens agree on the culprit.

The ownership verdict splits cleanly into three columns: what the **splitter** manufactures (R1.2 run-ons, block-layer fragments), what the **source** owns (gerund openers, "students" as agent, colons, em dashes, boilerplate), and what only a **TTS layer** can fix (heading markers, glyph expansion).

---

## Repository Layout

```
sentence-splitting-research/
├── README.md
├── suppression-spec.md              # spec for the suppression-based splitter (v1.2)
├── suppression_splitter.v1.py       # v1 reference implementation
├── corpus_trace.v1.txt              # v1 trace output (12,862 decisions)
├── trace-analysis.1.md              # Test 1 post-mortem, deep edition (supersedes v1)
├── structural-report.1.md           # unslop lens — the trace read as prose
├── prose-corpus.md                  # prose extracted from the HTML test material
├── *.md                             # research notes, abbreviation references, punctuation summaries
├── *.html                           # rendered prose test material
└── *.pdf                            # reference PDFs
```

### HTML test material

```
ch2.3-exam-readiness-questions.html    ch2.7-study-guide.html
ch2.3-study-guide.html                 ch2.8-exam-readiness-questions.html
ch2.4-exam-readiness-questions.html    ch2.8-study-guide.html
ch2.4-study-guide.html                 ch2.9-exam-readiness-questions.html
ch2.6-exam-readiness-questions.html    ch2.9-study-guide.html
ch2.6-study-guide.html                 u2-memorization.html
ch2.7-exam-readiness-questions.html    unit2-formula-sheet.html
ext-cp4-8-methods.html                 physics-reference.html
ext-past-papers-index.html             physics-reference-light.html
ext-practical-vocab.html               physics_formula_atlas.html
ext-synoptic.html                      physics_formula_atlas_light.html
ext-uncertainty.html                   waves-quanta-reference.html
```

### Markdown research notes

```
aistackexchange_abbreviated_words_2925.md    grammarly_types_of_abbreviations.md
cambridge-punctuation-summary.md             preply_english_abbreviations.md
charisma-punctuation-summary.md              quetext-end-punctuation-summary.md
end-of-sentence-punctuation-grammarly.md     researchgate_abbreviations_question.md
end-punctuation-lumenlearning.md             scielo_krajsavar_article.md
end-punctuation-quillbot.md                  stackoverflow_abbreviation_detection.md
```

### PDFs

```
54085.pdf
kompara.pdf
```

---

## The Corpus

The HTML files are **test material** to check whether rendered prose gets split correctly. The prose from all HTML files has been extracted into:

➡️ [`prose-corpus.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/prose-corpus.md)

**1,693,006 characters** (1,748,367 bytes), 17,535 blank-line-separated blocks, 759.7 candidates per 100k characters. The trace regenerates byte-identically from the current code + corpus.

---

## How to Test

```bash
git clone https://github.com/SANIUL-blackdragon/sentence-splitting-research.git
cd sentence-splitting-research

# Run the v1 splitter against the corpus
python suppression_splitter.v1.py prose-corpus.md

# Regenerate the trace (byte-identical from current code + corpus)
python suppression_splitter.v1.py prose-corpus.md --trace
```

Every number in the two analysis documents describes live behavior, not a stale artifact.

---

## Design Principles

- **No ML models.** Must run on very weak hardware.
- **Rule-based / algorithmic.** Deterministic, fast, and inspectable.
- **Streaming-friendly.** Output must be usable sentence-by-sentence, incrementally.
- **Correctness over coverage.** Better to under-split than to mis-split.

---

## Recommended Next Moves

From `trace-analysis.1.md` §11, ordered by expected value:

1. **Open the ingestion layer.** The single largest lever: 89.6% of terminator-less chunks are born at block tails. Either strip furniture upstream or extend D1/D12 to recognize markdown/table/diagram boundaries.
2. **Redesign R1.2 two-sidedly.** Move digits and units from the KEEP side to the SPLIT side; whitelist the six dotted-abbreviation families. Estimated: preserves ~97% of correct keeps, licenses ~1,976 splits.
3. **Close OI-5 with the measured frequencies.** AM-2 is 2,021 false merges, not a tail risk. The "unmeasured" era is over.
4. **Widen OI-1 into one enumerator/label rule** covering multi-digit numerals, `(a)`-style part labels, and `Q16a`/`M3`-style question keys. Closes the 159 Door A(ii) leaks plus the R3.1 part-label glue.
5. **Add an L3 namespace guard.** Entries colliding with element symbols (`Ca`), SI units (`ms`), or high-frequency verbs (`sat`) require corpus evidence before admission. Current wounds: 4 of 7 Set P fires.
6. **Reconcile the implementation to v1.2** before the next eval so the trace's rule citations are audit-meaningful.

---

## Contributing / Feedback

If this helps you, or if you have ideas for a better light-weight ruleset, open an issue or a PR. No promises on response time.

---

## License

No license file yet. Will be added later.

---

## Author

**SANIUL-blackdragon** — [GitHub](https://github.com/SANIUL-blackdragon)

---
