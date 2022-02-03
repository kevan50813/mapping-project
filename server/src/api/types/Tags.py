import json
from ariadne import ScalarType

tags_scalar = ScalarType("Tags")


@tags_scalar.serializer
def serialize_tags(value):
    """
        Serialise tags with JSON
    """
    return json.dumps(value)
