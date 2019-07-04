# Emrichen – Template engine for YAML & JSON

[![Build Status](https://travis-ci.org/japsu/emrichen.svg?branch=master)](https://travis-ci.org/japsu/emrichen) [![PyPI version](https://badge.fury.io/py/emrichen.svg)](https://badge.fury.io/py/emrichen)

Emrichen takes in templates written in YAML or JSON, processes tags that do things like variable substitution, and outputs YAML or JSON.

What makes Emrichen better for generating YAML or JSON than a text-based template system is that it works *within* YAML (or JSON).

Ever tried substituting a list or dict into a YAML document just to run into indentation issues? Horrible! Handling quotation marks and double backslash escapes? Nope!

In Emrichen, variables are typed in the familiar JSON types, making these a non-issue. Emrichen is a pragmatic and powerful way to generate YAML and JSON.

Consider the following template that produces a minimal Kubernetes deployment:

```yaml
!Defaults
tag: latest
image: !Format "nginx:{tag}"
replicas: 3
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: !Var replicas
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: !Var image
        ports:
        - containerPort: 80
```

This small template already demonstrates three of Emrichen's powerful tags: `!Defaults` that provides default values for variables; `!Var` that performs simple variable substitution; and `!Format` that performs string formatting.

Put it in a file, say, `nginx.in.yaml` (we use `.in.yaml` to denote templates) and render it using this command:

    emrichen nginx.in.yaml

Prefer JSON output?

    emrichen --output-format json nginx.in.yaml

Wanna change the tag?

    emrichen --define tag=1-alpine nginx.in.yaml

Note how `image` is evaluated lazily – you need not override `image` just to change `tag`!

See below for a table of supported tags. There's a lot of them. If you need one that's not there yet, please shoot us an issue or PR.

## Installation

Python 3.5+ required. Python 2 is not and will not be supported.

    pip3 install emrichen

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
| `!Debug` | Anything, really | `!Debug,Var foo` | Enriches its argument, outputs it to stderr and returns it. Useful to check the value <br> of some expression deep in a big template, perhaps even one that doesn't even fully render. |
| `!Defaults` | A dict of variable definitions | See `examples/defaults/` | Defines default values for variables. These will be overridden by any other variable source. <br> **NOTE:** `!Defaults` must appear in a document of its own in the template file (ie. separated by `---`).   The document containing `!Defaults` will be erased from the output. |
| `!Error` | Error message | `!Error "Must define either foo or bar, not both"` | If the `!Error` tag is present in the template after resolving all conditionals, <br> it will cause the template rendering to exit with error emitting the specified error message. |
| `!Exists` | JSONPath expression | `!Exists foo` | Returns `true` if the JSONPath expression returns one or more matches, `false` otherwise. |
| `!Filter` | `test`, `over` | See `tests/test_cond.py` | Takes in a list and only returns elements that pass a predicate. |
| `!Format` | Format string | `!Format "{foo} {bar!d}"` | Interpolate strings using [Python format strings](https://docs.python.org/3/library/string.html#formatstrings). <br> JSONPath supported in variable lookup (eg. `{people[0].first_name}` will do the right thing). <br> **NOTE:** When the format string starts with `{`, you need to quote it in order to avoid being interpreted as a YAML object. |
| `!Group` | Accepts the same arguments as `!Loop`, except `template` is optional (default identity), plus the following: <br> `by`: (required) An expression used to determine the key for the current value <br> `result_as`: (optional, string) When evaluating `by`, the enriched `template` is available under this name. | TBD | Makes a dict out of a list. Keys are determined by `by`. Items with the same key are grouped in a list. |
| `!If` | `test`, `then`, `else` | See `tests/test_cond.py` | Returns one of two values based on a condition. |
| `!Include` | Path to a template to include | `!Include ../foo.yml` | Renders the requested template at this location. Both absolute and relative paths work. |
| `!IncludeBase64` | Path to a binary file | `!IncludeBase64 ../foo.pdf` | Loads the given binary file and returns the contents encoded as Base64. |
| `!IncludeBinary` | Path to a binary file | `!IncludeBinary ../foo.pdf` | Loads the given binary file and returns the contents as bytes.  This is practically only useful for hashing. |
| `!IncludeText` | Path to an UTF-8 text file | `!IncludeText ../foo.toml` | Loads the given UTF-8 text file and returns the contents as a string. |
| `!Index` | Accepts the same arguments as `!Loop`, except `template` is optional (default identity), plus the following: <br> `by`: (required) An expression used to determine the key for the current value <br> `result_as`: (optional, string) When evaluating `by`, the enriched `template` is available under this name. <br> `duplicates`: (optional, default `error`) `error`, `warn(ing)` or `ignore` duplicate values. | TBD | Makes a dict out of a list. Keys are determined by `by`. |
| `!IsBoolean` | Data to typecheck. | `!IsBoolean ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!IsDict` | Data to typecheck. | `!IsDict ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!IsInteger` | Data to typecheck. | `!IsInteger ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!IsList` | Data to typecheck. | `!IsList ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!IsNone` | Data to typecheck. | `!IsNone ...` | Returns True if the value enriched is None (null) or Void, False otherwise. |
| `!IsNumber` | Data to typecheck. | `!IsNumber ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!IsString` | Data to typecheck. | `!IsString ...` | Returns True if the value enriched is of the given type, False otherwise. |
| `!Join` | `items`: (required) A list of items to be joined together. <br> `separator`: (optional, default space) The separator to place between the items. <br> **OR** <br> a list of items to be joined together with a space as the separator. | `!Join [foo, bar]` <br> `!Join { items: [foo, bar], separator: ', ' }` | Joins a list of items together with a separator. The result is always a string. |
| `!Lookup` | JSONPath expression | `!Lookup people[0].first_name` | Performs a JSONPath lookup returning the first match. If there is no match, an error is raised. |
| `!LookupAll` | JSONPath expression | `!LookupAll people[*].first_name` | Performs a JSONPath lookup returning all matches as a list. If no matches are found, the empty list `[]` is returned. |
| `!Loop` | `over`: (required) The data to iterate over (a literal list or dict, or !Var) <br> `as`: (optional, default `item`) The variable name given to the current value <br> `index_as`: (optional) The variable name given to the loop index. If over is a list, this is a numeric index starting from `0`. If over is a dict, this is the dict key. <br> `index_start`: (optional, default `0`) First index, for eg. 1-based indexing. <br> `previous_as`: (optional) The variable name given to the previous value. On the first iteration of the loop, the previous value is `null`. _Added in 0.2.0_ <br> `template`: (required) The template to process for each iteration of the loop. <br> `as_documents`: (optional) Whether to "unfold" the output of this loop into separate YAML documents when writing YAML. Only has an effect at the top level of a template. | See `examples/loop/`. | Loops over a list or dict and renders a template for each iteration. The output is always a list. |
| `!MD5` | Data to hash | `!MD5 'some data to hash'` | Hashes the given data using the MD5 algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!Merge` | A list of dicts | `!Merge [{a: 5}, {b: 6}]` | Merges objects. For overlapping keys the last one takes precedence. |
| `!Not` | a value | `!Not !Var foo` | Logically negates the given value (in Python semantics). |
| `!Op` | `a`, `op`, `b` | See `tests/test_cond.py` | Performs binary operators. Especially useful with `!If` to implement greater-than etc. |
| `!SHA1` | Data to hash | `!SHA1 'some data to hash'` | Hashes the given data using the SHA1 algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!SHA256` | Data to hash | `!SHA256 'some data to hash'` | Hashes the given data using the SHA256 algorithm. If the data is not binary, it is converted to UTF-8 bytes. |
| `!URLEncode` | A string to encode <br> **OR** <br> `url`: The URL to combine query parameters into <br> `query`: An object of query string parameters to add. | `!URLEncode "foo+bar"` <br> `!URLEncode { url: "https://example.com/", query: { foo: bar } }` | Encodes strings for safe inclusion in a URL, or combines query string parameters into a URL. |
| `!Var` | Variable name | `!Var image_name` | Replaced with the value of the variable. |
| `!Void` | Anything or nothing | `foo: !Void` | The dict key, list item or YAML document that resolves to `!Void` is removed from the output. |
| `!With` | `vars`: A dict of variable definitions. <br> `template`: The template to process with the variables defined. | See `examples/with/`. | Binds local variables that are only visible within `template`. Useful for giving a name for common sub-expressions. |
<!-- END SUPPORTED TAGS -->

### Tags in JSON

JSON doesn't have a native tag construct. Instead, use an object with a single key that is the name of the tag (including the bang, eg. `!Var`). For example:

```json
{
    "foo": {
        "!Var": "foo"
    }
}
```

Limitations of the JSON support:

* Object keys starting with `!` are not supported.
* A template rendered as JSON may only contain a single document.
  * JSON templates always have a single document only.
  * YAML templates may only contain a single non-`!Void`, non-`!Defaults` document.
* As `!Defaults` must appear in a document of its own, it's not supported in JSON templates. Use a var file instead.

### Tag composition

Due to YAML, you can't do `!Base64 !Var foo`. We provide a convenient workaround: `!Base64,Var foo`.

## CLI

```
usage: emrichen [-h] [--template-format {yaml,json}] [--var-file VAR_FILE]
                [--define VAR=VALUE] [--output-file OUTPUT_FILE]
                [--output-format {yaml,json}] [--include-env]
                [template_file]

A YAML to YAML preprocessor.

positional arguments:
  template_file         The YAML template to process. If unspecified, the
                        template is read from stdin.

optional arguments:
  -h, --help            show this help message and exit
  --template-format {yaml,json}
                        Template format. If unspecified, attempted to be
                        autodetected from the input filename (but defaults to
                        YAML).
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
  --output-format {yaml,json}
                        Output format. If unspecified, attempted to be
                        autodetected from the output filename (but defaults to
                        YAML).
  --include-env, -e     Expose process environment variables to the template.

Variable precedence: -D > -e > -f > !Defaults
```

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

    Copyright © 2018–2019 Santtu Pajukanta
    Copyright © 2018–2019 Aarni Koskela

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
