import unittest
import sys
sys.path.insert(0, '../../')
import er_generator


class TestUnitER(unittest.TestCase):
    """
    Unit test class for Erdos-Renyi network generator
    """
    def test_no_edges(self):
        """
        Test that when probability is 0 the graph is fully unconnected
        """
        N = 100
        P = 0.0
        G = er_generator.generate_web(N, P)
        self.assertEqual(G.number_of_edges(), 0)
        self.assertEqual(G.number_of_nodes(), 100)

    def test_full_edges(self):
        """
        Test that when probability is 1 the graph is fully connected
        """
        N = 100
        P = 1.0
        G = er_generator.generate_web(N, P)
        self.assertEqual(G.number_of_edges(), 5050)
        self.assertEqual(G.number_of_nodes(), 100)

    def test_negative_probability(self):
        """
        Test that when probability is beneath 0 is behaves like it is 0
        """
        N = 100
        P = -1
        G = er_generator.generate_web(N, P)
        self.assertEqual(G.number_of_edges(), 0)

    def test_large_probability(self):
        """
        Test that when probability is over 1 it behaves like it is 1
        """
        N = 100
        P = 10
        G = er_generator.generate_web(N, P)
        self.assertEqual(G.number_of_edges(), 5050)

    def test_common_probability(self):
        """
        Test that when probability is between 1 and 0 the edges percentage is similar to probability
        """
        N = 100
        P = 0.5
        G = er_generator.generate_web(N, P)
        X = round(G.number_of_edges() / 5050, 1)
        self.assertAlmostEqual(X, 0.5)