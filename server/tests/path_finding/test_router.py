from src.path_finding.router import Router
from src.types.map_types import PathNode, Polygon


class TestPathfinder:
    def test_basic_path(self):
        """ Can the pathfinder find the most simple route """
        nodes = [{'id': 0,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.56783186301712,
                  'lat': 53.8190438905365,
                  'tags': {'indoor': 'way'},
                  'poly_id': 0},
                 {'id': 1,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.56780921638632,
                  'lat': 53.8190394208067,
                  'tags': {'indoor': 'way'},
                  'poly_id': 0},
                 {'id': 2,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.5677800141519,
                  'lat': 53.8190263095994,
                  'tags': {'indoor': 'way'},
                  'poly_id': 6}]

        node_objects = [PathNode(**node) for node in nodes]

        edges = [(0, 1), (1, 2)]
        r = Router(node_objects, edges, [])
        routed_path = r.find_path(0, 2)
        assert routed_path == [0, 1, 2]

    def test_avoid_room_to_room(self):
        """
            Can the pathfinder account for avoiding
            room to room transitions
        """

        nodes = [
            PathNode(
                graph='test',
                id=0, level=2.0, lat=53.8092346296517, lon=-1.554293436273165,
                poly_id=1, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=1, level=2.0, lat=53.80924001632725, lon=-1.554292508641426,
                poly_id=4, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=2, level=2.0, lat=53.80926644252434, lon=-1.554281852916793,
                poly_id=4, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=3, level=2.0, lat=53.8089523443621, lon=-1.554169168431522,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=4, level=2.0, lat=53.809022377403664, lon=-
                1.554168001214163, poly_id=0,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=5, level=2.0, lat=53.80904922340294, lon=-1.554166833996803,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=6, level=2.0, lat=53.80911575479242, lon=-1.554165083170764,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=7, level=2.0, lat=53.80914059796671, lon=-1.554165272800163,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=8, level=2.0, lat=53.80914059796671, lon=-1.554165083170764,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=9, level=2.0, lat=53.80921613548534, lon=-1.554165083170764,
                poly_id=0, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=10, level=2.0, lat=53.80921817635743, lon=-
                1.554251701087707, poly_id=1,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=11, level=2.0, lat=53.80921817635743, lon=-
                1.554293034973305, poly_id=1,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=12, level=2.0, lat=53.80928616852691, lon=-
                1.554164499562084, poly_id=0,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=13, level=2.0, lat=53.80928325048351, lon=-
                1.554147574910372, poly_id=0,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=14, level=2.0, lat=53.80913952158484, lon=-
                1.554253707587008, poly_id=1,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=15, level=2.0, lat=53.809108621495604, lon=-
                1.554255312786449, poly_id=1,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=16, level=2.0, lat=53.80918687496833, lon=-
                1.554254108886868, poly_id=1,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=17, level=2.0, lat=53.80904742207967, lon=-1.5542878854664,
                poly_id=3, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=18, level=2.0, lat=53.8091051065981, lon=-1.554256523217439,
                poly_id=1, tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=19, level=2.0, lat=53.80895314524712, lon=-
                1.554178813364507, poly_id=2,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=20, level=2.0, lat=53.80895039263887, lon=-
                1.554265864600403, poly_id=2,
                tags={'level': 2.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=21, level=2.0, lat=53.808997875131176, lon=-
                1.55428478878212, poly_id=2,
                tags={'level': 2.0, 'indoor': 'way'})]

        edges = [
            (0, 1),
            (1, 2),
            (3, 4),
            (4, 5),
            (5, 6),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (9, 12),
            (12, 13),
            (6, 8),
            (11, 0),
            (14, 15),
            (10, 16),
            (16, 14),
            (17, 18),
            (18, 15),
            (3, 19),
            (19, 20),
            (20, 21),
            (21, 17)]
        polygons = [
                    Polygon(
                        graph='test',
                        id=0, level=2.0,
                        vertices=[(53.8087195109759, -1.554181865978637),
                                  (53.80887636682891, -1.554179231794218),
                                  (53.808875317568194, -1.554210366374809),
                                  (53.80887450830511, -1.554217538255843),
                                  (53.80889171261514, -1.554216881105572),
                                  (53.808890536748535, -1.554179069991607),
                                  (53.80922497720066, -1.554173756022222),
                                  (53.80929071663308, -1.554173534035772),
                                  (53.809291058664435, -1.554143054728902),
                                  (53.809273685075325, -1.554142342057906),
                                  (53.80927435716087, -1.554153665095874),
                                  (53.80914816605505, -1.554155826530967),
                                  (53.80914690582393, -1.554083111194927),
                                  (53.80915923160203, -1.554082528730552),
                                  (53.809159739958794, -1.554080324287884),
                                  (53.80913180491571, -1.554082045118811),
                                  (53.80913318033365, -1.55415101250413),
                                  (53.80910449304517, -1.554151208992407),
                                  (53.809104100068616, -1.554157103640725),
                                  (53.808964396903484, -1.554157693105557),
                                  (53.80896365773043, -1.554152975600888),
                                  (53.80896199150856, -1.554115589284632),
                                  (53.808961920883284, -1.554089754364339),
                                  (53.808962235532434, -1.55408499244297),
                                  (53.808944153044905, -1.554085175992325),
                                  (53.80894513661704, -1.554110761843014),
                                  (53.80894552673415, -1.554149871082799),
                                  (53.808944993686104, -1.554159854476606),
                                  (53.80871920906016, -1.554161939539588),
                                  (53.808719934959605, -1.554176400956951),
                                  (53.80871986905918, -1.554179293575265),
                                  (53.8087195109759, -1.554181865978637)],
                        NE=(53.809291058664435, -1.554080324287884),
                        SW=(53.80871920906016, -1.554217538255843),
                        tags={'room-no': '2.A25', 'room-name': 'Corridor',
                              'type': 'Access', 'ID': 3, 'indoor': 'corridor',
                              'stairs': None, 'highway': None, 'level': '2'}),
                    Polygon(
                        graph='test',
                        id=1, level=2.0,
                        vertices=[(53.80910509888405, -1.554266003174838),
                                  (53.809207272788115, -1.554263121346774),
                                  (53.809208320725595, -1.554333333157778),
                                  (53.809229803443884, -1.554334643079625),
                                  (53.80922770756893, -1.554304514877142),
                                  (53.80924110935127, -1.554305166014672),
                                  (53.809239658196304, -1.554293920609617),
                                  (53.80923966060577, -1.554286667191975),
                                  (53.80922774031696, -1.554285619254497),
                                  (53.80922497720066, -1.554173756022222),
                                  (53.8092059956143, -1.554173620936571),
                                  (53.80920678156741, -1.554244749692869),
                                  (53.80910509888404, -1.554247795261164),
                                  (53.80910509888405, -1.554266003174838)],
                        NE=(53.80924110935127, -1.554173620936571),
                        SW=(53.80910509888404, -1.554334643079625),
                        tags={'room-no': '2.A26', 'room-name': 'Corridor',
                              'type': 'Access', 'ID': 4, 'indoor': 'corridor',
                              'stairs': None, 'highway': None, 'level': '2'}),
                    Polygon(
                        graph='test',
                        id=2, level=2.0,
                        vertices=[(53.808901396836745, -1.554340008648096),
                                  (53.808998733230055, -1.554338441852983),
                                  (53.808997423308206, -1.554248581214272),
                                  (53.80899597375223, -1.554204723173265),
                                  (53.808996375370725, -1.554178107418898),
                                  (53.808944575500675, -1.554178154080554),
                                  (53.808945756812264, -1.554196214300959),
                                  (53.80894575681227, -1.554209557244505),
                                  (53.808944968033984, -1.554216491500352),
                                  (53.80889930332576, -1.554216753189224),
                                  (53.808901396836745, -1.554340008648096)],
                        NE=(53.808998733230055, -1.554178107418898),
                        SW=(53.80889930332576, -1.554340008648096),
                        tags={'room-no': '2.07',
                              'room-name': 'Flexible Physical Computing',
                              'type': 'Room', 'ID': 20, 'indoor': 'room',
                              'stairs': None, 'highway': None, 'level': '2'}),
                    Polygon(
                        graph='test',
                        id=3, level=2.0,
                        vertices=[(53.808998733230055, -1.554338441852983),
                                  (53.80910562285278, -1.554336476970211),
                                  (53.80910509888405, -1.554266003174838),
                                  (53.80910509888404, -1.554247795261164),
                                  (53.809038554854205, -1.554248581214272),
                                  (53.808997423308206, -1.554248581214272),
                                  (53.808998733230055, -1.554338441852983)],
                        NE=(53.80910562285278, -1.554247795261164),
                        SW=(53.808997423308206, -1.554338441852983),
                        tags={'room-no': '2.15',
                              'room-name': '24Hr Teaching Lab', 'type': 'Room',
                              'ID': 21, 'indoor': 'room', 'stairs': None,
                              'highway': None, 'level': '2'}),
                    Polygon(
                        graph='test',
                        id=4, level=2.0,
                        vertices=[(53.8092403155667, -1.554298325496414),
                                  (53.80928301901891, -1.554297670535491),
                                  (53.809282364057985, -1.554262957606543),
                                  (53.80924503128534, -1.554262826614358),
                                  (53.80924463830879, -1.55428679818416),
                                  (53.80925188307685, -1.554282983851703),
                                  (53.809250925933654, -1.55428679818416),
                                  (53.80923966060577, -1.554286667191975),
                                  (53.8092403155667, -1.554298325496414)],
                        NE=(53.80928301901891, -1.554262826614358),
                        SW=(53.80923966060577, -1.554298325496414),
                        tags={'room-no': '2.19', 'room-name': 'Male Toilets',
                              'type': 'Room', 'ID': 28, 'indoor': 'room',
                              'stairs': None, 'highway': None, 'level': '2'})]

        r = Router(nodes, edges, polygons)
        routed_path = r.find_path(3, 21)
        print(routed_path)
        assert 17 not in routed_path

    def test_returns_nodes(self):
        nodes = [{'id': 0,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.56783186301712,
                  'lat': 53.8190438905365,
                  'poly_id': 5},
                 {'id': 1,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.56780921638632,
                  'lat': 53.8190394208067,
                  'poly_id': 5},
                 {'id': 2,
                  'graph': 'test',
                  'level': 0.0,
                  'lon': -1.5677800141519,
                  'lat': 53.8190263095994,
                  'poly_id': 6}]

        node_objects = [PathNode(**node) for node in nodes]

        edges = [(0, 1), (1, 2)]
        r = Router(node_objects, edges, [])
        assert r.get_path_nodes([0, 1, 2]) == node_objects

    def test_written_instructions(self):
        nodes = [
            PathNode(
                graph='test',
                id=0, level=0.0, lat=53.81904389053648, lon=-1.567831863017121,
                poly_id=5, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=1, level=0.0, lat=53.81903942080672, lon=-1.567809216386322,
                poly_id=6, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=2, level=0.0, lat=53.81902630959941, lon=-1.56778001415187,
                poly_id=6, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=3, level=0.0, lat=53.819034504103975, lon=-
                1.567751258890394, poly_id=2,
                tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=4, level=0.0, lat=53.819005301869524, lon=-1.56772905923257,
                poly_id=2, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=5, level=0.0, lat=53.8190094736173, lon=-1.567823370530572,
                poly_id=3, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=6, level=0.0, lat=53.81902437271651, lon=-1.567802064818701,
                poly_id=3, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=7, level=0.0, lat=53.81904463549144, lon=-1.567761390277857,
                poly_id=6, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=8, level=0.0, lat=53.81906966597811, lon=-1.567729804187531,
                poly_id=1, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=9, level=0.0, lat=53.81908441608633, lon=-1.567839312566726,
                poly_id=0, tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=10, level=0.0, lat=53.819084565077326, lon=-
                1.567805044638543, poly_id=0,
                tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=11, level=0.0, lat=53.819048509257236, lon=-
                1.567782249016751, poly_id=6,
                tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=12, level=0.0, lat=53.81900649379746, lon=-
                1.567786271773538, poly_id=4,
                tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=13, level=0.0, lat=53.81899040277031, lon=-
                1.567781355070798, poly_id=4,
                tags={'level': 0.0, 'indoor': 'way'}),
            PathNode(
                graph='test',
                id=14, level=0.0, lat=53.81900726834339, lon=-
                1.567790284318108, poly_id=4,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=15, level=0.0, lat=53.81900780619028, lon=-
                1.567792614987926, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=16, level=0.0, lat=53.819023762314416, lon=-
                1.567797097045268, poly_id=6,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=17, level=0.0, lat=53.81902214877377, lon=-
                1.567790642882696, poly_id=6,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=18, level=0.0, lat=53.81898579969208, lon=-
                1.567796551109555, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=19, level=0.0, lat=53.81899633212348, lon=-
                1.567854825943833, poly_id=3,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=20, level=0.0, lat=53.81905918368623, lon=-
                1.567843631352185, poly_id=5,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=21, level=0.0, lat=53.81905316461058, lon=-1.56780695757142,
                poly_id=0, tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=22, level=0.0, lat=53.81904366264901, lon=-
                1.567808750394357, poly_id=5,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=23, level=0.0, lat=53.81904653116571, lon=-
                1.567771459677272, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=24, level=0.0, lat=53.81904545547195, lon=-
                1.567765184796993, poly_id=1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=25, level=0.0, lat=53.81900583408505, lon=-
                1.567782216614892, poly_id=4,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=26, level=0.0, lat=53.81900117274541, lon=-
                1.567757117093777, poly_id=2,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=27, level=0.0, lat=53.818979479587874, lon=-
                1.567761419868825, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=28, level=0.0, lat=53.81903075432387, lon=-
                1.567752455754142, poly_id=6,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=29, level=0.0, lat=53.81910390149969, lon=-
                1.567761240586532, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=30, level=0.0, lat=53.81910364174387, lon=-
                1.567761286855536, poly_id=0,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=31, level=0.0, lat=53.81908902106931, lon=-
                1.567681997812725, poly_id=1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=32, level=0.0, lat=53.81903241087262, lon=-
                1.567692405965479, poly_id=2,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=33, level=0.0, lat=53.81896908121484, lon=-
                1.567704049534848, poly_id=2,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=34, level=0.0, lat=53.81898575446815, lon=-
                1.567796559198387, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=35, level=0.0, lat=53.81904258695525, lon=-
                1.567750304366617, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=36, level=0.0, lat=53.81903218858221, lon=-
                1.567691141209703, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=37, level=0.0, lat=53.819039180591666, lon=-
                1.567750304366617, poly_id=2,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=38, level=0.0, lat=53.8190440212136, lon=-1.567756041400015,
                poly_id=1, tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=39, level=0.0, lat=53.81905926020856, lon=-
                1.567844069006212, poly_id=5,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=40, level=0.0, lat=53.81907987767234, lon=-
                1.567839945513458, poly_id=0,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=41, level=0.0, lat=53.819035057098915, lon=-
                1.567810543217294, poly_id=5,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=42, level=0.0, lat=53.819026451548815, lon=-
                1.567811618911056, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=43, level=0.0, lat=53.819033622840564, lon=-
                1.567847654652086, poly_id=-1,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=44, level=0.0, lat=53.81908830394014, lon=-
                1.567838511255108, poly_id=0,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=45, level=0.0, lat=53.81911698910713, lon=-
                1.567833670633179, poly_id=0,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=46, level=0.0, lat=53.81904760685947, lon=-
                1.567777555275257, poly_id=6,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=47, level=0.0, lat=53.81904904111782, lon=-
                1.567785622978472, poly_id=6,
                tags={'level': 0.0, 'indoor': 'wall'}),
            PathNode(
                graph='test',
                id=48, level=0.0, lat=53.81902501729047, lon=-
                1.567805702595365, poly_id=3,
                tags={'level': 0.0, 'indoor': 'wall'})]

        edges = [
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

        r = Router(nodes, edges, [])
        path = r.find_path(12, 0)
        instructions = r.generate_instructions(path)

        assert instructions == ["Forward", "Left"]