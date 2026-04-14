# Giving the Artisanal Language Model a job

A defining feature of an ALM is that it is purpose built for a well-defined
task. So far the task has only been described in general terms: proofreading
English prose of a novel draft.

It’s time to get more specific about what this ALM will do, what
its inputs and outputs will be, so that I can actually start building it.
It’s also time to define some tests and performance measures.
I’ll need them when I have something running and I make a change;
I’ll need some way to measure whether it got better.

## Inputs

After the ALM has been trained, I’ll want to feed it text to proofread.
To start with I’ll plan to do this through the simplest and clunkiest way
I can think of: passing it the path to a text file containing the text
to be proofread. In an actual professional product built for users,
this is probably not ideal, but it’s a nice generalizable front door
that slicker user interfaces can be built around in the future.

## Outputs

After the proofreader has done its job and identified segments that might
need correction, those segments will be reported as positions in
the input text. Specifically, when the text file is read in as a string,
the index of starting character position and ending character will be used
to tag segments for inspection and correction.
Position of the suspected error will be reported as a pair of indices.
This collection of start/finish pairs will be the output of the proofreader.

There are a lot of other things that could be enhanced about this to provide
a good user experience, and I leave the door open to add those later.
For instance, the text file could be modified to include special characters
marking the suspect segments. Or a fancier graphical UI could simply
highlight the potential errors or underline them, as is common in
word processors. An even fancier extension could propose corrections
and offer the user a single keystroke way to select from a number
of suggestions. But all of these could be built on top of a pair of
start and end markers for each proofreading note.

## Evaluation

I’ll need a way to evaluate the progress. If I try to enhance my
proofreading model, how will I know if it worked? The variety
of all possible text to be proofread is so large, it’s impossible to test
every variation exhaustively. The best I can hope to do is come up with is
a representative sample.

This falls somewhere in between the traditional software engineering practice
of testing, where the notion of right and wrong answers and what a function
must do is fairly clean cut, and bench marking, which is a consensus
driven measure for comparing solutions in a broadly recognized way.
It’s what has come to be known in LLM development as evaluations or,
more affectionately, **evals**.
Evals are a reasonable sample of the space in which a language model
is expected to work. They lack the recognition and respect has
a full-blown benchmark, and also lack the rigor and confidence of carefully
designed tests. But despite having the worst of both worlds,
evals operate in a space that we cannot ignore, and for which there is
no better solution that I know of.

In practice, evals are organic. They grow to cover new use cases
and new failure modes during the development process. But it’s helpful
think through a reasonable initial set. For proofreading there
are several classes of errors that are important to cover.

- **Spelling**. Febuary. Febrewary. Februry. Fabuwary.
- **Word choice**. Catching when it should be "imply" and when it should be "infer".
To/two/too. There/their/they're.
- **Punctuation**. Appropriate sentence termination. Comma usage.
Quotation mark usage.
- **White space**. Extra spaces. Spaces around punctuation. Weird indents.
- **Capitalization**.
- **Grammar**. Verb tense. Pronoun-antecedent agreement.
Preposition choice.

These aren’t exhaustive, but there’s no need for evals to be exhaustive
in order to be useful. I will almost certainly add more later as I
discover new categories that aren’t getting picked up well.
But they are a good place to start.

## Creating evals for each category

In practice, to test how well a given language model performs in each of
these areas, I’ll need to create an evaluation data set. For each of the
areas above, I’ll pull five paragraphs arbitrarily from an evaluation text
(Frankenstein by Mary Wollstonecraft (Godwin) Shelley) and throw 10 errors into
the text of a given type. Having five paragraphs full of spelling errors
gives a total of 50 spelling errors to detect. Each paragraph will come
with its own answer key, the beginning and end of each word or phrase
containing the error. After the proofreading model processes the paragraph,
the errors it detects will be compared against the ground truth.

- A ground truth error that is overlapped by at least one model detected-error
is considered detected (**true positive**). This is not quite the same thing as
- A model-detected error that overlaps at least
one ground truth error. This is considered an accurate detection, but there
may be several of these per ground truth error. I can't use this as the
true positive count because it could result in inflated counts.
- A model-detected
error that doesn’t overlap a ground truth error will be considered
a **false positive**.
- A ground truth error that is not overlapped by at least
one model detected error will be considered a **false negative**.

![Examples of true positives, false positives, and false negatives.
](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/alms_task/errors_pos_neg.png)

**Recall** will be defined as the total number of model-detected ground truth
errors (true positives) over the total number of ground truth errors
(true positives plus false negatives).

**Accuracy** will be a total number of model-detected ground truth errors
(true positives) divided by the total number of true positives
plus false positives. When there are no true positives or false positives,
accuracy will be undefined.

## Creating the evaluation dataset

Putting this into computer-readable form required creating a Python script
with some error-ridden example text and the locations of the errors.
I created
[the initial set of evals for spelling errors](https://codeberg.org/brohrer/alms/src/commit/57294820c5035a0be140d54e7f07b6a470c31c7e/data/eval/spelling.py),
but held off on creating evals for the other error types (punctiation,
capitalization, etc.) for now.
By the time you read this, there is a good chance it will already have evolved.
If that's the case, you can find
[the latest version here](https://codeberg.org/brohrer/alms/src/branch/main/data/eval/spelling.py).
The evaluation dataset is a list of dicts, each of which contain a paragraph
of text taken from a different chapter of Frankenstein which I modified to
contain ten spelling mistakes. It also contains a list of ten
dicts, each containing

- the mis-spelled word
- the index of its first and last character
- the corrected version of the word

Here's a snippet of the result

```
evaluation_dataset = [
    {
        'source': 'Frankenstein',
        'chapter': 'L1',
        'paragraph': """
I am already far north of London, and as I walk in the streets of
Petersburgh, I feel a cold northern breeze play upon my cheeks, which
braces my nerves and fills me with delight. Do you understand this
feeling? This breeze, which has travelled from the regions towards
which I am advancing, gives me a foretaste of those icey climes.
Inspirited by this wind of promise, my daydreams become more fervent
and vivid. I try in vain to be persuaded that the pole is the seat of
frost and desolation; it ever presents itself to my imagniation as the
region of beauty and delight. There, Margaret, the sun is for ever
visible, its broad disk just skirting the horizon and diffusing a
perpettual splendour. There—for with your leave, my sister, I will put
...
requisite; or by ascertaining the secret of the magnet, which, if at
all possible, can only be effected by an undertaking such as mine.
                """,
        'mistakes': [
            {
                'first_char': 322,
                'last_char': 325,
                'wrong_text': 'icey',
                'correct_text': 'icy',
            },
            {
                'first_char': 526,
                'last_char': 536,
                'wrong_text': 'imagniation',
                'correct_text': 'imagination',
            },
            {
                'first_char': 678,
                'last_char': 687,
                'wrong_text': 'perpettual',
                'correct_text': 'perpetual',
            },
            ...
        ]
    },
]
```

## End-to-end prototyping

It’s fair to ask why I don’t go ahead and complete the evaluation datasets
for the other types of errors. It seems logical to completely finish this
step before moving onto the next. We can imagine this as a breadth-first
solution to the problem, thoroughly working through one stage of development,
putting some polish on it before moving to the next. When this work is
spread across teams, this is called waterfall style development. One team
completes a whole stage of the project like design or backend support
before passing it onto the next.

The alternative to this is a depth-first development strategy.
Building a bare bones end-to-end solution and then adding breadth and
sophistication to it in subsequent passes. Starting with an end-to-end
prototype means leaving a lot of things incomplete in the first pass.
It means creating something that you would be embarrassed to show to
your friends. If you’re working across multiple teams, it means a whole lot
more communication up front.

In theory, both of these approaches are valid and will produce a good result
in similar timeframes. But in practice, they don’t. The waterfall approach
assumes that all of the work done at each stage gets to remain in its
final form. In fact, every additional stage teaches us things we didn’t
know about what needed to come before. This requires a lot of rework on
stages that we had previously thought were complete. In an end-to-end
prototyping approach this rework happens quickly. The whole project has
a lot less momentum and can pivot more gracefully. It is more agile.

This lesson can take a long time to learn, and in some cases, it is in
managers' interest to ignore it, depending on the incentives of
the organization. But since I am all of the engineering teams and all
of the levels of management for this project I get to decide:
We’re going to start with a lightweight end-to-end prototype.

So now that the spelling evals are done, onto the next stage---building a
model to detect misspelled words. 
