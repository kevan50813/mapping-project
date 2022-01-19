"""
    Query type resolvers
    These define how we respond to queries
"""
from ariadne import QueryType
from api.api_database import db
from api.types.path import PathObj
from src.types.map_types import Polygon, PoI

query = QueryType()


@query.field("node")
async def resolve_node(*_, graph, id):
    """
        Resolve a single node by ID
    """
    return await db.get_node_by_id(graph, id)


@query.field("nodes")
async def resolve_nodes(*_, graph):
    """
        Resolver for loading all nodes in graph
    """
    return await db.load_nodes(graph)


@query.field("search_nodes")
async def resolve_search_nodes(*_, graph, search):
    """
        Resolver for searching for nodes within a graph
    """
    return (await db.search_room_nodes(graph, search))[1]


@query.field("search_polygons")
async def resolve_search_polys(*_, graph, search):
    """
        Resolver for searching for polygons within a graph
    """
    return (await db.search_room_nodes(graph, search))[0]


@query.field("edges")
async def resolve_edges(*_, graph):
    """
        Resolver for loading all edges in a graph
    """
    edges = await db.load_edges(graph)
    dictionary = [{'edge': e, 'graph': graph} for e in edges]
    return dictionary


@query.field("poi")
async def resolve_poi(*_, graph, id):
    """
        resolve PoI by ID
    """
    return await db.load_entry_by_id(graph, id, PoI)


@query.field("pois")
async def resolve_pois(*_, graph):
    """
        Resolver for loading all PoIs in a graph
    """
    return await db.load_entries(graph, PoI)


@query.field("search_pois")
async def resolve_search_pois(*_, search):
    """
        Resolver for searching for PoIs (overall, perhaps need one for graph)
    """
    return await db.search_poi_by_name(search)


@query.field("search_pois_in_graph")
async def resolve_search_pois_in_graphy(*_, graph, search):
    """
        Resolver for searching for PoIs in a graph
    """
    return await db.search_poi_by_name_in_graph(graph, search)


@query.field("find_route")
async def resolve_find_route(*_, graph, start_id, end_id):
    """
        Pathfinding resolver
    """
    # NB: this could be done smarter I think, lazy loading
    nodes, edges = await db.load_graph(graph)
    polys = await db.load_entries(graph, Polygon)

    path_obj = PathObj(nodes, edges, polys, start_id, end_id)
    return path_obj


@query.field("polygon")
async def resolve_poly(*_, graph, id):
    """
        resolve Polgon by ID
    """
    return await db.load_entry_by_id(graph, id, Polygon)


@query.field("polygons")
async def resolve_polygons(*_, graph):
    """
        Resolver for all polygons in a graph
    """
    return await db.load_entries(graph, Polygon)
