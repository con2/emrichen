from emrichen import Context, Template


def test_format():
    template = Template.parse(
        '!Format "This tests formatting. {person.name!s} {chance:.0%} == {chance:.5f}"', 'yaml'
    )
    ctx = Context({'person': {'name': 'Pipimi'}, 'chance': .99})
    output = template.enrich(ctx)[0]
    assert output == 'This tests formatting. Pipimi 99% == 0.99000'
