import argparse
import sys

from .input import PARSERS
from .output import RENDERERS


def get_parser(with_pargs=True):
    """
    Returns the Emrichen command line parser.

    :param with_pargs: If False, the `template_file` positional argument is omitted.
        Useful for extending the CLI.
    """

    parser = argparse.ArgumentParser(
        description='A YAML to YAML preprocessor.',
        prog='emrichen',
        epilog='Variable precedence: -D > -e > -f > !Defaults',
    )

    if with_pargs:
        parser.add_argument(
            'template_file',
            nargs='?',
            type=argparse.FileType('r'),
            default=sys.stdin,
            help='The YAML template to process. If unspecified, the template is read from stdin.',
        )

    parser.add_argument(
        '--template-format',
        choices=PARSERS,
        default=None,
        help=(
            'Template format. If unspecified, attempted to be autodetected from the '
            'input filename (but defaults to YAML).'
        ),
    )
    parser.add_argument(
        '--var-file',
        '-f',
        dest='var_files',
        metavar='VAR_FILE',
        type=argparse.FileType('r'),
        action='append',
        default=[],
        help=(
            'A YAML file containing an object whose top-level keys will be defined as variables. '
            'May be specified multiple times.'
        ),
    )
    parser.add_argument(
        '--define',
        '-D',
        metavar='VAR=VALUE',
        action='append',
        default=[],
        help='Defines a single variable. May be specified multiple times.',
    )
    parser.add_argument(
        '--output-file',
        '-o',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output file. If unspecified, the template output is written into stdout.',
    )
    parser.add_argument(
        '--output-format',
        choices=RENDERERS,
        default=None,
        help=(
            'Output format. If unspecified, attempted to be autodetected from the '
            'output filename (but defaults to YAML).'
        ),
    )
    parser.add_argument(
        '--include-env',
        '-e',
        action='store_true',
        default=False,
        help='Expose process environment variables to the template.',
    )
    return parser
