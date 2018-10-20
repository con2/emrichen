import argparse
import os
import sys

from .context import Context
from .input import PARSERS
from .output import RENDERERS
from .template import Template, determine_format


def get_parser():
    parser = argparse.ArgumentParser(
        description='A YAML to YAML preprocessor.',
        prog='emrichen',
        epilog='Variable precedence: -D > -e > -f > !Defaults',
    )
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


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(args)

    override_variables = dict(item.split('=', 1) for item in args.define)

    variable_sources = list(args.var_files)
    if args.include_env:
        variable_sources.append(os.environ)

    args.output_format = args.output_format or determine_format(
        getattr(args.output_file, 'name', None), RENDERERS, 'yaml'
    )

    context = Context(*variable_sources, **override_variables)
    template = Template.parse(args.template_file, format=args.template_format)
    output = template.render(context, format=args.output_format)

    args.output_file.write(output)


if __name__ == '__main__':
    main()
