# get notes context
def get_note_context(request, page_obj):
    from itertools import zip_longest

    note_rows = list(zip_longest(*[iter(page_obj)] * 3))
    return {
        'note_rows': note_rows,
    }