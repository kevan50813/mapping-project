"""
    PoI type resolvers
"""
from api.api_database import db
from ariadne import ObjectType

poi = ObjectType("PoI")


@poi.field("nearest_path_node")
async def nearest_path_node(obj, *_):
    """
        Resolve the nearest path node object for the PoI
    """
    return await db.get_node_by_id(obj.graph, obj.nearest_path_node)
