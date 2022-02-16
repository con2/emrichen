import os
import uuid

import pytest
import yaml

from emrichen.__main__ import main
from emrichen.input import parse
from emrichen.output import RENDERERS


@pytest.mark.parametrize('output_format', set(RENDERERS) - {'pprint'})
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
    out, _ = capsys.readouterr()
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
    out, _ = capsys.readouterr()
    assert f'tracon/kompassi:{tag}' in out


def test_custom_tags(examples_dir, capsys):
    main(
        [
            '-m',
            'tests.custom_tags',
            os.path.join(examples_dir, 'custom_tags.yml'),
        ]
    )
    out, _ = capsys.readouterr()
    obj = yaml.safe_load(out)
    assert sorted(obj["spec"]["template"]["spec"]["env"], key=lambda e: e["name"]) == [
        {'name': 'FOO', 'value': 'bar'},
        {'name': 'QUUX', 'value': '1'},
    ]


def test_same_input_output(tmp_path):
    secret = str(uuid.uuid4())
    data_path = (tmp_path / "data.yaml")
    data_path.write_text("""
blep: flerp
blop: !Var FOO
""")
    main(
        [
            "-o", str(data_path),
            "-D", f"FOO={secret}",
            str(data_path),
        ]
    )

    assert yaml.safe_load(data_path.read_text()) == {
        "blep": "flerp",
        "blop": secret,
    }
