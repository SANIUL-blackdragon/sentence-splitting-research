# unslop structural report v1

**Lens:** the unslop skill (30 rules with stable IDs) applied as a detection instrument to the splitter's output stream.
**Object:** the 22,257 reading chunks implied by `corpus_trace.v1.txt` (17,535 blank-line block tails + 4,722 in-block DL1+DL5 pieces), rebuilt from `prose-corpus.md`.
**Method:** direct read of the opening region, chars 0 to 11,500 (177 chunks, the region quoted in chat), plus a whole-stream census of every rule that can be counted, plus attribution of every mid-chunk full stop back to its trace decision.
**Scope note:** unslop is an editing skill (scan, then rewrite). This corpus is read-only research material, so the rewrite step is replaced by measurement and by an ownership verdict. Nothing in the repo was rewritten.
**Notation:** `‖` marks a chunk boundary the splitter emits; `¶` marks a chunk boundary inherited from the source's blank lines. All counts are measured on the full stream unless stated as samples.

---

## 1. The headline

The stream passes every lexical slop rule and fails the structural ones. The corpus is human exam prose. The output is structurally slopped, and the splitter manufactures most of it.

| unslop rule | Measured | Reading consequence |
|---|---|---|
| 28 dense sentences, reader must backtrack | 1,788 chunks carry at least one mid-chunk full stop; 3,052 glued boundaries total | two or more sentences spoken as one breath |
| 33 over-compression, verbless fragments, symbol-speak | 13,193 chunks (59.3%) end with no `. ! ? …` terminator under the strict definition (see 5.1) | the listener hears fragments with no prosodic close |
| 17 title case headings | 2,041 marker headings are emitted as literal text | the listener hears "hash hash hash, 1, Wave Properties" |
| 18 decorative emojis | 117 chunks contain UI glyphs (☰ 🌙 📊 ✕ ☽ ☾ ✓ □ ▼ ▲); 39 chunks are exactly one character | the listener hears UI chrome |
| 3 superficial -ing openers | 521 chunks open on a gerund | "Forgetting to square...", "Stating the formula...", spoken as sentence starts |
| 5 vague attributions | 338 chunks say "students" | "Students who skip the check..." as the whole attribution |
| 14 colon overuse | 6,207 chunks (27.9%) contain a colon; 7,275 total | label-register spoken mid-stream |
| 13 em dash overuse | 2,897 chunks (13.0%) carry at least one of 3,184 em dashes | source style, not splitter damage |
| 7 AI vocabulary | 2 hits in the whole stream | clean |
| 20, 22, 23, 24, 31 chatbot, sycophancy, filler, hedging, fancy synonyms | 1 incidental, 0, 2, 0, 0 | clean |
| 12 false ranges | 238 "from X to Y", sampled: all literal scales | clean |

Ownership splits cleanly. Section 7 gives the two-column verdict: what the splitter manufactures, what the source owns, what only a TTS layer can fix.

---

## 2. What the listener hears

### 2.1 The index (chars 0 to 1,300)

The first 21 chunks are a truncated question index. Each is one block, each ends on an ellipsis, each is spoken alone:

> Q1 DER Show that the critical angle C for total…
> Q2 GRD A ray of light travels from a glass block…
> Q3 DER A diffraction grating has slit spacing d…

Twenty-one utterances that all end on "dot dot dot". No TTS voice closes them. The splitter cut them correctly at block edges (DL3, the one license that never misfires); the source wrote them as teasers. Inherited, not manufactured.

### 2.2 The progress tracker (telegraphese)

The source's stat card flattens into paired fragments that the stream reads in scrambled order:

> ¶ Progress Tracker
> ¶ ## Exam Readiness Questions
> ¶ Ch 2.3 — Waves and Light · WPH12
> ¶ Pearson Edexcel IAL
> ¶ 20
> ¶ Questions
> ¶ 110
> ¶ Marks
> ¶ 160
> ¶ Minutes

The listener hears "20. Questions. 110. Marks. 160. Minutes." The number and its noun are separated chunks. Source-owned: the HTML card was flattened at extraction. Rule 33 debris either way.

One chunk here carries an extraction defect: the source text literally contains "Tier 1 — FoundationIf you can't answer these instantly" with no space at the glue point. The file has 9 such camelCase junctions (ionAppl, putTota, terIint and siblings). The splitter cannot split what extraction welded. Source-owned.

### 2.3 The marking block you pasted (chars 6,000 to 6,700)

This is the passage from your message, rendered as the stream emits it, with the trace rows attached:

> ¶ Marking Points
> ‖ M1 The maximum possible diffraction angle is θ = 90° (light travelling parallel to the grating).
> ‖ At this limit, sin θ = 1. Substituting into the grating equation: nλ = d × 1 = d.
> ‖ M2 Rearranging: nₘₐₓ = d/λ.
> ¶ Since n must be an integer and sin θ cannot exceed 1, the value is rounded down to the nearest whole number. ✓
> ¶ M3 d = 1/(300 × 10³) = 3.33 × 10⁻⁶ m. Then d/λ = 3.33 × 10⁻⁶ / (590 × 10⁻⁹) = 5.65.
> ‖ M4 Only whole-integer values of n produce visible maxima.
> ‖ The 6th order (n = 6) would require sin θ = 6λ/d = … which is greater than 1 and therefore impossible.
> ¶ So the highest visible order is n = 5.
> ¶ NOT Accepted

Line by line:

- The second ‖ chunk is your `KEEP R1.2 @6095` row. "At this limit, sin θ = 1." ends a sentence. The single-character pre-token `1` vetoed the split, so two sentences share one breath. Rule 28, manufactured.
- The ¶ chunk ending "…whole number. ✓" closes on a checkmark glyph. Rule 18 debris as a prosodic ending.
- The M3 chunk glues the setup and the arithmetic into one utterance (`M3 d = 1/(300 × 10³) = 3.33 × 10⁻⁶ m. Then d/λ…`, your `KEEP R1.2 @6330` row). Rule 28 again, manufactured.
- "¶ NOT Accepted" is a verbless label chunk. Rule 33.
- Note the rhythm damage: M1, M2, M4 each get a clean breath, the model answers around them do not. The mark-scheme cadence the author designed (label, then reason, then verdict) survives only in fragments.

### 2.4 The summary table (flattened)

The source's real HTML table became prose-shaped lines, so the stream reads:

> ¶ Wave properties (longitudinal waves, intensity) Q6–Q7 14 18 min

Nine data points, zero prosody, one breath. There are 156 multi-pipe lines in the file but zero true pipe tables; extraction flattened the real ones (156 lines are Hess cycles, wavefronts and absolute values). Source-owned at extraction, unsplittable by rules after that.

---

## 3. Run-on forensics (rule 28, manufactured)

Every mid-chunk full stop followed by a capital, digit or quote is a boundary a listener should have heard. There are 3,052 of them inside 1,788 chunks. Attribution to the trace decision that sits on the glue point:

| Cause (trace rule) | Glued boundaries | Share |
|---|---:|---:|
| KEEP R1.2 (single-char veto) | 2,155 | 70.6% |
| KEEP DL5 (fall-through) | 579 | 19.0% |
| KEEP R1.3 (caps/internal-period) | 147 | 4.8% |
| KEEP R3.1 (lowercase continuation) | 142 | 4.7% |
| KEEP R4.2 (ellipsis cluster) | 18 | 0.6% |
| KEEP R2.1 (Set P) | 7 | 0.2% |
| no logged keep (extraction glue) | 4 | 0.1% |

This matches the census in trace-analysis.1.md §4.1 from the reading side: the R1.2 mass (2,021 adjudicated false merges there, 2,155 boundary-adjacent attributions here under a looser ±4-char match) is the same population seen as prose damage instead of as decisions. The reading lens and the decision lens agree on the culprit.

Worst heard-aloud examples, verbatim:

> tron is accelerated through a potential difference of 1 volt. 1 eV = 1.60 × 10⁻¹⁹ J. Electronvolts are convenient…
> This remains one of the most frequent errors: students see "electron" and instinctively reach for 1.60 × 10⁻¹⁹ C. The de Broglie equation…
> The graph is sinusoidal with amplitude 1.5 × 10⁻⁶ m and wavelength 0.68 m. The speed of sound in air is 340 m s⁻¹.

Each is one emitted chunk. Each is two or three sentences.

---

## 4. The fragment economy (rule 33, mostly manufactured)

### 4.1 Definitions matter here

Strict definition (this report): the chunk's last character is none of `. ! ? …` or a quote or bracket that closes one of those. Under that rule 13,193 of 22,257 chunks (59.3%) end without a sentence terminator. The earlier audit in trace-analysis.1.md §6 counted 10,492 (47.1%) because it also accepted a bare `)` or `"` as a terminator; the 2,701 gap is exactly chunks that end on an unclosed parenthesis or similar. Earlier variants ranged from 6,229 to 8,668 depending on whether heading and label chunks were excluded. All definitions agree the mass is between 28 and 59 percent of the stream. The listener hears no closure on roughly every other utterance.

### 4.2 The composition

- 39 chunks are exactly one character (`× B B B N ☰ ☰ ☽ ☾ ↓`). Spoken alone, each is a syllable of noise.
- 3,466 chunks contain at least one `=`; the pure-arithmetic ones ("= 5.65.", "(I/2).") are spoken as verbless equations.
- 11 chunks end on the "(2 s.f.)" pattern.
- 2,071 chunks open on `#` markers; the listener hears the markup.

### 4.3 Who owns it

The block layer manufactures the bulk: 89.6 percent of terminator-less chunks are born as blank-line block tails before any rule fires (trace-analysis.1.md §6.2). The keep-refusals contribute 6.5 percent, logged splits 3.9 percent. The source contributes the flattened tables, the label lines and the UI chrome that feed that layer.

---

## 5. The rules the corpus passes (lexical)

For completeness, the clean bill:

- Rule 7 AI vocabulary: 2 hits in 22,257 chunks.
- Rule 8 fancy "is": 0. Rule 9 "not just X but Y": 2. Rule 20 chatbot phrases: 1 incidental ("certainly" in literal use). Rule 22 sycophancy: 0. Rule 23 filler: 2. Rule 24 hedging: 0. Rule 31 fancy synonyms: 0.
- Rule 26 metaphor nouns: 3 hits, none metaphorical ("vector" appears 4 times as the literal physics quantity).
- Rule 12 false ranges: 238 candidates, sampled 6, all real scales ("from Tier 1 to Tier 3", "from 60° to 30°", "from eV to joules").

Verdict: nobody slopped the text. The source register is dense, imperative and exam-flavored, and it is human. Every tell in the stream is structural, and structural tells are what a splitter either prevents or manufactures.

---

## 6. The register rules (source-owned, TTS-relevant)

These would survive a perfect splitter, because the author wrote them:

- Rule 3, gerund openers: 521 chunks begin with a gerund (Using 60, Marking 52, Forgetting 33, Saying 25, Confusing 24, Writing 21, Stating 18, Adding 13). This is mark-scheme grammar: "Forgetting to square the speed of light. Award M0." A TTS voice renders it as a dangling participle.
- Rule 5, "students" as the agent: 338 chunks. Exam-register attribution, repeated until it drones.
- Rule 14, colons: 6,207 chunks carry one. The label register ("Answer:", "Marking Points:", "Common error:") is legitimate list punctuation by unslop's own carve-out, but in speech it lands as a pause with no payload.
- Rule 13, em dashes: 3,184 in the source, 99.3 percent spaced, 2,897 chunks affected. Most are UI chrome and title punctuation ("Ch 2.3 — Waves and Light"). A TTS normalization pass, not the splitter, owns these.
- Boilerplate loops: "marks" appears 1,712 times, "mark scheme" 326, "Explain why" 165, "State the" 150, "Show that" 72, "past papers" 30, "bald answer" 13. The stream loops the same frames for hours.

---

## 7. Structural dimensions unslop does not name

The skill audits prose. A speech stream fails in ways prose does not, and the census caught three:

1. **Opener monotony.** Chunk-initial word census: `The` 1,181, heading markers 2,020 across `####`/`###`/`#####`, `Answer`/`Answer:` 893, `A` 363, `Spec` 308, `This` 300, `Jun` 269 (chunks beginning with a past-paper month reference, spoken cold), `↳` 250, `1` 235. A listener hears the same seven openings forever.
2. **Rhythm collapse.** Median chunk is 58 characters, about ten words, roughly four seconds of speech. When roughly every other burst ends without terminator (section 4.1), the stream has no phrase-level prosody at all. It is a wall of four-second tiles.
3. **Pairing destruction.** The source's layout pairs (number with noun, label with value) become adjacent chunks read in scrambled order (section 2.2). Splitting preserves sequence, not association.

---

## 8. The ownership verdict

| Finding | Owner | Fix lives in |
|---|---|---|
| 2,155 run-on boundaries on single-char keeps | splitter (R1.2) | trace-analysis.1.md §11.2, the two-sided R1.2 redesign |
| 579 run-ons on fall-through keeps | splitter (DL5 path) | §11.2 split-side license for digits and units |
| 289 run-ons on R1.3/R3.1/R2.1/R4.2 keeps | splitter | §11.3, §11.4, §11.5 |
| 59.3 percent terminator-less chunks, 89.6 percent of them born at block tails | ingestion layer (D1/D12) | §11.1, the furniture boundary |
| "hash hash" heading speech, glyph debris, one-character chunks | ingestion + TTS presentation | strip markers and expand glyphs at the audio layer |
| 21 ellipsis index lines, telegraphese cards, flattened tables, 9 glue artifacts, "FoundationIf" | source extraction | corpus regeneration with heading-aware extraction |
| Gerund openers, "students" agent, colons, em dashes, boilerplate loops | source register | optional TTS style pass; out of scope for splitting |

The unslop lens lands on the same verdict the decision-level audit reached, from the opposite direction. trace-analysis.1.md measured the rules and found the stack mis-calibrated. This report read the output as prose and found the same three culprits: R1.2 manufactures rule-28 run-ons, the block layer manufactures rule-33 fragments, and the source supplies the register. The architecture is innocent. The calibration and the missing ingestion boundary are guilty, and they are the same two suspects both audits keep arresting.

---

## Appendix: reproducibility

Chunk stream rebuilt exactly as in trace-analysis.1.md §2.3: blocks on `\n{2,}`, in-block cuts at the 4,722 DL1+DL5 offsets, chunk count 22,257 verified. Census run over the collapsed stream with the regexes named inline; run-on attribution by nearest logged keep within ±4 characters of each internal boundary; region transcript covers chars 0 to 11,500 (177 chunks) and is the basis of section 2. Counts in this report supersede prose-impression claims nowhere in trace-analysis.1.md; they are an independent second opinion that agrees.
