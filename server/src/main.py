"""
    main.py file to run the mapping server using uvicorn
"""
import importlib.resources
import uvicorn
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
from src.api.types import query, node, edge, poi, polygon, mutation
from src import api


def app():
    """
    Setup schema and create the graphQL ASGI app
    """
    # create schema
    schema = importlib.resources.read_text(api, "schema.graphql")
    exe_schema = make_executable_schema(
        schema,
        query.query,
        node.node,
        edge.edge,
        polygon.polygon,
        poi.poi,
        mutation.mutation,
    )

    # Create an ASGI app using the schema, running in debug mode
    asgi_app = GraphQL(exe_schema, debug=True)

    return asgi_app


if __name__ == "__main__":
    # Run the app using uvicorn
    uvicorn.run(app(), host="0.0.0.0", port=8888, log_level="debug")
