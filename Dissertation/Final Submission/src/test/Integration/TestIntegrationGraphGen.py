import unittest
import networkx as nx
import sys
sys.path.insert(0, '../../')
from graph_generator import GraphMaker


class TestIntegrationGraphGen(unittest.TestCase):

    def test_er_gen(self):
        """
        Test that generation Erdos-Renyi network using graph generator works
        """
        gm = GraphMaker()
        gm.set_selection(1)
        gm.set_received_values([100, 0.1])
        gm.make_graph()
        G = gm.get_G()
        self.assertEqual(G.number_of_nodes(), 100)
        self.assertLessEqual(G.number_of_edges(), 550)
        self.assertGreaterEqual(G.number_of_edges(), 450)

    def test_ws_gen(self):
        """
        Test that generation Watts-Strogatz network using graph generator works
        """
        gm = GraphMaker()
        gm.set_selection(2)
        gm.set_received_values([100, 10, 0.35])
        gm.make_graph()
        G = gm.get_G()
        self.assertEqual(G.number_of_nodes(), 100)
        self.assertLessEqual(G.number_of_edges(), 550)
        self.assertGreaterEqual(G.number_of_edges(), 450)
        self.assertLessEqual(nx.average_shortest_path_length(G), 6)


    def test_ba_gen(self):
        """
        Test that generation Barabasi-Albert network using graph generator works
        """
        gm = GraphMaker()
        gm.set_selection(3)
        gm.set_received_values([10, 3, 100])
        gm.make_graph()
        G = gm.get_G()
        self.assertEqual(G.number_of_nodes(), 100)
        self.assertLessEqual(G.number_of_edges(), 300)
        self.assertGreaterEqual(G.number_of_edges(), 250)
        high_degree = 0
        low_degree = 0
        for each in range(0, 100):
            if G.degree(each) > 10:
                high_degree += 1
            else:
                low_degree += 1
        self.assertLessEqual(high_degree, low_degree)

    def test_RPN_gen(self):
        """
        Test that generation Random Pseudo-Fractal network using graph generator works
        """
        gm = GraphMaker()
        gm.set_selection(4)
        gm.set_received_values([100, 3])
        gm.make_graph()
        G = gm.get_G()
        self.assertEqual(G.number_of_nodes(), 100)
        self.assertLessEqual(G.number_of_edges(), 400)
        self.assertGreaterEqual(G.number_of_edges(), 350)
        high_degree = 0
        low_degree = 0
        for each in range(0, 100):
            if G.degree(each) > 10:
                high_degree += 1
            else:
                low_degree += 1
        self.assertLessEqual(high_degree, low_degree)