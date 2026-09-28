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
| [`suppression-spec.md`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/suppression-spec.md) | The suppression-based splitting spec | — |
| [`suppression_splitter.v1.py`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/suppression_splitter.v1.py) | Reference implementation of the spec | ❌ |
| [`corpus_trace.v1.txt`](https://github.com/SANIUL-blackdragon/sentence-splitting-research/blob/main/corpus_trace.v1.txt) | Trace output against the prose corpus | ❌ |

The v1 suppression splitter does **not** split correctly against the current corpus. See the trace file for details.

---

## Repository Layout

```
sentence-splitting-research/
├── README.md
├── suppression-spec.md
├── suppression_splitter.v1.py
├── corpus_trace.v1.txt
├── prose-corpus.md
├── *.md                          # research notes, abbreviation references, punctuation summaries
├── *.html                        # rendered prose test material
└── *.pdf                         # reference PDFs
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

---

## How to Test

```bash
# Clone the repo
git clone https://github.com/SANIUL-blackdragon/sentence-splitting-research.git
cd sentence-splitting-research

# Run the v1 splitter against the corpus (example)
python suppression_splitter.v1.py prose-corpus.md
```

Compare the output against the expected splits in the HTML test files.

---

## Design Principles

- **No ML models.** Must run on very weak hardware.
- **Rule-based / algorithmic.** Deterministic, fast, and inspectable.
- **Streaming-friendly.** Output must be usable sentence-by-sentence, incrementally.
- **Correctness over coverage.** Better to under-split than to mis-split.

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
