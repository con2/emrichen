from typing import Any, List


class DocumentsList(list):
    pass
    # A marker for the YAML serializer to flatten this list into
    # documents at the top level.


def flatten_documents_lists(input_list: List[Any]) -> List[Any]:
    output_list: List[Any] = []
    for item in input_list:
        if isinstance(item, DocumentsList):
            output_list.extend(item)
        else:
            output_list.append(item)
    return output_list
