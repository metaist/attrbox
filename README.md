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

I have some specific things I wish python `dict` and `list` could do:

- (`dict`) **Attribute Syntax**: `thing.prop` to mean `thing["prop"]`.
- (`dict`) **Suppress `KeyError`**: instead of `.get()` just give me `None` if I ask for a key that's not there.
- (`dict`) **Better Merge**: I want to merge nested `dict` objects.
- (`list`) **Broadcast to Members**: accessing an attribute or making a function call on the list should apply it to all the members.

`attrbox` also packages the most common use cases:

- `AttrDict`, `AttrList`: basic attribute-based improvements
- `JSend`: approximate implementation of the [`JSend` specification](https://labs.omniti.com/labs/jsend) that makes it easy to create standard JSON responses.

## Install

```bash
python -m pip install attrbox
```

## Example

```python
import json
from attrbox import AttrDict

config = AttrDict() << json.load(open('test/example-appengine.json'))
print(config.get(["deployment", "files", "example-resource-file1", "sourceUrl"])
# => "https://storage.googleapis.com/[MY_BUCKET_ID]/example-application/example-resource-file1"
```

## License

[MIT License](https://github.com/metaist/attrbox/blob/main/LICENSE.md)
