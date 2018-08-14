# Emrichen – A YAML to YAML preprocessor

Emrichen takes in YAML, performs transformations and outputs YAML.

Currently the only supported transformation is substituting variables defined in either variable files (also YAML) or the command line. The full type system of YAML is supported in the values of the variables.

## Installation

Python 3.6+ required.

    pip3 install git+https://github.com/japsu/emrichen.git

## Supported tags

| Tag | Arguments | Example | Description |
|-----|-----------|---------|-------------|
| `!Defaults` | A dict of variable definitions | See `examples/defaults/` | Defines default values for variables. These will be overridden by any other variable source. **NOTE:** `!Defaults` must appear in a document of its own in the template file (ie. separated by `---`). The document containing `!Defaults` will be erased from the output. |
| `!Error` | Error message | `!Error "Must define either foo or bar, not both"` | If the `!Error` tag is present in the template after resolving all conditionals, it will cause the template rendering to exit with error emitting the specified error message. |
| `!Exists` | JSONPath expression | `!Exists foo` | Returns `true` if the JSONPath expression returns one or more matches, `false` otherwise. |
| `!Filter` | TBD | See `tests/test_cond.py` | Takes in a list and only returns elements that pass a predicate. |
| `!Format` | Format string | `!Var "{foo} {bar!d}"` | Interpolate strings using [Python format strings](https://docs.python.org/3/library/string.html#formatstrings). JSONPath supported in variable lookup (eg. `{people[0].first_name}` will do the right thing). **NOTE:** When the format string starts with `{`, you need to quote it in order to avoid being interpreted as a YAML object. |
| `!If` | TBD | See `tests/test_cond.py` | Returns one of two values based on a condition. |
| `!Lookup` | JSONPath expression | `!Lookup people[0].first_name` | Performs a JSONPath lookup returning the first match. If there is no match, an error is raised. |
| `!LookupAll` | JSONPath expression | `!Lookup people[*].first_name` | Performs a JSONPath lookup returning all matches as a list. If no matches are found, the empty list `[]` is returned. |
| `!Loop` | `over:` (required) The data to iterate over (a literal list or dict, or `!Var`)<br>`as`: (optional, default `item`) The variable name given to the current value<br>`index_as:` (optional) The variable name given to the loop index. If `over` is a list, this is a numeric index starting from `0`. If `over` is a dict, this is the dict key.<br>`template:` (required) The template to process for each iteration of the loop. | See `examples/loop/`. | Loops over a list or dict and renders a template for each iteration. The output is always a list.
| `!Var` | Variable name | `!Var image_name` | Replaced with the value of the variable. |
| `!Void` | None | `foo: !Void` | The dict key, list item or YAML document that resolves to `!Void` is removed from the output. |
| `!With` | `vars:` A dict of variable definitions.<br>`template:` The template to process with the variables defined. | See `examples/with/`. | Binds local variables that are only visible within `template`. Useful for giving a name for common sub-expressions. |

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
