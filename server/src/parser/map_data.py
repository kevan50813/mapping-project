"""
    Class that loads GeoJSON files

    Decouples from parser, means we can async these
"""
import os
import json


class MapData:
    """
        Class that loads GeoJSON map files
    """

    def __init__(self, path, graph_name=None):
        self.path = path
        self.polygons = []
        self.linestring = []
        self.points = []

        if graph_name is not None:
            self.graph_name = graph_name
        else:
            # get graph_name from path
            self.graph_name = os.path.split(path)[-1]

        self.load_polygons()
        self.load_linestring()
        self.load_points()

    def load_polygons(self):
        """
            Loads polygons from GeoJSON file
        """
        with open(self.path + "/Polygons.json", "r", encoding="utf-8") as file:
            self.polygons = json.loads(file.read())

    def load_linestring(self):
        """
            Loads linestrings from GeoJSON file
        """
        with open(self.path + "/LineString.json", "r", encoding="utf-8") as file:
            self.linestring = json.loads(file.read())

    def load_points(self):
        """
            Loads points from GeoJSON file
        """
        with open(self.path + "/Points.json", "r", encoding="utf-8") as file:
            self.points = json.loads(file.read())
