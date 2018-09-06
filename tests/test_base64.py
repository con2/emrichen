from emrichen import Context, Template


def test_base64():
    assert Template.parse('!Base64 foobar').enrich(Context()) == ['Zm9vYmFy']
