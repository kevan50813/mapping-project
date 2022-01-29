"""
    Node type resolvers
    These define how to resolve fields in the node type
"""
from ariadne import ObjectType
from src.types.map_types import Polygon
from api.api_database import db

node = ObjectType("Node")


@node.field("neighbours")
async def resolve_neighbours(obj, *_):
    """
        Resolve the node neighbours of a given node
    """
    return await db.get_node_neighbours(obj.graph, obj.id)


@node.field("polygon")
async def resolve_polygon(obj, *_):
    """
        Gets polygon nodes is in
    """
    if obj.poly_id == -1:
        # This is just a node that's not in a room
        return None

    return await db.load_entry_by_id(obj.graph, obj.poly_id, Polygon)
