from src.parser.graph_parser import Parser
from src.parser.map_data import MapData
from src.types.map_types import PathNode, PoI


class TestParser:
    @classmethod
    def setup_class(cls):
        cls.d = MapData("server/tests/parser/test_map")
        cls.p = Parser('test', cls.d.polygons, cls.d.linestring, cls.d.points)

    def test_nodes(cls):
        expected = [
                    PathNode(
                        id=0, graph='test', level=0.0, lat=53.81904389053648,
                        lon=-1.567831863017121, poly_id=5,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=1, graph='test', level=0.0, lat=53.81903942080672,
                        lon=-1.567809216386322, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=2, graph='test', level=0.0, lat=53.81902630959941,
                        lon=-1.56778001415187, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=3, graph='test', level=0.0, lat=53.819034504103975,
                        lon=-1.567751258890394, poly_id=2,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=4, graph='test', level=0.0, lat=53.819005301869524,
                        lon=-1.56772905923257, poly_id=2,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=5, graph='test', level=0.0, lat=53.8190094736173,
                        lon=-1.567823370530572, poly_id=3,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=6, graph='test', level=0.0, lat=53.81902437271651,
                        lon=-1.567802064818701, poly_id=3,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=7, graph='test', level=0.0, lat=53.81904463549144,
                        lon=-1.567761390277857, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=8, graph='test', level=0.0, lat=53.81906966597811,
                        lon=-1.567729804187531, poly_id=1,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=9, graph='test', level=0.0, lat=53.81908441608633,
                        lon=-1.567839312566726, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=10, graph='test', level=0.0, lat=53.819084565077326,
                        lon=-1.567805044638543, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=11, graph='test', level=0.0, lat=53.819048509257236,
                        lon=-1.567782249016751, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=12, graph='test', level=0.0, lat=53.81900649379746,
                        lon=-1.567786271773538, poly_id=4,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=13, graph='test', level=0.0, lat=53.81899040277031,
                        lon=-1.567781355070798, poly_id=4,
                        tags={'level': 0.0, 'indoor': 'way'}),
                    PathNode(
                        id=14, graph='test', level=0.0, lat=53.81900726834339,
                        lon=-1.567790284318108, poly_id=4,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=15, graph='test', level=0.0, lat=53.81900780619028,
                        lon=-1.567792614987926, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=16, graph='test', level=0.0, lat=53.819023762314416,
                        lon=-1.567797097045268, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=17, graph='test', level=0.0, lat=53.81902214877377,
                        lon=-1.567790642882696, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=18, graph='test', level=0.0, lat=53.81898579969208,
                        lon=-1.567796551109555, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=19, graph='test', level=0.0, lat=53.81899633212348,
                        lon=-1.567854825943833, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=20, graph='test', level=0.0, lat=53.81905918368623,
                        lon=-1.567843631352185, poly_id=5,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=21, graph='test', level=0.0, lat=53.81905316461058,
                        lon=-1.56780695757142, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=22, graph='test', level=0.0, lat=53.81904366264901,
                        lon=-1.567808750394357, poly_id=5,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=23, graph='test', level=0.0, lat=53.81904653116571,
                        lon=-1.567771459677272, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=24, graph='test', level=0.0, lat=53.81904545547195,
                        lon=-1.567765184796993, poly_id=1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=25, graph='test', level=0.0, lat=53.81900583408505,
                        lon=-1.567782216614892, poly_id=4,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=26, graph='test', level=0.0, lat=53.81900117274541,
                        lon=-1.567757117093777, poly_id=2,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=27, graph='test', level=0.0, lat=53.818979479587874,
                        lon=-1.567761419868825, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=28, graph='test', level=0.0, lat=53.81903075432387,
                        lon=-1.567752455754142, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=29, graph='test', level=0.0, lat=53.81910390149969,
                        lon=-1.567761240586532, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=30, graph='test', level=0.0, lat=53.81910364174387,
                        lon=-1.567761286855536, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=31, graph='test', level=0.0, lat=53.81908902106931,
                        lon=-1.567681997812725, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=32, graph='test', level=0.0, lat=53.81903241087262,
                        lon=-1.567692405965479, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=33, graph='test', level=0.0, lat=53.81896908121484,
                        lon=-1.567704049534848, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=34, graph='test', level=0.0, lat=53.81898575446815,
                        lon=-1.567796559198387, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=35, graph='test', level=0.0, lat=53.81904258695525,
                        lon=-1.567750304366617, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=36, graph='test', level=0.0, lat=53.81903218858221,
                        lon=-1.567691141209703, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=37, graph='test', level=0.0, lat=53.819039180591666,
                        lon=-1.567750304366617, poly_id=2,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=38, graph='test', level=0.0, lat=53.8190440212136,
                        lon=-1.567756041400015, poly_id=1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=39, graph='test', level=0.0, lat=53.81905926020856,
                        lon=-1.567844069006212, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=40, graph='test', level=0.0, lat=53.81907987767234,
                        lon=-1.567839945513458, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=41, graph='test', level=0.0, lat=53.819035057098915,
                        lon=-1.567810543217294, poly_id=5,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=42, graph='test', level=0.0, lat=53.819026451548815,
                        lon=-1.567811618911056, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=43, graph='test', level=0.0, lat=53.819033622840564,
                        lon=-1.567847654652086, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=44, graph='test', level=0.0, lat=53.81908830394014,
                        lon=-1.567838511255108, poly_id=0,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=45, graph='test', level=0.0, lat=53.81911698910713,
                        lon=-1.567833670633179, poly_id=-1,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=46, graph='test', level=0.0, lat=53.81904760685947,
                        lon=-1.567777555275257, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=47, graph='test', level=0.0, lat=53.81904904111782,
                        lon=-1.567785622978472, poly_id=6,
                        tags={'level': 0.0, 'indoor': 'wall'}),
                    PathNode(
                        id=48, graph='test', level=0.0, lat=53.81902501729047,
                        lon=-1.567805702595365, poly_id=3,
                        tags={'level': 0.0, 'indoor': 'wall'})]
        assert cls.p.nodes == expected

    def test_edges(cls):
        expected = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (5, 6),
            (6, 2),
            (2, 7),
            (7, 8),
            (9, 10),
            (10, 11),
            (11, 2),
            (2, 12),
            (12, 13),
            (14, 15),
            (16, 17),
            (17, 15),
            (15, 18),
            (18, 19),
            (19, 20),
            (20, 21),
            (21, 22),
            (23, 24),
            (25, 26),
            (26, 27),
            (26, 28),
            (29, 30),
            (30, 31),
            (31, 32),
            (32, 33),
            (33, 18),
            (18, 34),
            (35, 32),
            (32, 36),
            (37, 35),
            (35, 38),
            (39, 20),
            (20, 40),
            (41, 42),
            (42, 43),
            (44, 45),
            (45, 30),
            (30, 23),
            (23, 46),
            (21, 21),
            (21, 47),
            (42, 48)]

        assert cls.p.edges == expected

    def test_pois(cls):
        expected = [PoI(id=0,
                        graph='test',
                        level=0.0,
                        lon=-1.567805044638543,
                        lat=53.819084565077326,
                        nearest_path_node=10,
                        tags={'amenity': 'living room',
                              'level': 0.0}),
                    PoI(id=1,
                        graph='test',
                        level=0.0,
                        lon=-1.567729804187531,
                        lat=53.81906966597811,
                        nearest_path_node=8,
                        tags={'amenity': 'bedroom 1',
                              'level': 0.0}),
                    PoI(id=2,
                        graph='test',
                        level=0.0,
                        lon=-1.56772905923257,
                        lat=53.819005301869524,
                        nearest_path_node=4,
                        tags={'amenity': 'bedroom 2',
                              'level': 0.0}),
                    PoI(id=3,
                        graph='test',
                        level=0.0,
                        lon=-1.567781355070798,
                        lat=53.81899040277031,
                        nearest_path_node=13,
                        tags={'amenity': 'bathroom',
                              'level': 0.0}),
                    PoI(id=4,
                        graph='test',
                        level=0.0,
                        lon=-1.567823370530572,
                        lat=53.8190094736173,
                        nearest_path_node=5,
                        tags={'amenity': 'bedroom 3',
                              'level': 0.0}),
                    PoI(id=5,
                        graph='test',
                        level=0.0,
                        lon=-1.567831863017121,
                        lat=53.81904389053648,
                        nearest_path_node=0,
                        tags={'amenity': 'sauna',
                              'level': 0.0}),
                    PoI(id=6,
                        graph='test',
                        level=0.0,
                        lon=-1.56778001415187,
                        lat=53.81902630959941,
                        nearest_path_node=2,
                        tags={'amenity': 'kitchen',
                              'level': 0.0}),
                    PoI(id=7,
                        graph='test',
                        level=0.0,
                        lon=-1.567839312566726,
                        lat=53.81908441608633,
                        nearest_path_node=9,
                        tags={'amenity': 'front door',
                              'level': 0.0}),
                    PoI(id=8,
                        graph='test',
                        level=0.0,
                        lon=-1.567760088424428,
                        lat=53.81901001236848,
                        nearest_path_node=28,
                        tags={'amenity': 'washing machine',
                              'level': 0.0}),
                    PoI(id=9,
                        graph='test',
                        level=0.0,
                        lon=-1.567792702967536,
                        lat=53.81902463268091,
                        nearest_path_node=16,
                        tags={'amenity': 'themostat',
                              'level': 0.0}),
                    PoI(id=10,
                        graph='test',
                        level=0.0,
                        lon=-1.567773584097438,
                        lat=53.819102007872836,
                        nearest_path_node=30,
                        tags={'amenity': 'TV',
                              'level': 0.0})]
        assert cls.p.pois == expected