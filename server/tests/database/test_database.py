""" Test redis controller """
from database.controller import Controller
import pytest


class TestDatabase:
    @classmethod
    def setup_class(cls):
        cls.controller = Controller(host="redis")

    @classmethod
    def teardown_class(cls):
        cls.controller.redis_db.execute_command("FLUSHALL")

    @pytest.mark.asyncio
    async def test_save_and_load_graph(cls):
        nodes = [{'id': 0,
                  'floor': 0.0,
                  'name': 'sauna',
                  'lon': -1.56783186301712,
                  'lat': 53.8190438905365,
                  'number': '6',
                  'type': 'room'},
                 {'id': 1,
                  'floor': 0.0,
                  'name': 'kitchen',
                  'lon': -1.56780921638632,
                  'lat': 53.8190394208067,
                  'number': '6',
                  'type': 'access'},
                 {'id': 2,
                  'floor': 0.0,
                  'name': 'kitchen',
                  'lon': -1.5677800141519,
                  'lat': 53.8190263095994,
                  'number': '6',
                  'type': 'access'}]

        # NB: this edges list is longer than usual, the DB returns the full
        # set with both returned, but the upper / lower half of the adj matrix
        # can be passed to it with no worry
        edges = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
        await cls.controller.save_graph("test", nodes, edges)

        lnodes, ledges = await cls.controller.load_graph("test")

        assert lnodes == nodes
        assert ledges == edges

    @pytest.mark.asyncio
    async def test_save_and_load_poi(cls):
        pois = [{'id': 0,
                 'name': 'living room',
                 'floor': 0.0,
                 'lon': -1.567805044638543,
                 'lat': 53.819084565077326,
                 'nearest_path_node': 10},
                {'id': 1,
                 'name': 'bedroom 1',
                 'floor': 0.0,
                 'lon': -1.567729804187531,
                 'lat': 53.81906966597811,
                 'nearest_path_node': 8}]

        await cls.controller.add_pois("test", pois)
        lpois = await cls.controller.load_pois("test")

        # sort the dicts so we can compare them
        pois = sorted(pois, key=lambda x: x["id"])
        lpois = sorted(lpois, key=lambda x: x["id"])

        assert lpois == pois

    def test_room_search(cls):
        """Check that it's actually working on redis database."""
        nodes = [{'id': 0,
                  'floor': 0.0,
                  'name': 'sauna',
                  'lon': -1.56783186301712,
                  'lat': 53.8190438905365,
                  'number': '6',
                  'type': 'room'}]

        res = cls.controller.search_room_nodes("test", "sauna")

        assert res == nodes

    def test_poi_search(cls):
        pois = [{'id': 0,
                 'name': 'living room',
                 'floor': 0.0,
                 'lon': -1.567805044638543,
                 'lat': 53.819084565077326,
                 'nearest_path_node': 10}]

        res = cls.controller.search_poi_by_name("living room")

        assert res == pois

    def test_get_neighbours(cls):
        neighbours = [{'id': 1,
                      'floor': 0.0,
                       'name': 'kitchen',
                       'lon': -1.56780921638632,
                       'lat': 53.8190394208067,
                       'number': '6',
                       'type': 'access'},
                      {'id': 2,
                       'floor': 0.0,
                       'name': 'kitchen',
                       'lon': -1.5677800141519,
                       'lat': 53.8190263095994,
                       'number': '6',
                       'type': 'access'}]

        lneighbours = cls.controller.get_node_neighbours("test", 0)

        neighbours = sorted(neighbours, key=lambda x: x["id"])
        lneighbours = sorted(lneighbours, key=lambda x: x["id"])

        assert neighbours == lneighbours
