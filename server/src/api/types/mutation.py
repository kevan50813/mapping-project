"""
Mutation resolvers
"""
import asyncio
import logging
import json
from src.api.api_database import db
from src.parser.graph_parser import Parser
from ariadne import MutationType

mutation = MutationType()
log = logging.getLogger(__name__)


@mutation.field("add_graph")
async def resolve_add_graph(*_, graph, polygons, linestring, points):
    """
    Parses JSON strings and adds a graph to the database
    """
    log.info("Adding graph %s", graph)
    try:
        json_polygons = json.loads(polygons.encode("utf-8").decode("unicode-escape"))
        json_linestring = json.loads(
            linestring.encode("utf-8").decode("unicode-escape")
        )
        json_points = json.loads(points.encode("utf-8").decode("unicode-escape"))
    except json.JSONDecodeError:
        print("JSON FAIL")
        return False

    log.info("JSON loaded for %s", graph)

    try:
        parsed = Parser(graph, json_polygons, json_linestring, json_points)
    except (ValueError, KeyError):
        print("PARSER FAIL")
        return False

    log.info("Graph parsed for %s", graph)

    # probably if it parses fine it'll get saved okay
    tasks = []
    tasks.append(asyncio.create_task(db.save_graph(graph, parsed.nodes, parsed.edges)))
    tasks.append(asyncio.create_task(db.add_entries(graph, parsed.polygons)))
    tasks.append(asyncio.create_task(db.add_entries(graph, parsed.pois)))

    await asyncio.wait(tasks)
    log.info("Graph added for %s", graph)
    return True


@mutation.field("flush_all")
async def resolve_flush_all(*_):
    """
    DEBUG method (deletes everything in DB)
    """
    await db.redis_db.flushall()
    return True
