"""
    Methods for automatically generating ways

    Straight Skeleton: used for corridor centerlines
    Visibility: used for room & area
"""
from typing import List
from src.types.map_types import PathNode, PoI, Polygon


def straight_skeleton(polygon: Polygon,
                      points: List[PoI]) -> (List[PathNode], tuple):
    """
        Returns the straight skeleton of a polygon,
        with paths to the points too
    """
    print(polygon.vertices, points)


def visibility(polygon: Polygon,
               points: List[PoI]) -> (List[PathNode], tuple):
    """
        Returns the visibility matrix of a polygon,
        with paths to the points too
    """
    print(polygon, points)
