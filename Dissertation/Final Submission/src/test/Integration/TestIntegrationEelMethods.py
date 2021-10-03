import unittest
import sys
import os
sys.path.insert(0, '../../')
import eel_exposed_methods

"""
Class to test interaction between frontend and backend
"""


class TestIntegrationEelMethods(unittest.TestCase):

    def test_network_gen_er(self):
        """
        Test ER generation
        """
        eel_exposed_methods.get_network(1)
        eel_exposed_methods.set_values([1000, 0.01])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        self.assertEqual(eel_exposed_methods.G.number_of_nodes(), 1000)

    def test_network_gen_ws(self):
        """
         Test WS generation
         """
        eel_exposed_methods.get_network(2)
        eel_exposed_methods.set_values([1000, 10, 0.35])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        self.assertEqual(eel_exposed_methods.G.number_of_nodes(), 1000)
        self.assertGreaterEqual(eel_exposed_methods.G.number_of_edges() / 1000 * 2, 10)

    def test_network_gen_BA(self):
        """
        Test BA generation
        """
        eel_exposed_methods.get_network(3)
        eel_exposed_methods.set_values([10, 6, 1000])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        self.assertEqual(eel_exposed_methods.G.number_of_nodes(), 1000)
        self.assertGreaterEqual(eel_exposed_methods.G.number_of_edges() / 1000 * 2, 10)

    def test_network_gen_RPN(self):
        """
        Test RPN generation
        """
        eel_exposed_methods.get_network(4)
        eel_exposed_methods.set_values([1000, 5])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        self.assertEqual(eel_exposed_methods.G.number_of_nodes(), 1000)
        self.assertGreaterEqual(eel_exposed_methods.G.number_of_edges() / 1000 * 2, 10)

    def test_setters(self):
        """
        Test frontend setters work as expected
        """
        eel_exposed_methods.get_network(4)
        eel_exposed_methods.set_values([1000, 5])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        eel_exposed_methods.set_policy(["R"], [0.5], [0.1])
        eel_exposed_methods.set_sim_values(5, 1)
        self.assertEqual(eel_exposed_methods.policy, ["R"])
        self.assertEqual(eel_exposed_methods.values, [0.5])
        self.assertEqual(eel_exposed_methods.increments, [0.1])

    def test_sim(self):
        """
        Test simulation handling works as expected
        """
        eel_exposed_methods.get_network(4)
        eel_exposed_methods.set_values([1000, 5])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        eel_exposed_methods.set_policy(["R"], [0.5], [0.1])
        eel_exposed_methods.set_sim_values(5, 1)
        try:
            eel_exposed_methods.run_sim()
        except AttributeError:
            # do nothing
            print()
        self.assertEqual(eel_exposed_methods.rate[0], [0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertEqual(len(eel_exposed_methods.susceptible), 5)
        self.assertEqual(len(eel_exposed_methods.removed), 5)

    def test_figure(self):
        """
        Test figure can be built from simulation
        """
        eel_exposed_methods.get_network(4)
        eel_exposed_methods.set_values([1000, 5])
        try:
            eel_exposed_methods.make_graph()
        except AttributeError:
            # do nothing
            print()
        eel_exposed_methods.set_policy(["R"], [0.5], [0.1])
        eel_exposed_methods.set_sim_values(5, 1)
        try:
            eel_exposed_methods.run_sim()
        except AttributeError:
            # do nothing
            print()
        if os.path.exists("../../www/img/plot.png"):
            os.remove("../../www/img/plot.png")
        try:
            eel_exposed_methods.path = "../../www/img/plot.png"
            eel_exposed_methods.get_graph()
        except AttributeError:
            # do nothing
            print()
        self.assertTrue(os.path.exists("../../www/img/plot.png"))
