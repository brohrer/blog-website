# What does a Data Scientist do in 2026?

I became a data scientist in 2013 when the title was young.
It was so new that most companies had no idea what a data scientist should
be doing, only that they desperately needed one or they would be left behind.
Sound familiar?

I've tried to survey the job description of data science a couple of times with
varying degrees of success, most recently
to go with 
[some informal recommendations](https://github.com/brohrer/academic_advisory)
for creating data science degree programs.
Together with a group of colleages we tried to summarize
[what data scientists do](https://github.com/brohrer/academic_advisory/blob/main/what_DS_do.md)
and [the data science subtypes of maker, oracle, detective, generalist](https://brandonrohrer.com/data_science_archetypes.html).
But in the face of changing expectations this doesn't feel like enough
anymore. It's time for a refresh.

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

## What is "data science"?

I define data science as "answering questions using data". 
Also note that I am referring to lowercase-d data science here.
This can include job titles of Data Scientist, Data Analyst,
Quantitative Analyst, Data Engineer, and others.
I'm not including data-fueled features like product recommendations
or travel time estimates, which are typically the domain of
Machine Learning Engineers due to their scale and latency requirements.
These are typically dominated by a separate set of constraints, tools,
and skills (although there is plenty of overlap).

The questions data scientsts get to wrestle with are varied, and they
map closely to a company's org structure.

#### All organizations

- Decision support: Which choice should I make?
- Experimentation: Which version is better?

#### Product

- Personalization: Which one should I show you?
- Tip/donation recommendation: What suggestions should I give someone for how
much to give?
- Product experience: Which pages to users visit? What buttons to they click?
What features do they use? What does this tell us about how we can improve
their experience?
- Demand forecasting: How many people will buy my product next year?

#### Operations

- Optimization: Which plan is the best? How can I minimize inventory?

#### Marketing

- Price optimization: How much should I charge this customer for this thing or
service?
- Marketing Mix Modeling: What is the return on investment for each additional 
dollar spent in each of my marketing channels?

#### Finance

- Forecasting: What will our revenue and expenses be next quarter?

## What about Staff+ data scientists

A well-defined technical problem, including all those listed above, are
an excellent fit for the skills of a new data scientist or one with 3-5
years experience. These are quite challenging, but they are all
challenges you can train for and practice on.
They have fairly clear demands and success criteria.

Just like every other part of technology, the very hardest part is people.
In data science, this takes the form of understanding what people want,
setting their expectations, and coordinating misaligned or competing incentives.
Being familiar with sophisticated tools and approaches is definitely valuable,
but is often something that a data scientist with a couple years of experience
can do an excellent job on. It falls to more senior data folks to navigate
the uncharted and shifting terrain of stakeholder management, cross-team
coordination, and communication.

Disclaimer: for convenience. I’ll use the phrase "senior data scientist" here.
This is different than the job title with a capital S "Senior" common
in companies. Generally, I’m referring to staff level and higher, typically
folks who have been at it 5 to 7 years or more (although the actual time
in the role varies widely).

Most of these are struggles that data scientists have faced since
the beginning. Often, one of the biggest contributions that a senior
data scientist can make is to be a bridge between data science work
and the rest of the org---including engineers, marketing, finance, product, and
C-suite officers of all stripes. Senior data scientists are expected
to take the ambiguity out of the message, for instance translating what a
probability distribution means for reporting quarterly performance.

Here are the stickiest recurring topics I've been hearing about.

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
questions outside of its scope. DSs are answering more questions than ever.
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
that doesn't share the same set of quirks that your
org is working with. It produces condifent, plausible answers 100% of the
time, but they are accurate only 70% of the time, and the problem is that
you can't know whether a particular answer is in the 30% until you
dive in and re-create the analysis yourself.

There is a school of thought that being confident and fast is better than
being cautious and correct. 
It has bled over from strategic leadership (where
ambiguity is ubiquitous and one of the greatest risks is indecision)
to analysis and engineering (where incaution can lead to loss of limb,
life, and cash). And in most large organizations, individual stakeholders
don't get to feel the effects of being wrong. Those usually take time to
materialize. So they can prioritize being fast and confident, which
their AI analytics queries are all to happy to help them out with.

In almost every case, the overriding concern is not accuracy or rigor,
but rather someone rationally pursuing what is best for them and their team.
One of the hardest things a senior data scientist will ever have to do
is build a mental model of these incentives and chart a course that
successfully splits the difference
[between Scylla and Charybdis]()https://en.wikipedia.org/wiki/Between_Scylla_and_Charybdis).

## When stakeholders undervalue to skill and underestimate the time required

A closely related trend is a common assumption that data analysis has
somehow gotten easier and faster, so much so that it is disposable. 
Randy Au calls this
["data work in the fast fashion code era"](https://www.counting-stuff.com/data-work-in-the-fast-fashion-code-era/).
It's no big deal to extract nuanced insights from your collected data,
just feed it in to NotebookLM and ask, right? You should be able to have
something by this afternoon right? Not the full analysis of course, but
"rough numbers". Right?

I can't even come up with a rough number of the times I've had the conversation
that "rough numbers" are very rough indeed. Not just off by a few percent,
but maybe in the completely wrong direction. And there's no way to know for
sure until you go back and do the careful numbers.

It doesn't help that questions that seem easy are actually hard to answer well.
What caused this blip on this graph? Why didn't this feature boost engagement
metrics? It seems natural that there should be simple answers to these
questions, and obvious that someone familiar with the data should be able to
pull them out quickly. So when a data scientist starts talking about the
philosophical foundations of causality, and questioning whether we can really
know whether anything causes anything, you can literally feel the eye-rolling
of the product leader even if their camera is off.

## I want it now

In a separate but related issue, stakeholders are often reluctant to invest
the time required to get high quality results. Bullish demands for unrealistic
timelines have somehow become confused with strong leadership.
Conveying the return on that time investment is a recurring challenge.
How do you communicate the importance of carefully gathered data?
the return on a carefully run experiment? the cost of accurately attributing
a metric shift to a product change?
How do you advocate for six-month-plus time investments in
a company that never looks more than three months ahead?
And Heaven help you if you are trying to make a case for improving
the robustness of your pipelines or pre-emptively cleaning your data.

Learning things from data can be expensive. A carefully constructed
experiment takes time to plan and execute, particularly when data volumes
are low. There is a certain philosophy amongst some leaders that everything
should be experimented on, and than an experiment with a positive outcome
should be required before any change is made, no matter how small.
Communicating the opportunity cost of running an experiment is a regularly
occurring challenge. Leaders also may be seeking to proactively defend
themselves against challenges to a given decision by having receipts,
a successful experiment to point back to if their judgment is questioned.

## Real-time dashboards

One particular example of "I want it now" is common enough to call out on its
own: The up-to-the-minute data dashboard. The sense of power it gives is
intoxicating, so it's no surprise that it is such a commonly requested
data product.


How do you communicate the cost of real time data availability?

## 

Hard problems in data science.

Communication

How do you communicate uncertainty?
How do you communicate the gap between proxy metrics and actual impacts?

Coordination

How do you coordinate definitions, tools, practices, decision criteria across a large data science team? Across multiple organizations in the company?

How do you connect data science teams with work that lets them stretch their intellectual legs?

Epistemology
How do you help new hires release their death grip on academic standards of rigor?



How do you design KR’s to align with company goals?


Leadership communication

Most leaders don’t like it when numbers disagree with their intuition or expectations. As much as they profess to be dated driven, more often than not they seek to be data validated. If you get the answer, they expect, or a pleasant surprise, they will doubt it. If you come up with something surprising, disappointing, or uncomplimentary, they may push back question assumptions ask you to revisit it just changes to the approach we’re simply reject the result.
