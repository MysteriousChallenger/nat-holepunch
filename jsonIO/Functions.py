import json

from .Serializable import Serializable


class _JsonIOEncoder(json.JSONEncoder):
    def default(self, _object):
        for _class in Serializable.serializable_classes:
            if type(_object) == _class:
                return {"type": _class.__name__, "json": _object.to_json()}
        return _object


def _deserialize(object: dict):
    if "type" in object:
        for _class in Serializable.serializable_classes:
            if object["type"] == _class.__name__:
                return _class.from_json(object["json"])
    return object


def loads(_string: str):
    return json.loads(_string, strict=False, object_hook=_deserialize)


def dumps(object, indent=2):
    return json.dumps(object, indent=indent, cls=_JsonIOEncoder)
