# What is the best technique to detect abbreviations in a text?

> *Source: ResearchGate — https://www.researchgate.net/post/What_is_the_best_technique_to_detect_abbreviations_in_a_text (verbatim copy of the archived page capture dated 11 Apr 2018)*

**Question**

**Asked** — 3 years ago

**Divya Vikash** (1.16)
*The LNM Institute of Information Technology*

## What is the best technique to detect abbreviations in a text?

Abbreviations or acronyms are widely used in text materials to reduce space. Their full meaning is however given at the place where it is first used. What is the best data mining approach to recognise such words wheever they occur in the document?

**Topics:**

| Topic | Questions | Followers |
|---|---|---|
| Pattern Recognition | 928 | 37,075 |
| Natural Language Processing | 643 | 15,717 |
| Data Mining | 1,691 | 130,002 |
| Data Structures | 173 | 29,198 |

Share

**2 Recommendations**

---

## Popular Answers (1)

**3 years ago**

**James Dominic O'Shea**
*Manchester Metropolitan University*

I have developed a "brute force" approach for a similar problem I had with recognising what is someone's actual name in a text string. You could use a similar (divide and conquer" scheme. First, you could use a list of the most frequently occuring cases of positive cases (abreviations / acronyms). Second you could use a list of most frequently occurring words in the english language to rule out negative cases. This will leave a set of uncertain wrods which have lower frequency of occurrence to deal with. At this point I would investigate using an n-gram based classifier (e.g. trigrams or quadragrams of letters) trained on the two high frequency sets.

Whatever approach you took, I would work by winnowing down the unknown cases in successive stages.

You need to take account of misclassification - misses and false alarms which may occur either because an acronym is actually a real a real word e.g. Fuzzy Algorithm for Similarity Testing (FAST) or because a real word is so obscure it looks like an  abbreviation e.g. syzygy - an alignment of three celestial objects.

Whatever apporach you take it sounds like it's going to be fun.!

**3 Recommendations**

---

## All Answers (17)

**3 years ago**

**Adewole K. S.**
*University of Ilorin*

Dear Divya,

This is a very good question and a door to leverage on the existing data mining methods and see how this problem can be best solved. I will see how the problem can be best modeled using the existing and get back to you as soon as possible.

All the best

**2 Recommendations**

---

**3 years ago**

**Quist-Aphetsi Kester**
*University of Cape Coast*

There will be no best general technique because it will depends on the context.

**1 Recommendation**

---

**3 years ago**

**Mohamed Mohsen Gammoudi**
*Université de la Manouba*

I agree With Joachim.

---

**3 years ago**

**Richard Mccart**
*RMIT University*

I think you need a look up list for abbreviations.

**1 Recommendation**

---

**3 years ago**

**Niladri Chatterjee**
*Indian Institute of Technology Delhi*

Are you talking about English? Or any language in general?

**1 Recommendation**

---

**3 years ago**

**Asterios Chardalias**
*Aristotle University of Thessaloniki*

Abbreviations are not uniform, so using only one parameter to pick them up would not work. It has to be a multipronged approach.

Abbreviations (usually):

\> Are not morphologically well-formed words

\> Infringe upon the phonotactics of the language in which they occur

\> Employ punctuation marks, predominantly the period "." , within them

\> Have the same collocations as their unabbreviated counterparts

They also might:

\> Use atypical alphanumeric characters such as /, & or ~

\> Resemble a phonetic transcription of their unabbreviated counterparts

\> Exploit the rebus principle (eg. inb4 "in before", NRG "energy")

**2 Recommendations**

---

**3 years ago**

**Marion G Ceruti**

*Added an answer*

B"H

I agree with Niladri's and Asterios' comments. Probably you will not be able to find the "best" technique because it involves an exhaustive search over a multivariate space. However, you probably can find a 90% solution by implementing a series of searches, each of which separately will yield incomplete results, but the aggregate of which is likely to produce a reasonable representation. This approach can be combined with a look-up list to include known abbreviations. The list can grow to include new abbreviations when they have been verified.

In English it is more difficult to identify acronyms because no punctuation is required to indicate them specifically and some acronyms have become like ordinary nouns in common use, such as RADAR and LASER, thus blurring the distinction between an acronym and something that was an acronym but is now used as if it were not an acronym. In fact, the word "laser" has lost some of its strict acronymic characteristics to the point where it is no longer grammatically incorrect to write it in lower case.  A verb, "to lase" has been derived from "laser" to describe the specific action that a laser performs to produce coherent, monochromatic light.

In Hebrew, it is easy to identify acronyms because a diacritic called "gershaim" is required before the last letter of the acronym to indicate that the consonant string is an acronym. It looks like a double quotation mark, the use of which carries over into the Latin alphabet when transliterating Hebrew acronyms. For example, B"H is an acronym meaning "B'esrat Hashem" meaning "with the help of God." B"H is clearly intended to be an acronym and not a person's initials, BH.

In English, many abbreviations and acronyms lack vowels and can be detected because of this, relating to Asterios' idea that abbreviations are not morphologically well-formed words. This can help to identify some abbreviations but not all, since some are well formed words and have vowels. Hence, the need for multiple searches over the same text each looking for a different characteristic of abbreviations and acronyms.

Some abbreviations are followed by a period, so when a period occurs in a place that is obviously not the end of a sentence, one can infer with better than chance accuracy that an abbreviation has been detected, also relating to the list that Asterios has suggested.

An algorithm based on the above suggestions can be refined through usage to detect more and more abbreviations over time. Will it be the best approach? We will not know that, but do you really need the best or will an approach that provides usable results be good enough? It really depends not only on context but even more so on why you need to detect abbreviations and acronyms.

**2 Recommendations**

---

**3 years ago**

**Marion G Ceruti**

*Added an answer*

Correction - I attributed the suggestion of a look-up list to Asterios when it should have been Richard. Sorry for the error.

**1 Recommendation**

---

**3 years ago**

**Marion G Ceruti**

*Added an answer*

Divya,

It might be helpful to add key words, "Computational linguistics" to your key-word list.

It is a branch of natural-language processing.

**1 Recommendation**

---

**3 years ago**

**James Dominic O'Shea**
*Manchester Metropolitan University*

I have developed a "brute force" approach for a similar problem I had with recognising what is someone's actual name in a text string. You could use a similar (divide and conquer" scheme. First, you could use a list of the most frequently occuring cases of positive cases (abreviations / acronyms). Second you could use a list of most frequently occurring words in the english language to rule out negative cases. This will leave a set of uncertain wrods which have lower frequency of occurrence to deal with. At this point I would investigate using an n-gram based classifier (e.g. trigrams or quadragrams of letters) trained on the two high frequency sets.

Whatever approach you took, I would work by winnowing down the unknown cases in successive stages.

You need to take account of misclassification - misses and false alarms which may occur either because an acronym is actually a real a real word e.g. Fuzzy Algorithm for Similarity Testing (FAST) or because a real word is so obscure it looks like an  abbreviation e.g. syzygy - an alignment of three celestial objects.

Whatever apporach you take it sounds like it's going to be fun.!

**3 Recommendations**

---

**3 years ago**

**Marion G Ceruti**

*Added an answer*

"Second you could use a list of most frequently occurring words in the english language to rule out negative cases."

James has a good idea - to use a list of words that are mistaken for acronyms or abbreviations but actually are not. Thus, you will have at least two lookup lists, known abbreviations and acronyms, and also a list of know words that are not abbreviations or acronyms.

"Syzygy" is an example of the rule that states that sometimes "y" is a vowel.

**2 Recommendations**

---

**3 years ago**

**Richard Mccart**
*RMIT University*

There is an impractical but interesting theoretical answer. You could train a genetic algorithm to know what an abbreviation was but this would be better than a language speaker as we don't know many of the abbreviations used in contexts we're unfamiliar with.

**2 Recommendations**

---

**3 years ago**

**Tiago A. Almeida**
*Universidade Federal de São Carlos*

We have designed a framework to normalize and expand noise and short text messages, such as SMS, tweets, etc. Basically, the most common slangs, typos, symbols and abbreviations are detected and replaced for their standard english words. You can also enrich the text sample by inserting concepts semantically related with the message context.

We have proved that such preprocessing can greatly improve the classification and clustering performances.

The TextExpansion tool is open-source and publicly available at

http://lasid.sor.ufscar.br/expansion/

Moreover, you can find other uselful machine learning tools available at

http://lasid.sor.ufscar.br/ml-tools/

**3 Recommendations**

---

**3 years ago**

**Marion G Ceruti**

*Added an answer*

Collectively, we have suggested many aspects of a comprehensive approach which, if used as an aggregate, are likely to yield a 90% or better than 90% result. The more comprehensive the approach beyond that, the more sophisticated the algorithm must become. To achieve a near 100% solution will be very difficult for theoretical reasons as well as practical reasons.

For example, if we want to detect all abbreviations and acronyms, we will need to decide where the dividing line exists between what is an abbreviation and what is not, and between what is an acronym and what is not. I'm not sure anyone has determined a method to do this that encompasses all cases. Yes, we can get close, but what do we do with the more difficult and more "borderline" cases?

Here again, it comes down to why we want to find acronyms and abbreviations in text. If we know the purpose of the exercise we can define criteria of acceptance that specify what we think "good enough" will be.

---

**3 years ago**

**Bilal Khan**
*COMSATS Institute of Information Technology*

i dont have idea for  abbreviations handling in data mining, although we can handle it using temporary table for abbrevition...

---

**3 years ago**

**James Dominic O'Shea**
*Manchester Metropolitan University*

Looking at Marion's contributions prompts the question "What is the best a human could do?" I'm pretty sure the average human wouldn't get 100%. Part of your study may be an evaluation of how well the algorithm performs (90%+ compared with humans <100%).

**1 Recommendation**

---

Can you help by adding an answer?

**Answer** — *Add your answer*

---

## Question followers (20)

See all

| Follower | Institution |
|---|---|
| Georgi Zapryanov | Technical University of Sofia |
| Quist-Aphetsi Kester | University of Cape Coast |
| Unnati Shah | C.K. Pithawalla College Of Engineering & Technology |
| Aieman Ahmad Al-Omari | Hashemite University |
| Mohamed Mohsen Gammoudi | Université de la Manouba |
| James Dominic O'Shea | Manchester Metropolitan University |
| Noureddine Ouerfelli | University of Dammam, College of Science. |
| Tiago A. Almeida | Universidade Federal de São Carlos |
| Divya Vikash | The LNM Institute of Information Technology |
| Bilal Khan | COMSATS Institute of Information Technology |

---

## Similar Questions

**What is the difference between linear and nonlinear classification techniques?**
Like Linear Discriminant Analysis is linear and ANN and SVM are nonlinear. What are the parameters/factors on which it is being decided that...
17 answers added

**How to find semantic similarity between two documents?**
I am working on a project that requires me to find the semantic similarity index between documents.  I currently use LSA but that causes...
7 answers added

**K modes clustering : how to choose the number of clusters?**
Dear all,
I am looking for a proper method to choose the number of clusters for K modes.
I tried to find the optimal number of clusters by...
14 answers added

**How to convert the C, C++ code to java?**
Can anyone help me to convert this code to java or javascript?
15 answers added

**Can you export the results of Google Scholar search to excel?**
Exporting the list of papers to Excel allow you to sort papers and delete duplicates
24 answers added

**What is the best distance measure for high dimensional data?**
Inspired by Aggarwal et al.`s paper "On the Surprising Behavior of Distance Metrics in High Dimensional Space" the question arises which distance...
41 answers added

**Which measure of inter-rater agreement is appropriate with diverse, multiple raters?**
I want to calculate and quote a measure of agreement between several raters who rate a number of subjects into one of three categories. The...
19 answers added

**Does anybody know how we can add the missing citations to our profile in Google Scholar?**
There are several articles and textbooks that cite my articles but are not included as citations in my Google Scholar profile. Google Scholar says...
144 answers added

**Difference between Corresponding author and First author and what are all their responsibilities?**
.
88 answers added

---

| Reads | Followers | Answers |
|---|---|---|
| 2.42k | 20 | 17 |

---

## Related Publications

**PSI-Toolkit — an Extensible and Tightly Integrated Set of NLP Tools**
[Show abstract] [Hide abstract]
ABSTRACT: The paper reports on PSI-Toolkit, an extensible set of NLP tools developed at Adam Mickiewicz University in Pozna´nPozna´n. All processors of the toolkit operate on a common data structure called PSI-lattice. This feature allows the seamless incorporation of NLP tools created by other researchers. PSI-Toolkit is licensed under LGPL, which allows for unrestricted commercial use.
Full-text · Chapter · Jan 2015
Krzysztof Jassem, Filip Graliński, Marcin Junczys-Dowmunt, +1 more author..., Paweł Skórzewski
Read full-text

**Data Mining Pubmed Using Natural Language Processing to Generate the ?-Catenin Biological Association Network**
Full-text · Chapter · Sep 2011
Fengming Lan, Xiao Yue, Lei Han, +1 more author..., Peiyu Pu
Read full-text

**Mining from Incomplete Patterns**
[Show abstract] [Hide abstract]
ABSTRACT: Often in higher order data mining (HOM) applications we need to use incomplete patterns received from different sources. In this paper, a solution is proposed for mining new patterns from incomplete or corrupted patterns received from the sources. The solution is based on a relation representation for the patterns, this representation may be used both for pattern discovery from incomplete information, and also for higher order data mining from sources with different competences as presented in [13].
Conference Paper · Aug 2009
Adrian Onet
Read

---

© 2008-2018 ResearchGate GmbH. All rights reserved.

About us · Help Center · Careers · Developers · News · Privacy · Terms · Copyright · Impressum | Advertising · Recruiting

or

Discover by subject area

Join for free

Log in
