# The Suppression Specification
### v1.0 -- drafted to be unambiguous: definitions, laws, rules, precedence, examples, and an interpretation index
Companion to `precision-first-split-theory.md` and `why-not-to-split.md`. Contains no code by design.
Stable IDs (D-, T-, C-, R-, DL-, W-, AM-, CI-) are citable. Nothing may be considered "implied" -- if it is not written here, it is not part of the specification.
Version: THIS IS AN UNPROVEN FILE AND IS NOT FINAL. DO NOT TAKE ANYTHING THAT'S NOT STATED TO BE CLOSE TO FUNCTIONAL, AS FUNCTIONAL. 
---

## §0. Rules of construction (how to read this document)

0.1 "Immediately" means: with no intervening token and no intervening whitespace.
0.2 "Before"/"after" refer to positions in the token stream (T3), not to visual layout.
0.3 Set membership tests against lexicons are **case-insensitive** unless a rule says otherwise.
0.4 Where this document gives a rule an ID, later sections cite rules by ID only.
0.5 If two rules could both apply, §DL2 decides which one governs. No reading of one rule may contradict §DL2.
0.6 The words "must", "may", and "cannot" are used in their strict senses. "May" marks discretion; everything else is mandatory.
0.7 A "ruling" in §7 is an application of the rules to an example. Rulings are illustrative; the rules govern.

---

## §1. Definitions

**D1 -- Text.** The input: a finite string of Unicode characters in English prose.

**D2 -- Character classes.**
- *Whitespace*: space, tab, line feed, carriage return, non-breaking space, and any character with the Unicode `White_Space` property.
- *Letter*: any character with Unicode general category L* (includes accented letters: š, č, é).
- *Digit*: any character with Unicode category Nd.
- *Uppercase*: a letter with the Unicode Uppercase property. "Lowercase letter" = a letter that is not uppercase.

**D3 -- Punctuation Set** (exhaustive, closed):
`. ! ? , ; : ( ) [ ] { } " “ ” " „ » « – -- …`
**Explicitly NOT in the Punctuation Set** (therefore word characters):
- the apostrophes `'` and `’` (so `don't` is ONE word token -- see AM-1);
- the hyphen `-` (so `well-known` is ONE word token);
- every other character not listed above (so `10⁻³`, `×`, `°C` are word characters).

**D4 -- Word token.** A maximal run of consecutive characters, none of which is whitespace or in the Punctuation Set. A word token may contain letters, digits, apostrophes, hyphens, underscores, and symbols.

**D5 -- Punctuation token.** Exactly one character of the Punctuation Set, standing as its own token.

**D6 -- Single-character token.** A word token of length exactly 1.

**D7 -- All-caps run.** A word token that (a) contains at least two letters, (b) contains no lowercase letter, and (c) contains at least one uppercase letter. Digits are tolerated (`COVID19`, `HTML5` qualify). A token with no letters (`1995`, `×`) is not an all-caps run.

**D8 -- Terminator.** A punctuation token whose character is `.`, `!`, `?`, or `…`.

**D9 -- Decoration.** A maximal run of punctuation tokens immediately after a terminator, drawn only from: `" ” ' ) ] } »`. Decoration stops at the first token not in that set.

**D10 -- Candidate.** A terminator followed (after any Decoration) by whitespace or by end-of-block (D12). Nothing else is a candidate. `9.81`, `example.com`, `v2.1.3` produce **no** candidate, because their periods are not followed by whitespace (R0.1).

**D11 -- Terminator cluster.** A maximal run of terminator tokens with no whitespace between them (`...`, `?!`, `!!`, `…?`, `."` -- the closing quote joins via D9). The cluster is governed as ONE candidate. **Cluster classification:** a cluster is an *ellipsis cluster* if it contains `…` or two or more `.` tokens; otherwise it is a *strong cluster* (governed by the class of its last token: `!`, `?`, or `.`).

**D12 -- Block.** A maximal run of text containing no blank line (two or more consecutive newlines) and no markup block boundary (in HTML sources: no `<h1>–<h6>`, `<li>`, `<td>`, `<p>`, `<div>` boundary after tag-stripping). A single newline inside a block is ordinary whitespace, NOT a block boundary.

**D13 -- End-of-block.** The position after the last character of a block (or of the text). Every end-of-block is a split position by DL3; candidacy is not required there.

**D14 -- "Sentence end."** Deliberately NOT defined. This specification does not define what a sentence is; it defines a procedure whose outputs are intended to be a subset of the positions a competent human editor would mark as sentence ends when preparing prose for text-to-speech reading. The Guarantee Clause (§8) is stated against that standard.

**D15 -- Lookahead window λ.** Exactly 3 word tokens after the Decoration of the candidate under consideration. No rule inspects anything beyond λ.

**D16 -- Quote parity.** A counter over the stream, incremented/decremented by the double-quote characters `" " „ « »` only (apostrophes excluded by D3). The counter starts at 0 (outside). At a candidate, parity is *open* if the count of quote characters before it is odd, *closed* if even. Brackets/parentheses do NOT affect parity. Limitation, declared: quotations marked with single quotes are invisible to parity (accepted risk, see AM-7).

---

## §2. Tokenization law

**T1.** The text is converted into a sequence of word tokens (D4) and punctuation tokens (D5), in order, losslessly. Tokenization is deterministic and performed ONCE, before any rule runs.

**T2.** No rule may re-tokenize. Rules operate on the token stream only.

**T3.** "Pre-candidate token" = the word or punctuation token immediately before the terminator cluster. "Following token" = the first word token after the Decoration. "Effective initial" of the following token = its first character that is a letter or digit, skipping any opening quotes/brackets (`“ " « ‘ (`) at its start; if none exists, the effective initial is "none".

**T4.** (Worked tokenizations, binding:) `U.S.A.` → `U` `.` `S` `.` `A` `.` · `e.g.` → `e` `.` `g` `.` · `don't.` → `don't` `.` · `9.81` → `9` `.` `81` · `(NLP).` → `(` `NLP` `)` `.` · `...` → `.` `.` `.` · `J. K. Rowling.` → `J` `.` `K` `.` `Rowling` `.`

---

## §3. Decision law

**DL1 -- Default decision.** For every candidate: **SPLIT**, unless a suppression rule (§4) fires for it.
**DL2 -- Order and exclusivity.** Suppression rules are evaluated in the order R0.1 → R0.2 → R1.1 → R1.2 → R1.3 → R2.1 → R3.1 → R3.2 → R4.2. The FIRST rule whose trigger matches ends evaluation: the candidate is suppressed (decision KEEP). No rule may un-suppress another's suppression. Rules never act except to suppress; only DL3 overrides.
**DL3 -- Block-edge override.** At end-of-block (D13): SPLIT unconditionally. No suppression rule applies there, regardless of terminator presence, lexicon state, quote parity, or anything else. This is the only override in the specification.
**DL4 -- Revisability.** A KEEP is provisional and may be revised by later text. A SPLIT is final. (Streaming clause: the algorithm may delay evaluating a candidate until λ tokens exist beyond it; delay is a KEEP, never a SPLIT.)
**DL5 -- Capital condition.** The default decision's SPLIT is contingent on the effective initial (T3) of the following token being an uppercase letter. If the effective initial is a lowercase letter, a digit, "none", or anything else, the decision is KEEP. (R3.1 is this contingency restated as a suppressor for clarity; they are the same test.)

---

## §4. The suppression rules

### Layer 0 -- Structure

**R0.1 -- Candidacy.** Only positions satisfying D10 are candidates. A period NOT followed by whitespace is not a candidate and never reaches any other rule.
*Absorbs:* `9.81`, `example.com`, `v2.1.3`, `10⁻³.5`, times, file names -- before any decision exists.

**R0.2 -- Cluster normalization.** A terminator cluster (D11) is ONE candidate. A dot-run (`...`) or any cluster containing `…` is an ellipsis cluster and is routed to R4.2. A strong cluster is adjudicated by its last token's class; `!` and `?` follow exactly the same rules as `.` (there is no special exclamation logic anywhere in this specification).

### Layer 1 -- Shape (no memory; generalizes to unseen words)

**R1.1 -- Internal period (adjacent).** Suppress if the pre-candidate token is a word token AND the token immediately after the terminator is a word token (both adjacent, no whitespace, no decoration between). This covers `U.S.A`, `Ph.D`, and both dots of `e.g.`
*Misreading guard:* R1.1 does NOT apply across whitespace. `J. K. Rowling` is handled by R1.2, not R1.1.

**R1.2 -- Single-character pre-token.** Suppress if the pre-candidate token is a single-character token (D6) -- letter OR digit. This covers initials (`J.`), list letters (`a.`), units (`5 A.`), single digits (`Figure 2.`), and the final dot of `U.S.` and `e.g.`
*Accepted consequences (see §7 schedule):* true boundaries after words like `A` or `I` (`taller than I.`) are suppressed -- a missed split, never a false one.

**R1.3 -- All-caps run.** Suppress if the pre-candidate token is an all-caps run (D7): `NASA.`, `IEEE.`, `COVID.`
*Misreading guard:* a token containing any lowercase letter (`PowerPoint`, `iPhone`) does NOT qualify. Roman numerals (`Chapter IV.`) DO qualify -- accepted miss (AM-3).

### Layer 2 -- Lexicon (the shape-blind spots)

**R2.1 -- Set P (never-final).** Suppress if the pre-candidate token matches, case-insensitively, an entry of the static set P. Set P contains plain-looking words that conventionally act as abbreviations and are **never** sentence-final:
`dr, mr, mrs, ms, prof, gen, sen, capt, sgt, lt, col, rev, hon, st, mt, ft, vs, ca, cf, pp, fig, eq, ch, sec, no, approx, dept, univ, assn, bros, inc*, jan, feb, mar, apr, may, jun, jul, aug, sep, sept, oct, nov, dec, mon, tue, tues, wed, thu, thur, thurs, fri, sat, sun, e.g, i.e, etc*, et al, n.b, …` (asterisked entries see R2.2 note)
*Ruling consequence:* `St. James`, `Dr. Smith arrived.`, `vs. The outcome`, `Jan. 5th` -- all suppressed at the first period, even before a capital.
*Misreading guards:* (a) R2.1 fires regardless of what follows -- the continuation cannot rescue the candidate; (b) R2.1 does NOT apply at end-of-block (DL3 outranks it: a paragraph ending `…Dr Smith's house.` still splits).

### Layer 3 -- Right context

**R3.1 -- Lowercase continuation.** Suppress if the effective initial (T3) of the following token is a lowercase letter. This is the lowercase face of DL5. Never is a split placed before a lowercase continuation.
*Absorbs:* `…bread, etc. and milk` (with R2.1 also already fired), `"…over." he said`, `…Inc. was founded`.

**R3.2 -- Attribution pattern.** Suppress if ALL of: (a) quote parity (D16) is OPEN at the candidate; (b) one of the following holds within λ (D15) word tokens after the Decoration:
  (i) the first following word token ∈ speech-verb lexicon (`said, asked, replied, answered, shouted, whispered, muttered, exclaimed, cried, continued, began, added, wrote, noted, explained`), or
  (ii) the first is a lowercase personal pronoun (`he, she, it, they, we, you, i`) AND the second ∈ speech-verb lexicon.
*Absorbs:* `"Stop!" he said.`, `"…the end," said John, "for now."`, `"What?" asked the teacher.`
*Misreading guards:* (a) a CAPITALIZED pronoun followed by a speech verb does NOT fire this rule -- `"It is over." He said nothing.` splits after the quote (ruling 7.13; the capitalized form is standard prose for a new sentence); (b) if parity is closed or unknown, R3.2 cannot fire; (c) name attributions (`"…" said John` -- verb-first) fire; (`"…" John said` -- name-first) do NOT -- declared limitation, AM-6.

### Layer 4 -- Policy

**R4.2 -- Ellipsis.** Suppress every ellipsis cluster (D11 classification), wherever it occurs inside a block. An ellipsis is a pause, not a terminator.
*Accepted consequence:* `It was over… A new era began.` stays merged (AM-4). DL3 still splits at the block edge.

*(There is no digit rule, no exclamation rule, no F/"final-capable" set. Single digits die at R1.2; `!`/`?` adjudicate identically to `.`; a final-capable abbreviation that looks like a plain word -- `etc. We left.` -- splits by DL1 with no lexicon help. The lexicon in this specification only ever SUPPRESSES; it never licenses. This is deliberate: one mechanism, fewer contradictions.)*

---

## §5. Lexicon law

**L1.** Set P (R2.1) is static, finite, versioned, and shipped with the algorithm. Each entry is one word, no periods (periods are tokenized away), stored lowercase.
**L2.** The speech-verb and pronoun lists (R3.2) are static and versioned under the same discipline.
**L3 -- Extension protocol.** An entry may be added only with: (a) the word; (b) which list; (c) one real example sentence where its absence produced a wrong decision; (d) a check that the word is not a common sentence-final plain word (`the, is, was…` are forever excluded). Each addition is one auditable row. Removal follows the same protocol in reverse.
**L4.** No entry may carry a "license" or "permit-split" flag. If a future amendment wants one, it is a new rule (§4 amendment), not a lexicon flag -- rules and data stay separate.

---

## §6. The three doors

Under this specification a false split can pass ONLY through:
- **Door A -- P omission:** an unknown plain-shaped abbreviation before a capital (`…the prof. The lecture…`). Repair: one P row (L3).
- **Door B -- attribution gap:** an attribution form outside R3.2's two patterns and quote parity's reach (AM-6, AM-7). Repair: extend the pattern lists, never the rule's logic.
- **Door C -- tokenization defect:** text where D3/D4 mis-segment (unusual unicode, markup leakage). Repair: T-law amendment.
Everything else is closed by construction. This enumeration is the spec's central warranty claim and is deliberately falsifiable.

---

## §7. Worked rulings (binding applications)

| # | Text | Ruling | Governing rules |
|---|---|---|---|
| 7.1 | `The value is 9.81 m/s². The test…` | no candidate at `9.81`; SPLIT after `².` | R0.1, DL1+DL5 |
| 7.2 | `See example.com for details. We…` | no candidate in domain; SPLIT after `details.` | R0.1, DL1 |
| 7.3 | `She earned her Ph.D. The committee…` | first dot R1.1; second dot R1.1 (`D` adjacent? -- yes, `Ph.D.`); SPLIT after `D.`? -- NO: second dot has `The` after whitespace, pre-token `D` is single-character → R1.2 → KEEP (AM-2) | R1.1, R1.2 |
| 7.4 | `Dr. Smith arrived. He sat.` | KEEP after `Dr.` (R2.1); SPLIT after `arrived.` | R2.1, DL1 |
| 7.5 | `St. James's Park is old. It…` | KEEP after `St.`; SPLIT after `old.` | R2.1, DL1 |
| 7.6 | `J. K. Rowling wrote it. More…` | KEEP, KEEP (R1.2 ×2); SPLIT after `it.` | R1.2, DL1 |
| 7.7 | `I don't. You do.` | SPLIT after `don't.` -- `don't` is ONE token (D3), not single-character | DL1, D3 |
| 7.8 | `"Stop!" he said. Then…` | KEEP after `!` (R3.1 lowercase); SPLIT after `said.` -- wait: `said.` pre-token `said` plain, `Then` capital → SPLIT ✓ (the quoted sentence and attribution travel as one chunk) | R3.1, DL1 |
| 7.9 | `"Stop!" He left.` | parity OPEN at `!`, following is capitalized pronoun only -- pattern (ii) needs a speech verb within λ: `left` ∉ verbs → no suppression → SPLIT after `!` + decoration. Ruling: SPLIT (declared: quoted fragment + new sentence) | R3.2 guards, DL1 |
| 7.10 | `"It is over." He said nothing.` | as 7.9 -- SPLIT after `."` | R3.2 guard (a) |
| 7.11 | `"What?" asked the teacher. Nobody…` | KEEP after `?"` (R3.2 (i): `asked` verb-first, parity open); SPLIT after `teacher.` | R3.2, DL1 |
| 7.12 | `We bought bread, etc. Then we left.` | SPLIT after `etc.` -- `etc` plain-shaped, `Then` capital, no suppressor fires | DL1+DL5 |
| 7.13 | `We bought bread, etc. and milk.` | KEEP after `etc.` | R3.1 |
| 7.14 | `The treaty followed in 1995. It held.` | SPLIT after `1995.` -- multi-character, not all-caps, not in P | DL1+DL5 |
| 7.15 | `The current reached 5 A. The voltage…` | KEEP after `A.` (R1.2) -- missed split, accepted | R1.2, AM-2 |
| 7.16 | `Chapter IV. The next chapter…` | KEEP after `IV.` (R1.3) -- missed split, accepted | R1.3, AM-3 |
| 7.17 | `It was over… A new era began.` | KEEP after `…` (R4.2) -- missed split, accepted | R4.2, AM-4 |
| 7.18 | `…uses natural language processing (NLP). We…` | the `)` is not a terminator; the period after `)` is the candidate, pre-token `)` is punctuation (not single-character word token, not in P, not all-caps) → SPLIT | DL1, R1.2 scope |
| 7.19 | `…signed in the U.S. The Senate adjourned.` | KEEP after `U.S.` (R1.2 on `S`) -- the famous ambiguity absorbed as a missed split, never a false one | R1.1, R1.2 |
| 7.20 | `…in the U.S. Senate adjourned early.` | same -- KEEP (identical features, identical ruling; see D14 note) | R1.2 |
| 7.21 | `Wait… what happened next. Nobody knows.` | KEEP after `…` (R4.2); SPLIT after `next.` | R4.2, DL1 |
| 7.22 | `NASA was founded. Later…` | SPLIT after `founded.`; the token `NASA` mid-sentence never matters | DL1 |
| 7.23 | `He is taller than I. Others disagree.` | KEEP after `I.` (R1.2) -- missed split, accepted | R1.2, AM-2 |
| 7.24 | `Prices rose 5. The next year…` | KEEP after `5.` (R1.2 single digit) | R1.2 |

---

## §8. Guarantee clause

**W1 -- Warranted.** Every SPLIT emitted inside a block satisfies: candidacy (D10) + no suppression rule fired (§4, in DL2 order) + uppercase effective initial (DL5). Every SPLIT at end-of-block satisfies DL3. Subject to §6's doors staying shut, no SPLIT is placed at a non-sentence-end (D14 standard).

**W2 -- Not warranted (recall).** This specification does NOT promise to find every sentence end. The following missed splits are accepted BY DESIGN and are not defects: AM-1 through AM-7 below.

**W3 -- The accepted-miss schedule.**
- **AM-1** -- none (contractions are safe by D3; listed for completeness of the class it prevents).
- **AM-2** -- true boundary after a single-character word or digit (`than I.`, `5 A.`, `Figure 2.`), because R1.2 suppresses all single-character pre-tokens. Cost: merged chunks. Frequency: low.
- **AM-3** -- true boundary after all-caps runs and Roman numerals (`Chapter IV. The…`) -- R1.3. Frequency: low; matters in numbered/classical texts.
- **AM-4** -- true boundary at an ellipsis (`over… A new era`) -- R4.2. Frequency: low.
- **AM-5** -- `U.S.`-class trailing ambiguity before capitals (7.19/7.20) -- R1.2. This is Layer E of the catalogue, absorbed in the safe direction.
- **AM-6** -- name-first attributions with closed parity (`"…" John said`) may split early -- Door B. Declared limitation.
- **AM-7** -- single-quoted dialogue is invisible to parity (D16) -- Door B. Declared limitation.

**W4 -- Failure protocol.** When a false split is observed in the wild: identify which door (§6) it passed through; apply exactly one repair (one P row / one pattern-list extension / one T-law fix); record it in the lexicon's audit trail. Threshold-tuning, per-document hacks, and multi-rule rewrites are PROHIBITED as responses to single failures.

---

## §9. Interpretation index ("this specification does NOT mean…")

- **CI-1:** It does NOT mean every `word. Capital` splits. Layer 2 and Layer 3 exist precisely to stop some of them.
- **CI-2:** It does NOT mean abbreviations need a dictionary to be safe. Shape (Layer 1) suppresses unseen abbreviations; the dictionary only patches what shape cannot see.
- **CI-3:** It does NOT mean the lexicon ever causes a split. Under this specification the lexicon only suppresses (§4 note; L4).
- **CI-4:** It does NOT mean `!` and `?` behave differently from `.` -- there is no exclamation-specific logic anywhere (R0.2).
- **CI-5:** It does NOT mean block edges need terminators. DL3 is unconditional.
- **CI-6:** It does NOT mean KEEP decisions are errors. Under W2, a KEEP is a legitimate outcome; only a false SPLIT is a defect.
- **CI-7:** It does NOT mean whitespace variants (double space, newline, NBSP) change any ruling. All whitespace is equivalent (D2); the double-space convention is deliberately ignored.
- **CI-8:** It does NOT mean the decision depends on sentence length, grammar, or meaning. Every rule is a function of local token shape, two static lists, and at most λ=3 tokens of right context.
