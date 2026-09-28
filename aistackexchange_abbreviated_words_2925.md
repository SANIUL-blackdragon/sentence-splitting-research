> **Source:** https://ai.stackexchange.com/questions/2925/which-algorithm-can-i-use-to-convert-abbreviated-words-to-the-original-ones (Artificial Intelligence Stack Exchange), fetched 2026-09-28
> 
> **Provenance notes:** The live page is behind a Cloudflare “Just a moment…” interstitial (direct reader, headless browser, StackPrinter and the Wayback Machine all unavailable/blocked at fetch time), so this copy was assembled from the official Stack Exchange API 2.3 (questions/answers/comments/related/users endpoints) plus the post-revisions endpoint. All post text, vote scores, dates, user names, reputations and badge counts are current live values; “Asked/Modified/Viewed” relative dates are computed as of the fetch date. The revisions history shows the question was edited on 2017-03-11 (“Fixed some grammar”) and on 2022-05-19 (“edited tags; edited title”), and the answer was last edited 2022-05-19; the API could not return the *editor identities* for those revisions (endpoint rate-limited for this IP), so the “edited” lines below omit the editor name. Comment shown under CC BY-SA 3.0; question and answer currently under CC BY-SA 4.0. Site chrome (nav bar, Ask Question button, vote arrows, sign-up banners) omitted. There are zero comments on the question and zero Linked questions; Related sidebar has 7 items, reproduced below.

---

## Which algorithm can I use to convert abbreviated words to the original ones?

**Artificial Intelligence Stack Exchange** · question #2925

Asked **9 years, 6 months ago** (Mar 6, 2017 at 0:28 UTC) · Modified **4 years, 4 months ago** (May 19, 2022 at 8:25 UTC) · Viewed **682** times

---

**[3]** *(score – up/down arrows not reproducible in markdown)*

I want to write a program that looks at abbreviated words, then figures out what the words are. For example, the abbreviation is "blk comp", and the translation is "black computer".

In order to give it context for more ambiguous terms, I will be inputting sets of words with each request. So, if I input the set "keyboard, software, mouse, monitor", I would expect to get "black computer". On the other hand, if I input "Honda, transmission, mileage, Ford", I then would expect to get "black compact", or at least something that has anything to do with cars.

Basing on the above case scenario, what kind of an algorithm should be applied in this case?


`natural-language-processing` `algorithm-request`

edited May 19, 2022 at 8:25 UTC *(revision 2: “Fixed some grammar”, Mar 11, 2017; revision 3: “edited tags; edited title”, May 19, 2022; editor identities not returned by API)*

**[Neo_999](https://ai.stackexchange.com/users/5860/neo-999)** — 33 rep · 2 bronze · asked Mar 6, 2017 at 0:28 UTC

---

## Answer

**✓ Accepted answer** — **[2]** *(score)*

Take a look at using a *skip gram model* to find what the abbreviated text is. The skip gram model turns a word into a vector, which allows it to be processed by other machine learning algorithms. Or, alternatively you can do some really cool addition and subtraction problems with the resulting vectors. With the skip gram model in your case you could generate a vector for your input and then compare it with other skip gram vectors and once you have found a near perfect match then that is the unabbreviated word.

You could also look at using sparse distributed representations of words to do this. This approach is similar to the skip gram model except that instead of a vector with maybe 500 values a sparse representation may contain thousands of binary digits of which only a couple are positive or 1.

If you would like to look at this approach take a look at cortical.io which has free API that you can use.

So, you could use a deep neural network in combination with the skip gram model to produce your output.

edited May 19, 2022 at 8:27 UTC *(editor identity not returned by API)*

**[Aiden Grossman](https://ai.stackexchange.com/users/4631/aiden-grossman)** — 863 rep · 5 silver, 8 bronze · answered Mar 7, 2017 at 2:19 UTC

**1 comment:**

> **[Neo_999](https://ai.stackexchange.com/users/5860/neo-999)**: Thank you, Aiden! This sounds like a good starting point to try to solve this problem. — *Mar 7, 2017 at 16:39 UTC*

---

## Related (sidebar)

- **[2]** (answers: 1) — [Can AI solve jumbled words?](https://ai.stackexchange.com/questions/6965/can-ai-solve-jumbled-words)
- **[1]** (answers: 1) — [Which RL algorithm should I use to learn an optimal weight vector?](https://ai.stackexchange.com/questions/35825/which-rl-algorithm-should-i-use-to-learn-an-optimal-weight-vector)
- **[4]** (answers: 1) — [Which algorithm can I use to minimise the number of wins of 2 weapons that fight each other in a game?](https://ai.stackexchange.com/questions/7518/which-algorithm-can-i-use-to-minimise-the-number-of-wins-of-2-weapons-that-fight)
- **[1]** (answers: 1) — [Which algorithm can be used for extracting text patterns in tabular data?](https://ai.stackexchange.com/questions/26568/which-algorithm-can-be-used-for-extracting-text-patterns-in-tabular-data)
- **[7]** (answers: 1) — [Which parsing algorithm can I use for NLP question answering system?](https://ai.stackexchange.com/questions/2787/which-parsing-algorithm-can-i-use-for-nlp-question-answering-system)
- **[2]** (answers: 1) — [Which matrix represents the similarity between words when using SVD?](https://ai.stackexchange.com/questions/11261/which-matrix-represents-the-similarity-between-words-when-using-svd)
- **[4]** (answers: 4) — [How to figure out which words have the same meaning in two different languages?](https://ai.stackexchange.com/questions/5115/how-to-figure-out-which-words-have-the-same-meaning-in-two-different-languages)

## Linked (sidebar)

*(none — no Linked questions for this post)*

---

**Not the answer you're looking for?** Browse other questions tagged [natural-language-processing](https://ai.stackexchange.com/questions/tagged/natural-language-processing) [algorithm-request](https://ai.stackexchange.com/questions/tagged/algorithm-request) or [ask your own question](https://ai.stackexchange.com/questions/ask).
