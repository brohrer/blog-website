# Empirical Design in Reinforcement Learning

A love letter to
[Empirical Design in Reinforcement Learning](arxiv.org/pdf/2304.01315) 
by Andrew Patterson, Samuel Neumann, Martha White, Adam White 
JMLR 25 (2024) 1-63 
(from this [Bluesky post](https://bsky.app/profile/brohrer.bsky.social/post/3lbmmmelles2t))

These aren’t the heroes we deserve, but they are the heroes we need.

I mean, look at this opening paragraph. This is written to be read and understood, not to impress and overwhelm. Not for the handful of reinforcement learning researchers in the world, but for the slightly larger handful of people trying to make it work on their machine.


![Reinforcement Learning, an Empirical Science
Running a good experiment in reinforcement learning is difficult. There are many decisions
to be made: How long should you run your agent? Should you count the number of episodes
or number of steps? Should performance be measured online or offline with test trials?
How should you measure and aggregate performance? Do we use rules of thumb to set
hyperparameters or some systematic search? What are the right baseline algorithms to
compare against? Which environments should you use? What does good learning even look
like in a given environment? The answer to each question can greatly impact the credibility
and utility of the result, ranging from insightful to down-right misleading](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_a.png "Opening paragraph from the paper")

The paper is refreshingly concrete, fully loaded with examples, case studies, recommendations, and pitfalls. It's a map to the landmines in reinforcement learning. It's what I would have gifted my younger self.


![Key insights: evaluating a fully-specified algorithm 1. A single agent’s performance is informative, however, consider plotting the performance of individual runs to gain additional understanding of your algorithm.  2. Agent behavior, with the same algorithm and environment, can be very different across random seeds. Consider reporting this variability using sample standard deviations or tolerance intervals, rather than just reporting the mean or median performance.  3. Confidence intervals around the mean primarily tell us about our certainty in our mean estimate, not about the variability in the underlying agents. If you primarily care about understanding mean performance, then report means with confidence intervals.  If you care about the behavior of each agent, not just the mean, then consider reporting tolerance intervals.  4. In general we advocate that you do not report standard errors. They are like a low-confidence confidence interval, and it is more sensible to decide on the confidence interval you want to report.  5. The required number of runs depends on your performance distribution, which is unknown to you. It is clear that in almost all cases 5 runs is insufficient to make strong claims, but even 30 runs can be insufficient if the distribution is heavily skewed.  6. Consider reporting performance versus steps of Interaction, rather than performance versus episodes. This choice ensures every agent receives the same number of samples every run. (See Section 2.1) 7. Choose the number of steps of interaction to reflect early learning or ability to learn the optimal policy, rather than inheriting what was done in previous work.  8. Aggressive episode cutoffs can significantly skew results.](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_b.png)

It's easy to lie to your readers in any ML work, but in reinforcement learning it's also easy to lie to yourself. The authors shine a bright light on all these sneaky backchannels. Designer's curse. Untuned baselines. Hypothesis After Results Known (HARK). Cherrypicking of all sorts.

![4.1 Designer’s curse: with great knowledge comes great responsibility
Evaluating your own algorithm is rife with bias. You know the ins and outs of your algorithm
better than anyone on the planet. You have spent months working with different versions of
your algorithm, tuning them for performance, finding environments where your algorithm
shines, and discarding ones where your algorithm does not. The baselines you eventually
compare against likely have not received the same attention. Worse, you will not have the
same detailed understanding of those baselines, nor knowledge of how to tune them well.
](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_c.png)

And for the love of the great Flying Spaghetti Monster DO NOT TUNE ON YOUR SEED. Just don't.

![Remember, the seed is NOT a tuneable hyperparameter.](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_d.png)

As an unexpected treat the authors have genuinely grown-up conversations with us about statistics. Reinforcement learning runs are so computationally intense and then add in hyperparameter sweeps, it's easy to see how representing distributions and confidence intervals falls by the wayside.
No more.

![A plot showing showing a bi-modal distribution of Return, P(M). There is a tall peak near -450 and a shorter peak near -325. 
Caption:
Figure 4: Performance distribution P(M) of DQN on Mountain Car
with stepsize=2 to the −9. The performance M is the final performance of the agent after 100,000 steps of learning. The density around values
for M represents the probability of an experimental trial yielding a
given outcome. For instance, if we run DQN for a single random
seed we will most likely observe an agent that achieves a return of
approximately -450 by the end of learning. This density is estimated
using 1000 independent DQN agents using the gaussian_kde kernel
density estimation function in scipy.
](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_e.png)

But the ride doesn't stop there. The authors take an ax to the root of the tree of ML leaderboard-based publishing. They make a strong case that reinforcement learning comparisons are all but infeasible to do in a meaningful way.

This low key refutes the entire ML conference industrial complex.

![4.3 Ranking algorithms (maybe don’t)
A common goal is to show that your new algorithm is better than some prior work. However,
providing supporting evidence towards this claim can be exceptionally difficult. In fact,
in all but the most rare cases, we might go so far as to say that providing such evidence
is entirely infeasible! The space of problem settings where any given algorithm may be
deployed is large and wholly unspecified; showing that any algorithm generally outperforms
another across this space would be impossible without first defining the space. Even once
this massive problem-space is well defined, gathering sufficient evidence to cover the space is
likely intractable](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_f.png)

The authors even take it a step further. If you can always choose environments in which your algorithm excels, then the interesting question becomes *which* conditions and *why*. 
Each RL algorithm is a special and unique snowflake. What if the real science is the quirks we discovered along the way?

![The aim should not be to show an
algorithm is good, but rather understand an algorithm’s properties, potentially
relative to other algorithms.](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_g.png)

As an absolute tour de force, the authors attempt what has so far only been dreamed of - reproducing results from another paper. They prove that it's not a path for the faint of heart, but they get there, and in style.

![Figure 16: Our attempt to run an experiment that closely resembles the principles laid out
in this document, particularly with respect to tuning baselines. For reference, the original
experiments Haarnoja et al. (2018) conducted with SAC on Half Cheetah have been inset.
DDPG has been tuned here for Half Cheetah. See text for details.](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/empirical_rl/img_h.png)
You like lists? The authors finish with a list of common errors in reinforcement learning experiments.

1. Averaging over 3 or 5 runs
2. Reusing code from another source (including hyperparameters) as is
3. Untuned agents in ablations
4. Not controlling seeds
5. Discarding or replacing runs
6. Cutting off episodes early
7. Treating episode cutoffs as termination
8. Randomizing start states
9. HARK’ing (hypothesis after results known)
10. Environment overfitting
11. Overly complex algorithms
12. Choosing gamma incorrectly
13. Reporting offline performance while making conclusions about online performance
14. Invalid errorbars or shaded regions
15. Using random problems
16. Not reporting implementation details
17. Not comparing against stupid baselines
18. Running inefficient code
19. Attempting to run an experiment beyond your computational budget
20. Gatekeeping with benchmark problems
 
and they note that this list will be appended to in an accompanying online blog post.

The only thing the paper lacked IMO was it should have ended with *mic drop*.

