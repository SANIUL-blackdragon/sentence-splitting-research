# Trace Analysis v1 — `corpus_trace.v1.txt` against the Suppression Specification

> **Status: Test 1 post-mortem.** Companion to [`corpus_trace.v1.txt`](corpus_trace.v1.txt), [`suppression_splitter.v1.py`](suppression_splitter.v1.py), [`suppression-spec.md`](suppression-spec.md) (v1.2), and [`prose-corpus.md`](prose-corpus.md).
>
> **Scope:** analysis and measurement only. This document contains no code and proposes no implementation. Every claim cites a rule ID from the spec (D-, T-, DL-, R-, L-, W-, AM-, OI-) or a measurable quantity from the trace.

---

## 0. Verdict (read this first)

**The trace is not a precision failure. The precision guarantee (W1) held: no false split was found outside the doors §6 already declares.**

**Test 1 fails on recall and on corpus fit.** Three independent collapse modes, all measurable:

1. The accepted-miss schedule (W3a) is **falsified for this genre**. AM-2 (single-character pre-tokens) is not a tail risk in exam/technical prose — it is the *modal* suppression: 20.9% of all candidates die at R1.2, and the majority of those are true sentence ends (units, point labels, single digits, single-digit enumerators).
2. The enumerator/label family left open by OI-1 **measures in the hundreds**, and it fails in both directions: multi-digit labels orphan-split (false splits, exactly as Door A(ii) predicts), single-digit labels and part labels glue (false merges).
3. **28% of output chunks contain no sentence terminator at all.** The corpus is study-guide render — tables, ASCII diagrams, headings, mark-scheme labels — and the specification has no concept of non-prose furniture, so the splitter adjudicates it as if it were prose.

Additionally, the reference implementation still implements v1.0 behavior; none of its conformance deltas changed an outcome on this corpus, but several are landmines (§7).

---

## 1. Method and reproducibility

- Source: `corpus_trace.v1.txt` (12,862 decisions), produced by `suppression_splitter.v1.py` against `prose-corpus.md` (35,959 lines, ≈285k words, ≈17.5k blank-line-separated blocks).
- **The committed trace regenerates byte-identically** from the current code + corpus (`python suppression_splitter.v1.py prose-corpus.md --trace`). Every number below describes live behavior, not a stale artifact.
- Contexts quoted from the trace are shown with `…` marking the ±25-character context window. Offsets are character positions in `prose-corpus.md`.
- Decision counts were aggregated over all 12,862 trace lines; class counts quoted as "measured" are exact pattern matches over trace contexts unless marked *lower bound* (regex-visible subset of the class) or *sampled* (eyeball classification of random slices).

---

## 2. The numbers

| Decision | Rule cited | Count | Share of candidates | Share of keeps |
|---|---|---:|---:|---:|
| SPLIT | DL3 (block edge) | 4,367 | 33.9% | — |
| SPLIT | DL1+DL5 (in-block) | 4,722 | 36.7% | — |
| KEEP | R1.2 (single-char pre-token) | **2,686** | **20.9%** | **71.2%** |
| KEEP | DL5 (non-capital continuation) | 700 | 5.4% | 18.6% |
| KEEP | R3.1 (lowercase continuation) | 206 | 1.6% | 5.5% |
| KEEP | R1.3 (all-caps run) | 155 | 1.2% | 4.1% |
| KEEP | R4.2 (ellipsis) | 19 | 0.15% | 0.5% |
| KEEP | R2.1 (set P) | **7** | **0.05%** | 0.2% |
| | **Total** | **12,862** | 100% | 3,773 keeps |

Output: 22,257 chunks (= 17,535 block tails + 4,722 in-block splits, exactly). Average chunk 77 characters; 300 chunks > 300 chars; 20 > 600; **6,172 chunks (27.7%) contain no sentence terminator**.

Sanity arithmetic: 17,535 + 4,722 = 22,257 confirms the splitter never dropped or duplicated a block, and the decision stream is internally consistent with the chunk stream.

---

## 3. Issue 1 — R1.2 is the modal suppression, and most of its work is wrong for this genre

AM-2 records "frequency: unmeasured." Measured: **2,686 keeps, 20.9% of all candidates**. Decomposition:

**Correct keeps — ≈770 (≤29% of R1.2's fires).** The dotted-abbreviation machinery working exactly as designed (R0.1 absorbs internal dots; R1.2 holds the final dot). Corpus occurrences: `p.d.` ×367, `e.g.` ×235, `e.m.f.` ×149, `i.e.` ×19. One keep per occurrence (upper bound; occurrences at block edges resolve by DL3 instead).

**False merges — ≈1,900.** True sentence ends welded shut because the sentence-final token is a single character:

| Sub-class | Measured | Trace examples |
|---|---|---|
| Single-letter units | ≈190–210 contexts *(lower bound)* | `…2.0 × 10⁻¹⁷ J. Show that its de Broglie…` · `…0.85 m. The second-order maximum…` · `…1 g. Therefore, if you have 50.0 cm³…` · `…6.88 × 10⁻¹⁹ J. Applies photoelectric…` |
| Single-digit math ends | ≥14 contexts | `…At this limit, sin θ = 1. Substituting into the…` · `…bonds = n − 1 = 8 − 1 = 7. The number of C–H bonds…` |
| Point labels (diagram P/Q) | observed class (sampled) | `…maximum at P. Stating that density is…` · `…minimum at Q. Any answer that does not…` |
| Single-digit enumerators | see Issue 2 | glues list items into one chunk |

In ordinary prose, sentence-final single characters are rare and the AM-2 assumption ("cost: merged chunks", low frequency) is reasonable. In exam-mark-scheme prose, sentences **end with units, point labels, and numbers constantly**. The accepted-miss schedule was calibrated for the wrong genre.

---

## 4. Issue 2 — Enumerators: OI-1 fires in both directions

The spec left enumerators open (OI-1, Door A(ii)). The corpus measures the family:

**Multi-digit labels orphan-split (false splits).** 47 output chunks are *nothing but* a label: `10.` ×17, `11.` ×13, `12.` ×10, `13.` ×5, `14.` ×2. Mechanism: pre-token `10` is not a single character (R1.2 silent), not an all-caps run (R1.3 silent), not in P (R2.1 silent) → DL1 splits the label off its own text. This is §6 Door A(ii) exactly as written — the spec predicted its own defect correctly.

**Single-digit labels glue (false merges).** The pre-candidate token of `2.` is the digit `2` itself → R1.2 keeps → entire single-newline lists fuse into one chunk. Verified at offset 723075 of the corpus: `1. Wrong mass. Use the solution… 2. Missing the negative sign… 3. Not dividing by moles… 4. Reading ΔT from the peak… 5. Significant figures.` — one chunk.

**Part labels glue via R3.1 (206 keeps, ~all sampled).** `(b)` and `(c)` begin with an opening mark, so T3 skips it and the effective initial is the lowercase letter → R3.1 suppresses → question stem fuses with its sub-parts: `…measured from the normal. (b) Calculate the critical angle…`.

**The OI-1 scope is too narrow.** It names multi-digit numerals and lowercase Roman numerals. The measured family also includes: `(a)`-style part labels, `Q16a`, `M3`, `MS:`, `Spec ref:`, `✓`, and `77 —` page markers. One rule covering the label family would close the 47 orphan splits, the ~206 part-label merges, and the list glue through a single door.

---

## 5. Issue 3 — R1.3 eats physics formulae (AM-3 confirmed heavy)

155 keeps, sampled nearly all true ends. Under D7 a formula token **is** an all-caps run — two uppercase letters is all it takes:

- `…circuit: V = W/Q. It is the energy lost per…` (pre-token `W/Q`)
- `…current through it: R = V/I. 66 20 marks…` · `…derived using V = IR. 69 —…`
- `…P = VI: P = I(IR) = I²R. Useful when current…`
- `…smallest ΔE. Arrow length on an…` · `…required for DER. Each algebraic…` · `…boundary for TIR. Without cladding…` · `…readings in CP7. Its role is…`

AM-3's hedge — "likely non-trivial in modern and technical prose" — was an understatement. In this genre the sentence-final token is a formula or acronym on a regular basis, and each occurrence merges the next sentence into the current one.

---

## 6. Issue 4 — Set P is dormant on this corpus, and net-harmful when it fires

**7 fires in 12,862 candidates (0.05%).** The corpus contains no honorifics and no months — it is physics. Of the 7 fires, **3 are correct** (`pp.` page refs, ×3) and **4 are wrong-direction keeps**:

| Fire | Collision | Glued text |
|---|---|---|
| `Ca.` the **element** matched `ca` **circa** | chemistry symbol ∈ P | `…Flame test colour of Ca. MS: Orange-red / brick-red…` |
| `ms.` **milliseconds** matched `ms` **the honorific** (×2 in corpus) | SI unit ∈ P | `…× 0.1 ms = 0.30 ± 0.10 ms. Convert to seconds…` |
| `sat.` the **verb** matched `sat` **Saturday** (‡) | common verb ∈ P | `…2026 has not yet been sat. See the master index…` |
| `No.` the **answer word** (‡) | declared AM-9, observed in the wild | `…No. Carbon is not electronegative…` |

Two structural observations:

1. The lexicon's L3 audit protocol guards against function words, but nobody scoped the **chemistry/SI-unit namespace**: `ca`, `no`, `cf`, `mt` are all in P and all are element symbols; `ms`, `s`, `A`, `V`, `K`, `T`, `W` collide with units. A namespace guard is a lexicon-law problem, not an entry problem.
2. R2.1 contributed nothing positive to this corpus (3 correct page-ref keeps) while its 4 wrong fires each destroyed a true boundary. Set P, as constituted, is not merely under-tuned for this genre — its few interactions are net-negative.

---

## 7. Issue 5 — Ruling (d) created an undeclared glue class (em dash)

v1.2 ruling (d) returned `—` to the word-character class (correct per the principal; `word—Next` is one token). Declared consequence: tokenization. **Undeclared consequence:** after a terminator, an em dash is now a word token, so the *following token* is `—`, the effective initial is *none* → suppression fires (R3.1/DL5):

- `…occur at a glass block?" — diffraction (it occurs…` (following token after `?"` is `—`)
- `…equals the e.m.f. — at this point all of the…`

Measured: 47 DL5 keep-contexts contain an em dash adjacent to the candidate (upper bound — includes mid-sentence dashes inside the context window); ≥7 follow a closing quote. Small in this corpus, but structural: **every terminator-then-em-dash is now a keep, by construction, with no W3a/W3b row acknowledging it.** The specification should either declare it a new AM row or amend T3 to treat a terminator followed by an em dash like an opening mark (a design decision for the principal — it is a rule change, not a lexicon change).

---

## 8. Issue 6 — Non-prose furniture dominates the chunk stream (ingestion layer)

The corpus is rendered study-guide material. The specification defines markup block boundaries only for HTML tags (D12) and has no concept of furniture, so the splitter adjudicates tables, diagrams, and labels as prose:

| Furniture class | Measured | Effect |
|---|---|---|
| Chunks with no sentence terminator | 6,172 (27.7% of output) | fragment stream, not sentence stream |
| Chunks beginning with `#` (markdown headings) | 2,071 | TTS reads the hashes; heading enumerators (`### 3. Hess's…`) reach R1.2 |
| Chunks containing table pipes | 154 | one chunk per table row |
| Chunks containing ASCII-diagram debris (`\`, boxes, arrows) | 392 | the Hess-cycle drawings also generate fake `...` clusters → R4.2 keeps |
| Glue tokens: `77 —` page markers, `✓`, `" (3 marks, Jun 2024 Q16b)`, `MS:`, `Spec ref:` | observed throughout | merge into neighboring chunks via DL5/R3.1 |

Door C itself barely fired: 2 `**` occurrences in the whole corpus (1 in output), `<` is physics less-than, not markup. **Tokenization held up; the corpus composition is the problem.** Either strip furniture upstream (as the HTML→corpus conversion already stripped tags), or extend D1/D12 to recognize markdown/table/diagram block boundaries. This is the single largest lever on output hygiene, and it is a boundary-definition decision, not a suppression rule.

---

## 9. Issue 7 — The reference implementation still implements v1.0 (conformance deltas)

None of these changed an outcome on this corpus (the trace reproduces identically and R3.2 fired 0 times), but all of them are live in the code:

1. **`--strict-asterisks` exists.** L5 names this exact toggle as non-conformant ("no flag, mode, build option, profile, or runtime configuration may add, remove, or vary entries").
2. **R3.2 is implemented though withdrawn** (v1.1): speech-verb lexicon + pronoun list (L2 withdrawn), λ=3 (D15 says 1), parity counted over the whole stream (D16 says per-block), verb matching case-insensitive (even v1.0's own guard excluded capitalized continuations).
3. **`BLOCK_TAGS` is missing `th`.** The v1.1 D12 fix (th added) never reached the code; `<th>` cells in HTML input will fuse.
4. **Whitespace-only lines are not blank lines** in the code (contradicts D12: "a line containing only whitespace (possibly empty)" is a blank line).
5. **T3 divergence:** the code scans forward to the first *word* token, skipping all punctuation; the spec skips only opening marks, else the following token is not usable. Divergent outcome class exists (e.g. `."), She` → code SPLITs, spec KEEPs).
6. **D6 divergence:** the code treats any 1-character word token as a single-character token, including lone symbols (`%`, `°`, `×`); D6 says one Letter or one Digit only. Direction of error: extra keeps (safe side), but non-conformant.
7. **Citation drift:** the code cites R1.2/DL5 where the spec would cite R3.1 (digit-initial and *none* initials are R3.1 fires per v1.2). Outcomes identical; citations differ — which matters when the trace is the audit artifact.

Reconciling the implementation to v1.2 before the next eval is what makes the trace's *rule column* meaningful as evidence.

---

## 10. What held (for the record)

- **W1 held.** No false split was found outside §6's doors. Door B's 146 quote-then-capital splits were sampled and are overwhelmingly *correct* (quoted fragment ends, capital commentary begins: `…the tube is too short." Using bullet points…`).
- **DL3 is clean.** All 4,367 block-edge splits sampled so far are true boundaries.
- **R0.1 is doing silent, heavy work correctly**: every decimal (`9.81`, `3.33 × 10⁻⁶`), domain, ratio, and scientific-notation token produced no candidate, as designed.
- **Dotted abbreviations are fully absorbed** (`p.d.`, `e.m.f.`, `e.g.`, `i.e.` — ≈770 correct keeps).
- **R3.2 never fired** (dormant, but see §9.2).
- **Output granularity is salvageable**: average chunk 77 chars; only 300 chunks >300 chars, and those are multi-part answers and lists (Issues 2 and 6), not runaway merges.

The architecture did what precision-first theory says it should: the suppression stack prevented mis-splits. What failed is the *calibration of the accepted-miss schedule* and the *absence of an ingestion boundary* for non-prose furniture.

---

## 11. Recommended next moves (rules and math only)

Ordered by expected value:

1. **Close OI-5 with this trace.** Write the measured frequencies into W3a: AM-2 = 20.9% of candidates (≈71% of keeps), AM-3 = 155, AM-9 observed (4 wrong R2.1 fires). The "unmeasured" era is over; the schedule is falsified for technical prose and W3a should say so.
2. **Decide OI-2 with data.** Scoping R1.2/R1.3 to `.`-only trades the AM-2/AM-3 mass for AM-8 expansion (`NASA? We…`, `What is 5? Ten.`). The measured volumes make this a genuine design decision: 2,686 + 155 keeps on one side, the AM-8 class on the other.
3. **Widen OI-1 into one enumerator/label rule** covering the measured family: multi-digit numerals, `(a)`-style part labels, `Q16a`/`M3`-style question keys. One rule, one layer, one audit row — closes 47 orphan splits + ~206 part-label merges + list glue.
4. **Add an L3 namespace guard.** Entries colliding with element symbols (`ca`, `no`, `cf`, `mt`), SI units (`ms`, `s`, `A`, `V`, `K`, `T`, `W`), or high-frequency verbs (`sat`) require corpus evidence of the honorific/date sense before admission. Current wounds: 4 of 7 R2.1 fires.
5. **Open a new issue for the em-dash consequence of ruling (d)** (§7 above): declare it an AM row, or amend T3 to treat a terminator followed by an em dash like an opening mark. It must not remain implicit.
6. **Make the D1/D12 furniture decision** (§8): markdown/table/diagram boundaries are either stripped upstream or recognized at the block layer. Biggest chunk-hygiene lever; not a suppression-rule change.
7. **Reconcile the implementation to v1.2** (§9) before the next eval so the trace's rule citations are audit-meaningful, and the L5-violating toggle is removed.

---

## Appendix A — Trace line format

```
DECISION RULE     @offset  ...context...
```

- `DECISION`: SPLIT or KEEP.
- `RULE`: the rule ID the implementation cited (subject to the citation drift in §9.7 — the spec's governing-rule citations would differ in some rows, never the outcome).
- `@offset`: character position in `prose-corpus.md` of the split point (end of terminator cluster + decoration).
- `context`: ±25 characters around the candidate, newlines shown as spaces; the candidate's terminator is at character 25 of the context (block-start candidates are truncated on the left).

## Appendix B — Count provenance

| Figure | Provenance |
|---|---|
| Rule totals (§2) | exact: aggregation over all 12,862 trace lines |
| Chunk counts (§2) | exact: splitter output over the corpus |
| Dotted-abbrev occurrences (§3) | exact: pattern count over `prose-corpus.md` |
| Unit/digit/point-label keeps (§3) | lower bound: regex-visible subset of trace contexts |
| Orphan labels (§4) | exact: chunks matching `^\d{1,3}\.$` |
| Part-label keeps (§4) | sampled: 14 of 206 examined, all `(b)/(c)` class except one |
| R2.1 fires (§6) | exact: all 7 individually examined |
| Em-dash class (§7) | upper bound: context-window pattern matches |
| Furniture classes (§8) | exact: pattern counts over chunk output |
