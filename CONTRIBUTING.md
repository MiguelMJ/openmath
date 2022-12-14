# Contributing to Openmath for Python

Thanks for thinking about contributing to Openmath for Python! Here are the steps to do it.

1. Read this document (you are on the right path in this moment).
2. Check if there's any open issue with your idea, and whether it is already assigned to someone or not.
3. If it is not, then you can open a new issue or comment in the existent one and I will assign it to you.
4. Fork the repo and make your changes in the dev branch.
5. Make a pull request.

## Where is help wanted?

- Adding support for more content dictionaries in the submodules (see below).
- Writing more extensive tests.
- Documenting new use cases or adding functioning examples.
- Improving the existing documentation,  maybe start the GitHub wiki.

## How to add support to a Content Dictionary

The first thing you have to do is to create a new `.py` file with the name of the dictionary in the directory of the submodule. See the `arith1.py` files [[1](openmath/eval/arith1.py)][[2](openmath/latex/arith1.py)] as example.

The content of the files depend on the submodule you are contributing to.

### `eval` submodule

The file must have:
- **For each symbol in the dictionary**:
  - If the role of the symbol is `application`, then a function with the same name, that implements the application described in the dictionary.
  - If the role of the symbol is `constant`, then a variable (python doesn't have proper constants) with the same name and the value described in the dictionary.
  - Other roles are not currently supported for evaluation.

### `latex` submodule

*Note that any support added to* `latex` *translates into support for* **`mathml`** thanks to [latex2mathml](https://github.com/roniemartinez/latex2mathml).

The file must have:
- **For each symbol in the dictionary**:
  - A function with the same name, that takes as arguments the LaTeX representation of the arguments described in the dictionary, if any. This function must return a string in LaTeX format.
    - Alternatively, a variable with the same name containing a tuple with the form `(<latexcode>, <"infix"|"call"|"suffix"|"prefix">)`, as a shortcut for general representation of operators and calls.
- Optionally, a list called **`priority`**, containing `openmath.Symbol` objects in desdending order of operator priority. This will be used to correctly enclose operations between parenthesis.
