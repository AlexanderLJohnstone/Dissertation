import eel
from networkx import graph
import networkx as nx
from graph_generator import GraphMaker
import figure_builder as FB
from sim_runner import Runner

G: graph
gm = GraphMaker()

policy = []
values = []
increments = []
path = 'www/img/plot.png'

susceptible = []
removed = []
rate = [[], [], [], []]

iterations = 1
repetitions = 1


@eel.expose
def get_network(choice):
    """
    This exposed method can be called by frontend to send a choice selected by the user
    :param choice: An integer representing a network choice
    """
    global gm
    gm.set_selection(choice)


@eel.expose
def get_parameters():
    """
    This exposed method can be used by the front end to request the parameters required for the graph.
    The function will build a set of parameters and expected values so the front end can create input
    fields.
    :return: none
    """
    global gm
    selection = gm.selection
    parameters = []
    types = []
    if selection == 1:
        parameters.append("Number of Nodes")
        parameters.append("Probability of Each Edge")
        types.append("int")
        types.append("float")
    if selection == 2:
        parameters.append("Number of Nodes")
        parameters.append("Mean Degree")
        parameters.append("Rewiring Parameter (beta)")
        types.append("int")
        types.append("int")
        types.append("float")
    if selection == 3:
        parameters.append("Initial Nodes")
        parameters.append("Number of Edges for New Nodes")
        parameters.append("Limit on Growth (Final Number of Nodes)")
        types.append("int")
        types.append("int")
        types.append("int")
    if selection == 4:
        parameters.append("Number of Nodes")
        parameters.append("Number of Edges for New Nodes")
        types.append("int")
        types.append("int")
    eel.parameterAdder(parameters, types)


@eel.expose
def make_graph():
    """
    This method can be called by front end to generate graphs using already set parameters
    :return: ...
    """
    global gm
    global G
    gm.make_graph()
    G = gm.get_G()
    print(nx.info(G))

    eel.finished_loading()


@eel.expose
def set_values(values):
    """
    This exposed method allows frontend to send parameters that have been entered
    :param values: An array of sanitised parameters entered by the user
    """
    global gm
    gm.set_received_values(values)


@eel.expose
def set_policy(pol, value, incs):
    """
    Exposed method for frontend to pass back policy parameters
    :param pol: list of policies
    :param value: list of starting values
    :param incs: list of increments
    :return:
    """
    global policy
    global values
    global increments
    policy = pol
    values = value
    increments = incs

@eel.expose
def set_sim_values(itr, rep):
    """
    Exposed method for frontend to pass back iteration values
    :param itr: list of number of increments/iterations
    :param rep: list of number of repetitions per increment
    :return:
    """
    global iterations
    global repetitions
    iterations = int(itr)
    repetitions = int(rep)


@eel.expose
def run_sim():
    """
    Exposed method that allows frontend to initiate simulation.
    Once completed the method sends a command to the frontend to
    move onto results.
    :return:
    """
    global policy
    global values
    global increments
    global susceptible
    global removed
    global rate
    simulator = Runner(policy, values, increments, iterations, G, repetitions)
    simulator.run()
    rate, removed, susceptible = simulator.return_results()
    eel.final_page()


@eel.expose
def get_graph():
    """
    Exposed method to build graph and save it so frontend can access it
    :return:
    """
    FB.build(rate, policy, iterations, removed, susceptible, path)
    eel.display()



