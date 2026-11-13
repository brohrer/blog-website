# Version 1.t (tuned): Getting models to work together part 2

I ended the [last installation](alms_blended.html) with the development
of tuned Markov models. That set things up for some exciting exploration
with a new set of tools.

## Add tuning data

I also called out the need for a second evaluation dataset, which I've
been referring to as a "tuning" data set to distinguish the two.
The first (`tuning`) dataset is for optimizing some of the
hyperparameters via the redsho algorithm, and the second (`eval`) dataset
is for optimizing the rest of them via manual trial-and-error. It's
worth noting that we still lack a proper testing dataset that would
evaluate how well the tool works on previously unseen data. I plan to
save that for a future installment.

The 6 categories of errors are represented by separate data files.

- `extra_word.py`
- `missing_word.py` 
- `capitalization.py` 
- `grammar.py`
- `punctuation.py`
- `spelling.py`

Previous to this, some categories had 100 error examples and others had 50.
To complete this initial split of tuning and eval, I fleshed out the other
4 so that all 6 categories had 100 examples, then split them evenly so that
there are 50 examples each in tuning and eval datasets.

(This is easier said than done. I confess it is the most tedious part
of this development.)

## Retrain and re-run

With the change in tuning data set, the tunable models in play need
to be tuned again. Also, the performance numbers now include an F-score.
For the tuning of the models, I used F-.5, to indicate that for a single
model recall was half as important as precision. When individual
models are combined, precision usually goes down and recall usually
goes up. For the composite model, I chose F-2, indicating that
recall is twice as important as precision. It means I would happily
allow two false positives in order to ensure an additional true
positive. This is a design choice. I want the proofreader to be able to
catch as many errors as possible, even if two out of every three
reported errors ends up being a false alarm.

| version | capitalization | extra words | grammar | missing words | punctuation | spelling | overall |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; &nbsp; **017**<br>precision<br>  recall<br>  f-score | <br>0.70<br>0.32<br>0.36 | <br>0.79<br>0.38<br>0.42 | <br>0.29<br>0.04<br>0.05 | <br>0.58<br>0.22<br>0.25 | <br>0.36<br>0.08<br>0.09 | <br>0.64<br>0.18<br>0.21 | <br>0.56<br>0.20<br>**0.23** |
| &nbsp; &nbsp; **018**<br>precision<br>  recall<br>  f-score | <br>0.69<br>0.36<br>0.40 | <br>0.81<br>0.34<br>0.38 | <br>0.10<br>0.02<br>0.02 | <br>0.50<br>0.12<br>0.14 | <br>0.60<br>0.12<br>0.14 | <br>0.75<br>0.24<br>0.28 | <br>0.58<br>0.20<br>**0.23** |
| &nbsp; &nbsp; **019**<br>precision<br>  recall<br>  f-score | <br>0.59<br>0.44<br>0.46 | <br>0.72<br>0.46<br>0.50 | <br>0.18<br>0.06<br>0.07 | <br>0.50<br>0.26<br>0.29 | <br>0.39<br>0.14<br>0.16 | <br>0.61<br>0.28<br>0.31 | <br>0.50<br>0.27<br>**0.30** |

The three proofreaders reported here are a forward first-order model, `017`:

```
pr017, combo=min, cutoff=1.0
    mm01, Tunable forward 1st-order Markov, alpha=4.64, beta=16, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
```

a backward first-order model, `018`:

```
pr018, combo=min, cutoff=1.0
    mm03, Tunable backward 1st-order Markov, alpha=1.0, beta=0, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
```

and a composite of the two, `019`:

```
pr019, combo=min, cutoff=1.0
    mm01, Tunable forward 1st-order Markov, alpha=4.64, beta=16, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
    mm03, Tunable backward 1st-order Markov, alpha=1.0, beta=0, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
```

This shows clearly what we had hoped: that the combination
of individually-tuned forward and a backward models performs better than
either individually. The overall F-scores of the individual models are both
0.23. The F-score of the ensemble is 0.30, a 30% improvement!

The other thing that this illustrates is that the alpha and beta values
that fall out of the tuning process are different for each model.
This helps show the usefulness of tuning at the model level, instead of
the ensemble level, allowing each model to find the combination that
works best for it in isolation before combining.

## Explore tokenizer alphabet size

One quantity that doesn't get tuned on individual models is the alphabet
size of the tokenizer used. That's a decision that has to be made
before the model is created. To learn about the effects of alphabet
size, it's necessary to create and train a new set of models each time.
Doing this is worth the effort. It reveals some new patterns.

| version | alphabet | capital. | extra | grammar | missing | punct. | spelling | overall |
| -------- | ------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; &nbsp; **022** <br>precision<br>  recall<br>  f-score | 10k | <br>0.53<br>0.34<br>0.37 | <br>0.86<br>0.48<br>0.53 | <br>0.25<br>0.34<br>0.32 | <br>0.92<br>0.22<br>0.26 | <br>0.69<br>0.22<br>0.25 | <br>0.54<br>0.26<br>0.29 | <br>0.63<br>0.31<br>**0.35** |
| &nbsp; &nbsp; **025** <br>precision<br>  recall<br>  f-score | 5k | <br>0.55<br>0.42<br>0.44 | <br>0.88<br>0.56<br>0.60 | <br>0.17<br>0.18<br>0.18 | <br>0.64<br>0.32<br>0.36 | <br>0.50<br>0.24<br>0.27 | <br>0.52<br>0.32<br>0.35 | <br>0.54<br>0.34<br>**0.37** |
| &nbsp; &nbsp; **028** <br>precision<br>  recall<br>  f-score | 2k | <br>0.45<br>0.48<br>0.47 | <br>0.78<br>0.64<br>0.66 | <br>0.14<br>0.20<br>0.19 | <br>0.50<br>0.34<br>0.36 | <br>0.35<br>0.22<br>0.24 | <br>0.47<br>0.34<br>0.36 | <br>0.45<br>0.37<br>**0.38** |
| &nbsp; &nbsp; **019** <br>precision<br>  recall<br>  f-score | 1k | <br>0.59<br>0.44<br>0.46 | <br>0.72<br>0.46<br>0.50 | <br>0.18<br>0.06<br>0.07 | <br>0.50<br>0.26<br>0.29 | <br>0.39<br>0.14<br>0.16 | <br>0.61<br>0.28<br>0.31 | <br>0.50<br>0.27<br>**0.30** |
| &nbsp; &nbsp; **031** <br>precision<br>  recall<br>  f-score | 500 | <br>0.34<br>0.40<br>0.39 | <br>0.48<br>0.46<br>0.46 | <br>0.20<br>0.18<br>0.18 | <br>0.38<br>0.26<br>0.28 | <br>0.29<br>0.30<br>0.30 | <br>0.31<br>0.32<br>0.32 | <br>0.33<br>0.32<br>**0.32** |
| &nbsp; &nbsp; **034** <br>precision<br>  recall<br>  f-score | 200 | <br>0.44<br>0.30<br>0.32 | <br>0.50<br>0.16<br>0.19 | <br>0.25<br>0.08<br>0.09 | <br>0.50<br>0.08<br>0.10 | <br>0.50<br>0.16<br>0.19 | <br>0.30<br>0.12<br>0.14 | <br>0.42<br>0.15<br>**0.17** |

The first thing that jumps out is that the 1k alphabet size used in the
previous table is far from the best performing one. By overall
F-score, the 2k alphabet beats it handily at 0.38. Another 27% jump!

There are also some intriguing differences between categories of
proofreading errors. Capitalization, spelling, extra words, and missing
words all show their peak F-scores at a 2k alphabet. (Although extra
words shows a matching F-score and considerably higher precision at 5k.)
Punctuation shows its peak at 500, but reasonable performance across
the spectrum. And grammar shows its peak at 10k,
dramatically higher than at any smaller alphabet.

This pattern is consistent with the fact that larger alphabets result in
longer tokens, many of them having two or more words. This gives a longer
context window, more information from which to make determinations.
Grammar errors in particular require the ability to look ahead or behind
for several words to determine whether the current word is a correct one.
Spelling on the other hand, can often be evaluated very locally just
from looking at a word in its entirety. Punctuation has a bit of both.
Some punctuation errors require an entire phrase to learn whether or
not a comma should be used, while the errant placement of an unusual
punctuation symbol can almost be flagged with no context at all.

As a side note, it becomes even clearer
that individual models benefit from being tuned
separately. The alpha, beta, and error threshold values vary quite a
bit between forward and backward models and across alphabet (vocab) sizes.

```
pr022, combo=min, cutoff=1.0
    mm04, Tunable forward 1st-order Markov, alpha=0.000464, beta=0, err=4.64e-06, books=38k
        tk06, vocab=10k, books=416, norm=identity, type=unigram, ws_split=False
    mm05, Tunable backward 1st-order Markov, alpha=0.0001, beta=0, err=2.78e-06, books=38k
        tk06, vocab=10k, books=416, norm=identity, type=unigram, ws_split=False
pr025, combo=min, cutoff=1.0
    mm06, Tunable forward 1st-order Markov, alpha=2.15, beta=0, err=1.29e-05, books=38k
        tk07, vocab=5k, books=416, norm=identity, type=unigram, ws_split=False
    mm07, Tunable backward 1st-order Markov, alpha=0.215, beta=0, err=7.74e-06, books=38k
        tk07, vocab=5k, books=416, norm=identity, type=unigram, ws_split=False
pr028, combo=min, cutoff=1.0
    mm08, Tunable forward 1st-order Markov, alpha=0.215, beta=27, err=3.59e-05, books=38k
        tk08, vocab=2k, books=416, norm=identity, type=unigram, ws_split=False
    mm09, Tunable backward 1st-order Markov, alpha=4.64, beta=0, err=3.59e-05, books=38k
        tk08, vocab=2k, books=416, norm=identity, type=unigram, ws_split=False
pr019, combo=min, cutoff=1.0
    mm01, Tunable forward 1st-order Markov, alpha=4.64, beta=16, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
    mm03, Tunable backward 1st-order Markov, alpha=1.0, beta=0, err=3.59e-05, books=38k
        tk09, vocab=1k, books=416, norm=identity, type=unigram, ws_split=False
pr031, combo=min, cutoff=1.0
    mm10, Tunable forward 1st-order Markov, alpha=4.64, beta=46, err=0.0001, books=38k
        tk11, vocab=500, books=416, norm=identity, type=unigram, ws_split=False
    mm11, Tunable backward 1st-order Markov, alpha=0.001, beta=0, err=0.000167, books=38k
        tk11, vocab=500, books=416, norm=identity, type=unigram, ws_split=False
pr034, combo=min, cutoff=1.0
    mm12, Tunable forward 1st-order Markov, alpha=0.00464, beta=215, err=0.000167, books=38k
        tk12, vocab=200, books=416, norm=identity, type=unigram, ws_split=False
    mm13, Tunable backward 1st-order Markov, alpha=0.00464, beta=77, err=0.000167, books=38k
        tk12, vocab=200, books=416, norm=identity, type=unigram, ws_split=False
```

Taken all together, this suggests that ensemble models that include models
with a variety of alphabet sizes may perform better still. Building this
will require some extra work, because so far proofreaders have operated
at the token level. This builds in the assumption that every model in
the ensemble is using the same tokenizer, and hence, the same alphabet size.
Combining tokenizers will require first migrating the representation of
detected errors to the character level.

Yet another avenue this opens up is combining tokenizers with different
normalization options. Normalization such as collapsing whitespace,
removing punctuation, and casting to lower case, can obscure some errors
but accentuate others. The ability to combine models that take different
normalization approaches can exploit the strengths of both.

## Skip-gram models

But before we get to that, there is an even lower hanging piece of
fruit. So far, the first-order Markov models used have looked at
consecutive tokens---the conditional probability of token *n*, given the
occurence of token *n*-1. There's no reason we couldn't also look at
the relationship between token *n* and *n*-2. Or *n*-3. Or *n*-7. Skip-grams
reveal patterns that consecutive n-grams can miss. At the very least, it's
worth trying them out.

Extending the models to forward and backward skip-1 first order Markov models
shows some fun relationships.

| version | type | capitalization | extra words | grammar | missing words | punctuation | spelling | overall |
| -------- | -------- |  -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; &nbsp; **035**<br>precision<br>  recall<br>  f-score | skip-1 <br> fwd | <br>0.12<br>0.44<br>0.28 | <br>0.25<br>0.54<br>0.44 | <br>0.07<br>0.24<br>0.16 | <br>0.13<br>0.32<br>0.25 | <br>0.09<br>0.32<br>0.22 | <br>0.09<br>0.28<br>0.20 | <br>0.12<br>0.36<br>**0.26** |
| &nbsp; &nbsp; **036**<br>precision<br>  recall<br>  f-score | skip-1 <br> bak | <br>0.22<br>0.28<br>0.26 | <br>0.32<br>0.24<br>0.25 | <br>0.09<br>0.12<br>0.11 | <br>0.23<br>0.16<br>0.17 | <br>0.22<br>0.24<br>0.24 | <br>0.22<br>0.22<br>0.22 | <br>0.22<br>0.21<br>**0.21** |
| &nbsp; &nbsp; **037**<br>precision<br>  recall<br>  f-score | skip-1 <br> fwd+bak | <br>0.11<br>0.50<br>0.29 | <br>0.25<br>0.62<br>0.48 | <br>0.08<br>0.34<br>0.21 | <br>0.14<br>0.40<br>0.29 | <br>0.11<br>0.42<br>0.26 | <br>0.10<br>0.38<br>0.25 | <br>0.13<br>0.44<br>**0.30** |
| &nbsp; &nbsp; **028**<br>precision<br>  recall<br>  f-score | skip-0 <br> fwd+bak | <br>0.45<br>0.48<br>0.47 | <br>0.78<br>0.64<br>0.66 | <br>0.14<br>0.20<br>0.19 | <br>0.50<br>0.34<br>0.36 | <br>0.35<br>0.22<br>0.24 | <br>0.47<br>0.34<br>0.36 | <br>0.45<br>0.37<br>**0.38** |
| &nbsp; &nbsp; **038**<br>precision<br>  recall<br>  f-score | skip-1 + <br> skip-0 <br> fwd+bak | <br>0.14<br>0.66<br>0.37 | <br>0.27<br>0.74<br>0.55 | <br>0.09<br>0.38<br>0.23 | <br>0.17<br>0.54<br>0.37 | <br>0.13<br>0.54<br>0.33 | <br>0.13<br>0.52<br>0.32 | <br>0.15<br>0.56<br>**0.37** |

Skip-1 models don't perform as well as skip-0 models, but when the two
are combined they achieve some pretty impressive performance, at least
in recall.

Trying skip-2 models shows more of the same. They perform so-so
individually. When combined with skip-1 and skip-0 models they can
keep the F-scores comparable, but with some impressive recall numbers.

| version | | capitalization | extra words | grammar | missing words | punctuation | spelling | overall |
| -------- |------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; **039**<br>skip-2<br>fwd | <br>pr<br>  rec<br>  f | <br>0.09<br>0.10<br>0.10 | <br>0.20<br>0.08<br>0.09 | <br>0.07<br>0.06<br>0.06 | <br>0.17<br>0.08<br>0.09 | <br>0.04<br>0.04<br>0.04 | <br>0.05<br>0.04<br>0.04 | <br>0.10<br>0.07<br>**0.07** |
| &nbsp; **040**<br>skip-2<br>back | <br>pr<br>  rec<br>  f | <br>0.06<br>0.20<br>0.14 | <br>0.12<br>0.22<br>0.19 | <br>0.07<br>0.20<br>0.15 | <br>0.10<br>0.28<br>0.20 | <br>0.09<br>0.26<br>0.19 | <br>0.08<br>0.24<br>0.17 | <br>0.09<br>0.23<br>**0.17** |
| &nbsp; **041**<br>skip-2<br>combo | <br>pr<br>  rec<br>  f | <br>0.07<br>0.28<br>0.18 | <br>0.12<br>0.28<br>0.22 | <br>0.07<br>0.24<br>0.16 | <br>0.10<br>0.34<br>0.23 | <br>0.08<br>0.28<br>0.19 | <br>0.07<br>0.28<br>0.18 | <br>0.09<br>0.28<br>**0.20** |
| &nbsp; **037**<br>skip-1<br>combo | <br>pr<br>  rec<br>  f | <br>0.11<br>0.50<br>0.29 | <br>0.25<br>0.62<br>0.48 | <br>0.08<br>0.34<br>0.21 | <br>0.14<br>0.40<br>0.29 | <br>0.11<br>0.42<br>0.26 | <br>0.10<br>0.38<br>0.25 | <br>0.13<br>0.44<br>**0.30** |
| &nbsp; **028**<br>skip-0<br>combo | <br>pr<br>  rec<br>  f | <br>0.45<br>0.48<br>0.47 | <br>0.78<br>0.64<br>0.66 | <br>0.14<br>0.20<br>0.19 | <br>0.50<br>0.34<br>0.36 | <br>0.35<br>0.22<br>0.24 | <br>0.47<br>0.34<br>0.36 | <br>0.45<br>0.37<br>**0.38** |
| &nbsp; **038**<br>skip-0+1<br>combo | <br>pr<br>  rec<br>  f | <br>0.14<br>0.66<br>0.37 | <br>0.27<br>0.74<br>0.55 | <br>0.09<br>0.38<br>0.23 | <br>0.17<br>0.54<br>0.37 | <br>0.13<br>0.54<br>0.33 | <br>0.13<br>0.52<br>0.32 | <br>0.15<br>0.56<br>**0.37** |
| &nbsp; **042**<br>skip-0+2<br>combo | <br>pr<br>  rec<br>  f | <br>0.13<br>0.62<br>0.36 | <br>0.25<br>0.68<br>0.51 | <br>0.08<br>0.38<br>0.22 | <br>0.16<br>0.60<br>0.39 | <br>0.12<br>0.46<br>0.29 | <br>0.11<br>0.46<br>0.28 | <br>0.14<br>0.53<br>**0.35** |
| &nbsp; **043**<br>skip-0+1+2<br>combo | <br>pr<br>  rec<br>  f | <br>0.10<br>0.74<br>0.33 | <br>0.18<br>0.76<br>0.46 | <br>0.07<br>0.50<br>0.23 | <br>0.13<br>0.72<br>0.37 | <br>0.10<br>0.64<br>0.31 | <br>0.09<br>0.62<br>0.29 | <br>0.11<br>0.66<br>**0.34** |

Because the F-scores, our measure of overall performance, don't go up
when including the skip-gram models, these results on their own don't
jusitfy adding the skip-grams to the proofreader. That's OK. The real value
here is the picture it gives about how precision and recall of two models
are reflected in the composite model when they are combined.

## Combined recall is higher than either model's recall

In the tables above, comparing two individual model rows against a third
in which they are combined shows that recall goes up almost every time.
If the recall of two models is dissimilar, their combination nevertheless
has a recall that is still a bit higher than either of the two. And if the
two models are comparable, the recall of their combined model can be almost
double that of the individual models.

For the proofreader this is very good news. An ideal proofreader has perfect
recall. Every mistake is highlighted for the author to evaluate and rethink.
Combining a wide variety of models shows promise as a way to get closer to
perfect recall.

## Precision regresses to the lower of either model's precision

On the other hand, the precision of a combined model falls between the
precision of the two individual models, and it tends to be much closer
to the lower of the two. This is fine if both models' precision is in
an aceptable range, but if even one component model has a low precision,
that can tank the precision of the whole ensemble.

This suggests that we should be watching precision very carefully. If a
model has a precision below the acceptable level it should not be included
because it will make it very difficult for the model to recover, no matter
how well any of the other component models perform.

It also suggests that models with a very high precision are a waste.
As mentioned, a precision of around one-half is acceptable. That means that
a user of the proofreader will have half false alarms, half real errors
flagged. I have deemed this an acceptable false positive rate for the
user experience I am aiming for. If a model has, say, a precision of
0.9, and gets combined with another that has a precision of 0.5, most of
that high precision will be lost. The worst part of that is that high
precision could have been backed off and traded for recall, which accumulates.

## Tuning models to be ideal contributors to the esnsemble

All of this combines to suggest that individual models should be tuned
to have precision in the desired range of the final model (say 0.5 to 0.6),
and the maximum recall it can achieve. The current training regimen doesn't
do this, but there are some changes that can get us closer to it.

One tweak we can do is penalize precision when it gets too high.
The math trick for this is to add a nonlinear transformation to precision.
For precision less than 2/3, multiply it by 1.5, and for precision
greater than 2/3, make it two minus 1.5 times precision.

&rho;<sub>new</sub> = &rho; * 3/2, for &rho; &le; 2/3<br>
&rho;<sub>new</sub> = 2 - &rho; * 3/2, for &rho; &gt; 2/3

This transformed
precision &rho;<sub>new</sub> reaches a maximum value
of one when &rho;=2/3, and when &rho;=1,
&rho;<sub>new</sub> = 0.5. When fed into the redsho optimization algorithm,
this will tend to drive the solution to a precision of around 2/3 and,
after reaching that constraint, a recall as high as it can reach.

I chose the target of 2/3 to give a little breathing room above 1/2, and
allow for noisiness in the tuning process. If that proves higher than
necessary, I'll go back and reduce it.

Another way to ensure proofreader performance is to put a hard limit
on component model precision. After models are tuned, only models with
precision higher than a floor, say 0.5, will be allowed to become part of
the proofreader model. This check lets us train and add as many model
variants as we like, as long as they meet this criterion, whoth reasonable
confidence that they won't hurt the performance of the overall model.
This second approach assumes that there will be plenty of models to
select from with a precision greater than 0.5, but so far that's only
aspirational. But we'll keep it in mind for when things get more mature.

## F-score correction: not &rho; but &rho;<sup>2</sup> 

Up until this point (in this very post!),
I explained erroneously that the &rho; parameter
in the F-&rho; score can be interpreted as a weight for recall. In fact it
is the *square* of &rho; that is the weight. So an F-2 score actually
weights recall four times more than precision.

For the final top line evaluation score, where I wanted recall to be 
weighted twice as heavily as precision, I realized this requires
a &rho; of 1.414, the square root of two. And after a round of trial and
error, I decided to stick with a &rho; of .5 for the tuning process.
Because the precision of one model is essentially the ceiling for precision
of the ensemble of models, pushing it as high as possible for each
individual model is helpful. Keeping it weighted four times heavier than
recall produced the best results.

During the experimentation, sadly, no combination of parameters or
optimization approaches I tried was able to get the skip-one or skip-two
models up to a reasonable precision. They were often down at .1 or lower.
For now, this makes them unsuitable for use in a proofreader, but I’ll tuck
this exploration away for future use. It’s possible that with a different
tokenizer or larger training data set, I may be able to get
those higher eventually

Re-running tuning on all of the no-skip Markov models and using F-1.414 as
the top line evaluation score, here’s what the combined forward-plus-backward
models look like for alphabets of various sizes. Several of the precision
values are at or near .5 which is a very pleasant surprise.

| version | alphabet | capital. | extra words | grammar | missing words | punct. | spelling | overall |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; &nbsp; **046**<br>precision<br>  recall<br>  f-score | 20k | <br>0.49<br>0.46<br>0.47 | <br>0.74<br>0.52<br>0.58 | <br>0.19<br>0.36<br>0.28 | <br>0.53<br>0.34<br>0.39 | <br>0.53<br>0.32<br>0.37 | <br>0.39<br>0.32<br>0.34 | <br>0.48<br>0.39<br>**0.41** |
| &nbsp; &nbsp; **022**<br>precision<br>  recall<br>  f-score | 10k | <br>0.51<br>0.44<br>0.46 | <br>0.81<br>0.58<br>0.64 | <br>0.24<br>0.42<br>0.34 | <br>0.64<br>0.28<br>0.34 | <br>0.62<br>0.26<br>0.32 | <br>0.49<br>0.34<br>0.38 | <br>0.55<br>0.39<br>**0.43** |
| &nbsp; &nbsp; **025**<br>precision<br>  recall<br>  f-score | 5k | <br>0.50<br>0.48<br>0.49 | <br>0.74<br>0.58<br>0.63 | <br>0.18<br>0.24<br>0.22 | <br>0.50<br>0.34<br>0.38 | <br>0.43<br>0.26<br>0.30 | <br>0.49<br>0.36<br>0.39 | <br>0.47<br>0.38<br>**0.40** |
| &nbsp; &nbsp; **028**<br>precision<br>  recall<br>  f-score | 2k | <br>0.43<br>0.48<br>0.46 | <br>0.75<br>0.66<br>0.69 | <br>0.14<br>0.20<br>0.17 | <br>0.50<br>0.36<br>0.40 | <br>0.31<br>0.22<br>0.24 | <br>0.41<br>0.34<br>0.36 | <br>0.42<br>0.38<br>**0.39** |
| &nbsp; &nbsp; **019**<br>precision<br>  recall<br>  f-score | 1k | <br>0.59<br>0.44<br>0.48 | <br>0.72<br>0.46<br>0.52 | <br>0.18<br>0.06<br>0.08 | <br>0.50<br>0.26<br>0.31 | <br>0.39<br>0.14<br>0.18 | <br>0.61<br>0.28<br>0.34 | <br>0.50<br>0.27<br>**0.32** |
| &nbsp; &nbsp; **031**<br>precision<br>  recall<br>  f-score | 500 | <br>0.34<br>0.40<br>0.38 | <br>0.47<br>0.46<br>0.46 | <br>0.20<br>0.18<br>0.19 | <br>0.39<br>0.28<br>0.31 | <br>0.29<br>0.30<br>0.30 | <br>0.31<br>0.32<br>0.32 | <br>0.33<br>0.32<br>**0.33** |
| &nbsp; &nbsp; **034**<br>precision<br>  recall<br>  f-score | 200 | <br>0.36<br>0.36<br>0.36 | <br>0.44<br>0.22<br>0.26 | <br>0.21<br>0.14<br>0.16 | <br>0.41<br>0.14<br>0.18 | <br>0.38<br>0.18<br>0.22 | <br>0.27<br>0.14<br>0.17 | <br>0.34<br>0.20<br>**0.23** |

It is notable
that these tend to occur across the spectrum of alphabet sizes,
except for the smallest alphabets. This is hopeful, because it also suggests
that these different models may be picking up on different patterns, and
that combining them will be fruitful. Unfortunately, this isn’t something
that I can do yet. Combining these models at the moment requires that
they use the same tokenizer, and therefore have the same alphabet.
Some additional legwork will be required to combine models
from different tokenizers.

## Exploring other tokenizer variants

We have reached the place where it’s useful to do a comparison against
some other tokenizer settings. So far, all of the tokens have used
identity normalization (that is, they have made no pre-processing change
to the text), unigram type tokenization, and no enforced splitting
at word boundaries. We justified these assumptions as a starting point
early on, but now we can actually test whether these were good choices.

| version | tokenizer | capitalization | extra words | grammar | missing words | punctuation | spelling | overall |
| -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| &nbsp; &nbsp; **022**<br>precision<br>  recall<br>  f-score | no normalization | <br>0.51<br>0.44<br>0.46 | <br>0.81<br>0.58<br>0.64 | <br>0.24<br>0.42<br>0.34 | <br>0.64<br>0.28<br>0.34 | <br>0.62<br>0.26<br>0.32 | <br>0.49<br>0.34<br>0.38 | <br>0.55<br>0.39<br>**0.43** |
| &nbsp; &nbsp; **049**<br>precision<br>  recall<br>  f-score | byte-pair encoding (BPE) | <br>0.64<br>0.54<br>0.57 | <br>0.91<br>0.60<br>0.68 | <br>0.25<br>0.30<br>0.28 | <br>0.75<br>0.30<br>0.38 | <br>0.59<br>0.26<br>0.32 | <br>0.47<br>0.34<br>0.38 | <br>0.60<br>0.39<br>**0.44** |
| &nbsp; &nbsp; **052**<br>precision<br>  recall<br>  f-score | split by whitespace | <br>0.50<br>0.34<br>0.38 | <br>0.80<br>0.40<br>0.48 | <br>0.24<br>0.40<br>0.32 | <br>0.53<br>0.20<br>0.25 | <br>0.63<br>0.24<br>0.30 | <br>0.48<br>0.32<br>0.36 | <br>0.53<br>0.32<br>**0.37** |
| &nbsp; &nbsp; **055**<br>precision<br>  recall<br>  f-score | NFKC normalization | <br>0.59<br>0.40<br>0.45 | <br>0.75<br>0.54<br>0.60 | <br>0.25<br>0.44<br>0.35 | <br>0.85<br>0.34<br>0.43 | <br>0.66<br>0.38<br>0.44 | <br>0.42<br>0.32<br>0.35 | <br>0.59<br>0.40<br>**0.45** |
| &nbsp; &nbsp; **058**<br>precision<br>  recall<br>  f-score | NFKC + case folding | <br>0.17<br>0.12<br>0.13 | <br>0.61<br>0.60<br>0.60 | <br>0.21<br>0.46<br>0.33 | <br>0.64<br>0.46<br>0.51 | <br>0.38<br>0.32<br>0.34 | <br>0.28<br>0.34<br>0.32 | <br>0.38<br>0.38<br>**0.38** |
| &nbsp; &nbsp; **061**<br>precision<br>  recall<br>  f-score | NFKC + BPE | <br>0.60<br>0.54<br>0.56 | <br>0.73<br>0.66<br>0.68 | <br>0.22<br>0.34<br>0.29 | <br>0.64<br>0.36<br>0.42 | <br>0.68<br>0.42<br>0.48 | <br>0.40<br>0.36<br>0.37 | <br>0.55<br>0.45<br>**0.48** |

Trying out of some of the other options available on an encoder
with alphabet size of 10,000 showed that
[byte-pair encoding](https://en.wikipedia.org/wiki/Byte-pair_encoding) and 
[NFKC normalization](https://en.wikipedia.org/wiki/Unicode_equivalence#Normalization)
both give a modest boost in performance, and combining them helps even more,
giving a respectable precision of 0.55, recall of 0.45, and F-score of 0.48.
These numbers still aren't good enough to ship, but they are getting closer.
A precision over 0.5 is good enough, but a recall of 0.45 means that it's
missing more than half the errors :grimace-emoji:. But I'm not worried.
Out bag of tricks is far from empty.

## Next steps

In the next installment, we get to tackle the big step of combining
the results of models that are based on different tokenizers. This has the
potential to meld complementary strengths of different models, like a
proofreading Voltron.

There will be other stuff too, but honestly I'm making this up as I go along.
We'll be surprised together.
