# Version 2.0: First-order Markov model

It would be tempting to jump straight to a transformer-based language
model at this point, but that is a trap. There are a lot of small architectural
decisions to work out yet, and there are some wrinkles that still need
to be smoothed. Starting with simpler models helps to work through those
much more quickly. In simpler models
there are far fewer places for bugs to hide. Also,
we would be robbing ourselves of the satisfaction of seeing just how weak
the simple models are and how much performance we are buying by using
more computationally expensive models.

## How to train a Markov model

The next simplest model I can think of is a first-order Markov model
(a.k.a. [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) ).
It is the first baby step in the journey toward sophistication. The concept
behind it is that each token can be used to predict what the next token is likely
to be. There is a deeper dive into the mechanics as part of
[this post on transformers](https://brandonrohrer.at/transformers.html#markov_chain)
but the most important nugget to understand is that knowing the current token
gives a probability for each token that follows.

For example, let's say the word *jellybean* appears frequently in the training
corpus, and that there are two tokens involved, one for *jelly* and one
for *bean*. In the future when the model encounters the token *jelly*
it will assign a high probability to the following token being *bean*.
If it has also seen *jellyroll*, *jelly jar*, and *jellybelly*, then it will
also assign some probability to *roll*, *_jar*, and *belly*. But the more
often a sequence is observed, the more likely that sequence is predicted to be.

For brevity, I'll use short token names A, B, C, etc. instead of the text they
represent, *jelly*, *bean*, *belly*, etc. Markov models can be learned in a
straightforward way. Any time a two-token sequence is observed, note it.
Keep a running count of how many times is occurs in the training corpus.
For sequences starting with A, the counts might end up looking like AA=2,
AB=17, AC=0, AD=5, AE=1. In this example, the token A occurred a total of
25 times in the training data. 17 of those were followed by token B,
5 of those were followed by token D, etc.

To get from counts to probabilities, divide sequence count by total
token count. The probability that the next token after A will be B is
given by

P(AB|A) = count(AB) / count(A) = 17 / 25 = 68%

## Implementation

The bulk of the computing consists of crawling through the text and noting each
time every token pair occurs. This is most efficiently done in a single pass,
and incrementing the count of each pair as it occurs. A straightforward
way to track these is in a two-dimensional array, where each row
represents the first token in the pair and each column represents the second.
This implies that the array will need as many rows and columns as there
are tokens in the dictionary. For a dictionary size *n*, the count
array will have *n^2* elements. For *n* = 1000, this works out to one
million elements. This won't even make your RAM break a sweat. Even for
*n* = 10,000, this works out to 100 million elements, which is less than
1GB of memory. At the *n* = 100,000 point (ten billion elements), you
start to need a beefed up workstation and to be thoughtful about how
you operate on the array. Luckily the whole promise of ALMs is that small
is beautiful.

As of this writing the proofreading ALM is working with
a dictionary size of 20,000, which gives the first-order Markov model
400 million elements. Nothing burdensome.
Serialized with `pickle`, this saves to a 4.8GB file, and that's without
pulling out any tricks for compression or sparse coding.

You can follow along in
[the Python implmentation](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/src/proofread_eng_scifi/models/fomm/fomm.py).

In pseudo-Python the count array is initialized as zeros

```
pair_counts = zeros(dictionary_size, dictionary_size)
```

and the counts are collected as the code walks the length of token ids
that make up the full tokenized training corpus.

```
for i_pair in range(len(token_ids) - 1):
    pair_counts[token_ids[i_pair], token_ids[i_pair + 1]] += 1
```

To get the probabilities, the counts are summed across all columns (axis 1)
to get the total count of occurrences of the first token of the pair.
Then the count of each pair is divided by the count of its first token.

```
pair_probabilities = pair_counts / sum(pair_counts, axis=1)
```

In the actual implementation, a probability floor is added in, just so the
predicted probability never comes out to be zero. Systems can behave
strangely when something occurs that the model believed to be impossible.

Token pairs are also referred to as transitions. This is a Markov-related
term, as Markov models originated to describe transitions from one
state to the next.

## Spelling performance

Now that the model is trained, the burning question is how it compares
to the random baseline on the spelling evals.

| model | name | precision | recall |
|-------|------|-----------|--------|
| random | proof_01 | 0.10 | 0.22 |
| first-order Markov model | proof_02 | 0.07 | 0.98 |

Because the random baseline is random, it varies from run to run, and this
is just one sample run, but this gives a rough sense of how the first-order
Markov Model compares. Precision is lower, but not dramatically so.
Recall, however, is dramatically higher. This means that the first-order
Markov model calls a lot of false alarms, but it finds nearly all of
the actual errors in the process. That shows progress! And room for
improvement.

## Adding in Capitalization errors

Now is a good time to add another dimension to the evaluation.
I added a
[capitalization evaluation dataset](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/evals/capitalization.py),
structured similarly to the spelling evaluation set, with 50 errors
scattered throughout 5 paragraphs that the model was not trained on.
Both models' performance on these were very similar to the spelling eval.

| model | name | precision | recall |
|-------|------|-----------|--------|
| random | proof_01 | 0.09 | 0.16 |
| first-order Markov model | proof_02 | 0.07 | 0.98 |


## Automatically generating a table

Having two models and two evals, it's time to up the reporting game.
Keeping in mind that this will eventually need to extend to 6 evals
and an unknown number of models, some table reformatting helps
keep it compact. Also, because manually compiling a larger table
will be tedious and error prone, the `report_results()` function in
the [eval_proofreading.py](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/evals/eval_proofreading.py)
module got an upgrade, so that it generates the table in markdown format
automatically when `uv run `report_results.py` is run.

Here is everything in one place.

| model | name | capitalization | spelling |
| -------- | -------- | -------- |
| random |proof_01 | (9) 16 | (12) 22 |
| FOMM |proof_02 | (7) 98 | (7) 98 |

where the results for each model on each eval are shown as
`(precision %) recall %`. It's worth noting that false negatives
(failing to report an error) are worse than false positives (flagging
something that isn't an error). That implies that having a high recall
is more important than having a high precision, if we're forced to choose.
That said, single-digit precision means that more than 9 in 10
reported errors are not actually errors. The model is currently The Boy
Who Cried Wolf. It reports so many errors incorrectly that it is
not useful.

## Next steps

While the FOMM's recall numbers are excellent, the precision is abysmal.
It is spraying error detections machine gun-style, hitting the targets,
but also hitting everything else in the process. To get precision
higher there are a few things to try.

- A more sophisticated model. It's possible a second-order Markov model
will be an improvement.
- A larger training data set. Inspection of the model shows that the reason
so many errors are flagged is that there are a lot of token pairings that
the model has never run across in the training corpus. Ten books is a
hilariously small training set for a language model. Doubling this
and seeing what happens will be an interesting experiment.
- Adding more evals. Now that the structure for the evals seems to be
stabilizing it makes sense to invest the time in creating evaluation
data sets for a few more of them. Each eval category is qualitatively
different and may give new insights into the strengths and weaknesses
of each model.
