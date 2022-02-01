"""
    Path type resolvers
"""
from src.path_finding.router import Router


class PathObj:
    """Path resolvers"""

    def __init__(self, nodes, edges, polys, start_id, end_id):
        self.router = Router(nodes, edges, polys)
        self.path_ids = self.router.find_path(start_id, end_id)
        self.path_nodes = self.router.get_path_nodes(self.path_ids)

    def ids(self, *_):
        """path ids (list)"""
        return self.path_ids

    def nodes(self, *_):
        """path node objects"""
        return self.path_nodes

    def instructions(self, *_):
        """text instructions for route"""
        return self.router.generate_instructions(self.path_ids)

    def levels(self, *_):
        """list of floors that are spanned by a path"""
        levels = {x.level for x in self.path_nodes}
        return levels
