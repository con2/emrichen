from emrichen import Context, Template, emrichen

TEMPLATE = """
---
foo: bar
quux:
  xyzzy: !Var kitten
  klik: !Format "{klak} kluk"
"""

TEMPLATE_JSON = """
{
  "foo": "bar",
  "quux": {
    "xyzzy": {"!Var": "kitten"},
    "klik": {"!Format": "{klak} kluk"}
  }
}"""

VARIABLES = """
kitten: meow
klak: klok
"""

EXPECTED = """foo: bar
quux:
  klik: klok kluk
  xyzzy: meow
"""


def test_emrichen():
    output = emrichen(TEMPLATE, VARIABLES)
    assert output == EXPECTED


def test_emrichen_json():
    c = Context(VARIABLES)
    t = Template.parse(TEMPLATE_JSON, 'json')
    output = t.render(c)
    assert output == EXPECTED
