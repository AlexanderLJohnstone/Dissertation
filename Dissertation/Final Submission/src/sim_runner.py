import eel
from epydemic import SIR, StochasticDynamics
from covid_sir_model import SIR_Q
from networkx import graph

"""
A class that handles the running of the simulation
"""


class Runner:
    policy: list
    values: list
    increments: list
    susceptible: list
    removed: list
    rate: list
    iterations: int
    repetitions: int
    G: graph

    param = dict()
    param[SIR.P_INFECT] = 0.0287
    param[SIR.P_REMOVE] = 0.0826
    param[SIR.P_INFECTED] = 0.01

    def __init__(self, policy, values, increments, iterations, G, repetitions):
        self.policy = policy
        self.values = values
        self.increments = increments
        self.iterations = iterations
        self.repetitions = repetitions
        self.G = G
        self.susceptible = []
        self.removed = []
        self.rate = [[], [], [], [], [], []]

    def run(self):
        """
        This method runs the simulations updating each model using specification parameters
        and storing generated data
        """
        for i in range(0, self.iterations):  # Loop over number of iterations
            s = 0
            r = 0
            for k in range(0, self.repetitions):  # Repeat specified number of times
                model = SIR_Q()
                model = self.set_params(model, self.policy, self.values, self.increments, i)  # Set up test
                e = StochasticDynamics(model, self.G)
                e.set(self.param)
                rc = e.run()  # Run test
                s += e.results()['results']['epydemic.SIR.S']
                r += e.results()['results']['epydemic.SIR.R']
            s = s / self.repetitions  # Take averages
            r = r / self.repetitions
            self.susceptible.append(s)
            self.removed.append(r)
            try:
                eel.updateLoad(i + 1, self.iterations)
            except AttributeError:
                print("Can't locate front end")

    def set_params(self, model, pol, vals, inc, j):
        """
         Using input data create  fresh SIR model using parameters
        :param model: The model
        :param pol: set of policies in use
        :param vals: set of starting vlues
        :param inc: set of increments
        :param j: the iteration
        :return: A SIR model
        """
        for i in range(len(pol)):
            if pol[i] == "R":
                init = float(vals[i])
                increment = float(inc[i])
                r = init + j * increment
                model.set_r(r)
                if r not in self.rate[0]:
                    self.rate[0].append(r)
            if pol[i] == "Case":
                init = float(vals[i])
                increment = float(inc[i])
                case = init + j * increment
                model.set_cases(case)
                if case not in self.rate[1]:
                    self.rate[1].append(case)
            if pol[i] == "Variance":
                init = float(vals[i])
                increment = float(inc[i])
                mean = init + j * increment
                model.check_variance(mean)
                if mean not in self.rate[2]:
                    self.rate[2].append(mean)
            if pol[i] == "Cluster":
                init = float(vals[i])
                increment = float(inc[i])
                mean = init + j * increment
                model.check_cluster(mean, self.G)
                if mean not in self.rate[3]:
                    self.rate[3].append(mean)
            if pol[i] == "Isolation":
                init = float(vals[i])
                increment = float(inc[i])
                mean = init + j * increment
                model.set_isolation(mean)
                if mean not in self.rate[4]:
                    self.rate[4].append(mean)
            if pol[i] == "Tracing":
                init = float(vals[i])
                increment = float(inc[i])
                mean = init + j * increment
                model.set_tracing(mean)
                if mean not in self.rate[5]:
                    self.rate[5].append(mean)
        return model

    def return_results(self):
        return self.rate, self.removed, self.susceptible
