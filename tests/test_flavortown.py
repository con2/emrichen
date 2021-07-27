from emrichen import Context, Template

FLAVORTOWN_YAML = """
flavours: !Loop
  as: a
  template: !Merge
    - flavour_name: !Void
      available: true
    - !If
      test: !IsString,Lookup a
      then:
        flavour_name: !Lookup a
      else:
        !Lookup a
  over:
  - peasoup
  - hard liquor
  - flavour_name: manifold
    available: false
  - John
"""

FLAVORTOWN_RESULT = {
    "flavours": [
        {"available": True, "flavour_name": "peasoup"},
        {"available": True, "flavour_name": "hard liquor"},
        {"available": False, "flavour_name": "manifold"},
        {"available": True, "flavour_name": "John"},
    ]
}


def test_flavortown():
    assert Template.parse(FLAVORTOWN_YAML).enrich(Context()) == [FLAVORTOWN_RESULT]
