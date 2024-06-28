# Odyssey

The _new_ Axos AI python monorepo.

## Organization

The monorepo is divided into two high level directories:

- `libs`: contains internal Axos AI packages for code that should be shared across projects
- `projects`: individual working directories for teams to work on specific projects, where code is unique to that project

If you notice code snippets being repeated across multiple projects, consider packaging it as a library.

## TODOs

- [ ] Move all other projects into monorepo as projects: prior authorization, transcription, EMS assistant/copilot
- [ ] Move testing code in individual files' `__main__` into pytests or use `argparse` to pass in arguments
- [ ] Set up a unified config file for `agents` and `parallax` packages
- [ ] Make test suite
- [ ] Set up CI/CD

## Getting Started

Example for running the FastAPI app via `projects`:

First, install all dependencies for the project.

```
cd projects/infra
pip install -e .
```

Create a `.env` file and dump all env variables into the file. Now that all your env variables are set, you want to export them.

Currently, `.env` file loading is broken due to the import structure, which needs to be debugged.
As a stopgap, place your `.env` file at the root directory and then run

```
source export_env.sh
```

from the root directory before trying to run anything.

Finally, run the commands to start the web app from `infra/axos`:

```
uvicorn parallax_v2:app
celery -A parallax_worker.celery worker --loglevel=info --pool=threads
```

## Notes on Monorepo Structure

This repository's design is explained on the Tweag blog:

- [Python monorepo; part 1](https://www.tweag.io/blog/2023-04-04-python-monorepo-1/)
  describes the monorepo's structure, how libraries are linked together and which
  tools are used.
- [Python monorepo; part 2](https://www.tweag.io/blog/2023-07-13-python-monorepo-2)
  describes the monorepo's CI, striking a good balance between being easy to use and being
  featureful.

The design strives to be simple, to work well in a startup environment where
CI specialists are not yet available, and yet to achieve a great deal
of [reproducibility](https://reproducible-builds.org/) to prepare for scaling.

We use a virtual environment per library/project, to allow dependencies to
diverge if you need to. Another alternative is to have a single virtual environment
for the entire repository, to maximize uniformity. Choose what suits you best.

We use [editable installs](https://setuptools.pypa.io/en/latest/userguide/development_mode.html)
for dependencies _within_ this repository, so that changes to a library are reflected
immediately in code depending on the said library. This implements
the _live at HEAD_ workflow, a term made popular by
[Titus Winters](https://www.youtube.com/watch?v=tISy7EJQPzI) from Google.
