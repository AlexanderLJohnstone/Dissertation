import math
import unittest
from epydemic import SIR, StochasticDynamics, Locus
from networkx import graph
import sys
sys.path.insert(0, '../../')
from covid_sir_model import SIR_Q
import rpn_generator


class TestUnitSIR(unittest.TestCase):
    model: SIR_Q
    G: graph
    param = dict()
    param[SIR.P_INFECT] = 0.0287
    param[SIR.P_REMOVE] = 0.0826
    param[SIR.P_INFECTED] = 0.01

    def setUp(self):
        '''
        Set up model before each test
        '''
        self.model = SIR_Q()
        self.G = rpn_generator.generate_web(1000, 3)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.time = e.results()['metadata']['epydemic.Dynamics.time']
        # self.model.infect(math.ceil(time), (12, 23))
        self.s = self.model.compartment('epydemic.SIR.S')
        self.i = self.model.compartment('epydemic.SIR.I')
        self.r = self.model.compartment('epydemic.SIR.R')
        self.model.changeCompartment(self.s[0], self.model.INFECTED)
        self.sn = -1
        for each in self.model.network().nodes:
            if len(list(self.model.network().neighbors(each))) > 2:
                self.sn = each
                break

    def test_case_tracker(self, ):
        """
        Test when an infection happens case tracking is updated
        """
        neighbour = list(self.model.network().neighbors(self.sn))
        for each in neighbour:
            if each in self.s:
                self.model.infect(math.ceil(self.time), (each, self.sn))
                self.assertEqual(self.model.cases[int(math.ceil(self.time))], 1)
                break


    def test_r_tracker(self, ):
        """
        Test when an infection happens r tracking is updated
        """
        neighbour = list(self.model.network().neighbors(self.sn))
        self.model.infections[self.sn] = []       # Set up infection state
        for each in neighbour:
            if each in self.s:
                if each != self.sn:
                    self.model.infect(math.ceil(self.time), (each, self.sn))

        self.assertGreaterEqual(len(self.model.infections.keys()), 2)
        self.assertGreaterEqual(len(self.model.infections[self.sn]), 1)

    def test_undo_r(self, ):
        """
        Test when a node is removed r tracking is updated
        """
        neighbour = list(self.model.network().neighbors(self.s[0]))
        count = 0
        for each in neighbour:
            if each in self.s:
                self.model.infect(math.ceil(self.time), (each, self.s[0]))
                self.model.remove(math.ceil(self.time), each)
                break
        self.assertEqual(len(self.model.infections.keys()), 0)

    def test_r_lockdown_true(self):
        '''
        Test asserts when all lockdown criteria are met for rate of reproduction
        then a lockdown is posted
        '''
        self.model.set_r(0.7)
        for each in self.s:
            self.model.changeCompartment(each, self.model.INFECTED)
        for each in self.s:
            self.model.infections[each] = [1, 2, 3, 4]
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) > 0)

    def test_r_lockdown_false(self):
        '''
        Test asserts when rate of reproduction is too  low the lockdown isn't posted
        '''
        self.model.set_r(1.1)
        for each in self.s:
            self.model.changeCompartment(each, self.model.INFECTED)
        for each in self.s:
            self.model.infections[each] = [1]
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_r_lockdown_small_cases(self):
        '''
        Test asserts when there are too few cases R isn't used
        '''
        self.model.set_r(0.7)
        self.model.infections[12] = [1, 2, 3, 4]
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_r_lockdown_removed_edges(self):
        '''
        Test asserts when there are already removed edges ( a lockdown) it isn't posted
        '''
        self.model.set_r(0.7)
        for each in self.s:
            self.model.changeCompartment(each, self.model.INFECTED)
        for each in self.s:
            self.model.infections[each] = [1, 2, 3, 4]
        self.model.removed_edges = [[1,2], [1,2]]
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_r_lockdown_cases_checked(self):
        '''
        Test asserts when there are is a lockdown posted for cases a new one isn't posted
        '''
        self.model.set_r(0.7)
        for each in self.s:
            self.model.changeCompartment(each, self.model.INFECTED)
        for each in self.s:
            self.model.infections[each] = [1, 2, 3, 4]
        self.model.locked_down_c = True
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_r_lockdown_r_checked(self):
        '''
        Test asserts when there are is a lockdown posted for R already a new one isn't posted
        '''
        self.model.set_r(0.7)
        for each in self.s:
            self.model.changeCompartment(each, self.model.INFECTED)
        for each in self.s:
            self.model.infections[each] = [1, 2, 3, 4]
        self.model.locked_down_r = True
        self.model.check_r(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_cases_lockdown_true(self):
        '''
        Test asserts when all lockdown criteria are met for cases
        then a lockdown is posted
        '''
        self.model.set_cases(0.01)
        self.model.cases = list(range(0, int(self.time) + 1))
        self.model.cases[int(self.time) - 1] = 900
        print(self.time)
        self.model.check_cases(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) > 0)

    def test_cases_lockdown_false(self):
        '''
        Test asserts when there are insufficient cases
        then a lockdown isn't posted
        '''
        self.model.set_cases(0.01)
        self.model.cases = list(range(0, int(self.time) + 1))
        self.model.cases[int(self.time) - 1] = 9
        self.model.check_cases(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_cases_lockdown_removed_edges(self):
        '''
        Test asserts when there are sufficient cases but removed edges
        then a lockdown isn't posted
        '''
        self.model.set_cases(0.01)
        self.model.removed_edges = [[1,2]]
        self.model.cases = list(range(0, int(self.time) + 1))
        self.model.cases[int(self.time) - 1] = 900
        self.model.check_cases(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_cases_lockdown_r_checked(self):
        '''
        Test asserts when there are sufficient cases but a lockdown for R
        then a lockdown isn't posted
        '''
        self.model.set_cases(0.01)
        self.model.locked_down_r = True
        self.model.cases = list(range(0, int(self.time) + 1))
        self.model.cases[int(self.time) - 1] = 900
        self.model.check_cases(self.time, 9)
        self.assertTrue(len(self.model._dynamics._postedEvents) == 0)

    def test_normal_lockdown(self):
        '''
        Test when a normal lockdown is posted the expected number of nodes are removed
        '''
        original = self.model.network().number_of_edges()
        self.model.lockdown(self.time, 9)
        self.assertLessEqual(self.model.network().number_of_edges(), original)

    def test_ease_lockdown(self):
        '''
        Test when a normal lockdown is posted then removed that the number of edges is restored
        '''
        original = self.model.network().number_of_edges()
        self.model.lockdown(self.time, 9)
        self.model.ease_lockdown(self.time, 9)
        self.assertEqual(self.model.network().number_of_edges(), original)

    def test_lockdown_variance(self):
        '''
        Test an individually varied lockdown
        '''
        original = self.model.network().number_of_edges()
        self.model.check_variance(0.6)
        self.model.lockdown(self.time, 9)
        self.assertLessEqual(self.model.network().number_of_edges(), original)

    def test_lockdown_cluster(self):
        '''
        Test a clustered varied lockdown
        '''
        original = self.model.network().number_of_edges()
        self.model.check_cluster(0.6, self.G)
        self.model.lockdown(self.time, 9)
        self.assertLessEqual(self.model.network().number_of_edges(), original)

    def test_community_finder(self):
        '''
        Test that the community algorithm creates communities of an expected size
        '''
        self.model.get_communities(self.G)
        self.assertEqual(len(list(self.model.communities)), 20)

    def test_post_isolation(self):
        '''
        Test isolation event is posted
        '''
        self.model.set_isolation(1.0)
        neighbour = list(self.model.network().neighbors(self.sn))
        count = 0
        for each in neighbour:
            self.model.infect(math.ceil(self.time), (each, self.sn))
            break
        self.assertTrue(len(self.model._dynamics._postedEvents) > 0)

    def test_isolation(self):
        '''
        Test isolation event works as expected
        '''
        self.model.set_isolation(1.0)
        self.model.isolate(9, [self.sn, 9])
        self.assertTrue(len(list(self.model.network().neighbors(self.sn))) == 0)

    def test_post_tracing(self):
        '''
        Test tracing event is posted
        '''
        self.model.set_tracing(1.0)
        self.model.set_isolation(1.0)
        neighbour = list(self.model.network().neighbors(self.sn))
        count = 0
        for each in neighbour:
            self.model.isolate(math.ceil(self.time), (each, self.sn))
        self.assertTrue(len(self.model._dynamics._postedEvents) > 0)

    def test_tracing(self):
        '''
        Test tracing event works as expected
        '''
        self.model.set_tracing(1.0)
        original = self.model.network().number_of_edges()
        self.model.trace(9, [self.sn, list(self.model.network().neighbors(self.sn))])
        self.assertLessEqual(self.model.network().number_of_edges(), original)

    def test_post_undo_trace(self):
        '''
        Test that the tracing event posts an undo trace event
        '''
        self.model.set_tracing(1.0)
        self.model.trace(9, [self.sn, list(self.model.network().neighbors(self.sn))])
        self.assertTrue(len(self.model._dynamics._postedEvents) > 0)

    def test_undo_trace(self):
        '''
        Test an undo trace restores network edges
        '''
        self.model.set_tracing(1.0)
        original = self.model.network().number_of_edges()
        neighbours = list(self.model.network().neighbors(self.sn))
        self.model.trace(9, [self.sn, neighbours])
        self.model.undo_trace(9, neighbours)
        self.assertTrue(original == self.model.network().number_of_edges())



