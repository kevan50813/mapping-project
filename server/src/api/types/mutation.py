"""
Mutation resolvers
"""
import asyncio
import json
from src.api.api_database import db
from src.parser.graph_parser import Parser
from ariadne import MutationType

mutation = MutationType()


@mutation.field("add_graph")
async def resolve_add_graph(_, graph_name, polygons, linestring, points):
    """
    Parses JSON strings and adds a graph to the database
    """
    try:
        json_polygons = json.loads(polygons)
        json_linestring = json.loads(linestring)
        json_points = json.loads(points)
    except json.JSONDecodeError:
        return False

    try:
        parsed = Parser(
            graph_name,
            json_polygons,
            json_linestring,
            json_points)
    except (ValueError, KeyError):
        return False

    # probably if it parses fine it'll get saved okay
    tasks = []
    tasks.append(asyncio.create_task(
        db.save_graph(graph_name, parsed.nodes, parsed.edges)))
    tasks.append(asyncio.create_task(
        db.add_entries(graph_name, parsed.polygons)))
    tasks.append(asyncio.create_task(
        db.add_entries(graph_name, parsed.pois)))

    await asyncio.wait(tasks)
    return True
