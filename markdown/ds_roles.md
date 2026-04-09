# Being a Staff+ Data Scientist in 2026

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

The field of data science was named in 1997,
and the discipline has existed by other names
for a very long time. After all,
people have been answering questions using data for thousands of years.

When data science first got huge, organizations expected
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
map closely to a company's org structure. Here are some greatest hits.

#### Product

- Personalization: Which one should I show you?
- Tip/donation recommendation: What suggestions should I give someone for how
much to give?
- Product experience: Which pages do users visit? What buttons to they click?
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

#### All organizations

- Decision support: Which choice should I make?
- Experimentation: Which version is better?

## What about staff+ data scientists?

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
can do an excellent job on. As a staff+ you can still expect to tackle some
of the most challenging or time-sensitive technical tasks, but those
will probably not be the toughest part of your job.
It falls to staff+ data folks to navigate
the uncharted and shifting terrain of stakeholder management, cross-team
coordination, and communication.
(I'm using "staff+" to refer to staff level and higher, typically
folks who have been at it 5 to 7 years or more, although the actual time
in the role varies widely.)

Most of these are struggles that data scientists have faced since
the beginning. Often, one of the biggest contributions that a staff+
data scientist can make is to be a bridge between data science work
and the rest of the org---including engineers, marketing, finance, product, and
C-suite officers of all stripes. Staff+ data scientists are expected
to take the ambiguity out of the message, for instance translating what a
probability distribution means for reporting quarterly performance.

Here are the stickiest recurring topics I've been hearing about.

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
life, and cash). And in most large organizations individual stakeholders
don't get to feel the effects of being wrong. Those usually take time to
materialize. So they can prioritize being fast and confident, which
their AI-assisted analytics queries are all too happy to help them out with.

In almost every case, the overriding concern is not accuracy or rigor,
but rather someone rationally pursuing what is best for them and their team.
One of the hardest things a staff+ data scientist will ever have to do
is build a mental model of these incentives and chart a course that
successfully splits the difference
[between Scylla and Charybdis](https://en.wikipedia.org/wiki/Between_Scylla_and_Charybdis).

## When stakeholders undervalue the skill and underestimate the time required

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

In a separate but related issue, stakeholders are sometimes reluctant to invest
the time required to get high quality results. Bullish demands for unrealistic
timelines have somehow become confused with strong leadership.
Conveying the return on that time investment is a recurring challenge.
How do you communicate the importance of carefully gathered data?
the return on a carefully run experiment? the cost of accurately attributing
a metric shift to a product change?
How do you advocate for six-month-plus time investments in
a company that never looks more than three months ahead?
And heaven help you if you are trying to make a case for improving
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
On the surface, it seems like a reasonable request.  A leader looking at
a dashboard is like a pilot in the cockpit of a fighter jet.
They can see their instruments, look out the windows, and use all
the information at their fingertips to make quick decisions and save the day.
Of course they would want that information to be real time.
If it were delayed, then they might miss critical opportunities
and get shot down.

But an analytics dashboard is different than a fighter cockpit in more
than one way. The world it’s representing doesn’t meaningfully change
from one second to the next unless you’re doing high-speed trading.
In most cases, it barely changes from one day to the next. When that’s
the case, real time updates feel useful, but don’t deliver any
actionable information.

More importantly, the decisions that get made based on those dashboards
don’t get made minute-to-minute or even hour-to-hour. They are
typically decisions that factor into quarterly planning
or sprint planning---decisions that occur every few months or weeks.
Maybe every few days. Because of that, having the dash more update
frequently this does not drive better decisions.

The engineering effort required to go from nightly updates to few-second
latency are considerable. Nightly updates, or even hourly, can be done by
some DAG-based pipeline orchestror. It operates on tables and produces tables,
which are easy to read and write to in code. Real time updates involve
using stream technology, like Kafka or Flink. These are amazing when you
need them, but they have many more moving parts, more things that can break,
more things that you have to keep an eye on, more things that can cause
the pipeline to go down and the dashboard to get wonky and
require laborious backfills and carefully worded responses to frustrated
questions from leaders about why their nerve center dashboard suite
has gone down. To operate at the same reliability, it might require
3 to 5 times the effort and dollars.

This is a conversation that most staff+ data scientists end up having
at least once in their careers. And they usually lose.

## The perrenial promise of self-serve

Every data science organization I've worked in has gone through this cycle:

1. Data scientists generate useful results
2. Stakeholders find them valuable
3. Stakeholders ask for more such results, with increasing frequency
4. Data scientists get tired of running similar queries over and over
5. A "self-serve analytics" function is proposed

I've never seen this approach solve the original problem of getting stakeholders
all the information they need without burdening the data scientists.
One of these things happens instead.

- a basic self-serve system is fielded, which inevitably leads to follow-up
questions outside of its scope. Data scientists are answering more questions than ever.
- a complex self-serve system is fielded, which requires stakeholders to
learn a querying language, like SQL or a simplified version of it.
They don't, and data scientists remain in the role of human user interface.
- data scientists get deep into building an intuitive, highly capable
self-serve system. The project scope is large and occupies all of their
attention and is never quite finished.
They aren't available to field query questions of any sort.

## Communicating uncertainty

Statistics, the native language of the data scientist, is all about
distributions. But decisions get made based on concrete values.
A business decision maker may have a rule of thumb in their head like
“If the cost is less than three dollars, buy it, otherwise pass”.
So they ask a data scientist, how much it will cost.

DS: About three and a half dollars.

BDM: What do you mean "about"? What will the actual price be?

DS: Between two and five dollars.

BDM: That’s a huge range. But you’re saying it definitely won’t be less
than two dollars? And definitely not more than five?

DS: Well, no, it might be less than two or more than five.
But it probably won’t.

BDM: * Reaches for magic eight ball *

Translating from the fuzzy smear of a probability distribution
to concrete values to support decision making is one of the hardest things
a data scientist has to do. The two representations are fundamentally
mismatched, and the mental models required to reason about them are
nearly irreconcilable.

If your audience is familiar with gambling, this gives some useful
footholds like over-under and  odds ratios. Even better if they are
familiar with rolling 20-sided dice. You can also try using percentages,
statistical significance, confidence intervals, and upper/lower bounds,
and see which you have the greatest success with.

The more senior you get as a data scientist, the more of these conversations
you end up having, talking with people who haven’t spent years
building mental models of distributions.
This conversation is a recurring one. Some version of it occurs with every
analysis, and every decision. Bridging this gap well is what lets
the hard work of a data science team carry maximum weight in the rest
of the company. Learning to do it well is well worth it.

## Building within-team consensus on how things are done

Closely related is helping data science teams communicate about 
uncertainty consistently within themselves. New career data scientists
are usually taught frequentist null hypothesis significance testing.
The *p* &lt; .05 threshold is drilled into them as an axiom. As a rule
of thumb it’s useful, but as an iron law, it is limiting.
Another very useful thing a staff+ data scientist can do is help
the rest of the team look past the *p*-value and consider the context
of the decision. Talking through the cost of false positives and
false negatives, the likely distribution of classes in practice,
the opportunity cost of running long experiments in order to reach
significance, alternative ways of evaluating distributions
for decision-making. Helping the whole team to level up and to speak
the same language naturally falls on the staff+ data scientist
as a technical leader. 

This work extends to coordinating definitions, tools, practices,
and decision criteria more generally. There is tension between the
scientific freedom of allowing everyone to use the analyses, statistical
tools, modeling techniciques, presentation formats, and feature definitions
that they prefer, and the chaos that brings about. The larger the data
science team, the greater the chaos. Setting norms for these,
particularly across multiple organizations, is a big undertaking and
difficult to do in a way that doesn't feel heavy handed. Staff+ 
data scientists that are able to pull this off are rare but their impact
is huge.

## Collaboration with partner teams

Data scientists work as a specialized piece of a larger machine.
They work with
data analysts to define data models and metric definitions. They work with
data engineers to establish availability, freshness, data types, and
standard transformations. They work with infrastructure engineers to make
sure the data they need is accessible at reasonable latencies.
They work with frontend engineers to make sure important events are
instrumented and logged. They work with backend engineers to make sure
important events are logged there as well and sometimes to pre-compute
expensive features.

Data scientists are part of an interconnected web and can only do what they do
because of the other work that goes on around them. Coordinating with
these teams, supporting them in turn, keeping those communication
lines open and trust high.

## Designing a data science organization: Centralized vs Distributed

At a certain level of seniority in a small company, you may be asked to help
grow a data science team from scratch. Once the product team and the
marketing team and the finance team all see how useful a data scientist can be,
they'll each want their own team. A budding data science manager may prefer
to keep the team together under one umbrella, perhaps in the same org as
the analytics or the data engineering team. It is a recurring dilemma
of central vs distributed data science teams.

There is no right answer. Either can work *if* the organization is healthy
and incentives are properly aligned.  If not, than *neither* will work well.
But all else being equal, a central data science team that works closely
with other teams is the easiest to pull off. It's good for getting
data scientists the support they need and building capabilities
that are applicable across the company. It's natural to morph into a
matrixed arrangement from there, where a data scientist reports to their
DS manager, but attends a lot of team meetings with the specific team
they are embedded with.


## Delivering Disappointing Results

Most leaders don’t like it when numbers disagree with their intuition
or expectations. As much as they profess to be data-driven, more often
than not they seek to be data-validated. If you get the answer they expect,
they will accept and maybe celebrate it. If you come up with something
surprising, disappointing, or uncomplimentary, they may push back,
question assumptions, ask you to revisit it, suggest changes to the approach,
or simply reject the result.

There's no one size fits all answer to this, but here are some things to
watch out for.

- Don't assume that the stakeholder will be persuaded by a rigorous and
watertight analysis. They are balancing a lot of antagonistic concerns.
Correctness is just one of them.
- Don't assume that the stakeholder wants to know that real answer.
Sometimes the incentives to believe a difference answer are just too
compelling.
- Don't assume that the stakeholder doesn't want to know the real answer.
Pushback and follow up questions are a natural due diligence step.
When a result is surprising and will require a lot of work to acknowledge, some
questioning is appropriate.
- Don't assume the stakeholder is questioning your capabilities, motives,
or integrity.

Processing difficult analyses is a conversation, not a homework assignment
where you get to stick it to the professor. It works best when you approach
the leader as another human being who has their own biases, fears, and
goals. Talk it through. Expect to walk them through the numbers, re-run them,
examing your assumptions, and run some follow up analyses. More times than I
care to admit, these pushback sessions have exposed my blindspots and
resulted in more nuanced conclusions. At the very least, give the stakeholders
space to mourn their lost hopes.

-----

This list isn't exhaustive of course. Every company and team has its own
personality. But it gives a general flavor of the the life of a staff+
data scientist in 2026. Have I sold you on it?

## The good bits are very very good

With all of these sticky wickets, you might be wondering whether a
career in data science is even worth it. What I haven’t mentioned yet
is the upside, the marvelous feeling of being in the zone when your team
is working together with other teams in synchrony, bridging the chasm
between ones and zeros and the biggest decisions in the company.
At the staff+ level, this is very similar to the Zen of a software engineer
or a machine learning engineer who is in the zone, for all the same reasons.
There’s nothing quite like it. It’s a satisfaction you feel somewhere
deeply, somehwere just behind your sternum.
You'll have to answer this question for yourself, but for me, yes, it’s worth it.
