from types import SimpleNamespace


def dict_to_namespace(obj):
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        return [dict_to_namespace(item) for item in obj]
    else:
        return obj


def namespace_to_dict(obj):
    if isinstance(obj, SimpleNamespace):
        return {k: namespace_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [namespace_to_dict(item) for item in obj]
    else:
        return obj
