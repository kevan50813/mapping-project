"""
    Tags scalar type, convert dict to JSON
"""
import json
from ariadne import ScalarType

tags_scalar = ScalarType("Tags")


@tags_scalar.serializer
def serialize_tags(value):
    """
    Serialise tags as json string
    """
    return json.dumps(value)
