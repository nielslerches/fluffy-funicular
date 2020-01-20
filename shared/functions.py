from collections import Counter


def get_most_common_properties(objs, maximum: int = 3, ignore: list = None, iteritems=None):
    if not ignore:
        ignore = []

    if not iteritems:
        iteritems = lambda obj: obj.items()

    counter = Counter(
        key
        for obj
        in objs
        for key
        in (
            (key, val)
            for key, value
            in iteritems(obj)
            for val
            in (value if isinstance(value, (tuple, list, set, frozenset)) else (value,))
        )
        if key not in ignore
    )

    return [
        key
        for key, count
        in counter.most_common(maximum)
    ]
