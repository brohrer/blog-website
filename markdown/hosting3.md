# Beef up security on your webserver

[Part 1](hosting.html) of this series showed how to create a new web server
from scratch and [Part 2](hosting2.html) showed how to set up a new
domain name on it. Now it's time to make that website more secure, so it can
be protected from the rougher edges of the cyber world.

## Enable HTTPS

Currently the web server we've built is only serving unencrypted (http) requests,
rather than encrypted (https) requests. https has become the standard for
the web. It's obviously useful when sharing personal information like
credit card numbers and love notes, but it's even beneficial for seemingly
benign browsing. It's hard to foresee all the ways that someone might use
the browsing habits of your readers against them. To protect them, we'll
set up https.

As with so many topics there is an extremely accessible explanation of
how https works in
[The Wizard Zine on http](https://wizardzines.com/zines/http/).

If you have been following the other two posts closely, then you are perfectly
set up to follow [the DigitalOcean tutorial
](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04)
walking through https setup. It builds on all the pieces we've put in place:
ufw, a sudo-capable non-root user, a domain name, DNS records, server blocks.
I won't bother copying and pasting here. It's an excellent guide so I'll just
point you to it.

![The table of contents of the DigitalOcean tutorial
](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/hosting/https_tutorial.png)

If you later decide to add more subdomains or entirely new domains
to your server, you can add them to your certbot with

```
sudo certbot --expand -d blog.e2eml.school,brandonrohrer.com,www.brandonrohrer.com
```

and you can check on them any time

```
sudo certbot certificates
```

## Harden ssh

Any publicly exposed ssh port
gets A TON of traffic trying to worm its way in.
In a typical five minute window, my server got requests from users named

- `default`
- `admin`
- `admin1`
- `sysadmin`
- `root2`
- `user (twice)`
- `user1`
- `mytest`
- `wangxx`
- `dennis (twice)`
- `ben`

`dennis` gets extra points for persistence and `wangxx` gets points for style,
but what this drives home is that there are always people trying to get
into your system, no matter how small a target. If they can get in by luck
or clever guesses, they eventually will. 

Using ssh with keys is a great start. Guessing a modern private key
is very close to impossible.
There are a few other things we can do to protect our new little server. 

### Disallow passwords for login

To get the full protection of ssh keys, it's necessary to
enforce their use all the time. You can set this up in the `ssh_config`
file, the central location for all the settings that control ssh behavior.

```
sudo nano /etc/ssh/ssh_config
```

Find the commented out line containing `PasswordAuthentication`.
Uncomment it and change it to

```
   PasswordAuthentication no
```

After making a change to `ssh_config` restart the ssh daemon so that
it takes effect.

```
sudo systemctl restart ssh
```

### Make logging verbose

For diagnosing any funny behavior, you can include even more information
in the logs. Also in `/etc/ssh/ssh_confg` add the line

```
    LogLevel INFO
```

To inspect the logs at any time

```
sudo cat /var/log/auth.log
```

This will let you see who is trying to hack into your ssh too.


### Keep it updated

Periodically ssh in to your server and update 

```
sudo apt update
sudo apt upgrade -y
```

### ssh by domain name rather than IP address

As a helpful reader pointed out, any workflow that requires us to remember
an IP address is flawed. With a few notable exceptions humans are really bad
at consistently remembering strings of numbers. 
You can set it up so that you can 

```
ssh myserver
```

instead of having to remember any numbers.

On your local machine---the one you have hands on keyboard--- open
`~/.ssh/config` for editing and add lines that look like this

```
Host myserver
  Hostname 192.0.2.146
  User brohrer
```

From now on ssh will re-interpret `ssh myserver` as
`ssh brohrer@192.0.2.146`. If you need to log on as another user you
can still do it the old fashioned way: `ssh anotheruser@192.0.2.146`. 

-----

This collection of defenses puts the web server in a reasonably strong
state. Nothing connected to the internet is ever perfectly protected,
but this makes the server a less appealing target than others.
