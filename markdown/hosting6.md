# Automating traffic control

In [my last post](hosting5.html) I said "Automating firewall updates will be
an adventure for another day." Today is that day. This is the latest in a
growing series on hosting your own static blog. (
[I](hosting.html),
[II](hosting2.html),
[III](hosting3.html),
[IV](hosting4.html),
[V](hosting5.html)
[VI](hosting6.html)
[VII](hosting7.html)
)


Protecting your website requires you to keep your eyes on it at all times.
That can get tiring. Sometimes you need to eat and sleep and maybe work
for a living. It can be useful to have automated helpers to fill those gaps.

## Detection

The first step in keeping your blog traffic healthy is to be able to detect
when someone is doing something they shouldn't. In my
[traffic control post](hosting5.html) I described five behaviors that I
wanted to limit

1. Scanning for secrets
2. Fishing for files
3. Rapid-fire requests
4. Trying to hide rapid-fire requests
5. Attempting unsupported actions

The post describes these in words, but they need to be made more specific
before they can be enforced by an automated detector. Doing this step well
is where most of the art and cleverness is required. If you define a rule
too narrowly, there will be a lot of IP addresses that *should* get blocked,
but get missed (false negatives for the detector). On the other hand, if
you define a rule too broadly, there will be a lot of legitimate IP traffic
that gets blocked (false positives) and you will have a lot of sad readers
who can't access your cat pictures.

There is also value in having rules that are simple as possible. The more
caveats and quirks in a ruleset, the harder it is to mentally keep track
of what combination of conditions will pass and what will be blocked. In
exchange for more flexibility in defining which behaviors get blocked, you
have a higher cognitive burden for keeping track of it and closing loopholes
and corner cases that an enterprising asshole might exploit.

With all these things in mind, here is my attempt at a rule set to catch the
bad behaviors I listed. They're based on the URLs/pages an IP address
tries to access, the http actions they use, and the http status codes they
generate.

There are some behaviors that are clearly mischievous.
Doing these things even once show that you are up to no good and get you a block.
These are **one-strike-and-you're-out** behaviors.

Other behviors are only a problem if they are repeated. Trying to access
a page that's not there and generating a 404 status happens all the time
in normal browsing. Mis-typed URLs and outdated links are part of browsing
life. But a whole lot of 404s from the same URL starts to look like someone
is fishing. These are **n-strikes-and-you're-out** behaviors.

Walking through my logs helped me learn which pages, statuses, and actions
are most likely to occur for my server. Here is my list as of this writing,
although it grows over time. The full current list is always available
[here](https://codeberg.org/brohrer/webserver-toolbox/src/branch/main/config.py).

### One-strike pages

Right now it's just `.env`. There are other targets that are problematic,
like `.git/config` or `password`, but so far every IP that has tried
to hit one of those has also tried to hit `.env`. Because this is a very
strict rule I want to make sure to limit it to certain violations. I don't
want to lock out anyone making an honest mistake. But if you're going after
a `.env` file you're clearly looking for someone else's secrets.

Another way to keep this narrow is that the match needs to be exact.
`.environment` or `.enviable` would not get an IP address blocked, only URLs
like `config/.env` or `.env/tokens` or even just `.env`.

### n-strike pages

A big difference with n-strike pages is that they only need to be
partial matches on the filename. Most of them are filename extensions.
This allows them to cast a wider net, and because they have to be repeated
n times, there is still not a big risk that they will occur accidentally during
innocent browsing.

The n-strike pages are problematic, but could more plausibly be accidental.
Some are compressed archives, like `.7z`, `.gz`, `.rar`, or `.zip`. I'm not
currently hosting any of these on my site, so anyone trying to hit one
repeatedly is hunting. Others are for PHP content, `.php`, or for
WordPress content, `wp-includes` and `wp-content`. I don't have any of these
either, but crawlers love to scan for common WordPress and PHP filenames
anyway, especially those associated with site administration.
I went with *n* = 5 on these rules.

This is a good example of how my one-strike and n-strike rules are specific
to my site. There's nothing wrong with hosting WordPress files, I just
happen not to be doing it, so I can use it as a bad behavior signal. What these
rules lack in sophistication they make up for in the ability to be tailored
to your site content and use cases.

### One-strike actions

There are
[HTTP actions](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)
that don't occur often in casual browsing and can
be red flags.

`PROPFIND` tries to retrieve a table of contents list of all the files on
the server. It's not used during normal browsing, and smacks of scraping and
hunting for vulnerabilities. Blocked.

`CONNECT` tries to set up a tunnel to a remote server. It is
used for more sophisticated networking than I'm doing, and having it show up
where it shouldn't makes me nervous. Blocked.

`SSTP_DUPLEX_POST` is also about setting up connections, specifically
encrypted connections like for ssh and VPNs. And there is absolutely no
reason someone should be doing it with my server. Blocked.

### n-strike actions

There are other more benign actions that my server doesn't support. One
or two of these is not an issue but a large number of them suggests that
someone is up to no good. (I used *n* = 8.)

`POST` is very common and useful for any data
transfer operations from the client to the server, say when a customer
attempts to log in or fills out a form. It's just that I don't host any
activities that require a POST so if someone is making dozens of POST
requests I comfortably cut them off.

Occasionally empty HTTP requests come through - no GET, no POST, no nothing.
These are just weird and that make me suspicious, so when they come in groups
they are a blockable offense.

### n-strike statuses

I haven't found any statuses yet that I need to block on the first occurrence,
but there are several that are probably indicators of funny business.
For these I settled on *n* = 8.

`403 Forbidden` is the code for when the requested page is off limits.
If this happens once or twice it might be an accident, but if it happens a lot
someone is probably trying to get into something they shouldn't.

`404 Not Found` A couple not-found files is to be expected, but lots and lots
of them means means someone is searching for something they haven't been
invited to see, like looking through your mom's closet for your Christmas
presents.

`429 Too Many Requests` Someone can be click-happy occasionally and generate
a 429, but a string of them means than an IP address is hammering your site.
That's just rude, and in extreme cases it can make it hard for other
people to get their page requests in.


## Blocking

The checks above are implemented in
[autoblock.py](https://codeberg.org/brohrer/webserver-toolbox/src/branch/main/autoblock.py).
It walks through these rules for the current day's access logs and compiles
a list of IP addresses that have earned a block.

`autoblock.py` also takes that list of IP addresses and uses them to create
a shell script which, when run as root, blocks those addresses
in the `ufw` (Uncomplicated FireWall).

To fully automate this, both `autoblock.py` and the shell script are added
to cron jobs. 

For the cron jobs of the not-special user `brohrer`: 

```
\*/5 \* \* \* \*
/home/brohrer/.local/bin/uv run
--project /home/brohrer/webserver-toolbox/
/home/brohrer/webserver-toolbox/autoblock.py >>
/home/brohrer/webserver-toolbox/logs/cron.log 2>&1
```

- Every five minutes
- run with `uv`
- the project `webserver-toolbox`
- and the script `autoblock.py` within
- and dump all of the errors (stderr) and outputs (stdout)
to the file `cron.log`.

And for root's cron jobs:

```
3-59/5 \* \* \* \*
sh /home/brohrer/webserver-toolbox/update_firewall.sh >>
/home/brohrer/webserver-toolbox/logs/cron.su.log 2>&1
```

- Every five minutes, starting from minute 3 of the hour
- run the shell script `update_firewall.sh`
- and dump stderr and stdout to the log file `cron.su.log` .


The decision to run this every five minutes was a trade-off between wanting to
shut down misbehavior quickly and not wanting to wantonly burden the server.
As you've probably noticed there are lots of small decisions that have gone
into setting this up. Some of them are hard coded into the cron jobs,
like the timing of the automated runs and the names of the log files,
but the rest is concentrated in
[`config.py`](https://codeberg.org/brohrer/webserver-toolbox/src/branch/main/config.py).
If you want to pull down the
[webserver-toolbox](https://codeberg.org/brohrer/webserver-toolbox) and
use it yourself, you can do a lot of customization there.

There are lots of different reasons a particular website might have to
block an IP address, and they will be very different depending on the
website and the expected access patterns. For instance, one
of the most common IP-blocking tools,
[Fail2ban](https://en.wikipedia.org/wiki/Fail2ban), focuses a lot on
failed login attempts. Too many and too fast is grounds for blocking an
IP. That makes a lot of sense for any website with
a login, but no sense for my website which is just static html with no
access restrictions. The lesson here isn't that one way is best, but
that the best way for one website will not be the same as another.
And a custom blocker, tailored to the function and usage of a particular
websiste, will always be more effective than a generic, one-size-fits-all
tool.

## Automation

Coming back to the project at hand, we now have an automated blocker
that is happily spinning away, catching
violators every five minutes and banishing them from the joys of the
website. Sadly, we've only gotten started.

In the world of robotics, an automated system is often described as
a sense-decide-act loop. In the case if IP blocking, "sense" is
recording the access logs. `nginx` takes care of that. The "decide"
portion is what happens in `autoblock.py`, where violators are detected.
And the "act" portion is the actual blocking of the IPs in the firewall.

Describing this as a loop reminds us that it's a cycle that continues
to run over time. The earth will spin, people will go to bed and wake up,
trees will grow, and pendulums will swing. Some of these events affect our
system. When a trans-oceanic telecommunications cable gets cut, when
a blog post goes viral, when some dork wakes up and thinks of a new way to take down
my website, those events interfere with the predictable patterns of the
carefully tuned sense-decide-act loop that was created before those things
happened. 

Getting an automation to run once, when you are paying close attention to it,
means that you have a nice demo. It doesn't mean tha you have a system that
is robust, that can weather the storms of traffic
that increasingly obnoxious webscrapers may throw at it.
For that you need to allow for logging, monitoring, alerts, and
the ability to make changes to the system within guardrails, so that
I don't do anything too drastic like erasing the entire blocklist.

## Building with guardrails

When building automated systems with machinery or power electronics,
a bug during development can mean fire, mayhem, and dismemberment,
rather than just an error on the console. If you want to have a long
career as a nerd, it's important to build automated systems with guardrails.

One really fun thing you can do when you are administering your own
webserver is to accidentally put your own IP address on the blocklist. 
Once that happens, it can only be remedied with truly drastic measures.
In order to prevent this, the autoblock tool starts by adding any
IP addresses in the allowlist to the top of the ufw rule set. Because
ufw goes through the rules sequentially and honors the first applicable rule
it finds, this ensures that any allowlisted addresses will never be blocked.
The autoblocker also takes pains to insert any block rules after the end
of the allow list, so it doesn't supersede any of them.

And in the darkest of universes, where something goes horribly wrong and I lock
myself out of my server entirely, I can always rebuild because I've chosen
to keep a copy of all the software tools in
[a git repository](https://codeberg.org/brohrer/webserver-toolbox)
outside of the server.

Another guard rail is the ability to do a dry run---to identify all the
addresses that the autoblocker would like to block, but to not act on them
just yet, and to hold off writing the shell script that would add them
to the ufw rule list. This is done with the `--dryrun` option on
`autoblock.py`. It is really helpful for verifying that any clever new
blocking rules work as expected.

And as an additional convenience there is a `--local` option so I can do
some quick development on my home machine without having to upload everything
the server first in order to check it. It tightens up the fuck-around-find-out
 so that I can make mistakes faster and with lower stakes and
greater gusto. It uses
a copy of some old log files just to work the wrinkles out of any new
methods that might be under development. I used it a lot when writing
the n-strike checks, and I expect to use it again in the future when
I notice new patterns in IP addresses that I want to use as a block signal.

The final guardrail that the autoblocker uses is making a backup copy
of the blocklist each time it runs. That means that I can turn the clock
back if I need to and pretend that any regrettable autoblock runs never
happened.

## Explainability

Another thing that can happen in an automated system is that someone
might ask why it made a particular decision. The ability to perform an
audit, to look inside the algorithmic thought process of the code,
is especially important when these decisions affect other people.
If someone comes to me asking why they were blocked from my dinky
website, it's good to have an answer and a way to change that decision.

Due to the simplicity of the autoblocking rules, it's enough to record
the date and the rule violated by the IP. These are captured in a set
of files in `logs/blocks_$<$rule$>$.txt` of `website_tools`. If someone comes
to me with a question I can search for their IP address across these
files and find the date and rule that was violated. Then we can have
a conversation and decide
whether to leave them blocked, remove them from the blocklist, or, if
we both expect the violation to recur and are OK with it, add them
to the allowlist.

Explainability is often neglected in modern automated systems, especially
if the purpose of those systems is to shield the humans behind them from having
to explain their decisions. Explainability in complex algorithms
like neural networks and large language models is difficult, if not infeasible.
The conclusion I draw from this is that LLMs are not suitable for
automated systems performing any serious task.

## Monitoring

Automating IP blocking doesn't mean that the system won't break. It just
means that I won't be watching it when it does.
In the days before self-driving cars there was a joke about the guy driving
his motor home down the highway and put it on cruise control so he could go
in the back and get a Coke. (It's still funny now but for different reasons.)
Automation doesn't mean we can stop paying attention. It just means we
get to pay attention to different things.

It's still important to keep an eye on what's going on, just at a different
level. I have an automated helper that stays up 24/7 watching for rule
breakers and blocking them, but I still need to check in on it.

I do this by logging in to the server every couple of days and looking
around. I wrote a couple of helper scripts to do some aggregations.

- I can check to total number of access requests to each page with
`uv run pages.py`. I know from watching that the most popular posts are
on [transformers](transformers.html),
[setting up ssh](ssh_at_home.html),
and [converting RGB color to grayscale](convert_rgb_to_grayscale.html), and
from there they taper off. If I see anything different from this, then I know
something may be off.
- I can check the total number of access requests, by IP address with
`uv run ips.py`. Scrapers and bots tend to have many access requests.
If most of the IP addresses are in the single digits for access requests,
then I'm comfortable
that the overall composition of folks reaching my site is healthy. 
- I can check which pages were attempted but were not found with
`uv run history.py --status 404`. This is particularly helpful for
identifying IP addresses that are hunting for sensitive files, rather
than for blog pages.
- And finally, I can take a look through the raw logs with 
`uv run history.py`. This is good for using our uniquely human ability
to spot things that just look off, and might merit adding new rules
to the one-strike and n-strike checks.

If I wanted to get more professional about this, I could set up a recurring
script to pull out common cross sections of these data sets and put them
into an attractive plot, but honestly it's not necessary. The most critical
element of good monitoring is spending a few focused minutes looking at
the system from a few different directions until you are convinced it is
doing its job.

## Alerting

My website is not a critical piece of infrastructure. It's not a
flight control system or a nuclear power plant. If it goes down for
an hour or a day or a week. No one will die. If I'm really lucky,
a few people will notice.

That's lucky because sometimes I forget to check on it for a few days.
But if I were really super on top of it, I could implement some alerting
on top of the monitoring. Alerting is, in essence, adding another layer of
automation. I'm automating the part where I hop on the server and look
for unhealthiness in the logs. If I've done my job right in this post so far,
this will be a little bit nervous making. "Wait", you may say, "we just went
to a whole lot of work to make sure that our automation wouldn't break
in horrible ways. Now you're talking about adding *another* story in this
house of cards?" And you would be correct to ask this.

Automating alerts is important for the same reason as automating blocking;
it's usually too much to ask a human to sit there around the clock and
keep and eye on things. And even when constant surveillance is in place,
it may still be too much to ask of a human to watch millions of log entries
per second or to keep track of dozens of gauges simultaneously. Alerts serve
to draw a human observer's attention when they are absent or distracted.

Implementing alerting well is every bit as hard as implementing autoblocking
well. It's another sense-decide-act loop, where the "act" part is activating
an alert. Monitoring is the "sense" side of things. Determining what to
monitor is an art in itself, related to feature engineering, which I'll have
to cover in another post.

And "decide" is a separate design problem.
After I've found a useful signal to sense, say, the number of access requests
resulting in a 404 Not Found status, determining how many 404's represent
an alert-worthy event is a tricky trade-off. Make the threshold too low,
and the alert becomes too sensitive, resulting in many false positivites---a
nuisance alarm, like the boy who cried wolf. Even if it's right sometimes,
it's too much work to check it out every time it fires so it gets ignored.
And if the threshold is too high, then the alert isn't sensitive enough.
It misses genuine problems, has a high false negative rate. Incorporating
additional factors like changing how long of a time window to count over
or making allowances for seasonality in the behavior can help balance
false positives and false negatives, but also introduce additional complexity
of their own.

Alerts a very useful, but they also deserve careful design attention,
testing, and periodic reevalution. And then of course there is monitoring
for your alerting system, and health checks and automated alerts in case
your alerts go down. It's just turtles all the way down, as deep as you
care to take it.

But if all you're building is a derpy blog website, then you don't need to
worry about them.
