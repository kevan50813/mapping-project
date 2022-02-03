from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from pydantic import validate_arguments


@validate_arguments(config=dict(arbitrary_types_allowed=True))
@dataclass
class PathNode:
    """
    Path Node

    id: unique ID for node
    level: float representing the floor this node is on
    lat: latitude
    lon: longitude
    poly_id: id of polygon that the path node is in
    tags: dict of anything you'd like
    """

    id: int
    graph: str
    level: float
    lat: float
    lon: float
    poly_id: int
    tags: Optional[dict] = field(default_factory=dict)


@validate_arguments(config=dict(arbitrary_types_allowed=True))
@dataclass
class PoI:
    """
    Point

    id: unique ID for Point object
    level: float representing the floor this node is on
    lat: latitude
    lon: longitude
    nearest_path_node: closest PathNode object ID
    tags: dict of anything you'd like
    """

    id: int
    graph: str
    level: float
    lon: float
    lat: float
    nearest_path_node: Optional[int]  # This can probably go if were generating
    tags: Optional[dict] = field(default_factory=dict)


@validate_arguments(config=dict(arbitrary_types_allowed=True))
@dataclass
class Polygon:
    """
    Polygon

    id: unique ID for Point object
    level: float representing the floor this node is on
    vertices: list of vertices that make up this polygon
    NE: The most northeasterly point
    SW: The most southwesterly point -> together with NE,
                                        make the bounding box
    tags: dict of anything you'd like
    """

    id: int
    graph: str
    level: str
    vertices: List[Tuple[float, float]]
    NE: Tuple[float, float]
    SW: Tuple[float, float]
    tags: Optional[dict] = field(default_factory=dict)
