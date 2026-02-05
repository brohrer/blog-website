# What does a Data Scientist do in 2026?

I became a data scientist in 2013 when the title was young.
It was so new that most companies had no idea what a data scientist should
be doing, only that they desperately needed one or they would be left behind.
Sound familiar?

## A brief and biased history of the Data Scientist role

### In the beginning...

When data science first got huge organizations expected
data scientists to spin straw into gold---to transform
unorganized data archives into profit. Big Data, it was believed,
held inherent value, which only needed to be coaxed into cash form.
This rarely panned out, so the
approach evolved into a) data scientists produce "insights" and then
b) "insights" generate profit. This also proved elusive in the end.
Eventually data scientists settled into various niches involving
*answering questions using data*, and some companies decided they didn't
need as many data scientists as they had originally thought.

### The Neural Network era

Then came the Neural Network revolution, where the machine learning
hammer of choice became the convolutional neural network and many
problems got recast as an image recognition problem. The software
engineering, data engineering, and operations engineering that production
CNNs required merited the job title of Machine Learning Engineer.
Image recognition became synonymous with "modern machine learning".
A data scientist's job description got blurry. Did it include ML
Engineering as a subset? Should a good data scientist candidate have
CNN experience? Every team took their own stance. No consensus emerged.

### The age of Large Language Models

Then the spotlight abruptly shifted to Transformers and Large Language Models.
With their massive scale, the engineering and operations requirements
increased yet again. Only a small handful of enterprises are even
capable of training such a model, and they accomplish this only with
an army of engineers and an unfathomable amount of specialized computing
power. LLMs are effectively black boxes. Their structure is known but their
vast collection of parameters makes their behavior unpredictable and
inexplicable. Using them is a matter of API calls, rather than
training and evaluation. Most importantly, they are generative, rather than inductive. They
don't actually answer questions, they create answer-looking things that
are correct often enough to lull us into complacency.

LLMs are far enough removed from a core data scientist's skillset that
their care and feeding isn't part of the data science job description.
But they can still have a big effect on a data scientist's day.
(More on that below.)

### The next Big Thing

The next hot new trend has not yet emerged, but if the historical 5 year cycle
holds true, it's due any day now.

### The Before Times

On the pre-history side, the field of data science was named in 1997,
and the discipline has existed by other names
for a very long time. After all,
people have been answering questions using data for thousands of years.

## Answering questions with data

### Decision support: Which choice should I make?

### Experimentation: Which version is better?

### Personalization: Which one should I show you?

### Optimization: Which plan is the best?

Price optimization - how much should I charge this customer for this thing or
service?

Tip/donation recommendation - what suggestions should I give someone for how
much to give?

### Product experience: Which pages to users visit? What buttons to they click?
What features do they use? What does this tell us about how we can improve
their experience?

## The perrenial promise of self-serve

Every DS organization I've worked in has gone through this cycle:

1. Data scientists generate useful results
2. Stakeholders find them valuable
3. Stakeholders ask for more such results, with increasing frequency
4. DSs get tired of running similar queries over and over
5. A "self-serve analytics" function is proposed

I've never seen this approach solve the original problem of getting stakeholders
all the information they need without burdening the DSs. Either

- a basic self-serve system is fielded, which inevitably leads to follow-up
questions outside of its scope
- a complex self-serve system is fielded, which requires stakeholders to
learn a querying language, like SQL or a simplified version of it.
They don't, and DSs remain in the role of human user interface.
- DSs get deep into building an intuitive, highly capable
self-serve system. The project stope is large and they and aren't available
to field query questions of any sort.

## When stakeholders prefer a cheap, fast wrong answer to a good one

The biggest impact of AI (large language model) assistants on data science
is the idea that anyone can query data with natural language Q-and-A.
Sadly the reality of such systems is that they are trained on data
that doesn't share the same set of quirks and idiosyncracies that your
org is working with. It produces condifent, plausible answers 100% of the
time, but they are accurate only 70% of the time, and the problem is that
you can't know whether a particular answer is in the 30% until you
dive in and re-create the analysis yourself.

There is a school of thought that being confident and fast is better than
being cautious and correct. It has bled over from strategic leadership (where
ambiguity is ubiquitous and one of the greatest risks is indecision)
to analysis and engineering (where incaution can lead to loss of limb,
life, or money). And in most large organizations, individual stakeholders
don't often get to feel the effects of being wrong. Those usually take time to
materialize. So they can prioritize being fast and confident, which
their AI analytics queries are all to happy to help them out with.



