import math
import unittest
import sys
sys.path.insert(0, '../../')
from covid_sir_model import SIR_Q
from epydemic import SIR, StochasticDynamics, Locus
from networkx import graph
import rpn_generator


class TestIntegrationSIR(unittest.TestCase):
    model: SIR_Q
    G: graph
    param = dict()
    param[SIR.P_INFECT] = 0.0287
    param[SIR.P_REMOVE] = 0.0826
    param[SIR.P_INFECTED] = 0.01

    def setUp(self):
        self.model = SIR_Q()
        self.G = rpn_generator.generate_web(1000, 3)

    def test_check_variance(self):
        """
        Test that setting distributed variance works as expected
        """
        self.model.check_variance(0.5)
        self.assertEqual(self.model.mean, 0.5)
        self.assertEqual(self.model.cluster, False)
        self.assertTrue(len(list(self.model.communities)) == 0)

    def test_check_cluster(self):
        """
        Test that setting clustered variance works creates communities
        """
        self.model.check_cluster(0.5, self.G)
        self.assertEqual(self.model.mean, 0.5)
        self.assertEqual(self.model.variance, False)
        self.assertTrue(len(list(self.model.communities)) > 0)

    def test_behaviour_low_r(self):
        """
        Test that setting very low r leads to lockdown (minimal spread)
        """
        self.model.set_r(0.5)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_high_r(self):
        """
        Test that setting very high r leads to lockdown (widespreads)
        """
        self.model.set_r(1.2)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_low_cases(self):
        """
        Test that setting very low cases leads to lockdown (minimal spread)
        """
        self.model.set_cases(0.001)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_high_cases(self):
        """
        Test that setting very high cases leads to no lockdown (widespreads)
        """
        self.model.set_cases(0.9)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])
        
    def test_behaviour_varied_obedience(self):
        """
        Test that setting very high obedience leads to lockdowns with minimal spread
        """
        self.model.set_r(0.4)
        self.model.check_variance(0.99)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_varied_obedience_low(self):
        """
        Test that setting very low obedience leads to ineffective lockdowns
        """
        self.model.set_r(0.4)
        self.model.check_variance(0.01)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_clustered_obedience(self):
        """
        Test that setting very high obedience leads to lockdowns with minimal spread
        """
        self.model.set_r(0.4)
        self.model.check_cluster(0.99, self.G)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_clustered_obedience_low(self):
        """
        Test that setting very low obedience leads to ineffective lockdowns
        """
        self.model.set_r(0.4)
        self.model.check_cluster(0.01, self.G)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])
        
    def test_behaviour_iso_high(self):
        """
        Test that setting very high case finding leads to isolation with minimal spread
        """
        self.model.set_isolation(1)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_iso_low(self):
        """
        Test that setting very low case finding leads to ineffective isolation
        """
        self.model.set_isolation(0.01)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_tt_high(self):
        """
        Test that setting very high track and trace leads to minimal spread
        """
        self.model.set_isolation(0.7)
        self.model.set_tracing(1)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertGreaterEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])

    def test_behaviour_tt_low(self):
        """
        Test that setting very low track and trace leads to ineffective isolations
        """
        self.model.set_isolation(0.1)
        self.model.set_tracing(0.01)
        e = StochasticDynamics(self.model, self.G)
        e.set(self.param)
        rc = e.run()
        self.assertLessEqual(e.results()['results']['epydemic.SIR.S'],
                                e.results()['results']['epydemic.SIR.R'])




