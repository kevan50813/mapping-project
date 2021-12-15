from path_finding.graph_parser import Parser


class TestParser:
    @classmethod
    def setup_class(cls):
        cls.p = Parser("tests/test_map")

    def test_nodes(cls):
        expected = [{'id': 0,
                     'floor': 0.0,
                     'name': 'sauna',
                     'lon': -1.567831863017121,
                     'lat': 53.81904389053648,
                     'number': '6',
                     'type': 'room'},
                    {'id': 1,
                     'floor': 0.0,
                     'name': 'kitchen',
                     'lon': -1.567809216386322,
                     'lat': 53.81903942080672,
                     'number': '6',
                     'type': 'access'},
                    {'id': 2,
                     'floor': 0.0,
                     'name': 'kitchen',
                     'lon': -1.56778001415187,
                     'lat': 53.81902630959941,
                     'number': '6',
                     'type': 'access'},
                    {'id': 3,
                     'floor': 0.0,
                     'name': 'bed',
                     'lon': -1.567751258890394,
                     'lat': 53.819034504103975,
                     'number': '3',
                     'type': 'room'},
                    {'id': 4,
                     'floor': 0.0,
                     'name': 'bed',
                     'lon': -1.56772905923257,
                     'lat': 53.819005301869524,
                     'number': '3',
                     'type': 'room'},
                    {'id': 5,
                     'floor': 0.0,
                     'name': 'bed',
                     'lon': -1.567823370530572,
                     'lat': 53.8190094736173,
                     'number': '4',
                     'type': 'room'},
                    {'id': 6,
                     'floor': 0.0,
                     'name': 'bed',
                     'lon': -1.567802064818701,
                     'lat': 53.81902437271651,
                     'number': '4',
                     'type': 'room'},
                    {'id': 7,
                     'floor': 0.0,
                     'name': 'kitchen',
                     'lon': -1.567761390277857,
                     'lat': 53.81904463549144,
                     'number': '6',
                     'type': 'access'},
                    {'id': 8,
                     'floor': 0.0,
                     'name': 'bed',
                     'lon': -1.567729804187531,
                     'lat': 53.81906966597811,
                     'number': '2',
                     'type': 'room'},
                    {'id': 9,
                     'floor': 0.0,
                     'name': 'living',
                     'lon': -1.567839312566726,
                     'lat': 53.81908441608633,
                     'number': '1',
                     'type': 'room'},
                    {'id': 10,
                     'floor': 0.0,
                     'name': 'living',
                     'lon': -1.567805044638543,
                     'lat': 53.819084565077326,
                     'number': '1',
                     'type': 'room'},
                    {'id': 11,
                     'floor': 0.0,
                     'name': 'kitchen',
                     'lon': -1.567782249016751,
                     'lat': 53.819048509257236,
                     'number': '6',
                     'type': 'access'},
                    {'id': 12,
                     'floor': 0.0,
                     'name': 'bath',
                     'lon': -1.567786271773538,
                     'lat': 53.81900649379746,
                     'number': '5',
                     'type': 'room'},
                    {'id': 13,
                     'floor': 0.0,
                     'name': 'bath',
                     'lon': -1.567781355070798,
                     'lat': 53.81899040277031,
                     'number': '5',
                     'type': 'room'}]
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
            (12, 13)]
        assert cls.p.edges == expected

    def test_pois(cls):
        expected = [{'id': 0,
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
                     'nearest_path_node': 8},
                    {'id': 2,
                     'name': 'bedroom 2',
                     'floor': 0.0,
                     'lon': -1.56772905923257,
                     'lat': 53.819005301869524,
                     'nearest_path_node': 4},
                    {'id': 3,
                     'name': 'bathroom',
                     'floor': 0.0,
                     'lon': -1.567781355070798,
                     'lat': 53.81899040277031,
                     'nearest_path_node': 13},
                    {'id': 4,
                     'name': 'bedroom 3',
                     'floor': 0.0,
                     'lon': -1.567823370530572,
                     'lat': 53.8190094736173,
                     'nearest_path_node': 5},
                    {'id': 5,
                     'name': 'sauna',
                     'floor': 0.0,
                     'lon': -1.567831863017121,
                     'lat': 53.81904389053648,
                     'nearest_path_node': 0},
                    {'id': 6,
                     'name': 'kitchen',
                     'floor': 0.0,
                     'lon': -1.56778001415187,
                     'lat': 53.81902630959941,
                     'nearest_path_node': 2},
                    {'id': 7,
                     'name': 'front door',
                     'floor': 0.0,
                     'lon': -1.567839312566726,
                     'lat': 53.81908441608633,
                     'nearest_path_node': 9},
                    {'id': 8,
                     'name': 'washing machine',
                     'floor': 0.0,
                     'lon': -1.567760088424428,
                     'lat': 53.81901001236848,
                     'nearest_path_node': 2},
                    {'id': 9,
                     'name': 'themostat',
                     'floor': 0.0,
                     'lon': -1.567792702967536,
                     'lat': 53.81902463268091,
                     'nearest_path_node': 2},
                    {'id': 10,
                     'name': 'TV',
                     'floor': 0.0,
                     'lon': -1.567773584097438,
                     'lat': 53.819102007872836,
                     'nearest_path_node': 10}]
        assert cls.p.pois == expected


# if __name__ == '__main__':
#     g = Graph()
#     p = Parser("../../json-maps/qgis-bragg")
#     p.print_lists()
#     # start = 0  # testing purpose will change later
#     # end = 3
#     # # the number of vertices is the number of nodes found by the parser
#     # v = len(p.nodes)
#     # # create the edges of the graph based on the adjacency's table and the
#     # # neighboring nodes
#     # adj = [[] for i in range(v)]
#     # # loop though the list of edges and created edges on the graph.
#     # for i in p.edges:
#     #     Graph.add_edge(g, adj, i[0], i[1])
#     #     # print(i)
#     #     # print(i[0])
#     #     # print(i[1])

#     # Graph.print_path(g, adj, start, end, v)
