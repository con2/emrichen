# Emrichen – A YAML to YAML preprocessor

Emrichen takes in YAML, performs transformations and outputs YAML.

Currently the only supported transformation is substituting variables defined in either variable files (also YAML) or the command line. The full type system of YAML is supported in the values of the variables.

## Installation

Python 3.6+ required.

    pip3 install git+https://github.com/japsu/emrichen.git

## Supported tags

* `!Var VAR_NAME` – replaced with the value of the variable
* `!Format FORMAT_STRING` – interpolate strings using [Python format strings](https://docs.python.org/3/library/string.html#formatstrings) such as `"{foo} {bar!d}"`
    * **NOTE:** When the format string starts with `{`, you need to quote it in order to avoid being interpreted as a YAML object.

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

    Variable precedence: -D > -e > -f

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
