import unittest
import networkx as nx
import sys
sys.path.insert(0, '../../')
import rpn_generator

class TestUnitRPN(unittest.TestCase):
    """
    Unit test class for Random-Pseudofractal network generator
    """

    def test_no_edges(self):
        """
        Test that when new connections is 0 the graph is unconnected
        """
        N = 10
        M = 0
        G = rpn_generator.generate_web(N, M)
        self.assertEqual(G.number_of_edges(), 1)
        self.assertEqual(G.number_of_nodes(), 10)


    def test_all_edges(self):
        """
        Test that when new connections is higher than nodes that the graph is fully connected
        """
        N = 10
        M = 100
        G = rpn_generator.generate_web(N, M)
        self.assertGreaterEqual(G.number_of_edges(), 40)
        self.assertEqual(G.number_of_nodes(), 10)

    def test_power_law(self):
        """
        Test that power law effect occurs
        """
        N = 100
        M = 3
        G = rpn_generator.generate_web(N, M)
        high_degree = 0
        low_degree = 0
        for each in range(0, 100):
            if len(list(G.neighbors(each))) > 10:
                high_degree += 1
            else:
                low_degree += 1
        self.assertLessEqual(high_degree, low_degree)

    def test_small_world(self):
        """
        Test that small world properties are produced
        """
        N = 100
        M = 3
        G = rpn_generator.generate_web(N, M)
        self.assertLessEqual(nx.average_shortest_path_length(G), 10)

    def test_cut_off(self):
        """
        Test that cut-off works
        """
        N = 100
        M = 10
        G = rpn_generator.generate_web(N, M)
        for i in range(0, 100):
            self.assertLessEqual(G.degree(i), 30)
