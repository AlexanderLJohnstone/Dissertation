import unittest
import matplotlib as plt
import sys
sys.path.insert(0, '../../')
import figure_builder



class TestUniFigureBuilder(unittest.TestCase):
    rate = [[],[],[],[],[],[]]
    removed = []
    iterations: int
    susceptible = []
    policy = []

    def setUp(self):
        self.rate = [[], [], [], [], [], []]
        self.removed = [1, 2, 3, 4, 5]
        self.susceptible = [5, 4, 3, 2, 1]
        self.iterations = 5
        self.policy = []

    def test_single_iterations(self):
        """
        Test that builder can plot correctly with no axis
        """
        self.policy.append("R")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible, "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes), "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, "
                                        "xlabel='X - Iterations', ylabel='Y - nodes'>]")

    def test_single_r(self):
        """
        Test that builder can plot R rate axis correctly
        """
        self.rate[0] = [1, 2, 3, 4, 5]
        self.policy.append("R")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible, "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes), "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, "
                                        "xlabel='X - R Rate', ylabel='Y - nodes'>]")

    def test_single_case(self):
        """
        Test that builder can plot cases axis correctly
        """
        self.rate[1] = [1, 2, 3, 4, 5]
        self.policy.append("Case")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes),
                         "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, xlabel='X - "
                         "Daily Cases (%)', ylabel='Y - nodes'>]")

    def test_single_var(self):
        """
        Test that builder can plot individual variance axis correctly
        """
        self.rate[2] = [1, 2, 3, 4, 5]
        self.policy.append("Variance")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes),
                         "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, xlabel='X - "
                         "Distribution Mean (Varied Individual Obedience)', ylabel='Y - nodes'>]")

    def test_single_clus(self):
        """
        Test that builder can plot clustered variance axis correctly
        """
        self.rate[3] = [1, 2, 3, 4, 5]
        self.policy.append("Cluster")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes),
                         "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, xlabel='X - "
                         "Distribution Mean (Cluster Obedience)', ylabel='Y - nodes'>]")

    def test_single_iso(self):
        """
        Test that builder can plot isolation axis correctly
        """
        self.rate[4] = [1, 2, 3, 4, 5]
        self.policy.append("Isolation")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes),
                         "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, xlabel='X - "
                         "Percentage of confirmed cases (Isolation)', ylabel='Y - nodes'>]")

    def test_single_tt(self):
        """
        Test that builder can plot track and trace axis correctly
        """
        self.rate[5] = [1, 2, 3, 4, 5]
        self.policy.append("Tracing")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertEqual(str(fig.axes),
                         "[<AxesSubplot:title={'center':'Covid Simulation on Lockdown intervention '}, xlabel='X - "
                         "Percentage of contacts traced from a confirmed case ', ylabel='Y - nodes'>]")


    def test_double_single(self):
        """
        Test that builder can identify when one axis is to small when two are specified
        """
        self.rate[0] = [1, 2, 3, 4, 5]
        self.rate[1] = []
        self.policy.append("R")
        self.policy.append("Case")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertTrue('X - R Rate' in str(fig.axes))
        self.assertTrue('X - Daily Cases (%)' not in str(fig.axes))

    def test_double_r_case(self):
        """
        Test that builder can plot r and case axes together
        """
        self.rate[0] = [1, 2, 3, 4, 5]
        self.rate[1] = [1, 2, 3, 4, 5]
        self.policy.append("R")
        self.policy.append("Case")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertTrue('X - R Rate' in str(fig.axes))
        self.assertTrue('X - Daily Cases (%)' in str(fig.axes))

    def test_double_r_variance(self):
        """
        Test that builder can plot r and variance together
        """
        self.rate[0] = [1, 2, 3, 4, 5]
        self.rate[2] = [1, 2, 3, 4, 5]
        self.policy.append("R")
        self.policy.append("Variance")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertTrue('X - R Rate' in str(fig.axes))
        self.assertTrue('X - Distribution Mean (Varied Individual Obedience)' in str(fig.axes))

    def test_triple(self):
        """
        Test that builder can pick two axis and plot when more than  two policies are specified
        """
        self.rate[0] = [1, 2, 3, 4, 5]
        self.rate[1] = [1, 2, 3, 4, 5]
        self.rate[2] = [1, 2, 3, 4, 5]
        self.policy.append("R")
        self.policy.append("Case")
        self.policy.append("Variance")
        fig = figure_builder.build(self.rate, self.policy, self.iterations, self.removed, self.susceptible,
                                  "../../../FrontEnd/src/www/img/plot.png")
        self.assertTrue('X - R Rate' in str(fig.axes))
        self.assertTrue('X - Daily Cases (%)' in str(fig.axes))
        self.assertFalse('X - Distribution Mean (Varied Individual Obedience)' in str(fig.axes))
