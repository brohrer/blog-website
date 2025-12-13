# Moving your code from prototype to production

So you wrote a cool little weather app that predicts temperatures
in your neighborhood.
Now you want to be able to share those predictions with everyone of
the thousand people who live there. How do you go from
"It works on my machine" to "No matter where you are in the world you can
use this in your own browser."?

There are a lot of dimensions to making your code ready to leave the nest
and be on its own in the real world, but an important one is
deploying it from your laptop to a globally available server.

This post is about one good way to do this. There are lots of others,
but this one is solid and, believe it or not, one of the simplest.
This deployment starter kit includes

- [Flask](https://flask.palletsprojects.com/en/stable/), a Python package for turning your code into an app.
- [Gunicorn](https://gunicorn.org), a more serious production grade WSGI server.
- [nginx](https://nginx.org/en/), an industry standard web server.
- [ufw](https://wiki.ubuntu.com/UncomplicatedFirewall), an Uncomplicated Firewall for Linux
- [systemd](https://systemd.io) the Linux tool for turning your code into a daemon.

I won’t bother walking through How to do this because DigitalOcean has
[an amazing documentation page](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
for setting this up in Ubuntu 22.04. It worked for me on 24.04 as well.
Follow their page to the letter and it will get you safely through.
And it is such a cool feeling when it does.

However, I feel like it is worth spending a couple minutes on the Why.
Why do any of this? Why not just share your code from your personal computer?
You could if you wanted to. But it turns out that
the Internet is an extremely busy and occasionally harsh place to be.
Prototyping on your laptop is like setting up a lemonade stand in a private garden
and selling cups to your mom. Opening your service up to the Internet
unfiltered is moving your card table lemonade stand to an active combat zone.

Luckily, there are really helpful tools for handling this.

**Flask** is the first layer of order we add.
It takes willy-nilly functions and makes sure they fit the structure of an API.
They turn your Python into a web app.
Flask takes your lemonade stand, and puts four walls, a ceiling, and
a well defined front door on it.

**Gunicorn** (short for Green Unicorn) is an open source WSGI server written
in Python. WSGI is short for
[web server gateway interface](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface),
and happily can be pronounced "whiskey". It serves as a bridge between a web app
and a web server. Gunicorn handles scalability and adds some security.
Gunicorn beefs up the walls of your lemonade stand and adds a headset-wearing
coordinator that lines up all the customers and makes sure they keep
moving, get their lemonade efficiently, and get out. It also builds
carbon-copies of your lemonade stands next to the original and forms a queue
of customers in front of each one. Gunicorn gets you ready to handle
the throes of people that want to come visit your stand.

**nginx** is a fully featured HTTP server. It often gets used on its own
to serve webpages, but it can also route API requests. In our setup,
we are going to use it as a
[reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy),
an extra front door and lobby with a security guard and a metal detector
that people have to get through before they can line up for lemonade.
nginx turns away lot of troublemakers who might be trying to sneak in
and take our lemons or trick our customers out of their cash.
nginx helps make sure that the people who show up are there to buy lemonade.

**ufw** provides additional security. It has one job, which is to check
people’s ID and destination (IP address and port).
You can feed it a list of known bad actors' IPs to block them preemptively.
ufw is a ridiculously high compound wall that surrounds your lemonade complex,
providing a comfortable layer of protection from anyone seeking
to do violence or so mayhem.

**systemd** lets us run Gunicorn as a daemon, a background process that
is automatically started when you turn the computer on and restarted
when necessary. Once you set up Gunicorn as a daemon, you don’t have
to worry about whether your lemonade vendors fell asleep, or decided
to go home. Nope, with systemd the lemonade emporium is up and running 24/7.

When you consider all of the things that could go wrong with a service
exposed to the Internet, it’s kind of amazing that we can get it to work at all,
which makes this setup extremely cool. Granted, it has more moving pieces
than I would prefer, but they all serve a purpose. Importantly,
the instructions for setting them up are well defined. There are other,
fancier ways to do all of these steps, and ways to handle yet more security
and yet larger scale, but this Flask/Gunicorn/nginx set up is something
you can put out into the world without apology.
It’s a fully-baked grown-up solution.
