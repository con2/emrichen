# https://github.com/con2/emrichen/issues/54

from pathlib import Path

import yaml

from emrichen.__main__ import main

ORIGINAL_YAML = """
a: 1
b: 2
"""

UPDATE_YAML = """
b: 3
"""

TEMPLATE_YAML = """
!Merge
  - !Include original.yaml
  - !Include update.yaml
"""


def test_main_notruncate(tmp_path: Path):
    original_path = tmp_path / "original.yaml"
    original_path.write_text(ORIGINAL_YAML)

    update_path = tmp_path / "update.yaml"
    update_path.write_text(UPDATE_YAML)

    template_path = tmp_path / "template.yaml"
    template_path.write_text(TEMPLATE_YAML)

    main(
        [
            "--output-file",
            str(original_path),
            str(template_path),
        ]
    )

    with open(original_path, encoding="UTF-8") as input_file:
        actual = yaml.safe_load(input_file)

    assert actual == {"a": 1, "b": 3}
