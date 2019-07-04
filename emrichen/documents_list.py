class DocumentsList(list):
    pass
    # A marker for the YAML serializer to flatten this list into
    # documents at the top level.


def flatten_documents_lists(input_list):
    output_list = []
    for item in input_list:
        if isinstance(item, DocumentsList):
            output_list.extend(item)
        else:
            output_list.append(item)
    return output_list
