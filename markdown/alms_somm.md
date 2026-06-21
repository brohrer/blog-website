# Version 3: Second-order Markov model

The most straightforward way to extend the first-order Markov model is
to add an order and make it a second-order model. This means that instead
of matching token pairs it matches token triples. It's like using the
two most recent words to predict the third. It's surprisingly effective.
How would you complete these phrases?

- sugar and ...
- big bad ...
- PB and ...
- Guns and ...

You probably said "big bad wolf" (possibly "big bad bear" or
"big bad dude") but it probably wasn't "big bad artichoke" and
I'm certain it wasn't "big bad consider". The pattern set by two words
is stronger than the pattern set by one. Tokens aren't quite the same thing.
They are sometimes just parts of words and can include symbols and punctuation.
But the idea still holds.

Similar to first-order models, the occurrences of all three-token sequences
are counted up.
To get from counts to probabilities, the sequence count is divided by total
two-token prefix count. The probability that the next token after A and B
will be C is given by

P(ABC | AB) = count(ABC) / count(AB)

In pseudo-Python the count array is initialized as a three-dimensional array
of zeros

```
sequence_counts = zeros(dictionary_size, dictionary_size, dictionary_size)
```

and the counts are collected as the code walks the length of token ids
that make up the full tokenized training corpus.

```
for i_pair in range(len(token_ids) - 2):
    sequence_counts[
        token_ids[i_pair],
        token_ids[i_pair + 1],
        token_ids[i_pair + 2]
    ] += 1
```

To get the probabilities, the counts are summed across all final tokens (axis 2)
to get the total count of occurrences of the two-token prefix of the sequence.
Then the count of each sequence is divided by the count of its prefix.

```
sequence_probabilities = sequence_counts / sum(sequence_counts, axis=2)
```

## Memory management

Working with a three-token sequence means that the count and probability
arrays become three-dimensional. That means that the total number of
parameters jumps from the square of the tokenizer dictionary size
to its cube. What was a manageable 20,000 squared (400 million) is now
20,000 cubed (8 trillion), and my laptop doesn't have the 32 TB of RAM to handle
that many parameters.

With some trial and error I found that a dictionary size of 1,000, resulting
in a 1 billion element array, is somthing I can handle with a handful
of GB of memory. That means that the representation will be quite different
than it would be for a 20,000-element dictionary tokenizer. But we can
still run it on the evals and see how it stacks up.

## Performance

| model | name | capitalization | spelling |
| -------- | -------- | -------- | -------- |
| random |proof_01 | (5) 8 | (8) 16 |
| FOMM_00 |proof_02 | (7) 98 | (7) 98 |
| SOMM_00 |proof_03 | (6) 100 | (6) 98 |

Even with 1/20 th the dictionary, the second-order model performs
on par with the first-order model. The 98% and 100% recall, coupled with
the 6% precision, indicates that both the models are under-trained.
Most sequences they encounters are entirely novel to them, and so get
tagged as errors. They lack the eperience (training data)
to competently distinguish correct from incorrect writing.

## Doubling the training data

Currently, the models are all training on ten novels. It's telling
to create new versions of the models that have been trained on an
additional ten novels and compare the results.

I added the next ten most popular novels from the Project Gutenberg
[Science Fiction and Fantasy](https://www.gutenberg.org/ebooks/bookshelf/638)
category:

- The King in Yellow by Robert W. Chambers
- Thuvia, Maid of Mars by Edgar Rice Burroughs
- A Honeymoon in Space by George Chetwynd Griffith
- The Misplaced Battleship by Henry Harrison
- Gulliver's Travels by Jonathan Swift
- A Connecticut Yankee in King Arthur's Court by Mark Twain
- A Journey to the Center of the Earth by Jules Verne
- A Midsummer Night's Dream by William Shakespeare
- The Sex Life of Gods by M. E. Knerr
- The Crack of Doom by Robert Cromie

and I added a volume to the evaluation data collection

- The Call of Cthulhu by H. P. Lovecraft

Some of these I have never heard of before, unlike the first batch, all of
which I was familiar with.

The resulting first-order model with double training data I numbered
version 4 and assigned the second-order model version number 5.

The results on the doubled training data were underwhelming.
Recall mostly held constant, and precision ticked up by a single percentage
point. More training data is useful with these models, but it appears that it
is going to the a metric ton of the stuff to make a dent in performance
using these models.

| model | name | capitalization | spelling |
| -------- | -------- | -------- | -------- | -------- | -------- |
| random |proof_01 | (8) 12 | (10) 16 |
| FOMM_00 |proof_02 | (7) 98 | (7) 98 |
| SOMM_00 |proof_03 | (6) 100 | (6) 98 |
| FOMM_01 |proof_04 | (8) 100 | (8) 98 |
| SOMM_01 |proof_05 | (8) 100 | (7) 96 |

## Adding in an eval for punctuation

Writing evals is somewhat tedious so I'm spreading out the work,
adding them in gradually. Here's what the updated results look like
with
[a punctuation eval](https://codeberg.org/brohrer/proofread-eng-scifi/src/branch/main/evals/punctuation.py)
added in.


| model | name | capitalization | punctuation | spelling |
| -------- | -------- | -------- | -------- | -------- | -------- |
| random |proof_01 | (12) 26 | (14) 20 | (13) 24 |
| FOMM_00 |proof_02 | (7) 98 | (7) 98 | (7) 98 |
| SOMM_00 |proof_03 | (6) 100 | (6) 94 | (6) 98 |
| FOMM_01 |proof_04 | (8) 100 | (8) 98 | (8) 98 |
| SOMM_01 |proof_05 | (8) 100 | (7) 90 | (7) 96 |

The precision numbers for punctuation are consistent with the others,
showing a huge number of false positives consistent with an under-trained
language model. But the recall numbers are lower for the second-order
Markov models, which also have a smaller tokenizer dictionary and shorter
tokens. This suggests that some inaccuracies in punctuation only
become clear when more context is taken into account. A missing comma,
or an extra one, requires understanding the flow of a sentence.
I'll get to test this
in future verstions that incorporate more context, more tokens.

## Adding a heartbeat

One thing about working with models and data sets that strain the capacity
of your hardware is that they can be sloooow. A psychological trick for
not driving yourself insane is to add a heartbeat to the code. Something,
anything really, that prints to the terminal and gives a sense of continued
progress. For instance, while training models on 20 novels,
I started printing the name of each novel as it came up. Having something
happen every second or two is all you need. It's also a useful indicator
for when something has stopped working entirely. It can save you waiting for 90
minutes before you decide that the code has hung.

## Next steps

It feels like this is progress, but the proofreading performance gains
haven't hit yet. Time to try some new things.

- While second-order models seemed to be an improvement over first-order,
the practical limitations of storing an O(n^3) array limited the
tokenizer dictionary size. There other representations to try that are
more space efficient.
- Extending to third- and higher-order Markov models give more context,
allowing detection of more subtle errors.
- It appears the the amount of training data is laughably low. It's
time to think seriously about scaling it up. Doing this without
becoming an indisriminate data vacuum will require careful thought.
