# Use Postgres with Python

I’ve been intimidated by Postgres for a long time, but now that
I’ve gone and got it working I feel kind of silly.
It is a wildly powerful tool, so I expected to have a painful installation
with building from source and modifying environment variables, 
but it turns out Postgres is built to be put to use quickly.

On Linux, installation is literally one line. Here’s what it looks like on
Ubuntu 24.04, and [other distros](https://www.postgresql.org/download/linux/)
are similar.

```
sudo apt-get install postgresql
```

For MacOS I installed [Postgres.app](https://postgresapp.com/downloads.html).
After a download and a double click, your Postgres server is up and running.

Sorry Windows, I haven't tried you yet, but
[here's where I'd start](https://www.postgresql.org/download/windows/).

For working with Postgres from Python, the
[psycopg package](https://www.psycopg.org/psycopg3/docs/basic/index.html)
is the ticket.

Install with uv

```
uv add "psycopg[binary]"
```

or pip.

```
pip install "psycopg[binary]"
```

Then the Python interface looks like this.

```
import psycopg <br>
with psycopg.connect(dbname="postgres", user="postgres") as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            pets ( name TEXT, weight_kg REAL, birthday DATE);
        """) <br>
        cursor.execute("""
            INSERT INTO pets (name, weight_kg, birthday)
            VALUES (%s, %s, %s)
        """, ('Mugsy', 24.3, '2022-10-18'))<br>
        cursor.execute("SELECT * FROM pets")
        print(cursor.fetchone()) <br>
        conn.commit()
```

It's very much like
[working with `sqlite3`](https://brandonrohrer.com/db_first_db.html),
but with a few small differences.

It’s helpful to be aware of the fact that the Postgres server is its
own process. It’s a separate program that you have to call from Python.
The fact that it’s not tied to the Python interpreter and can run
its own optimized code, purpose built for your operating system,
allows it to really scream.

The example above is pretty dense, especially if you’ve never worked
with databases before. Here’s a walk-through.

```
import psycopg
```
Heads up: the import name of the package is `psycopg`, not `psycopg3` or `psychopg`.

```
with psycopg.connect(dbname="postgres", user="postgres") as conn:
```
The `with` construction is a Python context manager, a shorthand for saying
"do some stuff with this database connection and, whether it finishes
successfully or crashes and burns, make sure to gracefully excuse yourself
to the server when you're done and close everything down
with as little damage as possible."

The `dbname="postgres"` is an instruction to connect to the `postgres`
database, one that exists by default on all Postgres servers.
A database is a collection of tables, the same way a spreadsheet
"workbook" is a collection of individual sheets. Initially
the `postgres` database will be empty, containing no tables.

The `user="postgres"` says to connect as the user named `postgres`,
a default user with default permissions.

Once the connection is established, return it as `conn`.

```
    with conn.cursor() as cursor:
```
A connection to a database isn't enough. You also need a cursor.
A cursor will let you create tables, add data, and run queries.
There's more about cursors in this
[intro to databases post](db_awkwardness.html).

```
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS
            pets ( name TEXT, weight_kg REAL, birthday DATE);
        """)
```
Make a new table called `pets`. If one already exists (for example, if you
run this script more than once) then don't worry about it.

Give the table three columns.

- The first is called `name` and expects text data.
- The second is called `weight_kg` and expects real valued
(floating point numerical) data.
- The third is called `birthday` and
expects a date. There are a lot of allowable
[Postgres date formats](https://www.postgresql.org/docs/current/datatype-datetime.html#DATATYPE-DATETIME-INPUT-DATES). 

```
        cursor.execute("""
            INSERT INTO pets (name, weight_kg, birthday)
            VALUES (%s, %s, %s)
        """, ('Mugsy', 24.3, '2022-10-18'))
```
Add a row to this table.

- Put `Mugsy` in the `name` column.
- Put `24.3` in the `weight_kg` column.
- Put October 18, 2022 in the `birthday` column.

This format with the `%s` placeholders is important. This lets Postgres
perform input validation---to check whether any of the input values
will break things. If you are familiar with Python string construction
it would be tempting to substitute the values directly in with an f-string.

```
pet_name = 'Mugsy'
pet_weight = 24.3
pet_birthday = '2022-10-18'
f"""
    INSERT INTO pets (name, weight_kg, birthday)
    VALUES ({pet_name}, {pet_weight}, {pet_birthday})
"""
```
Don't do this! It opens you up to SQL injection attacks. If someone
names their Pomeranian `Fluffy'); DROP TABLE pets;--`
then badness will happen [ [xkcd 327](https://xkcd.com/327) ].

```
        cursor.execute("SELECT * FROM pets")
        print(cursor.fetchone())
```
Run a query, selecting all the rows from your one-row table.

```
        conn.commit()
```
Until you commit it everything you've done is temporary. `commit()`
makes it permanent.


I recommend bookmarking the
[PostgreSQL documentation](https://www.postgresql.org/docs/18/index.html).
It is exhaustive.

