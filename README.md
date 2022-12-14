
<h1 align="center">OpenMath for Python</h1>
<h3 align="center">Unofficial implementation of the OpenMath standard</h3>
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

|||
|---|---|
| :heavy_check_mark: | Supported |
| :x: | Not supported |
| :construction: | Partially supported |

#### Official

| CD | `eval`| `latex` & `mathml` |
|---:|:---:|:---:|
| [alg1](http://www.openmath.org/cd/alg1) | :heavy_check_mark: | :heavy_check_mark: |
| [altenc](http://www.openmath.org/cd/altenc) | :x: | :x: |
| [arith1](http://www.openmath.org/cd/arith1) | :heavy_check_mark: | :heavy_check_mark: |
| [bigfloat1](http://www.openmath.org/cd/bigfloat1) | :x: | :x: |
| [calculus1](http://www.openmath.org/cd/calculus1) | :x: | :x: |
| [complex1](http://www.openmath.org/cd/complex1) | :x: | :x: |
| [error](http://www.openmath.org/cd/error) | :x: | :x: |
| [fns1](http://www.openmath.org/cd/fns1) | :construction: | :x: |
| [fns2](http://www.openmath.org/cd/fns2) | :x: | :x: |
| [integer1](http://www.openmath.org/cd/integer1) | :heavy_check_mark: | :heavy_check_mark: |
| [interval1](http://www.openmath.org/cd/interval1) | :heavy_check_mark: | :heavy_check_mark: |
| [limit1](http://www.openmath.org/cd/limit1) | :x: | :x: |
| [linalg1](http://www.openmath.org/cd/linalg1) | :x: | :x: |
| [linalg2](http://www.openmath.org/cd/linalg2) | :x: | :x: |
| [list1](http://www.openmath.org/cd/list1) | :x: | :x: |
| [list1](http://www.openmath.org/cd/list1) | :x: | :x: |
| [logic1](http://www.openmath.org/cd/logic1) | :x: | :x: |
| [mathmlattr](http://www.openmath.org/cd/mathmlattr) | :x: | :x: |
| [mathmltypes](http://www.openmath.org/cd/mathmltypes) | :x: | :x: |
| [meta](http://www.openmath.org/cd/meta) | :x: | :x: |
| [metagrp](http://www.openmath.org/cd/metagrp) | :x: | :x: |
| [metasig](http://www.openmath.org/cd/metasig) | :x: | :x: |
| [minmax1](http://www.openmath.org/cd/minmax1) | :x: | :x: |
| [multiset1](http://www.openmath.org/cd/multiset1) | :x: | :x: |
| [nums1](http://www.openmath.org/cd/nums1) | :construction: | :heavy_check_mark: |
| [piece1](http://www.openmath.org/cd/piece1) | :x: | :x: |
| [quant1](http://www.openmath.org/cd/quant1) | :x: | :x: |
| [relation1](http://www.openmath.org/cd/relation1) | :x: | :x: |
| [relation3](http://www.openmath.org/cd/relation3) | :x: | :x: |
| [rounding1](http://www.openmath.org/cd/rounding1) | :x: | :x: |
| [s_data1](http://www.openmath.org/cd/s_data1) | :x: | :x: |
| [s_dist1](http://www.openmath.org/cd/s_dist1) | :x: | :x: |
| [set1](http://www.openmath.org/cd/set1) | :x: | :x: |
| [setname1](http://www.openmath.org/cd/setname1) | :x: | :x: |
| [sts](http://www.openmath.org/cd/sts) | :x: | :x: |
| [transc1](http://www.openmath.org/cd/transc1) | :x: | :x: |
| [veccalc1](http://www.openmath.org/cd/veccalc1) | :x: | :x: |
| [list1](http://www.openmath.org/cd/list1) | :x: | :x: |

## License

This package is licensed under the [MIT License](LICENSE).