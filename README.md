![Logo: кошка Свинья](https://i.imgur.com/5AHvXQm.jpeg)

# catpig

[![License](https://img.shields.io/badge/License-CC0-blue)](https://github.com/hakavlad/catpig/blob/main/LICENSE)
[![Releases](https://img.shields.io/github/v/release/hakavlad/catpig)](https://github.com/hakavlad/catpig/releases)
[![PyPI](https://img.shields.io/pypi/v/catpig?color=blue&label=PyPI)](https://pypi.org/project/catpig/)
[![CodeQL](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml/badge.svg)](https://github.com/hakavlad/catpig/actions/workflows/codeql.yml)

`catpig` is a [memory-hard](https://en.wikipedia.org/wiki/Memory-hard_function) [key derivation function](https://en.wikipedia.org/wiki/Key_derivation_function).

It uses `SHAKE256` to create data that will occupy memory of a given size (`space_mib`).

The data will be read in 4096-byte chunks with a pseudo-random offset and hashed by the `BLAKE2b` function.

Memory access patterns during reading of the first half of a given amount of data depend only on the salt (iMHF). Memory access patterns during reading of the second half of a given amount of data also depend the results of previous steps (dMHF).

## Install

```bash
pip install catpig
```

## Usage

```python
from catpig.catpig import catpig
derived_key = catpig(password, salt, space_mib, passes, dklen=64)
```

`password` and `salt` must be bytes-like objects.

`space_mib` defines the memory usage in mebibytes.

`passes` defines the amount of data that will be read and hashed by the `BLAKE2b` function. One pass corresponds to the `space_mib` size.

`dklen` is the length of the derived key.

## Test vectors

```python
>>> from catpig.catpig import catpig
>>>
>>> catpig(b'', b'', space_mib=1, passes=1, dklen=64).hex()
'd7353e5679fae8c0ade683d093e449f314e98b744b08f5e05393450979c52fb579ecead60b27190f9facc3b40422ab87a75cdb706db02e3024d7469954a2b954'
>>>
>>> catpig(password=b'password', salt=b'salt', space_mib=64, passes=4).hex()
'79826615260804f0a114f5689225b2fc72e90d9b367d5bff9ba86b9adc94e71b5f55b31f098247cdc12f6ee32055bedf37454ff7cc47367096293f6b38737fb4'
>>>
>>> catpig(password=b'passphrase', salt=b'NaCl', space_mib=512, passes=8).hex()
'9f842ee90b2bb079dc88e867cff3184e17d8c35ecc6042cc2cbce1128af34fe764f1ffeff542fcb56cee6a4ef12a2393e96be5cd8baeeb109729a82a060e1794'
>>>
>>> catpig(password=b'new_passphrase', salt=b'SodiumChloride', space_mib=5000, passes=15).hex()
'5c2a79e4f0b69e00b3676e9c7b1a3159bc77c5153b1e88bed6fbae1497143caeb4d901a65324f496461eeb4c72b6a6cb9938c7be04aee33abd4dd83fa3306d57'
```

## Warnings

- The author is not an expert in cryptography.
- `catpig` has not been independently audited.

## Requirements

- Python >= 3.6
