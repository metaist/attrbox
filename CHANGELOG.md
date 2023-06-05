# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to [Semantic Versioning].

Sections order is: `Fixed`, `Changed`, `Added`, `Deprecated`, `Removed`, `Security`.

[keep a changelog]: http://keepachangelog.com/en/1.0.0/
[semantic versioning]: http://semver.org/spec/v2.0.0.html

---

## [Unreleased]

[unreleased]: https://github.com/metaist/attrbox/compare/prod...main

These are changes that are on `main` that are not yet in `prod`.

---

[0.1.4]: https://github.com/metaist/attrbox/compare/0.1.3...0.1.4

## [0.1.4] - 2023-06-05T11:25:13Z

Pushing on `prod` starts a release PyPI using GitHub Actions. Pushing twice on `prod` with quick succession without updating the version number causes both pushes to fail.

This is a zero-change version bump to cause the release to be successful.

---

[#11]: https://github.com/metaist/attrbox/issues/11
[0.1.3]: https://github.com/metaist/attrbox/compare/0.1.2...0.1.3

## [0.1.3] - 2023-06-05T03:14:31Z

**Fixed**

- [#11]: add `py.typed`

---

[#1]: https://github.com/metaist/attrbox/issues/1
[#2]: https://github.com/metaist/attrbox/issues/2
[#3]: https://github.com/metaist/attrbox/issues/3
[#4]: https://github.com/metaist/attrbox/issues/4
[#5]: https://github.com/metaist/attrbox/issues/5
[#6]: https://github.com/metaist/attrbox/issues/6
[#7]: https://github.com/metaist/attrbox/issues/7
[#8]: https://github.com/metaist/attrbox/issues/8
[#9]: https://github.com/metaist/attrbox/issues/9
[#10]: https://github.com/metaist/attrbox/issues/10
[0.1.2]: https://github.com/metaist/attrbox/compare/0.1.1...0.1.2

## [0.1.2] - 2023-06-01T04:33:39Z

**Fixed**

- [#1]: README badges
- [#7]: top-level imports
- [#8]: using `.startswith` and `.endswith` per PEP 8

**Changed**

- [#4]: Supported python versions are now 3.8, 3.9, 3.10, 3.11

**Added**

- Explicit `encoding=utf-8` when reading files.
- [#6]: `AttrDict.__contains__` to support complex keys
- `.toml` configuration loading
- [#2]: docopt configuration loading
- [#5]: `.env` configuration loading
- [#9]: dotted keys for `.env` value expansion
- [#10]: generic get/set functions for `dict` and `list`

**Removed**

- [#3]: functional wrappers for a uniform `list` + `dict` interface. This was never published to PyPI, but this was something I had briefly published to `main`.

---

[0.1.1]: https://github.com/metaist/attrbox/compare/0.1.0...0.1.1

## [0.1.1] - 2021-09-23T20:37:52Z

**Fixed**

- PyPI tags
- GitHub action workflow
- explicit `encoding="utf-8"` for reading files

---

[0.1.0]: https://github.com/metaist/attrbox/commits/0.1.0

## [0.1.0] - 2021-09-23T20:06:43Z

Initial release.
