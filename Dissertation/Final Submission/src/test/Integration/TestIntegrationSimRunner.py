import unittest
from networkx import graph
import sys
sys.path.insert(0, '../../')
from sim_runner import Runner
import er_generator

class TestIntegrationSimRunner(unittest.TestCase):
    policy: list
    values: list
    increments: list
    iterations: int
    repetitions: int
    G: graph

    def setUp(self):
        self.policy = []
        self.values = []
        self.increments = []
        self.iterations = 5
        self.repetitions = 1
        self.G = er_generator.generate_web(1000, 0.01)

    def test_sim_increment(self):
        """
        Test to check sim runner does correct number of increments and the correct increments
        """
        self.policy.append('R')
        self.values.append(0.5)
        self.increments.append(0.1)
        simulator = Runner(self.policy, self.values, self.increments, self.iterations, self.G, self.repetitions)
        simulator.run()
        rate, removed, susceptible = simulator.return_results()
        self.assertEqual(rate[0], [0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertEqual(len(removed), 5)
        self.assertEqual(len(susceptible), 5)

    def test_sim_no_increment(self):
        """
        Test to check sim runner does correct number of increments for no increment
        """
        self.policy.append('R')
        self.values.append(0.5)
        self.increments.append(0)
        simulator = Runner(self.policy, self.values, self.increments, self.iterations, self.G, self.repetitions)
        simulator.run()
        rate, removed, susceptible = simulator.return_results()
        self.assertEqual(rate[0], [0.5])
        self.assertEqual(len(removed), 5)
        self.assertEqual(len(susceptible), 5)

    def test_sim_many(self):
        """
        Test to check sim runner performs correctly for large input
        """
        self.policy.append('R')
        self.policy.append("Case")
        self.policy.append("Isolation")
        self.values.append(0.5)
        self.values.append(0.5)
        self.values.append(0.5)
        self.increments.append(0.1)
        self.increments.append(0.1)
        self.increments.append(0.1)
        simulator = Runner(self.policy, self.values, self.increments, self.iterations, self.G, self.repetitions)
        simulator.run()
        rate, removed, susceptible = simulator.return_results()
        self.assertEqual(rate[0], [0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertEqual(rate[1], [0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertEqual(rate[4], [0.5, 0.6, 0.7, 0.8, 0.9])
        self.assertEqual(len(removed), 5)
        self.assertEqual(len(susceptible), 5)
