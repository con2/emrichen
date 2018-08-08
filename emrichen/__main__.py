import argparse
import os
import sys

from . import emrichen


parser = argparse.ArgumentParser(
    description="A YAML to YAML preprocessor.",
    prog="emrichen",
    epilog="Variable precedence: -D > -e > -f",
)
parser.add_argument(
    'template_file',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='The YAML template to process. If unspecified, the template is read from stdin.',
)
parser.add_argument(
    '--var-file', '-f',
    dest='var_files',
    type=argparse.FileType('r'),
    action='append',
    default=[],
    help=(
        'A YAML file containing an object whose top-level keys will be defined as variables. '
        'May be specified multiple times.'
    )
)
parser.add_argument(
    '--define', '-D',
    metavar='VAR=VALUE',
    action='append',
    default=[],
    help=(
        'Defines a single variable. May be specified multiple times.'
    ),
)
parser.add_argument(
    '--output-file', '-o',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. If unspecified, the template output is written into stdout.',
)
parser.add_argument(
    '--include-env', '-e',
    action='store_true',
    default=False,
    help='Expose process environment variables to the template.',
)


def main():
    args = parser.parse_args()

    override_variables = dict(item.split('=', 1) for item in args.define)

    variable_sources = list(args.var_files)
    if args.include_env:
        variable_sources.append(os.environ)

    output = emrichen(args.template_file, *variable_sources, **override_variables)

    args.output_file.write(output)


if __name__ == "__main__":
    main()
