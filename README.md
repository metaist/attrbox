# attrbox

_Functional-style and attribute-based data structures._

[![Build Status](https://img.shields.io/github/actions/workflow/status/metaist/attrbox/.github/workflows/ci.yaml?branch=main&style=for-the-badge)](https://github.com/metaist/attrbox/actions)
[![attrbox on PyPI](https://img.shields.io/pypi/v/attrbox.svg?color=blue&style=for-the-badge)](https://pypi.org/project/attrbox)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/attrbox?style=for-the-badge)](https://pypi.org/project/attrbox)

[Changelog] - [Issues] - [Documentation]

[changelog]: https://github.com/metaist/attrbox/blob/main/CHANGELOG.md
[issues]: https://github.com/metaist/attrbox/issues
[documentation]: https://metaist.github.io/attrbox/

## Why?

`AttrDict` deals with shortcomings of the standard python `dict`:

- You can use attribute syntax (`thing.prop` instead of `thing["prop"]`).
- Instead of handling `KeyError` or using `.get(None)`, you can just get a `None` by default.
- It's easy to merge nested `dict` objects using the `<<` operator.

`AttrList` lets you build a powerful container that can easily query attributes of its members.

`JSend` is a rough implementation of the [`JSend` sepecification](https://labs.omniti.com/labs/jsend) that makes it easy to create standard JSON responses.

## Install

```bash
pip install attrbox
```

## Example

```python
import json
from attrbox import AttrDict

config = AttrDict() << json.load(open('test/example-appengine.json'))
print(config.deployment.files["example-resource-file1"].sourceUrl)
# => "https://storage.googleapis.com/[MY_BUCKET_ID]/example-application/example-resource-file1"
```

## License

[MIT License](https://github.com/metaist/attrbox/blob/main/LICENSE.md)
