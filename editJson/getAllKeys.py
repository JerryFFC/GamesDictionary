def get_all_keys(data):
    keys = set()
    if isinstance(data, dict):
        for key, value in data.items():
            keys.add(key)
            keys = keys.union(get_all_keys(value))
    elif isinstance(data, list):
        for item in data:
            keys = keys.union(get_all_keys(item))
    return keys
