# Contributing

## Toolchain

The top-level tool chain for managing this project is tested on Linux and macOS.
Here are links for installing the appropriate tools.

- [`cspell`](https://cspell.org/docs/installation/)
- [`ds`](https://github.com/metaist/ds#install)
- [`gh`](https://github.com/cli/cli#installation)
- [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [`uv`](https://github.com/astral-sh/uv#installation)

All remaining tools are installed below.

## Local Development

```bash
# get the code
git clone git@github.com:metaist/attrbox.git
cd attrbox
uv sync --extra dev
```

Periodically, you should run:

```bash
ds dev # check lint, type-checks, and run tests
```

This repo generally tries to maintain type-correctness (via `mypy` and `pyright`) and complete unit test coverage.

## Making a Release

Checkout `prod`:

```bash
git checkout prod
git merge --no-ff --no-edit main
```

Update top-most `__init__.py`:

```python
__version__ = "X.0.1"
```

Update `CHANGELOG.md`. To see recently closed issues run:

```bash
ds recent-closed
```

You can also look at the [unreleased](https://github.com/metaist/attrbox/compare/prod...main) log too.

Sections order is: `Fixed`, `Changed`, `Added`, `Deprecated`, `Removed`, `Security`.

```markdown
---

[X.0.1]: https://github.com/metaist/attrbox/compare/X.0.0...X.0.1

## [X.0.1] - XXXX-XX-XXT00:00:00Z

**Fixed**

**Changed**

**Added**

**Deprecated**

**Removed**

**Security**
```

### Final checks, tag, and push

```bash
export VER="X.0.1"

# final checks again every supported python version
ds dev-all # requires uv >= 0.3.0

# final build
ds docs build

# commit, push tags, create a new release
ds release: $VER
```

[Review the release on GitHub](https://github.com/metaist/attrbox/releases). Once published, the `pypi.yaml` workflow will attempt to publish it to PyPI.
