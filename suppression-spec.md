# The Suppression Specification

### v1.1 (draft) -- drafted for unambiguity: definitions, laws, rules, precedence, examples, and an interpretation index

> **STATUS: UNPROVEN AND NOT FINAL.** Nothing in this file may be treated as functional unless it is explicitly stated to have been shown to work.

Companion to `precision-first-split-theory.md` and `why-not-to-split.md`. Contains no code by design.

Stable IDs (D-, T-, DL-, R-, L-, W-, AM-, CI-, OI-) are citable and are never reused. A withdrawn ID stays in place as a marked stub so old citations still resolve. Nothing may be considered "implied" -- if it is not written here, it is not part of the specification.

The list of defects fixed in v1.1 is in §10.

---

## §0. Rules of construction (how to read this document)

0.1 "Immediately" means: with no intervening character (no token and no whitespace).

0.2 "Before"/"after" refer to positions in the token stream (T1), not to visual layout.

0.3 Set membership tests against lexicons are **case-insensitive** unless a rule says otherwise.

0.4 Where this document gives a rule an ID, later sections cite rules by ID only.

0.5 If two rules could both apply, DL2 decides which one is cited as governing. Because every rule only suppresses (DL2), this affects the citation, never the outcome.

0.6 The words "must", "may", and "cannot" are used in their strict senses. "May" marks discretion; everything else is mandatory.

0.7 A "ruling" in §7 is a **conformance vector**: an application of the rules to an example that an implementation must reproduce. If a ruling ever disagrees with the rules, that is a defect in this document, to be fixed by amendment; until it is fixed, the rules govern.

0.8 Withdrawn IDs (R1.1, R3.2, L2) remain as stubs. They have no force.

---

## §1. Definitions

**D1 -- Text.** The input: a finite string of Unicode characters in English prose. If the text originates from markup (e.g. HTML), block boundaries (D12) are detected on the markup *before* tags are stripped; stripping does not otherwise change the text.

**D2 -- Character classes.**

- *Newline*: LF, CR, or CRLF (each counts as one newline).
- *Whitespace*: space, tab, newline characters, non-breaking space, and any character with the Unicode `White_Space` property.
- *Letter*: any character with Unicode general category L* (includes accented letters: š, č, é).
- *Digit*: any character with Unicode category Nd.
- *Uppercase*: a letter with the Unicode Uppercase property.
- *Lowercase letter*: a letter with the Unicode Lowercase property. A letter with neither property (caseless letters, e.g. CJK) is neither uppercase nor lowercase.

**D3 -- Punctuation Set** (exhaustive, closed). Each of these characters is a punctuation token:

- `. ! ? , ; : ( ) [ ] { }`
- quotation marks `"` (U+0022), `“` (U+201C), `”` (U+201D), `„` (U+201E), `‟` (U+201F), `«`, `»`, and the single opening quote `‘` (U+2018);
- dashes `–` (U+2013) and `—` (U+2014);
- the ellipsis character `…` (U+2026);
- plus the two context-dependent cases D3a and D3b.

**D3a -- Apostrophes.** `'` (U+0027) and `’` (U+2019) are word characters **if and only if** they are immediately preceded AND immediately followed by a Letter or Digit (`don't`, `don’t`, `O'Brien` are ONE word token -- see AM-1). In every other position they are punctuation tokens (opening or closing single quotes, trailing possessives such as `dogs'`, initial elisions such as `'til`).

**D3b -- Dashes.** A maximal run of two or more hyphen-minus characters (`--`) is ONE punctuation token. This is the only punctuation token longer than one character. A single `-` is a word character (`well-known` is ONE word token).

**Not in the Punctuation Set** (therefore word characters): every other character, including `_`, `%`, `$`, `×`, `°`, and the superscripts in `10⁻³`.

**D4 -- Word token.** A maximal run of consecutive characters, none of which is whitespace or part of a punctuation token. A word token may contain letters, digits, word-internal apostrophes, single hyphens, underscores, and symbols.

**D5 -- Punctuation token.** Exactly one character of the Punctuation Set standing as its own token, or a hyphen run (D3b), or an apostrophe in a non-word-internal position (D3a).

**D6 -- Single-character token.** A word token consisting of exactly one Letter or exactly one Digit. (A lone symbol such as `%`, `×`, `-`, or `_` is not a single-character token.)

**D7 -- All-caps run.** A word token that (a) contains at least two letters, (b) contains no lowercase letter, and (c) contains at least one uppercase letter. Digits are tolerated (`COVID19`, `HTML5` qualify). A token with no letters (`1995`, `×`) is not an all-caps run.

**D8 -- Terminator.** A punctuation token whose character is `.`, `!`, `?`, or `…`.

**D9 -- Decoration.** A maximal run of punctuation tokens immediately after a terminator cluster (D11), drawn only from: `" ” ' ’ ) ] } »`. Decoration stops at the first token not in that set.

**D10 -- Candidate.** A terminator cluster (D11) that is followed, after any Decoration, by whitespace or by end-of-block (D13). Nothing else is a candidate. `9.81`, `example.com`, `v2.1.3` produce **no** candidate, because their periods are not followed by whitespace (R0.1).

**D11 -- Terminator cluster.** A maximal run of terminator tokens with no whitespace between them (`...`, `?!`, `!!`, `…?`). Decoration, if any, attaches after the cluster (`?!"`). The cluster is governed as ONE candidate. **Classification:** a cluster is an *ellipsis cluster* if it contains `…` or two or more `.` tokens; every other cluster is a *strong cluster*. All strong clusters are adjudicated identically (R0.2).

**D12 -- Block.** A maximal run of text containing no blank line and no markup block boundary.

- A *blank line* is a line containing only whitespace (possibly empty), i.e. two newlines separated by nothing but non-newline whitespace.
- A *markup block boundary* is the opening or closing tag of `h1`-`h6`, `li`, `td`, `th`, `p`, or `div`.
- A single newline inside a block is ordinary whitespace, NOT a block boundary.

**D13 -- End-of-block.** The position after the last non-whitespace character of a block (trailing whitespace is ignored), including the end of the text. Every block edge is a chunk boundary. A candidate located at end-of-block is decided by DL3; nothing else is required there.

**D14 -- "Sentence end."** Deliberately NOT defined. This specification does not define what a sentence is; it defines a procedure whose outputs are intended to be a subset of the positions a competent human editor would mark as sentence ends when preparing prose for text-to-speech reading. The Guarantee Clause (§8) is stated against that standard. (No adjudication protocol exists yet: see OI-4.)

**D15 -- Lookahead.** The only right context any rule inspects is the *following token* (T3): one token after the Decoration, after skipping opening marks. No rule inspects anything beyond it. (In v1.0 this was a 3-token window, needed only by the now-withdrawn R3.2.)

**D16 -- Quote parity. RESERVED.** No active rule uses quote parity (its only user, R3.2, is withdrawn). The definition is retained so that AM-7 and OI-3 can cite it. *Parity* = the number, modulo 2, of double-quote characters (`" “ ” „ ‟ « »`) occurring earlier **in the same block**; 1 = open, 0 = closed. Parity resets to 0 at every block start. Apostrophes and single quotes are excluded. Brackets and parentheses do not affect parity.

---

## §2. Tokenization law

**T1.** The text is converted into a stream of word tokens (D4) and punctuation tokens (D5), in order, losslessly. Between any two adjacent tokens lies a *gap*: the (possibly empty) run of whitespace between them. Gaps are not tokens, but they are kept in the stream, and rules may test whether a gap is empty or non-empty. Block boundaries (D12) are recorded in the stream. Tokenization is deterministic and performed ONCE, before any rule runs.

**T2.** No rule may re-tokenize. Rules operate on the token stream only.

**T3.** Definitions used by the rules:

- *Pre-candidate token*: the word or punctuation token immediately before the terminator cluster.
- *Following token*: the first token after the Decoration and after the gap, skipping any *opening marks* (`( [ { “ " „ ‟ « ‘ '`). It exists only if it lies in the same block. It is *usable* only if it is a word token.
- *Effective initial*: the first character of the following token that is a Letter or Digit. It is "none" if the following token is not usable, or is a word token containing no Letter or Digit.

**T4.** Worked tokenizations (binding):

- `U.S.A.` → `U` `.` `S` `.` `A` `.`
- `e.g.` → `e` `.` `g` `.`
- `don't.` → `don't` `.`
- `9.81` → `9` `.` `81`
- `(NLP).` → `(` `NLP` `)` `.`
- `...` → `.` `.` `.`
- `J. K. Rowling.` → `J` `.` `K` `.` `Rowling` `.`
- `'Go home.'` → `'` `Go` `home` `.` `'`
- `dogs'` → `dogs` `'`
- `wait—no` → `wait` `—` `no`
- `wait--no` → `wait` `--` `no`

---

## §3. Decision law

**DL1 -- Default decision.** For every candidate not at end-of-block: **SPLIT**, unless a suppression rule (§4) fires for it.

**DL2 -- Evaluation order and exclusivity.** R0.1 and R0.2 come first; they determine what a candidate is. Then suppressors are evaluated in the order **R1.2 → R1.3 → R2.1 → R3.1 → R4.2**. The FIRST rule whose trigger matches ends evaluation: the candidate is suppressed (decision KEEP). No rule may un-suppress another's suppression. Rules never act except to suppress; only DL3 overrides. Since every suppressor produces the same outcome (KEEP), evaluation order determines only which rule is cited as governing, never the decision.

**DL3 -- Block-edge override.** A candidate at end-of-block (D13): SPLIT unconditionally, before any suppressor is consulted. No suppression rule applies there, regardless of lexicon state, terminator class, or anything else. This is the only override in the specification.

**DL4 -- Resolution.** Each candidate is resolved exactly once, to SPLIT or KEEP, and the resolution is final. A candidate is PENDING until its following token (T3) is known or end-of-block is reached. A pending candidate emits no boundary. (Streaming clause: an implementation may hold a candidate PENDING; pending is never a SPLIT.)

**DL5 -- Capital condition (restatement).** A SPLIT inside a block requires the effective initial (T3) to be an uppercase letter. This is implemented solely by R3.1. DL5 and R3.1 must never diverge; if they appear to, the text of R3.1 governs.

---

## §4. The suppression rules

*Layer 0 rules define what counts as a candidate. They do not suppress a candidate; they prevent one from existing (same effect).*

### Layer 0 -- Structure

**R0.1 -- Candidacy.** Only positions satisfying D10 are candidates. A terminator cluster that is not followed, after any Decoration, by whitespace or end-of-block is not a candidate and never reaches any other rule. *Absorbs:* `9.81`, `example.com`, `v2.1.3`, `10⁻³.5`, times, file names, and every internal period such as `U.S.A` and `Ph.D` (this is everything v1.0's R1.1 tried to do). *Note:* `(He left.) Then` **is** a candidate, because `)` is Decoration.

**R0.2 -- Cluster normalization.** A terminator cluster (D11) is ONE candidate. An ellipsis cluster is suppressed by R4.2 (evaluation still follows DL2, so an earlier rule may be the one cited). A strong cluster is adjudicated exactly as a single terminator; `!` and `?` follow exactly the same rules as `.` -- there is no special exclamation logic anywhere in this specification. *Consequence (declared):* R1.2, R1.3 and R2.1 therefore also apply before `!` and `?` (AM-8).

### Layer 1 -- Shape (no memory; generalizes to unseen words)

**R1.1 -- WITHDRAWN in v1.1.** It suppressed a terminator immediately followed by a word token. By D10/R0.1 such a terminator is never a candidate, so R1.1 could never fire. Its work is done by R0.1.

**R1.2 -- Single-character pre-token.** Suppress if the pre-candidate token is a single-character token (D6) -- one Letter or one Digit. This covers initials (`J.`), list letters (`a.`), units (`5 A.`), single digits (`Figure 2.`), and the final dot of `U.S.`, `e.g.`, and `Ph.D.` *Accepted consequences (see AM-2, AM-5):* true boundaries after words like `A` or `I` (`taller than I.`) are suppressed -- a missed split, never a false one. *Scope guard:* a pre-candidate token that is punctuation (e.g. `)` in `(NLP).`) is not a single-character token; nor is a lone symbol like `%`.

**R1.3 -- All-caps run.** Suppress if the pre-candidate token is an all-caps run (D7): `NASA.`, `IEEE.`, `COVID.` *Misreading guard:* a token containing any lowercase letter (`PowerPoint`, `iPhone`) does NOT qualify. Roman numerals (`Chapter IV.`) DO qualify -- accepted miss (AM-3).

### Layer 2 -- Lexicon (the shape-blind spots)

**R2.1 -- Set P (presumed non-final).** Suppress if the pre-candidate token matches, case-insensitively, an entry of the static set P. Set P contains words that, before a capitalized continuation, are presumed to be abbreviations. Entries marked ‡ are also ordinary English words that *can* end a sentence; they are included deliberately, accepting the recall cost (AM-9).

`dr, mr, mrs, ms, prof, gen, gov, sen, capt, sgt, lt, col, rev, hon‡, st, mt, ft, vs, ca, cf, pp, fig‡, eq, ch, sec‡, no‡, approx, dept, univ, assn, bros, al‡, jan, feb, mar‡, apr, may‡, jun, jul, aug, sep, sept, oct, nov, dec, mon, tue, tues, wed‡, thu, thur, thurs, fri, sat‡, sun‡`

This list, as written, is complete. (`al` stands for `et al.`.) `etc` and `inc` are deliberately NOT in P: they can end sentences, and the specification's lexicon never licenses and never guesses (see ruling 7.12).

*Ruling consequence:* `St. James`, `Dr. Smith arrived.`, `vs. The outcome`, `Sat. Jan. 5` -- all suppressed at the first period, even before a capital. *Misreading guards:* (a) R2.1 fires regardless of what follows -- the continuation cannot rescue the candidate; (b) R2.1 does NOT apply at end-of-block (DL3 outranks it: a block ending `…visited St.` still splits).

### Layer 3 -- Right context

**R3.1 -- Non-capital continuation.** Suppress if a following token exists (T3) and its effective initial is **not an uppercase letter**: a lowercase letter, a digit, a caseless letter, or "none". Never is a split placed before a non-capital continuation. This is the sole implementation of DL5. It does not apply at end-of-block (DL3). *Absorbs:* `…bread, etc. and milk`, `"…over." he said`, `"What?" asked the teacher`, `…Inc. was founded`, `Section 12. 3 items follow`.

**R3.2 -- WITHDRAWN in v1.1.** The attribution rule never changed an outcome:

- every case it was written for (`"Stop!" he said.`, `"What?" asked the teacher.`) has a lowercase following token, which R3.1 already suppresses (and R3.1 precedes it in DL2 order);
- its own guard excluded capitalized continuations, the only inputs on which it could have differed;
- one of its examples (`"…the end," said John`) ends in a comma, not a terminator, so no candidate exists.

Capitalized attributions (`"Stop!" John said.`) are not handled: AM-6, OI-3.

### Layer 4 -- Policy

**R4.2 -- Ellipsis.** Suppress every ellipsis cluster (D11 classification), wherever it occurs inside a block. An ellipsis is a pause, not a terminator. *Accepted consequence:* `It was over… A new era began.` stays merged (AM-4). DL3 still splits at the block edge.

*(There is no digit rule, no exclamation rule, no F/"final-capable" set. Single digits die at R1.2; digit-initial continuations die at R3.1; `!`/`?` adjudicate identically to `.`; a final-capable abbreviation that looks like a plain word -- `etc. We left.` -- splits by DL1 with no lexicon help. The lexicon only ever SUPPRESSES; it never licenses. This is deliberate: one mechanism, fewer contradictions.)*

---

## §5. Lexicon law

**L1.** Set P (R2.1) is static, finite, versioned, and shipped with the algorithm. Each entry is one word: no periods, no spaces, stored lowercase. An entry that would contain a period or space (`e.g`, `et al`) is invalid: abbreviations with internal periods are handled by R0.1 and R1.2, and `et al` is entered as `al`.

**L2.** *(WITHDRAWN. It governed the speech-verb and pronoun lists of R3.2.)*

**L3 -- Extension protocol.** An entry may be added only with: (a) the word; (b) the list (currently only P); (c) one real example sentence where its absence produced a wrong decision; (d) a check that the word is not a function word (`the, is, was…` are forever excluded); if it is also an ordinary content word that can end a sentence, it is added only with a ‡ mark, which records the accepted recall cost (AM-9). Each addition is one auditable row. Removal follows the same protocol in reverse.

*Audit rows added in v1.1:*

| Word | List | Example (absence produced a wrong decision) |
|------|------|---------------------------------------------|
| `gov` | P | `Gov. Smith signed it.` -- without the entry, a false split after `Gov.` |
| `al` ‡ | P | `Smith et al. Jones disagreed.` -- replaces the invalid v1.0 entry `et al` |

**L4.** No entry may carry a "license" or "permit-split" flag. If a future amendment wants one, it is a new rule (§4 amendment), not a lexicon flag -- rules and data stay separate. (The ‡ mark records a *cost*; it never permits a split.)

---

## §6. The three doors

Under this specification a false split can pass ONLY through:

- **Door A -- P omission or unhandled enumerator.**
  (i) An unknown multi-letter abbreviation before a capital (`Cmdr. Shepard signed it.`). Repair: one P row (L3).
  (ii) A list marker that R1.2/R1.3 do not catch: multi-digit numerals (`10. Foo`) or lowercase Roman numerals (`iv. Bar`). A P row cannot repair these; repair is a specification amendment (OI-1).
- **Door B -- capitalized attribution.** A closing quote followed by an attribution that starts with a capital (`"Stop!" John said.`; AM-6, AM-7). Repair: a specification amendment adding one right-context rule (OI-3).
- **Door C -- tokenization defect.** Text where D3/D4 mis-segment (unusual Unicode, markup leakage such as `**Bold.** Next`). Repair: T-law amendment.

Everything else is closed by construction. This enumeration is the specification's central warranty claim and is deliberately falsifiable (adjudication protocol: OI-4).

---

## §7. Worked rulings (conformance vectors)

| #    | Text | Ruling | Governing rules |
| ---- | ---- | ------ | --------------- |
| 7.1  | `The value is 9.81 m/s². The test…` | no candidate at `9.81`; SPLIT after `².` | R0.1, DL1 |
| 7.2  | `See example.com for details. We…` | no candidate in the domain; SPLIT after `details.` | R0.1, DL1 |
| 7.3  | `She earned her Ph.D. The committee…` | first dot is not a candidate; at the second dot the pre-candidate token `D` is a single-character token, so KEEP (missed split, accepted) | R0.1, R1.2, AM-2 |
| 7.4  | `Dr. Smith arrived. He sat.` | KEEP after `Dr.`; SPLIT after `arrived.`; the final `sat.` is at end-of-block | R2.1, DL1, DL3 |
| 7.5  | `St. James's Park is old. It…` | KEEP after `St.`; SPLIT after `old.` | R2.1, DL1 |
| 7.6  | `J. K. Rowling wrote it. More…` | KEEP, KEEP; SPLIT after `it.` | R1.2, DL1 |
| 7.7  | `I don't. You do.` | SPLIT after `don't.` -- `don't` is ONE token (D3a), not single-character | DL1, D3a |
| 7.8  | `"Stop!" he said. Then…` | KEEP after `!"` (following token `he` is lowercase); SPLIT after `said.` (following `Then` is a capital). The quote and its attribution travel as one chunk | R3.1, DL1 |
| 7.9  | `"Stop!" He left.` | candidate `!"`; following token `He` is a capital; nothing suppresses; SPLIT after `!"` (declared: quoted fragment, then new sentence) | DL1, AM-6 |
| 7.10 | `"It is over." He said nothing.` | SPLIT after `."` -- a true boundary | DL1 |
| 7.11 | `"What?" asked the teacher. Nobody…` | KEEP after `?"` (following token `asked` is lowercase); SPLIT after `teacher.` | R3.1, DL1 |
| 7.12 | `We bought bread, etc. Then we left.` | SPLIT after `etc.` -- `etc` is not in P, `Then` is a capital, no suppressor fires | DL1 |
| 7.13 | `We bought bread, etc. and milk.` | KEEP after `etc.` | R3.1 |
| 7.14 | `The treaty followed in 1995. It held.` | SPLIT after `1995.` -- multi-character, not all-caps, not in P | DL1 |
| 7.15 | `The current reached 5 A. The voltage…` | KEEP after `A.` -- missed split, accepted | R1.2, AM-2 |
| 7.16 | `Chapter IV. The next chapter…` | KEEP after `IV.` -- missed split, accepted | R1.3, AM-3 |
| 7.17 | `It was over… A new era began.` | KEEP after `…` -- missed split, accepted | R4.2, AM-4 |
| 7.18 | `…uses natural language processing (NLP). We…` | the pre-candidate token is `)` (punctuation), so R1.2 and R1.3 do not apply; not in P; `We` is a capital; SPLIT | DL1 |
| 7.19 | `…signed in the U.S. The Senate adjourned.` | first dot is not a candidate; KEEP after `U.S.` (`S` is single-character) -- the famous ambiguity absorbed as a missed split, never a false one | R0.1, R1.2, AM-5 |
| 7.20 | `…in the U.S. Senate adjourned early.` | same -- KEEP (identical features, identical ruling; see D14) | R1.2 |
| 7.21 | `Wait… what happened next. Nobody knows.` | KEEP after `…` (following token `what` is lowercase; R4.2 also matches); SPLIT after `next.` | R3.1, R4.2, DL1 |
| 7.22 | `NASA was founded. Later…` | SPLIT after `founded.`; the token `NASA` mid-sentence never matters | DL1 |
| 7.23 | `He is taller than I. Others disagree.` | KEEP after `I.` -- missed split, accepted | R1.2, AM-2 |
| 7.24 | `Prices rose 5. The next year…` | KEEP after `5.` (single digit) | R1.2 |
| 7.25 | `He said, 'Go home.' Then he left.` | the closing `'` is Decoration (D3a, D9); SPLIT after `.'` | D3a, D9, DL1 |
| 7.26 | `Was it NASA? We do not know.` | KEEP after `?` -- R1.3 applies to `?` exactly as to `.`; missed split, accepted | R0.2, R1.3, AM-8 |
| 7.27 | `He sat. She stood.` | KEEP after `sat.` (`sat` is in P); missed split, accepted | R2.1, AM-9 |
| 7.28 | `Section 12. 3 items follow.` | KEEP after `12.` (digit-initial continuation) | R3.1 |
| 7.29 | `He worked for Acme Inc. The firm closed.` | SPLIT after `Inc.` -- `inc` is not in P | DL1 |
| 7.30 | `He visited St.` (end of block) | SPLIT: end-of-block outranks P | DL3 |
| 7.31 | `(He left.) Then she left.` | `)` is Decoration, so `.)` is a candidate; SPLIT after `.)` | D9, D10, DL1 |
| 7.32 | `Gov. Smith signed it.` | KEEP after `Gov.` | R2.1 |
| 7.33 | `He left. “Then he came.”` | the opening `“` is skipped when locating the effective initial (`T`); SPLIT after `left.` | T3, DL1 |

---

## §8. Guarantee clause

**W1 -- Warranted.** Every SPLIT emitted inside a block satisfies: candidacy (D10) + no suppression rule fired (§4, DL2) + uppercase effective initial (R3.1/DL5). Every SPLIT at end-of-block satisfies DL3. Subject to §6's doors staying shut, no SPLIT is placed at a non-sentence-end (D14 standard).

**W2 -- Not warranted (recall).** This specification does NOT promise to find every sentence end. The missed splits AM-1 through AM-5, AM-8 and AM-9 below are accepted BY DESIGN and are not defects.

**W3 -- The schedule.**

*W3a -- Accepted missed splits (a KEEP where a human would split):*

- **AM-1** -- no accepted miss. Contractions are safe by D3a (`don't.` is one token); listed so the class it prevents is documented.
- **AM-2** -- true boundary after a single-character word or digit (`than I.`, `5 A.`, `Figure 2.`, the `D` of `Ph.D.`), because R1.2 suppresses all single-character pre-tokens. Cost: merged chunks. Frequency: unmeasured.
- **AM-3** -- true boundary after all-caps runs and Roman numerals (`Chapter IV. The…`, `…built with AI. The…`, `…on TV. She…`) -- R1.3. Frequency: **unmeasured**; likely non-trivial in modern and technical prose, since sentences ending in acronyms are common.
- **AM-4** -- true boundary at an ellipsis (`over… A new era`) -- R4.2. Frequency: unmeasured.
- **AM-5** -- `U.S.`-class trailing ambiguity before capitals (7.19/7.20) -- R1.2. This is the "Layer E" case of the catalogue in the companion documents, absorbed in the safe direction.
- **AM-8** -- `!` and `?` inherit the abbreviation-shape suppressors (R0.2): a true boundary after a single-character, all-caps, or P token followed by `?` or `!` is missed (`Was it NASA? We…`, `What is 5? Ten.`). Frequency: unmeasured.
- **AM-9** -- lexicon-induced misses (R2.1): a true boundary after any P entry before a capital (`He sat. She stood.`, `…on Main St. It…`). Highest for ‡ entries.

*W3b -- Declared false-split risks.* These are NOT missed splits. They are false splits that the specification knowingly permits; they remain defects (CI-6), but acknowledged ones:

- **AM-6** -- a closing quote followed by a capitalized attribution (`"Stop!" John said.`, `"Stop!" He said.`) splits after the quote -- Door B.
- **AM-7** -- single-quoted dialogue is recognized only as Decoration (D9); it is invisible to quote parity (D16), and its attributions behave as in AM-6 -- Door B.

**W4 -- Failure protocol.** When a false split is observed in the wild: identify which door (§6) it passed through; apply exactly one repair.

- Door A(i): one P row (L3).
- Door C: one T-law fix.
- Door A(ii) and Door B: a specification amendment introducing one new rule, with its own ID, layer, and rulings -- never a lexicon flag (L4).

Record it in the audit trail. Threshold-tuning, per-document hacks, and multi-rule rewrites are PROHIBITED as responses to single failures.

---

## §9. Interpretation index ("this specification does NOT mean…")

- **CI-1:** It does NOT mean every `word. Capital` splits. Layers 1 and 2, and R4.2, exist precisely to stop some of them.
- **CI-2:** It does NOT mean abbreviations need a dictionary to be safe. Shape (Layer 1) suppresses initialisms, single-letter abbreviations and internal periods; the dictionary patches multi-letter abbreviations that shape cannot see.
- **CI-3:** It does NOT mean the lexicon ever causes a split. Under this specification the lexicon only suppresses (§4 note; L4).
- **CI-4:** It does NOT mean `!` and `?` behave differently from `.` -- there is no exclamation-specific logic anywhere (R0.2). The corollary (AM-8) is declared.
- **CI-5:** It does NOT mean block edges need terminators. DL3 is unconditional.
- **CI-6:** It does NOT mean KEEP decisions are errors. Under W2, a KEEP is a legitimate outcome; only a false SPLIT is a defect. The declared false-split risks (W3b) are defects with acknowledged status, not exemptions.
- **CI-7:** It does NOT mean whitespace variants (double space, newline, NBSP) change any ruling. All whitespace is equivalent (D2); the double-space convention is deliberately ignored.
- **CI-8:** It does NOT mean the decision depends on sentence length, grammar, or meaning. Every rule is a function of local token shape, one static list (P), and at most the single following token (D15), plus the block edge.

---

## §10. Change log: v1.0 → v1.1

| Ref | Defect in v1.0 | Fix in v1.1 |
| --- | -------------- | ----------- |
| Header | Preamble rendered as one giant heading; "v1.0" contradicted "unproven, not final"; the ID list named a non-existent `C-` prefix and omitted `L-` | Reformatted; version is v1.1 (draft); prefixes corrected |
| Layout | DL1-DL5 and L1-L4 ran together as single paragraphs | One paragraph per item (formatting only) |
| D3 | `--` was listed as punctuation but D5 says tokens are one character; the em dash `—` was absent (so `word—Word` was one token); the straight double quote appeared twice | D3b dash token; `—` added; code points given |
| D3/D9/T3 | Apostrophes were word characters (D3) yet D9 listed `'` as Decoration and omitted `’`, so `'Go home.' Then` never produced a candidate | D3a (word-internal apostrophes only); `’` added to D9 |
| T1/D10 | The token stream contained no whitespace, yet D10/R0.1 test whitespace; "lossless" was false | Gaps are kept in the stream |
| D2 | "Lowercase = a letter that is not uppercase" made caseless letters lowercase | Uses the Unicode Lowercase property |
| D6/R1.2 | D6 counted any one-character token (`%`, `×`); R1.2's prose said letter or digit | D6 = one Letter or one Digit |
| D10/R0.1 | R0.1 ("period not followed by whitespace") contradicted D10/D9 (`(He left.) Then`); D10 cited D12 instead of D13 | R0.1 defers to D10; reference fixed |
| R1.1 | Could never fire: an adjacent terminator is never a candidate | Withdrawn (stub); R0.1 absorbs its cases |
| D13/DL3 | Trailing newline/whitespace meant a candidate was never at "end-of-block"; DL3 ("SPLIT") and DL5 (`none` → KEEP) conflicted | D13 ignores trailing whitespace; R3.1 is scoped to non-edge candidates |
| DL5/R3.1 | Claimed to be "the same test", but R3.1 covered lowercase only while DL5 also covered digits/none; a digit-initial candidate was SPLIT by the rules and KEEP by DL5 | R3.1 = "effective initial is not an uppercase letter"; DL5 is a restatement |
| DL2/R0.2 | R0.2 "routed" ellipsis to R4.2, contradicting the DL2 order; R0.1/R0.2 listed as suppressors; order affects only citation | Clarified: Layer 0 defines candidates; order affects only the governing citation |
| DL4 | "A KEEP is provisional and may be revised" contradicted DL2 "no rule may un-suppress" | Pending → resolved once, final |
| D11/R0.2 | "Class of the last token" was meaningless (all classes are treated alike); the `."` example is not a terminator cluster | Removed |
| R3.2 | Dead rule: lowercase followers were already KEEP by R3.1; capitalized ones were excluded by its own guard; one example ended in a comma; ruling 7.11 cited it wrongly | Withdrawn (stub); λ reduced to 1 (D15); D16 reserved; L2 withdrawn |
| D16 | "Incremented/decremented" was ambiguous; parity leaked across paragraphs | Parity mod 2, reset per block; marked reserved |
| T3 | Told rules to skip opening quotes "at the start of the following token", but quotes are never inside word tokens; "first word token" silently skipped any punctuation | Only opening marks are skipped; otherwise the effective initial is "none" |
| R2.1/P | Contained `e.g`, `i.e`, `n.b`, `et al` (contradicting L1, and unable to match a single token); an open-ended `…` inside a "finite" list; `etc*`/`inc*` pointed to a non-existent R2.2 and contradicted ruling 7.12 and the §4 note | Invalid entries removed; `al` added; `etc` and `inc` removed; list stated complete |
| R2.1/L3 | "Never sentence-final" is false for `no`, `sat`, `sun`, `may`, `sec`, …; the entries violated L3(d) | Renamed "presumed non-final"; ‡ marks; AM-9; L3(d) revised |
| P | `Gov. Smith` produced a false split | `gov` added with an L3 audit row |
| §6 | Door A's example (`prof`) is already in P; multi-digit/lowercase-Roman list markers were unacknowledged; Door B referenced pattern lists | Examples fixed; Door A(ii) added; Door B rewritten |
| W2/W3/CI-6 | AM-6 and AM-7 are false splits but were filed as accepted *misses* | W3 split into W3a (misses) and W3b (declared false-split risks) |
| W3 | AM-1 was "none"; AM-2/AM-3 asserted "low" frequency with no data | Reworded; frequencies marked unmeasured |
| AM-8 | `!`/`?` inheriting abbreviation suppressors was undeclared | Added AM-8 |
| CI-1/2/8 | Mis-cited Layer 3; overclaimed Layer 1; referenced two lists and λ=3 | Corrected |
| §7 | 7.3 and 7.8 contained working-out ("-- NO:", "-- wait:"); 7.11, 7.19 and 7.21 cited the wrong governing rule; §0.7 said "illustrative" while §7 said "binding" | Rulings cleaned; §0.7 defines them as conformance vectors; 7.25-7.33 added |
| Cross-refs | `§DL2`; "§7 schedule" (it is §8); `R2.2`; T3 cited as the token stream (it is T1) | Fixed |
| D12 | "Two consecutive newlines" missed CRLF and whitespace-only blank lines; `th` missing; tag-detection order unspecified | Defined precisely |

### Open issues (need a design decision; deliberately not changed)

- **OI-1 -- Enumerators.** Multi-digit list numbers (`10. Foo`) and lowercase Roman numerals (`iv. Bar`) produce false splits (Door A(ii)). Needs a new rule.
- **OI-2 -- `!` and `?` share the abbreviation suppressors** (CI-4, AM-8). This is a design choice with a recall cost; consider whether R1.2, R1.3 and R2.1 should apply to `.` only.
- **OI-3 -- Capitalized attributions** (Door B, AM-6). A right-context rule would revive D15's wider window and D16's quote parity.
- **OI-4 -- D14 has no adjudication protocol.** The "deliberately falsifiable" warranty needs a stated procedure for deciding whether a position is a sentence end (who judges, how many editors, how ties are resolved).
- **OI-5 -- Unmeasured frequencies and a small seed lexicon.** AM-2, AM-3, AM-8 and AM-9 need corpus measurements. P omits common abbreviations such as `Ltd`, `Corp`, `Ave`, `Blvd`.
- **OI-6 -- Quote and whitespace ambiguity.** Straight `"` and `'` are ambiguous between opening and closing (and `5"` inch marks would toggle parity if D16 were revived). NBSP is treated as ordinary whitespace though it is often used to glue an abbreviation to a name. The HTML block list is minimal (`br`, `blockquote`, `tr`, `ul`, `ol` are not boundaries).
- **OI-7 -- Companion documents.** References to `precision-first-split-theory.md` and `why-not-to-split.md` (and the "catalogue" cited in AM-5) were not checked against those files.
