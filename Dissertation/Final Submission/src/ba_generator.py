"""
Authors: Sandy Johnstone
This script takes input from the user and creates a random network
according to the Barabasi-Albert model.
"""
import networkx as nx
import matplotlib.pyplot as plt
import random as rnd


# function to connect new nodes to the specified number of nodes using preferential attachment
def add_distinct_edges(G, node, m, repeated_nodes):
    connected_nodes = []
    while G.degree(node) < m:
        # Pick a random node uniformly
        random_node = rnd.choice(repeated_nodes)
        while random_node in connected_nodes:
            random_node = rnd.choice(repeated_nodes)
        G.add_edge(node, random_node)
        connected_nodes.append(random_node)
        connected_nodes.append(node)
    repeated_nodes.extend(connected_nodes)
    repeated_nodes = cut_off(G, repeated_nodes, connected_nodes)
    return repeated_nodes


# Retrieve network values from user
def get_input():
    # Take N number of nodes from user
    print("Enter number of initial nodes")
    N = int(input())
    # Take M number of connections
    print("Enter value of initial connections for new nodes")
    M = int(input())
    print("Set limit on network growth")
    lim = int(input())
    return N, M, lim


# Generate graph using BA algorithm
def generate():
    N, M, lim = get_input()

    # Add Initial nodes
    G = nx.Graph()
    G.add_nodes_from(range(0, N))

    # # Create connected graph from original nodes
    z = 0
    while z + 1 <= N:
        G.add_edge(z, z + 1, color='b')
        z = z + 1

    # Add edges to the graph randomly.
    for i in range(G.number_of_nodes(), lim):
        # create distinct connections
        node = G.number_of_nodes()
        G.add_node(node)
        # for each distinct connection
        repeated_nodes = list(G.nodes)
        add_distinct_edges(G, node, M, repeated_nodes)
    return G


def generate_web(N, M, lim):
    """
    Generate a graph according to the BA algorithm using provided parameters
    :param N: Initial nodes
    :param M: Number of edges per node
    :param lim: Limit on growth
    :return:
    """
    # Add Initial nodes
    G = nx.Graph()
    G.add_nodes_from(range(0, N))

    # Create connected graph from original nodes
    z = 0
    while z + 1 <= N:
        G.add_edge(z, z + 1, color='b')
        z = z + 1

    # Add edges to the graph randomly.
    if lim < G.number_of_nodes():
        lim = G.number_of_nodes()

    repeated_nodes = list(G.nodes)
    for i in range(G.number_of_nodes(), lim):
        # create distinct connections
        node = G.number_of_nodes()
        G.add_node(node)
        # for each distinct connection
        repeated_nodes = add_distinct_edges(G, node, M, repeated_nodes)
    return G


def cut_off(G, repeated_nodes: list, updated_nodes):
    """
    Method to check that the updated nodes aren't above cut-off
    :param G: Graph
    :param repeated_nodes: list of nodes based on their prevalence
    :param updated_nodes: list of nodes with new edges
    :return: updated repeated nodes
    """
    for i in updated_nodes:
        if G.degree(i) >= 30:
            repeated_nodes = list(filter(lambda a: a != i, repeated_nodes))
    return repeated_nodes
