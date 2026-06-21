# Version 6: A sparse second-order Markov model

After some trial and error with a few sparse representation concepts,
I settled on one that takes advantage of one of Python's strengths:
dictionaries. The sparse second-order model keeps two running
dictionaries: one full of bigram counts and one for trigram counts.

## Representation

A bigram is a token pair. For the token sequence AKFLS, the bigrams are
AK, KF, FL, LS. And a trigram is a triple. The same sequence would
contain trigrams AKF, KFL, FLS. (More generally, n-grams have n tokens.)

Dictionaries tracking these have bi/tri-grams as keys and counts as
values. Any -grams not yet observed will not be in the dictionary at all,
which is what allows it to be sparse.

```
bigram_dict = {
    "AK": 1,
    "KF": 1,
    "FL": 1,
    "LS": 1,
}
trigram_dict = {
    "AKF": 1,
    "KFL": 1,
    "FLS": 1,
}
```

To save some more space in memory, instead of using the token text itself,
I took the list of token ids, which are integers, and converted it to
a tuple. There are ways to shrink this further, but they start to get
more convoluted and I'll wait until I bump up against the limits of this
scheme before I wrestle with them.

## Implementation

In order calculate the likelihood of a next token with this formula

`P(ABC | AB) = count(ABC) / count(AB)`

the count(ABC) and count(AB) can be looked up directly in their respective
dictionaries. The pseudo-Python has two dictionary lookups to estimate
the likelihood of F following AK.

```
likelihood = trigram_dict["AKF"] / bigram_dict["AK"]
```

[The full code](https://codeberg.org/brohrer/proofread-eng-scifi/src/commit/2655998848b58179545c73e5144ce51f23ce5b22/src/proofread_eng_scifi/models/somm/somm_sparse.py#L40)
adds in default values of 0 for any missing dictionary keys
and some small values for numerical stability.

## Training

A fun thing about using dictionaries is that they are fast in Python.
Training happens almost as fast as the data can be read from disk.
A dictionary read is a hash lookup which screams, even with large
dictionaries. It's O(1) for you computer science nerds.

I also noticed on closer inspection that my earlier implementation re-calculated
the transition probabilities after loading each book. This was unnecessary,
and constituted the bulk of the training computation.
Skipping this step streamlined the training considerably.

Training for the sparse model ended up quite fast fast and is  sospace efficient
that it allowed me to go back to using the full 20,000-element tokenizer.

## Performance

Unfortunately, moving to the larger tokenizer meant that tokens were longer
and three-token sequences were even less likely to re-occur. This means
that the proofreader was surprised by a lot of things. The recall was perfect.
Every single error got called out as an error. But the precision dropped to
an abysmal 4 percent. That means for every mistake it identified correctly,
it found 24 others that were not actually mistakes. 

| version | model | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- |
| 01 | random | (9) 16 | (7) 12 | (8) 16 |
| 02 | fomm_00 | (7) 98 | (7) 98 | (7) 98 |
| 03 | somm_00 | (6) 100 | (6) 94 | (6) 98 |
| 04 | fomm_01 | (8) 100 | (8) 98 | (8) 98 |
| 05 | somm_01 | (8) 100 | (7) 90 | (7) 96 |
| 06 | somm_02 | (4) 100 | (4) 100 | (4) 100 |

## moar data

The solution to this is to give the model a richer training data set.
It has so little experience at this point, that everything is novel.
The model needs to cram a lot more text into its representation to be able
to better separate correct prose from incorrect.

The temptation here is to indiscriminately scrape a truckload of data
and assume that the model will learn the right patterns from it. That is
antithetical to the Artisanal approach. This is a point where I get to
walk the walk and figure out a way to *thoughtfully* expand our data set.

I relied heavily on this
[helpful collection of Project Gutenberg tools](https://github.com/pgcorpus/gutenberg)
which helped me download a lot of raw text versions and compiled a csv
of their metadata. This gave me a foothold for reading in the information
and selecting the most relevant texts. Using
[a Python script](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/scripts/create_dataset_400.py)
I whittled the list of 80,000 books down to a subset that

- are text, not audio
- in English
- have "Science fiction" as a subject

That left a little of 3,000 titles. I also removed the titles I had
set aside as evaluation texts--Alice in Wonderland, Frankenstein,
and Call of Cthulhu. Due to the fact that my download of the archive
is only partial so far, that left me with 416 titles in the new training
corpus. (It's obnixous to put this much data
in a repo, so you'll have to take my
word for it.)

Also, in the spirit of investing in data qualityi, I preprocessed the texts
to remove the Project Gutenberg headers and footers, ensuring that
the models would be focused on learning the underlying data and not
fixating on artifacts.

After retraining the tokenizer, the first-order model (version 07),
and the second-order model (version 08) on the larger training corpus,
the evals show some changes.

| version | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- |
| 05 | (8) 100 | (7) 90 | (7) 96 |
| 06 | (4) 100 | (4) 100 | (4) 100 |
| 07 | (10) 96 | (9) 94 | (10) 100 |
| 08 | (6) 100 | (6) 98 | (6) 100 |

Performance values are shown as: (precision %) recall %

Comparing version 08 to version 06, the second-order model shows a
tiny bump in precision. Progress, yes, but not very much.

Comparing version 07 to version 05, the first-order model shows a
small bump in precision, but it's still pretty low. About one in ten
flagged errors is real. The
recall is still ridiculously high.
Punctuation again has the lowest
recall numbers, illustrating how difficult it is and how much context
it takes to punctuate well.

The high recall and low precision numbers
indicate that the models are too specific. Much of what they see are brand-new
to them because they have never seen those particular sequences
before. The larger the tokenizer alphabet, the
longer the chararacter strings represented by tokens, the rarer they will
each seem to be. A good way to illustrate this is by training
a set of second-order models using tokenizers with smaller dictionaries.

## Dictionary size

Shrinking the dictionary size used with the second-order model does
indeed bring up precision at the cost of some recall. This sequence
shows dictionary sizes of 10k, 5k, 2k, 1k.

| version | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- |
| 09 | (6) 100 | (6) 98 | (6) 100 |
| 10 | (7) 100 | (7) 94 | (7) 100 |
| 12 | (11) 98 | (9) 88 | (10) 100 |
| 13 | (17) 92 | (12) 74 | (16) 100 |

These show how precision and recall can be traded off against each other
to a certain extent by adjusting the alphabet size. But they are still
too low to be useful. (I fear the answer is LOTS more data.)

## Sparsify first-order model

The second order sparse model worked so well that I went back
and sparsified the first-order Markov model too.
Comparing the two shows that the performance is identical.

| version | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- |
| 07 | (10) 96 | (9) 94 | (10) 100 |
| 11 | (10) 96 | (9) 94 | (10) 100 |

Actually when I first ran these, the performance was NOT identical.
It was a head scratcher for me until a found a bug where I was setting
ther error detection threshold in two different places and the two did
not agree. It's another illustration of how testing and double checking
things that should obviously work is a great way to surface subtle bugs
in your code. And there is *always* another bug.

## Reporting

At this point the reporting table is growing large enough to merit splitting
into a performance table and a model summary table. Also, the variants
are proliferating, so it's helpful to keep track of the characterics
of each model so that patterns in what works, and doesn't work, can
start to emerge.

Here's what a sample of the model table and eval table look like

| version |model |description |tokenizer |alphabet |books |error cutoff |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| 09 | somm_04 | sparse 2nd-order Markov | 06 | 10k | 416 | 1e-08 |
| 10 | somm_05 | sparse 2nd-order Markov | 07 | 5k | 416 | 1e-08 |
| 11 | fomm_03 | sparse 1st-order Markov | 05 | 20k | 416 | 0.0005 |
| 12 | somm_06 | sparse 2nd-order Markov | 08 | 2k | 416 | 1e-08 |
| 13 | somm_07 | sparse 2nd-order Markov | 09 | 1k | 416 | 1e-08 |


| version | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- |
| 09 | (6) 100 | (6) 98 | (6) 100 |
| 10 | (7) 100 | (7) 94 | (7) 100 |
| 11 | (10) 96 | (9) 94 | (10) 100 |
| 12 | (11) 98 | (9) 88 | (10) 100 |
| 13 | (17) 92 | (12) 74 | (16) 100 |

## Registry

In fact the work is also reaching the point where pulling out information about
each model and how it was trained can be confusing and error-prone.
It is far me far beyond the point where I can just hold it all in my head.
Tracking model versions, variants, experiments, and their characteristics
is the job of a Registry. There are vendors ready to sell you ML Registry
products that have a lot of convenient features, but for a project of this
size all we need is a file where these things are written down.

I created a few version tracking files. There is now

- [one for proofreader versions](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/registry.py)
- [one for tokenizer versions](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/models/tokenizer/registry.py)
- [one for first order Markov model versions](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/models/fomm/registry.py)
- [one for second order Markov model versions](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/models/somm/registry.py)
- [one for random model versions](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/models/random/registry.py) and
- [one for training data corpuses](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/data_registry.py)

Having separate files for each, distributed across the repo nearby the
artifacts they are tracking, greatly simplified and robustified
the process of retrieving and collating information to make the
reporting charts. It was also a helpful data modeling exercise,
thinking through which tidbits belong where. For instance, whether
`error_threshold` is a characteristic of a Markov model or a proofreader.

These "registries" lack all of the convenience tooling for automatic
generation and population. I have to manually create each entry.
But the record they provide has already proven quite useful.

## New eval: Grammar

I will continue to eat my vegetables and add a new eval at each stage.
This time it is grammar. Things like verb tense, pronoun-antecedent
agreement, and preposition choice. As I went about injecting errors
into sample text, I found it hard to distinguish between purely
grammatical errors and errors of word choice, another category I planned
to create an eval for. As a result the grammar eval also includes
many examples of erroneous word choice.

Nothing jumped out to me about the models' performance on the grammar eval.
The models are all hypersensitive and fire off false positives far
too often to be anything approaching useful. But after this round of
machinations, there are a stable of 13 models and four evals, summarized
thus:

| version | capitalization | grammar | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- | -------- |
| 01 | (10) 18 | (12) 16 | (12) 24 | (6) 12 |
| 02 | (7) 98 | (8) 100 | (7) 98 | (7) 98 |
| 03 | (6) 100 | (7) 96 | (6) 94 | (6) 98 |
| 04 | (8) 100 | (10) 100 | (8) 98 | (8) 98 |
| 05 | (8) 100 | (8) 94 | (7) 90 | (7) 96 |
| 06 | (4) 100 | (5) 100 | (4) 100 | (4) 100 |
| 07 | (10) 96 | (12) 98 | (9) 94 | (10) 100 |
| 08 | (6) 100 | (6) 100 | (6) 98 | (6) 100 |
| 09 | (6) 100 | (7) 100 | (6) 98 | (6) 100 |
| 10 | (7) 100 | (8) 100 | (7) 94 | (7) 100 |
| 11 | (10) 96 | (12) 98 | (9) 94 | (10) 100 |
| 12 | (11) 98 | (11) 92 | (9) 88 | (10) 100 |
| 13 | (17) 92 | (15) 78 | (12) 74 | (16) 100 |

Performance values are shown as: (precision %) recall %

| version |model |description |tokenizer |alphabet |books |error cutoff |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| 01 | random_00 | random baseline | None | 0k | 0 | 0.05 |
| 02 | fomm_00 | 1st-order Markov | 00 | 20k | 10 | 0.0005 |
| 03 | somm_00 | 2nd-order Markov | 04 | 1k | 10 | 0.0005 |
| 04 | fomm_01 | 1st-order Markov | 00 | 20k | 20 | 0.0005 |
| 05 | somm_01 | 2nd-order Markov | 04 | 1k | 20 | 0.0005 |
| 06 | somm_02 | sparse 2nd-order Markov | 00 | 20k | 20 | 0.0005 |
| 07 | fomm_02 | 1st-order Markov | 05 | 20k | 416 | 0.0005 |
| 08 | somm_03 | sparse 2nd-order Markov | 05 | 20k | 416 | 1e-08 |
| 09 | somm_04 | sparse 2nd-order Markov | 06 | 10k | 416 | 1e-08 |
| 10 | somm_05 | sparse 2nd-order Markov | 07 | 5k | 416 | 1e-08 |
| 11 | fomm_03 | sparse 1st-order Markov | 05 | 20k | 416 | 0.0005 |
| 12 | somm_06 | sparse 2nd-order Markov | 08 | 2k | 416 | 1e-08 |
| 13 | somm_07 | sparse 2nd-order Markov | 09 | 1k | 416 | 1e-08 |

## Next steps

The round of improvements pushed Artisanal Language Model for
proofreading ahead a little, but there is still much to do. Then next
obvious step is to get a lot more data, but in a way that is consistent
with the goals of ALMs. And after that explore the next round of models.

