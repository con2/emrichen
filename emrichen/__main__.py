import os
import sys

from .cli import get_parser
from .context import Context
from .output import RENDERERS
from .template import Template, determine_format


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
