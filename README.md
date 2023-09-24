![Logo: кошка Свинья](https://i.imgur.com/5AHvXQm.jpeg)

# catpig

[![License](https://img.shields.io/badge/License-CC0-blue)](https://github.com/hakavlad/catpig/blob/main/LICENSE)
[![Releases](https://img.shields.io/github/v/release/hakavlad/catpig)](https://github.com/hakavlad/catpig/releases)
[![PyPI](https://img.shields.io/pypi/v/catpig?color=blue&label=PyPI)](https://pypi.org/project/catpig/)
[![CodeQL](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml/badge.svg)](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml)
[![Semgrep](https://github.com/hakavlad/catpig/actions/workflows/semgrep.yml/badge.svg)](https://github.com/hakavlad/catpig/actions/workflows/semgrep.yml)
[![Codacy Security Scan](https://github.com/hakavlad/catpig/actions/workflows/codacy.yml/badge.svg)](https://github.com/hakavlad/catpig/actions/workflows/codacy.yml)

`catpig` is a [memory-hard](https://en.wikipedia.org/wiki/Memory-hard_function) [key derivation function](https://en.wikipedia.org/wiki/Key_derivation_function).

## Install

```
pip install catpig
```

## Usage

```
from catpig.catpig import catpig
derived_key = catpig(password, salt, space_mib=64, passes=4, dklen=64)
```

`password` and `salt` must be bytes-like objects.

`space_mib` defines the memory usage in mebibytes.

`passes` defines the amount of data that will be read and hashed by the `BLAKE2b` function. One pass corresponds to the `space_mib` size.

`dklen` is the length of the derived key.


## Test vectors

```
>>> from catpig.catpig import catpig
>>> password = b'password'
>>> salt = b'salt'
>>> derived_key = catpig(password, salt)
>>> derived_key.hex()
'79826615260804f0a114f5689225b2fc72e90d9b367d5bff9ba86b9adc94e71b5f55b31f098247cdc12f6ee32055bedf37454ff7cc47367096293f6b38737fb4'
>>> password = b'foo'
>>> salt = b'bar'
>>> derived_key = catpig(password, salt, space_mib=512, passes=8, dklen=32)
>>> derived_key.hex()
'697c8c936ca0442767ab73f6954dd927eb9dee019aa8bcc222769b49bcf64db1'
>>> derived_key = catpig(password, salt, space_mib=4096, passes=16)
>>> derived_key.hex()
'257b34c4d454419eacae1d71a1c2c64ab50cb408890df98faf1b153f4199e5efbab3c56bb930fc6b4c28f3ef978e96a83a650c2e965c6aaec4ba43330d72138b'
```

## Warnings

- The author is not an expert in cryptography.
- `catpig` has not been independently audited.

## Requirements

- Python >= 3.6
