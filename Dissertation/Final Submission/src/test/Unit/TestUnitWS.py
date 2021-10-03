import unittest
import networkx as nx
import sys
sys.path.insert(0, '../../')
import ws_generator


class TestUnitWS(unittest.TestCase):
    """
    Unit test class for Watts-Strogatz network generator
    """

    def test_no_edges(self):
        """
        Test that when mean degree is 0 the graph is fully unconnected
        """
        N = 100
        K = 0
        B = 0
        G = ws_generator.generate_web(N, K, B)
        self.assertEqual(G.number_of_edges(), 0)
        self.assertEqual(G.number_of_nodes(), 100)

    def test_all_edges(self):
        """
        Test that when mean degree is highest possible the graph is fully connected
        """
        N = 10
        K = 9
        B = 0
        G = ws_generator.generate_web(N, K, B)
        self.assertEqual(G.number_of_edges(), 44)
        self.assertEqual(G.number_of_nodes(), 10)

    def test_rewire_edges(self):
        """
        Test that when rewiring that the edges change
        """
        N = 100
        K = 5
        B = 0
        G = ws_generator.generate_web(N, K, B)
        B = 0.5
        G2 = ws_generator.generate_web(N, K, B)
        self.assertNotEqual(G.edges(), G2.edges())

    def test_rewire(self):
        """
        Test that checks rewiring works as expected
        """
        G = nx.Graph()
        G.add_nodes_from(range(0, 10))
        G.add_edge(0, 1)
        ws_generator.rewire(G, 0, 3)
        self.assertEqual(G.has_edge(0, 3), True)

    def test_rewire_edge_case(self):
        """
        Test that checks rewiring works as expected when only one possible rewiring is left
        """
        G = nx.Graph()
        G.add_nodes_from(range(0, 3))
        G.add_edge(0, 1)
        ws_generator.rewire(G, 0, 1)
        self.assertEqual(G.has_edge(0, 2), True)

    def test_clustering(self):
        """
        Test that the clustering of the network is high
        """
        N = 100
        K = 15
        B = 0.35
        G = ws_generator.generate_web(N, K, B)
        self.assertGreaterEqual(nx.average_clustering(G), 0.5)

    def test_small_world(self):
        """
        Test that small world properties are produced
        """
        N = 100
        K = 15
        B = 0.35
        G = ws_generator.generate_web(N, K, B)
        self.assertLessEqual(nx.average_shortest_path_length(G), 10)