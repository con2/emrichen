import pytest

from emrichen import Template


def test_index():
    assert (
        Template.parse(
            '''
!Index
  over:
    - name: manifold
      score: 7.8
    - name: John
      score: 9.9
    - name: John
      score: 9.8
  as: flavour
  by: !Lookup flavour.name
  duplicates: ignore
  template: !Lookup flavour.score
    '''
        ).enrich({})
        == [{'manifold': 7.8, 'John': 9.8}]
    )


def test_index_without_template():
    assert (
        Template.parse(
            '''
!Index
  over:
    - name: manifold
      score: 7.8
    - name: John
      score: 9.9
    - name: John
      score: 9.8
  as: flavour
  by: !Lookup flavour.name
  duplicates: ignore
    '''
        ).enrich({})
        == [{'manifold': {'name': 'manifold', 'score': 7.8}, 'John': {'name': 'John', 'score': 9.8}}]
    )


def test_index_result_as():
    assert (
        Template.parse(
            '''
!Index
  over:
    - name: manifold
      score: 7.8
    - name: John
      score: 9.9
    - name: John
      score: 9.8
  as: flavour
  template:
    NAME: !Lookup flavour.name
    SCORE: !Lookup flavour.score
  result_as: result
  by: !Lookup result.NAME
  duplicates: ignore
    '''
        ).enrich({})
        == [{'manifold': {'NAME': 'manifold', 'SCORE': 7.8}, 'John': {'NAME': 'John', 'SCORE': 9.8}}]
    )


def test_index_duplicates_error():
    with pytest.raises(ValueError):
        assert Template.parse(
            '''
!Index
  over:
    - name: manifold
      score: 7.8
    - name: John
      score: 9.9
    - name: John
      score: 9.8
  as: flavour
  by: !Lookup flavour.name
  duplicates: error
  template: !Lookup flavour.score
        '''
        ).enrich({})
