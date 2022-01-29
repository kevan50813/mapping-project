"""
    Node type resolvers
    These define how to resolve fields in the node type
"""
from ariadne import ObjectType

polygon = ObjectType("Polygon")


@polygon.field("ne")
async def resolve_ne(obj, *_):
    """
        returns NE field
    """
    return obj.NE


@polygon.field("sw")
async def resolve_sw(obj, *_):
    """
        returns SW field
    """
    return obj.SW
