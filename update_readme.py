import argparse
import io
import sys
import textwrap
import re

import yaml

from emrichen.tags.base import tag_registry

placeholder_re = re.compile(r'{(.+?)}')


def format_placeholders(val, fmt_env):
    return placeholder_re.sub(
        lambda m: fmt_env.get(m.group(1), m.group(0)),
        str(val or ''),
    )


def format_for_table(val, fmt_env):
    return (
        textwrap.dedent(format_placeholders(str(val or ''), fmt_env))
            .strip()
            .replace('\r\n', '\n')
            .replace('\n', ' <br> ')  # Spaces around the br make the raw text easier to read and diff.
            .replace(r'\ <br>', ' ')  # Allow "escaping" newlines
    )


def generate_markdown_table():
    out_sio = io.StringIO()
    out_sio.write('''
| Tag | Arguments | Example | Description |
|-----|-----------|---------|-------------|
''')
    for name, tag in sorted(tag_registry.items()):
        try:
            doc = textwrap.dedent(getattr(tag, '__doc__', None) or '')
            doc = next(yaml.safe_load_all(doc))
        except StopIteration:  # Probably means there's no documentation at all
            print(f'!{name}: no documentation', file=sys.stderr)
            doc = {}

        fmt_env = {
            'name': name,
        }

        out_sio.write(' | '.join([
            '',  # row start marker
            format_placeholders('`!{name}`', fmt_env),
            format_for_table(doc.get('arguments'), fmt_env),
            format_for_table(doc.get('example'), fmt_env),
            format_for_table(doc.get('description'), fmt_env),
            '',  # row end marker
        ]).strip() + '\n')
    return out_sio.getvalue()


def replace_marker_segment(input, replacement, start, end):
    marker_re = re.compile(f'({re.escape(start)})(.*)({re.escape(end)})', re.DOTALL)

    def replacer(match):
        return match.group(1) + replacement + match.group(3)

    return marker_re.sub(replacer, input)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', '-n', action='store_true', help='do not update README, just print the new one')
    args = ap.parse_args()

    table = generate_markdown_table()

    with open('README.md') as infp:
        input_readme = infp.read()

    output_readme = replace_marker_segment(
        input=input_readme,
        replacement=table,
        start='<!-- START SUPPORTED TAGS -->',
        end='<!-- END SUPPORTED TAGS -->',
    )

    if not args.dry_run:
        with open('README.md', 'w') as outfp:
            outfp.write(output_readme)
    else:
        print(output_readme)


if __name__ == '__main__':
    main()
