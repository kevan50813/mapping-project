""" Test redis controller """
import pytest
from src.database.controller import Controller
from src.types.map_types import PathNode, PoI, Polygon


class TestDatabase:
    @classmethod
    def setup_class(cls):
        cls.controller = Controller(host="redis")

    @classmethod
    def teardown_class(cls):
        cls.controller.redis_db.execute_command("FLUSHALL")

    @pytest.mark.asyncio
    async def test_save_and_load_graph(cls):
        nodes = [
            {
                "id": 0,
                "level": 0.0,
                "graph": "test",
                "lon": -1.56783186301712,
                "lat": 53.8190438905365,
                "tags": {"indoor": "way"},
                "poly_id": 0,
            },
            {
                "id": 1,
                "level": 0.0,
                "graph": "test",
                "lon": -1.56780921638632,
                "lat": 53.8190394208067,
                "tags": {"indoor": "way"},
                "poly_id": 0,
            },
            {
                "id": 2,
                "level": 0.0,
                "graph": "test",
                "lon": -1.5677800141519,
                "lat": 53.8190263095994,
                "tags": {"indoor": "way"},
                "poly_id": 6,
            },
        ]

        node_objects = [PathNode(**node) for node in nodes]

        # NB: this edges list is longer than usual, the DB returns the full
        # set with both returned, but the upper / lower half of the adj matrix
        # can be passed to it with no worry
        edges = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
        await cls.controller.save_graph("test", node_objects, edges)

        lnodes, ledges = await cls.controller.load_graph("test")

        assert lnodes == node_objects
        assert ledges == edges

    @pytest.mark.asyncio
    async def test_save_and_load_poi(cls):
        pois = [
            {
                "id": 0,
                "graph": "test",
                "level": 0.0,
                "lon": -1.567805044638543,
                "lat": 53.819084565077326,
                "nearest_path_node": 10,
                "tags": {"amenity": "living room"},
            },
            {
                "id": 1,
                "graph": "test",
                "level": 0.0,
                "lon": -1.567729804187531,
                "lat": 53.81906966597811,
                "nearest_path_node": 8,
            },
        ]

        poi_objects = [PoI(**poi) for poi in pois]

        await cls.controller.add_entries("test", poi_objects)
        lpois = await cls.controller.load_entries("test", PoI)

        # sort the dicts so we can compare them
        pois = sorted(poi_objects, key=lambda x: x.id)
        lpois = sorted(lpois, key=lambda x: x.id)

        assert lpois == poi_objects

    @pytest.mark.asyncio
    async def test_room_search(cls):
        """Check that it's actually working on redis database."""
        rooms = [
            Polygon(
                0,
                "test",
                0.0,
                [(0, 0), (0, 1)],
                (0, 0),
                (0, 1),
                {"room-name": "sauna", "room-no": "5"},
            )
        ]

        nodes = [
            {
                "id": 0,
                "level": 0.0,
                "graph": "test",
                "lon": -1.56783186301712,
                "lat": 53.8190438905365,
                "tags": {"indoor": "way"},
                "poly_id": 0,
            },
            {
                "id": 1,
                "level": 0.0,
                "graph": "test",
                "lon": -1.56780921638632,
                "lat": 53.8190394208067,
                "tags": {"indoor": "way"},
                "poly_id": 0,
            },
        ]

        node_objects = [PathNode(**node) for node in nodes]

        await cls.controller.add_entries("test", rooms)
        res = await cls.controller.search_room_nodes("test", "sauna")

        assert res[1] == node_objects

    @pytest.mark.asyncio
    async def test_poi_search(cls):
        pois = [
            PoI(
                0,
                "test",
                0.0,
                -1.567805044638543,
                53.819084565077326,
                10,
                {"amenity": "living room"},
            )
        ]

        await cls.controller.add_entries("test", pois)
        res = await cls.controller.search_poi_by_name("living room")

        assert res == pois

    @pytest.mark.asyncio
    async def test_get_neighbours(cls):
        neighbours = [
            {
                "id": 1,
                "graph": "test",
                "level": 0.0,
                "lon": -1.56780921638632,
                "lat": 53.8190394208067,
                "tags": {"indoor": "way"},
                "poly_id": 0,
            },
            {
                "id": 2,
                "graph": "test",
                "level": 0.0,
                "lon": -1.5677800141519,
                "lat": 53.8190263095994,
                "tags": {"indoor": "way"},
                "poly_id": 6,
            },
        ]

        n_objs = [PathNode(**n) for n in neighbours]

        lneighbours = await cls.controller.get_node_neighbours("test", 0)

        neighbours = sorted(n_objs, key=lambda x: x.id)
        lneighbours = sorted(lneighbours, key=lambda x: x.id)

        assert n_objs == lneighbours
