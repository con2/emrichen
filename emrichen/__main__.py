import argparse
import sys

from . import emrichen


parser = argparse.ArgumentParser(description="A YAML to YAML preprocessor.", prog="emrichen")
parser.add_argument(
    'template_file',
    nargs='?',
    type=argparse.FileType('r'),
    default=sys.stdin,
    help='The YAML template to process. If unspecified, the template is read from stdin.',
)
parser.add_argument(
    '--variables-file', '-f',
    type=argparse.FileType('r'),
    action='append',
    default=[],
    help=(
        'A YAML file containing an object whose top-level keys will be defined as variables. '
        'May be specified multiple times. If the same variable is specified in multiple sources, '
        'the last one takest precedence.'
    )
)
parser.add_argument(
    '--define', '-D',
    metavar='VAR=VALUE',
    action='append',
    default=[],
    help=(
        'Defines a single variable. May be specified multiple times. Variables specified via -D '
        'take precedence over those specified via variable files.'
    ),
)
parser.add_argument(
    '--output-file', '-o',
    type=argparse.FileType('w'),
    default=sys.stdout,
    help='Output file. If unspecified, the template output is written into stdout.',
)


def main():
    args = parser.parse_args()

    override_variables = dict(item.split('=', 1) for item in args.define)
    output = emrichen(args.template_file, *args.variables_file, **override_variables)

    args.output_file.write(output)


if __name__ == "__main__":
    main()
