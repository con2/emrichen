# Emrichen – A YAML to YAML preprocessor

Emrichen takes in YAML, performs transformations and outputs YAML.

Currently the only supported transformation is substituting variables defined in either variable files (also YAML) or the command line. The full type system of YAML is supported in the values of the variables.

## Installation

Python 3.6+ required.

    pip3 install git+https://github.com/japsu/emrichen.git

## Supported tags

<!-- This table is updated by `update_readme.py`; please don't edit by hand. -->
<!-- START SUPPORTED TAGS -->
| Tag | Arguments | Example | Description |
|-----|-----------|---------|-------------|
| `!All` | An iterable | `!All [true, false]` | Returns true iff all the items of the iterable argument are truthy. |
| `!Any` | An iterable | `!Any [true, false]` | Returns true iff at least one of the items of the iterable argument is truthy. |
| `!Base64` | The value to encode | `!Base64 foobar` | Encodes the value (or a string representation thereof) into base64. |
| `!Compose` | `value`: The value to apply tags on <br> `tags`: A list of tag names to apply, latest first | `!Base64,Var foo` | Used internally to implement tag composition. <br> Usually not used in the spelt-out form. <br> See _Tag composition_ below. |
| `!Concat` | A list of lists | `!Concat [[1, 2], [3, 4]]` | Concatenates lists. |
| `!Defaults` | A dict of variable definitions | See `examples/defaults/` | Defines default values for variables. These will be overridden by any other variable source. <br> **NOTE:** `!Defaults` must appear in a document of its own in the template file (ie. separated by `---`).   The document containing `!Defaults` will be erased from the output. |
| `!Error` | Error message | `!Error "Must define either foo or bar, not both"` | If the `!Error` tag is present in the template after resolving all conditionals, <br> it will cause the template rendering to exit with error emitting the specified error message. |
| `!Exists` | JSONPath expression | `!Exists foo` | Returns `true` if the JSONPath expression returns one or more matches, `false` otherwise. |
| `!Filter` | `test`, `over` | See `tests/test_cond.py` | Takes in a list and only returns elements that pass a predicate. |
| `!Format` | Format string | `!Var "{foo} {bar!d}"` | Interpolate strings using [Python format strings](https://docs.python.org/3/library/string.html#formatstrings). <br> JSONPath supported in variable lookup (eg. `{people[0].first_name}` will do the right thing). <br> **NOTE:** When the format string starts with `{`, you need to quote it in order to avoid being interpreted as a YAML object. |
| `!If` | `test`, `then`, `else` | See `tests/test_cond.py` | Returns one of two values based on a condition. |
| `!Include` | Path to a template to include | `!Include ../foo.yml` | Renders the requested template at this location. Both absolute and relative paths work. |
| `!IncludeBase64` | Path to a binary file | `!IncludeBase64 ../foo.pdf` | Loads the given binary file and returns the contents encoded as Base64. |
| `!IncludeBinary` | Path to a binary file | `!IncludeBinary ../foo.pdf` | Loads the given binary file and returns the contents as bytes.  This is practically only useful for hashing. |
| `!IncludeText` | Path to an UTF-8 text file | `!IncludeText ../foo.toml` | Loads the given UTF-8 text file and returns the contents as a string. |
| `!Join` | `items`: (required) A list of items to be joined together. <br> `separator`: (optional, default space) The separator to place between the items. <br> **OR** <br> a list of items to be joined together with a space as the separator. | `!Join [foo, bar]` <br> `!Join { items: [foo, bar], separator: ', ' }` | Joins a list of items together with a separator. The result is always a string. |
| `!Lookup` | JSONPath expression | `!Lookup people[0].first_name` | Performs a JSONPath lookup returning the first match. If there is no match, an error is raised. |
| `!LookupAll` | JSONPath expression | `!LookupAll people[*].first_name` | Performs a JSONPath lookup returning all matches as a list. If no matches are found, the empty list `[]` is returned. |
| `!Loop` | `over`: (required) The data to iterate over (a literal list or dict, or !Var) <br> `as`: (optional, default `item`) The variable name given to the current value <br> `index_as`: (optional) The variable name given to the loop index. If over is a list, this is a numeric index starting from `0`. If over is a dict, this is the dict key. <br> `index_start`: (optional, default `0`) First index, for eg. 1-based indexing. <br> `template`: (required) The template to process for each iteration of the loop. | See `examples/loop/`. | Loops over a list or dict and renders a template for each iteration. The output is always a list. |
| `!MD5` | Data to hash | `!Include ../foo.yml` | Hashes the given data using the given algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!Merge` | A list of dicts | `!Merge [{a: 5}, {b: 6}]` | Merges objects. For overlapping keys the last one takes precedence. |
| `!Not` | a value | `!Not !Var foo` | Logically negates the given value (in Python semantics). |
| `!Op` | `a`, `op`, `b` | See `tests/test_cond.py` | Performs binary operators. Especially useful with `!If` to implement greater-than etc. |
| `!SHA1` | Data to hash | `!Include ../foo.yml` | Hashes the given data using the given algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!SHA256` | Data to hash | `!Include ../foo.yml` | Hashes the given data using the given algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!URLEncode` | A string to encode <br> **OR** <br> `url`: The URL to combine query parameters into <br> `query`: An object of query string parameters to add. | `!URLEncode "foo+bar"` <br> `!URLEncode { url: "https://example.com/", query: { foo: bar } }` | Encodes strings for safe inclusion in a URL, or combines query string parameters into a URL. |
| `!Var` | Variable name | `!Var image_name` | Replaced with the value of the variable. |
| `!Void` | Anything or nothing | `foo: !Void` | The dict key, list item or YAML document that resolves to `!Void` is removed from the output. |
| `!With` | `vars`: A dict of variable definitions. <br> `template`: The template to process with the variables defined. | See `examples/with/`. | Binds local variables that are only visible within `template`. Useful for giving a name for common sub-expressions. |
<!-- END SUPPORTED TAGS -->

### Tag composition

Due to YAML, you can't do `!Base64 !Var foo`. We provide a convenient workaround: `!Base64,Var foo`.

## CLI

    usage: emrichen [-h] [--var-file VAR_FILES] [--define VAR=VALUE]
                    [--output-file OUTPUT_FILE] [--include-env]
                    [template_file]

    A YAML to YAML preprocessor.

    positional arguments:
      template_file         The YAML template to process. If unspecified, the
                            template is read from stdin.

    optional arguments:
      -h, --help            show this help message and exit
      --var-file VAR_FILE, -f VAR_FILE
                            A YAML file containing an object whose top-level keys
                            will be defined as variables. May be specified
                            multiple times.
      --define VAR=VALUE, -D VAR=VALUE
                            Defines a single variable. May be specified multiple
                            times.
      --output-file OUTPUT_FILE, -o OUTPUT_FILE
                            Output file. If unspecified, the template output is
                            written into stdout.
      --include-env, -e     Expose process environment variables to the template.

    Variable precedence: -D > -e > -f > !Defaults

### Examples

    cd examples/kubernetes
    emrichen -f vars.yml -D tag=build-256 deployment.in.yml

## Python API

TODO

### `emrichen(template, *variable_sources, **override_variables)`

### `Context(*variable_sources, **override_variables)`

### `Template(template_source)`

## License

    The MIT License (MIT)

    Copyright © 2018 Santtu Pajukanta
    Copyright © 2018 Aarni Koskela

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
