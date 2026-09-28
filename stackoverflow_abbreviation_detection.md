# Abbreviation detection

> **nlp - Abbreviation detection - Stack Overflow**
> *Source: https://stackoverflow.com/questions/20727552/abbreviation-detection*
>
> *Provenance: the live page blocks automated access (Cloudflare), so this verbatim copy is assembled from (a) the Wayback Machine full-page capture dated 06 May 2021 (the most recent) and (b) StackPrinter's live export, used to restore the 8 question comments that the snapshot had collapsed behind "Show 8 more comments" (their timestamps are not exposed while collapsed). Per the live StackPrinter check, the page today differs from the snapshot only in vote totals: the question now shows 16 votes (snapshot: 15) and the top answer 9 votes (snapshot: 8). Site-wide chrome (navigation, sign-up promos, "Your Answer" form, Overflow Blog / Meta / Hot Network Questions sidebars, footer) is omitted as non-content; the question-specific sidebar (Linked / Related) is included. All wording, spellings and typos below are unchanged from the original.*

**Asked** 7 years, 4 months ago | **Active** 7 years, 4 months ago | **Viewed** 7k times

**15 votes · 1 bookmark**

## Abbreviation detection

Under what field of study under natural language processing does abbreviation detection come? Looking for sources to learn abbreviation detection. I have considered Semantics, which basically detect synonyms. so i thought i might do multi-word semantics that would detect that "nlp" and "natural language processing" are similar. but i have found NO solution to do multi-word semantics.

**Note:** I know its really easy to down vote this question, but try to understand my problem. I have struggled for months now and any help is GREATLY appreciated...

Thankyou

**Tag:** nlp

*edited Dec 22 '13 at 8:21* — **Mat** — 188k reputation (38 gold badges, 365 silver badges, 382 bronze badges)

*asked Dec 22 '13 at 8:20* — **Anshu Dwibhashi** — 4,375 reputation (1 gold badge, 23 silver badges, 55 bronze badges)

### Comments (13 total)

*The first 5 were expanded in the snapshot (all scores 0); the last 8 were collapsed behind "Show 8 more comments" and are restored here from the live StackPrinter export:*

1. **chrylis -cautiouslyoptimistic-:** I'm no expert in the field, but this sounds like an especially difficult problem, as it's highly dependent on both context and semantics. — *Dec 22 '13 at 8:22*
2. **Anshu Dwibhashi:** no i dont think its really difficult, google, yahoo and bing are doing it — *Dec 22 '13 at 8:23*
3. **Elliott Frisch:** At a guess? Artificial Intelligence. — *Dec 22 '13 at 8:23*
4. **Anshu Dwibhashi:** more over, its just like semantics which is really easy, i just don't know how to do multi word semantics — *Dec 22 '13 at 8:23*
5. **Anshu Dwibhashi:** @ElliottFrisch what do you think natural language processing is? — *Dec 22 '13 at 8:23*
6. **Elliott Frisch:** [Compound term processing](http://en.wikipedia.org/wiki/Compound_term_processing)? — *(collapsed in snapshot; timestamp not exposed)*
7. **Anshu Dwibhashi:** @ElliottFrisch was that an answer to my post? or my comment? — *(collapsed in snapshot; timestamp not exposed)*
8. **Elliott Frisch:** To your post. I wasn't sure which "under" you meant originally. — *(collapsed in snapshot; timestamp not exposed)*
9. **Anshu Dwibhashi:** can you please give me resources to learn it? i would still prefer multi token semantics — *(collapsed in snapshot; timestamp not exposed)*
10. **ales_t:** Nothing is stopping you from doing multi-word semantics. If you define context as the window of several words, you can easily collect and compare context similarities of both single words and multiword expressions. — *(collapsed in snapshot; timestamp not exposed)*
11. **Chiron:** @AnshumanDwibhashi and do you consider Google, Yahoo and Microsoft aren't brilliant and they have armies of talented engineers? — *(collapsed in snapshot; timestamp not exposed)*
12. **Anshu Dwibhashi:** i'm sorry i didn't get you @Chiron — *(collapsed in snapshot; timestamp not exposed)*
13. **alvas:** this discussion is on MWE is getting way too wayward =) — *(collapsed in snapshot; timestamp not exposed)*

---

## 3 Answers

*Sort tabs on page: Active · Oldest · Votes (order as captured)*

### Score 8 — answered Dec 22 '13 at 11:24 — **Nino** (111 reputation, 2 bronze badges)

(Automatic) Detection of abbreviations is also a major subproblem and task of sentence segmentation and tokenization processes in general, i.e.: disambiguate sentence endings from punctuation attached to abbrevations. Statistical methods (NLP) have been applied to detect and extract them successfully, mostly in a (semi-)supervised manner. E.g. the PUNKT system, which actually has been developed for sentence boundary detection, *is able to detect abbreviations with high accuracy*, *based on the assumption that a large number of ambiguities in the determination of sentence boundaries can be eliminated once abbreviations have been identified* ([Kiss et al. 2006. *Unsupervised Multilingual Sentence Boundary Detection*](http://aclweb.org/anthology//J/J06/J06-4003.pdf)).

Now, before trying to modify the PUNKT system or similar, I was just trying to give a direction wrt. NLP-based abbr. detection. The system mentioned above, for example, applies techniques to measure collocational strengths between pairs of tokens, which can be two words, but also a word and some punctuation, treated as a token. It's all based on frequencies and probabilites, although the results in traditional collocational analysis' do allow for semantic research.

**Comments:**

- **Anshu Dwibhashi:** Thankyou so much for your answer @Nino it was great, but i have found an answer myself too. i'd rather accept that one. But thanks for your answer, i greatly appreciate your work being new to stackoverflow. i upvoted your answer, thankyou, and welcome to stackoverflow. — *Dec 22 '13 at 13:27*
- **arturomp:** Somewhat related question touching on collocations: stackoverflow.com/q/20710593/583834 — *Dec 22 '13 at 18:06*

---

### Score 6 — ✅ Accepted Answer — answered Dec 22 '13 at 13:29 — **Anshu Dwibhashi** (4,375 reputation, 1 gold badge, 23 silver badges, 55 bronze badges)

Thankyou to all who helped me, I think i found an answer myself. I trust it because it is from a research paper by the person who invented the abbreviation expansion algorithm for Yahoo! and it also shows signs of artificial intelligence. Again, thankyou all.

To others in the same boat as me, here's the solution:

[SEO by the sea - How search engines might expand abbreviations in search queries](http://www.seobythesea.com/2009/10/how-search-engines-might-expand-abbreviations-in-queries/)

---

### Score 0 — answered Dec 22 '13 at 10:23 — **ales_t** (1,902 reputation, 9 silver badges, 9 bronze badges)

You could start with simple rule-based solutions, e.g. look for patterns like "natural language processing (NLP)". I expect that given a large enough corpus, this could go a long way. And if you include a dump of Wikipedia...

**Comments:**

- **ales_t:** Maybe you don't have to. — *Dec 22 '13 at 10:28*
- **alvas:** how do you define abbreviations? — *Dec 23 '13 at 20:32*

---

## Sidebar — Linked

- **4** — NLP process for combining common collocations

## Sidebar — Related

- **7** — C++ - How to read Unicode characters( Hindi Script for e.g. ) using C++ or is there a better Way through some other programming language?
- **5** — Natural Language Processing Package
- **18** — SOLR and Natural Language Parsing - Can I use it?
- **2** — Which of these projects should I choose for summer workshop on NLP?
- **1** — Finding words from a dictionary in a string of text
- **1** — Suggestions for development of command and control kind of Natural Language based system
- **3** — NLP: retrieve vocabulary from text
- **0** — Assign a short text to one of two categories according to previous assignments (votes)

---

*site design / logo © 2021 Stack Exchange Inc; user contributions licensed under cc by-sa. rev 2021.5.6.39231 (as captured)*
