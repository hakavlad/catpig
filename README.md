![Logo: кошка Свинья](https://i.imgur.com/5AHvXQm.jpeg)

# catpig

[![License](https://img.shields.io/badge/License-CC0-blue)](https://github.com/hakavlad/catpig/blob/main/LICENSE)
[![Releases](https://img.shields.io/github/v/release/hakavlad/catpig)](https://github.com/hakavlad/catpig/releases)
[![PyPI](https://img.shields.io/pypi/v/catpig?color=blue&label=PyPI)](https://pypi.org/project/catpig/)
[![CodeQL](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml/badge.svg)](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml)

`catpig` is a [memory-hard](https://en.wikipedia.org/wiki/Memory-hard_function) [password-hashing function](https://en.wikipedia.org/wiki/Key_derivation_function).

It uses `SHAKE256` to create data that will occupy memory of a given size (`space_mib`).

The data will be read in 4096-byte chunks with a pseudo-random offset and hashed by the `BLAKE2b` function.

Memory access patterns during reading of the first half of a given amount of data depend only on the salt (iMHF). Memory access patterns during reading of the second half of a given amount of data also depend the results of previous steps (dMHF).

The output length is always 64 bytes.

## Install

```bash
pip install catpig
```

## Usage

```python
from catpig.catpig import catpig

derived_key = catpig(password, salt, space_mib, passes)
```

`password` and `salt` must be bytes-like objects.

`space_mib` defines the memory usage in mebibytes.

`passes` defines the amount of data that will be read and hashed by the `BLAKE2b` function. One pass corresponds to reading a data size equal to `space_mib`.

## Test vectors

```python
>>> from catpig.catpig import catpig
>>>
>>> catpig(b'', b'', space_mib=1, passes=1).hex()
'831e43e4a352066a8ade279225d95e7543203cce8ce77348e4f7898741f32b9f1b8793393aa69cef84016d5f391aa9a7840050c5c59b9defd6cc324cb44e3e9a'
>>>
>>> catpig(password=b'password', salt=b'salt', space_mib=64, passes=4).hex()
'd1999b1a7749de88ac8b6f1d8659ccf3b1c2cfe7fd84426bddc75de4b9f57bc07293cca52bb22e0915945d462bb760dfab02d78a713e65620307bc08b8fb7905'
>>>
>>> catpig(password=b'passphrase', salt=b'NaCl', space_mib=512, passes=8).hex()
'83b6181449eb405e7bb662642090c077298e445f63846a98f18b8102df5e80f8a50dcf43f951ce8e893aac5beb23d33e5282624fd288fac4d07b8647f6c9bffe'
>>>
>>> catpig(password=b'new_passphrase', salt=b'SodiumChloride', space_mib=5000, passes=15).hex()
'b4f96ceddf5c46380f6a425ebf2a30372cccfb3e4d7d95fd1cfc7c64910142eca3b7e61c20e32db7c97c72230c3b63abf1802dc068513297b67c274267fd1dde'
```

## Warnings

- The author is not an expert in cryptography.
- `catpig` has not been independently audited.

## Requirements

- Python >= 3.6
