# Training an Artisanal Language Model's tokenizer

The tokenizer is the first heavy duty processing that input data gets
exposed to when it churns through an LLM. The tokenizer takes the text
or audio or image and breaks it down into a sequence of bite-sized pieces
called tokens.

In theory, an LLM could operate on any discrete piece
of information, even fine-grained ones like characters, pixels, and bytes,
but in practice these are too small to carry much information individually
and working with them directly puts a greater burden on the model
to try to combine them and make sense of them. 

To give the models a leg up, the tiny pieces of input get pre-combined
into more useful bits called tokens. For instance, when processing a
string of English text like `How much wood could a woodchuck chuck?`, it
might be tokenized into `How much`, `wood`, `could`, `a wood`, `chuck`,
`chuck`, `?`. Tokens don't fall strictly on word boundaries and can contain
more than one word. Handling 7 tokens instead of 38 characters makes life
a lot easier for the stages that follow.

Tokenization is an example of feature engineering, specifically of
automated feature engineering, also known as feature learning or
feature discovery. It is well known among machine learning practitioners
that once you get a good set of features, you're 80% of the way to
solving your problem. It is an important step to get right, and has a huge
impact on the quality of results.

An advantage to an Artisanal Language Model with a curated data set is
that it gives an opportunity to create a model-specific tokenizer.
The representation of input data can be tailored to the needs of your
specific problem, instead of having to create something that could
potentially cover every conceivable question someone could ask and
task they could propose.

## Vocabulary

The collection of tokens that a tokenizer works with is called its
vocabulary. The tokenizers used by popular LLMs have vocabularies of
100,000 or more different tokens.

The size of the vocabluary is an important design parameter
that has a big effect on how big the model needs to be and how well it can
perform. A larger vocabulary means that word chunks and other pieces
of input can be bigger, saving the model the trouble of splicing them
together. It means that a given sequence of tokens can represent
a longer history of inputs. But it also means that the model has
a larger number of relationships to consider. Any given input token
might be predictive of any given output token, making the size of the
that space $O(N^2)$---something that grows as the *square* of the the
number of tokens. And when you add in the fact that it's not just
the current token, but the whole context history of tokens, that complexity
goes up further. (Attention is the magic trick that keeps it from
exploding catastrophically. More on that later.)

The flip side of this connection is that reducing a vocabulary to 10%
of its original size means that the demands on model reduce by far more than
that, down to something like 1% or 0.1%. The amount of training data needed,
the computation required, the inference time, all get reduced. The smaller
the vocabulary, the less time and expense to train and use a model.

Having an ALM focused on a single task with a curated data set makes
this possible. The more targeted the data set, the fewer the tokens
needed to represent it well.

All the numbers I mention above are very hand wavy because LLMs are so very
expensive to train and evaluate. I'm not aware of any research published
about the exactly nature of the relationship between
vocabulary size, number of model
parameters, and model performance. A smaller ALM that is feasible to
re-train a number of times make this investigation approachable.
It means that the tokenizer for a given ALM can be trial-and-error optimized
for its intended usage.

## Example use case: Proofreading English prose

Since the ALM is task-specific, the tokenizer can be chosen to be
match the task. So in order do choose the tokenizer it is first
necessary to define the task.

For the purposes of this example, the task is to proofread English
manuscript draft and highlight words or phrases
that might not be what the author intended. The manuscript will
be in the general vein of classic science fiction and fantasy.

The tokenizer will need some data to train on. The exact set of training
texts don't matter too much because it will always be possible to
retrain the tokenizer later. 
[Project Gutenberg](https://www.gutenberg.org) is a collection of Public
Domain books and a great place to collect a starter pack of training texts.
I pulled ten for training

1. Dracula by Bram Stoker
1. Hound of the Baskervilles by Arthur Conan Doyle
1. The Legend of Sleepy Hollow by by Washington Irving
1. The Lost World by Arthur Conan Doyle
1. Ozma of Oz by L. Frank Baum				
1. The Picture of Dorian Gray by Oscar Wilde
1. Seven Dials Mystery by Agatha Christie
1. The Time Machine by H. G. Wells
1. Twenty Thousand Leagues Under the Sea by Jules Verne
1. War of the Worlds by H. G. Wells

and set aside two for evaluation.

- Alice's Adventures in Wonderland by Lewis Carroll
- Frankenstein by Mary Wollstonecraft Shelley

## Choosing a tokenizer

There are a few common flavors of tokenizer, 
- Byte-Pair Encoding (BPE) (byte-level byte-pair encoding is a variation)
- WordPiece
- Unigram
- [SentencePiece](https://huggingface.co/papers/1808.06226)

These are described well in
[this summary by Huggingface](https://huggingface.co/docs/transformers/tokenizer_summary)

WordPiece splits on spaces, so it's a good fit for some languages
(including English), but not others (such as Chinese).
Default implementations of BPE assume space-delimitation too.
Unigram is similar to BPE except that
1) it starts with a huge set of token candidates and eliminates them,
rather than starting with non and adding them and 2) it chooses tokens
based on highest probability of co-occurrence, rather than raw frequency.
SentencePiece handles sentences as a whole, without assuming spaces
between words. It works in conjunction with BPE or Unigram to generate
tokens.

After looking through all the options, I decided to start with SentencePiece.
It is a good fit for the use case, and comes ready to use in 
[a repository](https://github.com/google/sentencepiece) from Google, also
available through PyPi.

## Training the tokenizer

Training a SentencePiece tokenizer is straightforward thanks to the public
repo and [the Python wrapper](https://github.com/google/sentencepiece/blob/master/python/README.md)
that can be installed with pip or `uv add sentencepiece`. It has a lot
of good defaults, so you can train a good tokenizer with a short call:

```
import sentencepiece as spm
spm.SentencePieceTrainer.train(input="training_file.txt", model_prefix="m")
```

And it is shockingly fast. I was pretty sure mine had errored out because it
finished in just a couple of seconds, but that's just how long it took.

A short demo shows that it's working.

```
sp = spm.SentencePieceProcessor()
sp.load("m.model")
test_sentence = "This is a test of the sentencepiece tokenizer."
test_pieces = sp.encode_as_pieces(test_sentence)
print(test_pieces)
test_ids = sp.encode_as_ids(test_sentence)
print(test_ids)

print(sp.decode_pieces(test_pieces))
print(sp.decode_ids(test_ids))
```

There are lots of options to tweak how the tokenizer works. At this point
there isn't a great way to say which is better. That can only happen
once it's connected to a language model and performing a task. But here
I'll note some variations and hyperparameters that will be worth
experimenting with.
There's [an exhaustive list here](https://github.com/google/sentencepiece/blob/master/doc/options.md)
for reference.

### `input`

This is the biggest one. It specifies the training data. You can include
multiple files in a comma-separated list like so
```
input="training_file_1.txt,training_file_2.txt,training_file_3.txt"
```

### `model_prefix`

This is just the name of the model files that get generated.
For `model_prefix="m"`, the files created are `m.model` and `m.vocab`.

### `vocab_size`

The total number of tokens to create, e.g. `vocab_size=40000`.

### `model_type`

Can be `unigram` (default), `bpe`, `char`, or `word`.
The input sentence must be pretokenized when using word type.

### `accept_language`

A comma-separated list of the languages of input sentences to include.
Others get rejected. For example

```
accept_language="english,spanish,chinese,russian"
```

### `shuffle_input_sentence`


### `split_by_whitespace`

### `normalization_rule_name`
