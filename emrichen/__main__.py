import os
import sys
from importlib import import_module
from typing import List, Optional

from .cli import get_parser
from .context import Context
from .output import RENDERERS
from .template import Template, determine_format


def main(arg_list: Optional[List[str]] = None) -> None:
    if arg_list is None:
        arg_list = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(arg_list)

    for module_path in args.import_module:
        import_module(module_path)

    override_variables = dict(item.split('=', 1) for item in args.define)

    variable_sources = list(args.var_files)
    if args.include_env:
        variable_sources.append(os.environ)

    output_filename = args.output_file
    args.output_format = args.output_format or determine_format(output_filename, RENDERERS, 'yaml')

    context = Context(*variable_sources, **override_variables)
    template = Template.parse(args.template_file, format=args.template_format)
    output = template.render(context, format=args.output_format)
    write_output(output_filename, output)


def write_output(filename: Optional[str], content: str) -> None:
    if filename in (None, "-"):
        fd = sys.stdout
        close_fd = False
    else:
        assert filename
        fd = open(filename, "wt")
        close_fd = True
    try:
        fd.write(content)
    finally:
        if close_fd:
            fd.close()


if __name__ == '__main__':
    main()
