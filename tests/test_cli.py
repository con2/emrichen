import os

import pytest

from emrichen.__main__ import main
from emrichen.input import parse
from emrichen.output import RENDERERS


@pytest.mark.parametrize('output_format', list(RENDERERS))
def test_cli_json_input(examples_dir, output_format, capsys):
    main(
        [
            os.path.join(examples_dir, 'example.json'),
            '-D',
            'kitten=Miuku',
            '-D',
            'sound=pikkuruinen miu',
            '--output-format',
            output_format,
        ]
    )
    out, err = capsys.readouterr()
    parse(out, format=output_format)
    assert 'pikkuruinen miu' in out


def test_cli_kubernetes_example(examples_dir, capsys):
    tag = 'you_are_it'
    main(
        [
            os.path.join(examples_dir, 'kubernetes', 'deployment.in.yml'),
            '-f',
            os.path.join(examples_dir, 'kubernetes', 'vars.yml'),
            '-D',
            f'tag={tag}',
        ]
    )
    out, err = capsys.readouterr()
    assert f'tracon/kompassi:{tag}' in out
