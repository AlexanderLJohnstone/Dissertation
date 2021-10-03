import unittest
import sys
sys.path.insert(0, '../../')
import ba_generator
import networkx as nx


class TestUnitBA(unittest.TestCase):
    """
    Unit test class for Barabasi-Albert network generator
    """

    def test_no_edges(self):
        """
        Test that when connections is 0 the graph is fully unconnected and empty
        """
        N = 0
        M = 0
        Lim = 0
        G = ba_generator.generate_web(N, M, Lim)
        self.assertEqual(G.number_of_edges(), 0)
        self.assertEqual(G.number_of_nodes(), 0)

    def test_common_edges(self):
        """
        Test that when new input is normal the graph has expected characteristics
        """
        N = 10
        M = 5
        Lim = 100
        G = ba_generator.generate_web(N, M, Lim)
        self.assertLessEqual(G.number_of_edges(), 460)
        self.assertEqual(G.number_of_nodes(), 100)

    def test_negative_edges(self):
        """
        Test that M is negative the algorithm behaves as if M is 0
        """
        N = 10
        M = -5
        Lim = 100
        G = ba_generator.generate_web(N, M, Lim)
        self.assertEqual(G.number_of_edges(), 10)
        self.assertEqual(G.number_of_nodes(), 100)

    def test_preferential_attachment(self):
        """
        Test that the preferential_attachment method picks expected number from a list
        """
        G = nx.Graph()
        G.add_nodes_from(range(0, 5))
        ba_generator.add_distinct_edges(G, 0, 1, [5, 5, 5, 5, 5])
        self.assertEqual(G.number_of_edges(), 1)
        self.assertEqual(G.has_edge(0, 5), True)

    def test_power_law(self):
        """
        Test that in a power law many have few connections and few have many
        """
        N = 10
        M = 5
        Lim = 100
        G = ba_generator.generate_web(N, M, Lim)
        high_degree = 0
        low_degree = 0
        for each in range(0, 100):
            if G.degree(each) > 10:
                high_degree += 1
            else:
                low_degree += 1
        self.assertLessEqual(high_degree, low_degree)


    def test_cut_off(self):
        """
        Test that cut-off works
        """
        N = 10
        M = 5
        Lim = 100
        G = ba_generator.generate_web(N, M, Lim)
        for i in range(0, 100):
            self.assertLessEqual(G.degree(i), 30)
