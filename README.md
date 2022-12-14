
<h1 align="center">OpenMath for Python</h1>
<h3 align="center implementation of the OpenMath standard</h3>
<p align="center">
<img src="https://img.shields.io/badge/python-3.10-306998?style=for-the-badge&logo=python&logoColor=ffdc51">
<a href="https://www.openmath.org"><img src="https://img.shields.io/badge/OpenMath-2.0-5b78fd?style=for-the-badge"></a>
<!--img src="https://img.shields.io/badge/version-v1.0-informational?style=for-the-badge"/-->
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational?style=for-the-badge"/></a>
</p>

This package provides the classes and functions necessary to work with _most_ of the [OpenMath standard v2.0](https://openmath.org/standard/om20-2019-07-01/), plus additional utilities.

## Features

- Implementation of the OpenMath objects with a minimal interface for their manipulation.
- De/serialization from/to JSON and XML.
- Intuitive access to remote Content Dictionaries, directly from the OpenMath objects.
- Submodules for more complex operations like evaluation or representation.

### What is not implemented

The parts of the standard not supported by the library are:

- The XML encoding of bytearray objects.
- IDs and references.
- Foreign objects (`OMFOREIGN`).

## Contributors

This list is empty right now.

## Contributing

- Read the [CONTRIBUTING](CONTRIBUTING.md) file if you want to contribute to the code.
- Open a new issue [![issues](https://img.shields.io/github/issues/MiguelMJ/openmath?logo=github&style=social)](https://github.com/MiguelMJ/openmath/issues/new) to make a request or report a bug.
- Add more tests, examples, use cases, documentation, etc for the library.
- And of course, :star: **star this repository** and give it some visibility [![stargazers](https://img.shields.io/github/stars/MiguelMJ/openmath?logo=github&style=social)](https://github.com/MiguelMJ/openmath/stargazers).

## Modules

### `openmath`

The main module provides the implementation of the standard, properly. This means: the classes for OpenMath objects and the de/serializing functions. The submodules, on the other hand, provide a richer set of functions to work with these objects.

### `openmath.cd`

Allows the user to load Content Dictionaries, both local and remote, and access their information.

### `openmath.config`

Controls the user configuration for the following submodules.

### `openmath.eval`

Provides a function to evaluate application mathematical objects into a single value.

### `openmath.latex`

Provides a function to convert mathematical objects into LaTex.

### `openmath.mathml`

Wraps the `openmath.latex` module and converts its LaTex output into MathML using [latex2mathml](https://github.com/roniemartinez/latex2mathml).

### Content Dictionaries support

Only official dictionaries will be supported for now.

| CD | `eval`| `latex` & `mathml` |
|---:|:---:|:---:|
| alg1 | :x: | :x: |
| altenc | :x: | :x: |
| arith1 | :heavy_check_mark: | :heavy_check_mark: |
| bigfloat1 | :x: | :x: |
| calculus1 | :x: | :x: |
| complex1 | :x: | :x: |
| error | :x: | :x: |
| fns1 | :x: | :x: |
| fns2 | :x: | :x: |
| integer1 | :x: | :x: |
| interval1 | :x: | :heavy_check_mark: |
| limit1 | :x: | :x: |
| linalg1 | :x: | :x: |
| linalg2 | :x: | :x: |
| list1 | :x: | :x: |
| list1 | :x: | :x: |
| logic1 | :x: | :x: |
| mathmlattr | :x: | :x: |
| mathmltypes | :x: | :x: |
| meta | :x: | :x: |
| metagrp | :x: | :x: |
| metasig | :x: | :x: |
| minmax1 | :x: | :x: |
| multiset1 | :x: | :x: |
| nums1 | :x: | :x: |
| piece1 | :x: | :x: |
| quant1 | :x: | :x: |
| relation1 | :x: | :x: |
| relation3 | :x: | :x: |
| rounding1 | :x: | :x: |
| s_data1 | :x: | :x: |
| s_dist1 | :x: | :x: |
| set1 | :x: | :x: |
| setname1 | :x: | :x: |
| sts | :x: | :x: |
| transc1 | :x: | :x: |
| veccalc1 | :x: | :x: |
| list1 | :x: | :x: |

## License

This package is licensed under the [MIT License](LICENSE).