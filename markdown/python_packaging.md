# Python packaging with uv

For a long time, every time I needed to create a new project or
Python package I copied an existing repository. It worked pretty well, but
never perfectly. It always felt like I was wearing someone else’s shoes.
And then when I went to make changes, I realized quickly how little I
understood about how projects, builds, and distributions work.

Here are some questions that I’ve had and some answers I've found.
They focus on the uv toolset of environment management and packaging.
This post doesn’t say anything about setuptools, even though setuptools,
setup.py, and setup.cfg 
are still present in a lot of well-built projects, especially pre-2025 ones.

I expect this list of questions to grow and evolve over time as I learn.
My primary audience is a clueless future me, but I hope it helps you too.

## How do I name projects? Packages? Modules? Repositories?

As the saying goes, naming things is one of the hardest problems in
computer science. This is particularly true when it comes to packaging.
There are a lot of different entities to be named, and it’s unclear sometimes
what names belong to which. There is a repository name, a top level directory
name, a project name, and a package name. All of these can be different.
For extra confusion, they can get confused with module names and function
names as well.

The Python interpreter and build tools have no problem knowing whether
a particular name is supposed to reference the project or the package.
They determine this from context. For human brains, especially the ones
new to packaging,
this can be a lot to keep track of. To save yourself unnecessary hassle,
a good trick is to use the same name for all these things. A brief,
memorable, all-lowercase name is ideal. The one way in which these names
will differ is in how they handle multiword names. For project, repository,
and top level directory names, separate words with a hyphen, as in
`my-amazing-tool`. For Python
packages and modules separate multiple words with an underscore, for example
`my_amazing_tool`. This keeps
things consistent with the conventions of the various tools and communities. 

But don’t worry too much if you feel the need to deviate from this.
Plenty of smart people have differing opinions and it’s a matter
of convention only.
The [PEP 8 recommendation](https://peps.python.org/pep-0008/#package-and-module-names)
is to give packages single-word names, without underscores, but this can
be challenging to do in a readable way.  Everyone ignores this.

If you plan to distribute it publically on [https://pypi.org](PyPI),
check it first to make sure the package name isn't already taken.

## What are wheels and sdists?

An sdist is a *source distribution* and a wheel is a *binary distribution*.
I have no idea why it's called a wheel. Source is the code itself---`.py`
files and their supporting cast. It comes in a single `.tar.gz` archive
which has to be unzipped with `tar -xvf` before it can be properly read.
[Detail on sdists here.](https://packaging.python.org/en/latest/discussions/package-formats/#what-is-a-source-distribution)

The wheel is the compiled version of the source, containing
only the files needed to actually run the code. Because compilation
is platform specific, a wheel is tied to a particular operating system,
processor architecture, and Python version. A single project can have many
wheels if it's meant to be run on many platforms and architectures.
The big caveat here is that Python files don't get pre-built into binaries.
The local Python interpreter does that at runtime. So if it's a purely Python
package, then one wheel is usually sufficient for all platforms and OS's.
[Detail on wheels here.](https://packaging.python.org/en/latest/discussions/package-formats/#what-is-a-wheel)

## What are build tools and why do they matter?

Build tools do the work of taking the original files and the information
from `pyproject.toml` and using them as ingredients for building
the sdist and the wheel.

There are two parts to this, a build frontend and a build backend. For the
purposes of this post, the frontend is
[uv build](https://docs.astral.sh/uv/concepts/projects/build/#using-uv-build)
it does some gathering and interpretation of the files and prepares them
for the next step. pip and build are other popular build frontends.


There are a few common build backend tools, including hatchling, setuptools,
and uv's own uv_build.
[Here's a short guide](https://pydevtools.com/handbook/explanation/what-is-a-build-backend/#choosing-a-backend)
for choosing between them, but when in doubt hatchling is a good choice.
The backend needs to be called out in pyproject.toml
[like this](https://pydevtools.com/handbook/explanation/what-is-a-build-backend/#how-the-frontend-finds-the-backend)

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

[Here are some examples](https://packaging.python.org/en/latest/tutorials/packaging-projects/#choosing-a-build-backend)
for the other backends as well.

## Why have a `src` directory?

There are two common patterns for organizing projects
[flat and src layouts](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout).

A flat layout is intuitive. The package code sits at the top level of the
project and is more straightforward to access. But because of how imports work
it's easy to lose track of whether your other code, like tests, are
referencing the working copy of your code in the project or a previously
installed version of the package. It can result in maddening bugs.

A src layout alleviates this. Because the package sits one level lower,
it's not so easily reachable for direct import. Any import would need
an installed version of the package. Using an editable install makes
sure that your most recent changes to the code are what is run.

The src layout gives the benefit of protecting us from ourselves
a bit more. And it comes at the cost of a slightly more complex file
structure and an extra step to ensure an editable install.

## How do I make a package visible across the project?

To make a package a visible from other locations in a project
that are outside the package directories, for instance in `tests/`,
the most reliable way is to do an editable install.
From within the top level directory of the project run

`uv pip install -e .`

Modules outside your package shouldn't need `__init__.py` files
in each directory. But now they will be able to `import mypackage`
and go to town.

Note that it's also totally valid to include `tests\` within the
package. In that case they will very much need their `__init__.py`
files. More detail in
[pytest best practices](https://docs.pytest.org/en/latest/explanation/goodpractices.html).


## How do I add other file types to the package? And how do I access them from the code?

The easiest way is to include them under the package directory tree.
By default, hatchling includes in the sdist any non-Python files under
the `mypackage` directory that are not in
`.gitignore`. This behavior can be aribitrarily modified for both
types of build targets, sdists and wheels.
[Examples here.](https://hatch.pypa.io/1.16/config/build/#file-selection)
They can be instructed to include files from outside the project as well.

From within the code, these files can be accessed by their absolute path
The `__file__` attribute gives the absolute path of a given module.
It can the be modified to point to the data instead. For example for this
structure

```
myproject
├── pyproject.toml
└── src
    └── mypackage
        ├── __init__.py
        ├── mymodule.py
        └── data 
            └── mydata.json
```

within `mymodule`

```import os<br>
mymodule_abspath = __file__
mydata_abspath = os.path.join(mymodule_abspath, 'data')
mydata_absfilename = os.path.join(mydata_abspath, 'mydata.json')
with open(mydata_absfilename, 'rt') as f:
    mydata = f.read()
```    

## What goes into `pyproject.toml`?

While `pyproject.toml` files are powerful and flexible and can be quite long,
[a minimal pyproject.toml](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html)
contains just some basic project and build system information, like this.

```
[build-system]
requires = ['hatchling']
build-backend = "hatchling.build"<br>
[project]
name = 'myproject'
version = '0.1.0'
```

There are some other
[commonly used fields](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html#optional-fields-to-include-in-the-project-table)
for the `project` table, including description, license, authors, and
keywords. project-dependencies will list other packages that yours depends on.
The classifiers field gives a set of standard tags that can help humans
and software tools alike make better use of your package.
[The full list of classifiers](https://pypi.org/classifiers/) is lengthy,
but some especially helpful ones are

- Development Status
- Intended Audience
- Topic
- Programming language

## Resources

These are the references that I find most useful when answering these
questions.

- [python.org packaging](https://packaging.python.org/en/latest/)
- [uv project configuration](https://docs.astral.sh/uv/concepts/projects/)
- [build frontends](https://pydevtools.com/handbook/explanation/what-is-a-build-frontend/)
- [build backends](https://pydevtools.com/handbook/explanation/what-is-a-build-backend/)
- [hatch configuration](https://hatch.pypa.io/1.16/config/build/)
- [pyproject.toml configuration](https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html)
