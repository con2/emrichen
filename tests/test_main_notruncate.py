# https://github.com/con2/emrichen/issues/54

from tempfile import TemporaryDirectory
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


def test_main_notruncate():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        original_path = temp_path / "original.yaml"
        update_path = temp_path / "update.yaml"
        template_path = temp_path / "template.yaml"

        for path, content in [
            (original_path, ORIGINAL_YAML),
            (update_path, UPDATE_YAML),
            (template_path, TEMPLATE_YAML),
        ]:
            with open(path, 'w', encoding="UTF-8") as output_file:
                output_file.write(content)

        main(
            [
                "--output-file",
                str(original_path),
                str(template_path),
            ]
        )

        with open(original_path, "r", encoding="UTF-8") as input_file:
            actual = yaml.safe_load(input_file)

        assert actual == {"a": 1, "b": 3}
