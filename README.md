
<h1 align="center">OpenMath for Python</h1>
<h3 align="center">Unofficial implementation of the OpenMath standard</h3>
<p align="center">
<img src="https://img.shields.io/badge/python-3.10-306998?style=for-the-badge&logo=python&logoColor=ffdc51">
<a href="https://www.openmath.org"><img src="https://img.shields.io/badge/OpenMath-v2.0-5b78fd?style=for-the-badge"></a>
<!--img src="https://img.shields.io/badge/version-v1.0-informational?style=for-the-badge"/-->
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational?style=for-the-badge"/></a>
</p>

This package provides the classes and functions necessary to work with _most_ of the [OpenMath standard v2.0](https://openmath.org/standard/om20-2019-07-01/), plus additional utilities.

## Features

- Implementation of the OpenMath objects with a minimal interface for their manipulation.
- De/serialization from/to JSON and XML.
- Intuitive access to remote Content Dictionaries, directly from the OpenMath objects.
- Utility functions for more complex operations.

### What is not implemented

The parts of the standard not supported by the library are:

- The XML encoding of bytearray objects.
- IDs and references.
- Foreign objects (`OMFOREIGN`).

## Contributors

This list is empty right now.

## Contributing

- 

## Example

```python
import openmath as OM
import openmath.cd
from openmath.util import replace

# this mathematical object is: 3*x + 1
obj = OM.Object(
    OM.Application(
        OM.Symbol("plus", "arith1"),
        OM.Application(
            OM.Symbol("product", "arith1"),
            OM.Integer(3),
            OM.Variable("x")
        ),
        OM.Integer(1)
    ),
    cdbase="http://www.openmath.org/cd"
)
# try the encoding
inXML = obj.toXML(indent=2)
print(inXML)
print(obj == OM.parse(inXML))

inJSON = obj.toJSON(indent=2)
print(inJSON)
print(obj == OM.parse(inJSON))

# make some changes
# directly on the object
minus = OM.Symbol("minus", "arith1")
obj.object.applicant = minus

# or via the utilities
replace(obj, OM.Variable("x"), OM.Float(1.5))

print(obj.toXML(indent=2))

# get some information about the symbols
print(OM.cd.help(minus))
```

<details>

<summary>
Click here to see the output
</summary>

```
<?xml version="1.0" ?>
<OMOBJ xmlns="http://www.openmath.org/OpenMath" cdbase="http://www.openmath.org/cd">
  <OMA>
    <OMS name="plus" cd="arith1"/>
    <OMA>
      <OMS name="product" cd="arith1"/>
      <OMI>3</OMI>
      <OMV name="x"/>
    </OMA>
    <OMI>1</OMI>
  </OMA>
</OMOBJ>

True
{
  "kind": "OMOBJ",
  "cdbase": "http://www.openmath.org/cd",
  "object": {
    "kind": "OMA",
    "applicant": {
      "kind": "OMS",
      "cd": "arith1",
      "name": "plus"
    },
    "arguments": [
      {
        "kind": "OMA",
        "applicant": {
          "kind": "OMS",
          "cd": "arith1",
          "name": "product"
        },
        "arguments": [
          {
            "kind": "OMI",
            "integer": 3
          },
          {
            "kind": "OMV",
            "name": "x"
          }
        ]
      },
      {
        "kind": "OMI",
        "integer": 1
      }
    ]
  }
}
True
<?xml version="1.0" ?>
<OMOBJ xmlns="http://www.openmath.org/OpenMath" cdbase="http://www.openmath.org/cd">
  <OMA>
    <OMS name="minus" cd="arith1"/>
    <OMA>
      <OMS name="product" cd="arith1"/>
      <OMI>3</OMI>
      <OMF>1.5</OMF>
    </OMA>
    <OMI>1</OMI>
  </OMA>
</OMOBJ>

('application', 'The symbol representing a binary minus function. This is equivalent to\nadding the additive inverse.')

```

</details>

## License

This package is licensed under the [MIT License](LICENSE).