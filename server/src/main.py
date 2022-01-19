from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from api.types import query, node, edge, poi, polygon

# create schema
schema = load_schema_from_path("api/schema.graphql")
exe_schema = make_executable_schema(
    schema,
    query.query,
    node.node,
    edge.edge,
    polygon.polygon,
    poi.poi)

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(exe_schema, debug=True)
