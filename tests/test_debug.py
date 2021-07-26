from emrichen import Template


def test_debug(capsys):
    assert (
        Template.parse(
            '''
!Defaults
a: 5
---
b: !Debug,Var a
'''
        ).enrich({})[0]
        == {'b': 5}
    )
    captured = capsys.readouterr()
    assert captured.err == '5\n'
