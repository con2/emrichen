from emrichen import Context, Template


def test_format():
    template = Template.parse(
        '!Format "This tests formatting. {person.name!s} {chance:.0%} == {chance:.5f}"', 'yaml'
    )
    ctx = Context({'person': {'name': 'Pipimi'}, 'chance': 0.99})
    output = template.enrich(ctx)[0]
    assert output == 'This tests formatting. Pipimi 99% == 0.99000'


def test_format_var():
    assert (
        Template.parse(
            '''
!Defaults
a: !Op [2, plus, 3]
---
!Format "five {a}"
    '''
        ).enrich({})
        == ['five 5']
    )
