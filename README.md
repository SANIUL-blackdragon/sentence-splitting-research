# Sentence Splitting Research

A lightweight, rule-based sentence splitting research archive — built for real-time TTS streaming on low-end hardware.

---

## Why This Exists

This repo is a **public research archive** for a narrow problem: **how to split prose into sentences with algorithms**, without ML models.

I'm building a project (to be open-sourced later) with an **English TTS feature**. The TTS layer needs to split prose **per sentence only**, so that:

- Sentence *N* can be spoken while sentence *N+1* (and onward) is being generated as audio **in parallel**.
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
| [`corpus_trace.v1.txt`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/corpus_trace.v1.txt) | Trace output against the prose corpus (12,862 decisions) | ❌ |
| [`trace-analysis.v1.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/trace-analysis.v1.md) | **Test 1 post-mortem** — measured analysis of the trace | 📊 |

The v1 suppression splitter does **not** split correctly against the current corpus. The trace analysis documents *why*: the failure is on **recall** and **corpus fit**, not precision. See the [full analysis](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/trace-analysis.v1.md) for measured numbers and rule-level attribution.

---

## Test 1 Post-Mortem — Key Findings

The trace analysis ([`trace-analysis.v1.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/trace-analysis.v1.md)) is a measurement-only companion to the trace. It contains no code and proposes no implementation — every claim cites a rule ID from the spec or a measurable quantity from the trace.

**Verdict:** The precision guarantee (W1) held — no false split was found outside the doors §6 already declares. The failure is on recall and corpus fit. Three independent collapse modes:

1. **R1.2 is the modal suppression, and most of its work is wrong for this genre.**
   AM-2 (single-character pre-tokens) was scheduled as a tail risk. Measured: **2,686 keeps — 20.9% of all candidates and 71.2% of all keeps**. Only ~29% of those are correct (dotted abbreviations like `p.d.`, `e.g.`, `e.m.f.`). The rest are false merges: sentence-final units (`…10⁻¹⁷ J. Show that…`), single-digit math ends (`…= 7. The number…`), and point labels (`…at P. Stating that…`). The accepted-miss schedule was calibrated for the wrong genre.

2. **Enumerators fire in both directions.**
   47 output chunks are *nothing but* a label (`10.`, `11.`, `12.`, …) — orphan splits, exactly as Door A(ii) predicted. Single-digit labels (`2.`, `3.`) glue entire lists into one chunk. Part labels like `(b)` and `(c)` glue question stems to sub-parts via R3.1. The OI-1 scope is too narrow — the measured family includes `(a)`-style part labels, `Q16a`, `M3`, `MS:`, `Spec ref:`, `✓`, and `77 —` page markers.

3. **28% of output chunks contain no sentence terminator at all.**
   The corpus is study-guide render — tables, ASCII diagrams, headings, mark-scheme labels. The specification has no concept of non-prose furniture, so the splitter adjudicates it as prose. **6,172 of 22,257 chunks (27.7%)** have no sentence terminator. 2,071 chunks begin with `#` (markdown headings). 392 contain ASCII-diagram debris.

Additional findings: R1.3 eats physics formulae (155 keeps; `V = W/Q.`, `R = V/I.` merge the next sentence). Set P fired only 7 times, with 4 of those being wrong-direction keeps (`Ca.` the element, `ms.` milliseconds, `sat.` the verb, `No.` the answer word). Ruling (d) created an undeclared glue class for em dashes. The reference implementation still implements v1.0 behavior on several conformance deltas (§9 of the analysis).

**What held:** W1 (precision), DL3 (block-edge splits), R0.1 (decimal/domain/scientific-notation absorption), and dotted-abbreviation absorption. The architecture did what precision-first theory says it should — it prevented mis-splits. What failed is the *calibration of the accepted-miss schedule* and the *absence of an ingestion boundary* for non-prose furniture.

---

## Repository Layout

```
sentence-splitting-research/
├── README.md
├── suppression-spec.md              # spec for the suppression-based splitter (v1.2)
├── suppression_splitter.v1.py       # v1 reference implementation
├── corpus_trace.v1.txt              # v1 trace output (12,862 decisions)
├── trace-analysis.v1.md             # Test 1 post-mortem — measured analysis
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

35,959 lines, ≈285k words, ≈17.5k blank-line-separated blocks.

---

## How to Test

```bash
# Clone the repo
git clone https://github.com/SANIUL-blackdragon/sentence-splitting-research.git
cd sentence-splitting-research

# Run the v1 splitter against the corpus (example)
python suppression_splitter.v1.py prose-corpus.md

# Regenerate the trace (byte-identical from current code + corpus)
python suppression_splitter.v1.py prose-corpus.md --trace
```

Compare the output against the expected splits in the HTML test files. Every number in the trace analysis describes live behavior, not a stale artifact.

---

## Design Principles

- **No ML models.** Must run on very weak hardware.
- **Rule-based / algorithmic.** Deterministic, fast, and inspectable.
- **Streaming-friendly.** Output must be usable sentence-by-sentence, incrementally.
- **Correctness over coverage.** Better to under-split than to mis-split.

---

## Recommended Next Moves

From the trace analysis (§11), ordered by expected value:

1. **Close OI-5 with this trace.** Write the measured frequencies into W3a. The "unmeasured" era is over; the schedule is falsified for technical prose.
2. **Decide OI-2 with data.** Scoping R1.2/R1.3 to `.`-only trades the AM-2/AM-3 mass for AM-8 expansion.
3. **Widen OI-1 into one enumerator/label rule** covering multi-digit numerals, `(a)`-style part labels, and `Q16a`/`M3`-style question keys.
4. **Add an L3 namespace guard** for entries colliding with element symbols, SI units, or high-frequency verbs.
5. **Open a new issue for the em-dash consequence** of ruling (d).
6. **Make the D1/D12 furniture decision** — strip furniture upstream or recognize markdown/table/diagram boundaries.
7. **Reconcile the implementation to v1.2** before the next eval.

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
