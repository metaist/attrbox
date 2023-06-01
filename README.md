# attrbox

_Attribute-based data structures._

[![Build Status](https://img.shields.io/github/actions/workflow/status/metaist/attrbox/.github/workflows/ci.yaml?branch=main&style=for-the-badge)](https://github.com/metaist/attrbox/actions)
[![attrbox on PyPI](https://img.shields.io/pypi/v/attrbox.svg?color=blue&style=for-the-badge)](https://pypi.org/project/attrbox)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/attrbox?style=for-the-badge)](https://pypi.org/project/attrbox)

[Changelog] - [Issues] - [Documentation]

[changelog]: https://github.com/metaist/attrbox/blob/main/CHANGELOG.md
[issues]: https://github.com/metaist/attrbox/issues
[documentation]: https://metaist.github.io/attrbox/

## Why?

I have common use cases where I want to improve python's `dict` and `list`:

- [`AttrDict`](#attrdict): attribute-based `dict` with better merge and deep value access
- [`AttrList`](#attrlist): `list` that broadcasts operations to its members
- [Environment](#environment): reading environment files
- [Configuration](#configuration): loading command-line arguments and configuration files
- [`JSend`](#jsend): sending JSON responses

## Install

```bash
python -m pip install attrbox
```

## AttrDict

`AttrDict` features:

- **Attribute Syntax** for `dict` similar to [accessing properties in JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects#accessing_properties): `thing.prop` means `thing["prop"]` for get / set / delete.

- **No `KeyError`**: if a key is missing, just return `None` (like `dict.get()`).

- **Deep Indexing**: use a list of keys and `int` to get and set deeply nested values. This is similar to [lodash.get](https://lodash.com/docs/#get) except that only the array-like syntax is supported and you must use actual `int` to index across `list` objects.

- **Deep Merge**: combine two `dict` objects by extending deeply-nested keys where possible. This is different than the new `dict` union operator ([PEP 584](https://peps.python.org/pep-0584/)).

```python
from attrbox import AttrDict

items = AttrDict(a=1, b=[{"c": {"d": 5}}], e={"f": {"g": 7}})
items.a
# => 1
items.x is None
# => True
items.x = 10
items['x']
# => 10
items.get(["b", 0, "c", "d"])
# => 5
items <<= {"e": {"f": {"g": 20, "h": [30, 40]}}}
items.e.f.g
# => 20
items[['e', 'f', 'h', 1]]
# => 40
```

[Read more about `AttrDict`](https://metaist.github.io/attrbox/attrdict.html#attrbox.attrdict.AttrDict)

## AttrList

`AttrList` provides **member broadcast**: performing operations on the list performs the operation on all the items in the list. I typically use this to achieve the [Composite design pattern](https://en.wikipedia.org/wiki/Composite_pattern).

```python
from attrbox import AttrDict, AttrList

numbers = AttrList([complex(1, 2), complex(3, 4), complex(5, 6)])
numbers.real
# => [1.0, 3.0, 5.0]

words = AttrList(["Apple", "Bat", "Cat"])
words.lower()
# => ['apple', 'bat', 'cat']

items = AttrList([AttrDict(a=1, b=2), AttrDict(a=5)])
items.a
# => [1, 5]
items.b
# => [2, None]
```

[Read more about `AttrList`](https://metaist.github.io/attrbox/attrlist.html#attrbox.attrlist.AttrList)

## Environment

`attrbox.env` is similar to [python-dotenv](https://github.com/theskumar/python-dotenv), but uses the `AttrDict` ability to do deep indexing to allow for things like dotted variable names. Typically, you'll use it by calling `attrbox.load_env()` which will find the nearest <code>.env</code> file and load it into `os.environ`.

[Read more about `attrbox.env`](https://metaist.github.io/attrbox/env.html)

## Configuration

`attrbox` supports loading configuration files from `.json`, `.toml`, and `.env` files. By default, `load_config()` looks for a key `imports` and will recursively import those files (relative to the current file) before loading the rest of the current file (data is merged using `AttrDict`). This allows you to create templates or smaller configurations that build up to a larger configuration.

For CLI applications, `attrbox.parse_docopt()` let's you use the power of [`docopt`](https://github.com/docopt/docopt) with the flexibility of `AttrDict`. By default, `--config` and `<config>` arguments will load the file using the `load_config()`

```python
"""Usage: prog.py [--help] [--version] [-c CONFIG] --file FILE

Options:
  --help                show this message and exit
  --version             show the version number and exit
  -c, --config CONFIG   load this configuration file (supported: .toml, .json, .env)
  --file FILE           the file to process
"""

def main():
    args = parse_docopt(__doc__, version=__version__)
    args.file # has the value of --file

if __name__ == "__main__":
    main()
```

Building on top of `docopt` we strip off leading dashes and convert them to underscores so that we can access the arguments as `AttrDict` attributes.

[Read more about `attrbox.config`](https://metaist.github.io/attrbox/config.html)

## JSend

`JSend` is an approximate implementation of the [`JSend` specification](https://labs.omniti.com/labs/jsend) that makes it easy to create standard JSON responses. The main difference is that I added an `ok` attribute to make it easy to tell if there was a problem (`fail` or `error`).

```python
from attrbox import JSend

def some_function(arg1):
    result = JSend() # default is "success"

    if not is_good(arg1):
        # fail = controlled problem
        return result.fail(message="You gone messed up.")

    try:
        result.success(data=process(arg1))
    except Exception:
        # error = uncontrolled problem
        return result.error(message="We have a problem.")

    return result
```

Because the `JSend` object is an `AttrDict`, it acts like a `dict` in every other respect (e.g., it is JSON-serializable).

[Read more about `JSend`](https://metaist.github.io/attrbox/jsend.html#attrbox.jsend.JSend)

## License

[MIT License](https://github.com/metaist/attrbox/blob/main/LICENSE.md)
