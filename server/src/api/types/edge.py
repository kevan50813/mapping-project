"""
    Edge type resolvers
"""
from api.api_database import db
from ariadne import ObjectType

edge = ObjectType("Edge")


@edge.field("adjacent_nodes")
async def resolved_adj_nodes(obj, *_):
    """
        Get two adjacent nodes with edge
    """
    nodes = []
    for node_id in obj["edge"]:
        nodes.append(await db.get_node_by_id(obj["graph"], node_id))

    return nodes
