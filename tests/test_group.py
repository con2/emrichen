from emrichen import Template


def test_group():
    assert (
        Template.parse(
            '''
!Group
  over:
    - name: manifold
      score: 7.8
    - name: John
      score: 9.9
    - name: John
      score: 9.8
  as: flavour
  by: !Lookup flavour.name
  template: !Lookup flavour.score
    '''
        ).enrich({})
        == [{'manifold': [7.8], 'John': [9.9, 9.8]}]
    )
