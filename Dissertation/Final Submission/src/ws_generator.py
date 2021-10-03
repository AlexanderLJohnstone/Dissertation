"""
Authors: Sandy Johnstone
This script takes input from the user and creates a random network
according to the Watts-Strogatz model.
"""
import networkx as nx
import random as rnd
import math as mt


def rewire(G, current_node, random_node):
    """
    A function that adds a new edge to the graph while preventing self loops
    :param G: the graph
    :param current_node: the node to be rewired
    :param random_node: a provisional node to be rewired to
    """
    while random_node == current_node or G.has_edge(current_node, random_node):
        random_node = rnd.randint(0, G.number_of_nodes() - 1)
    G.add_edge(random_node, current_node, color='g')


def get_input():
    # Take N number of nodes from user
    print("Enter number of nodes")
    N = int(input())

    # Take P probability value for edges
    print("Enter the mean degree")
    K = int(input())

    print("Enter special parameter B")
    B = float(input())
    return N, K, B


def generate():
    """
       DEPRECATED generate a graph according to WS algorithm using user input
       :return: a networkx graph
       """
    N, K, B = get_input()

    # Construct Ring
    G = nx.Graph()
    G.add_nodes_from(range(0, N))
    for i in range(0, N):
        for j in range(i, N):
            edge_value = abs(i - j)
            # Control mean degree for odd numbers
            if rnd.random() < 0.5:
                degree_parameter = (K / 2)
            else:
                degree_parameter = mt.ceil(K / 2)
            edge_value = edge_value % ((N - 1) - degree_parameter)
            if 0 < edge_value <= degree_parameter:
                G.add_edge(i, j, color='b')

    # Rewiring
    for i in range(0, N):
        for j in range(i, N):
            random_float = rnd.random()
            if random_float < B:
                edge_value = abs(i - j)
                edge_value = edge_value % ((N - 1) - K / 2)
                if edge_value == mt.floor(K / 2):
                    G.remove_edge(i, j)
                    rewire(G, i, rnd.randint(0, G.number_of_nodes() - 2))

    return G


def generate_web(N, K, B):
    """
    Generate a graph according to the WS algorithm using provided parameters
    :param N: Number of nodes
    :param K: Mean Degree
    :param B: Rewiring percentage
    :return: a networkx graph
    """
    # Construct Ring
    G = nx.Graph()
    G.add_nodes_from(range(0, N))
    for i in range(0, N):
        for j in range(i, N):
            edge_value = abs(i - j)
            # Control mean degree for odd numbers
            if i - j < 0:
                degree_parameter = (K / 2)
            else:
                degree_parameter = mt.ceil(K / 2)
            edge_value = edge_value % ((N - 1) - degree_parameter)
            if 0 < edge_value <= degree_parameter:
                G.add_edge(i, j, color='b')

    # Rewiring
    for i in range(0, N):
        for j in range(i, N):
            random_float = rnd.random()
            if random_float < B and K > 0:
                edge_value = abs(i - j)
                edge_value = edge_value % ((N - 1) - K / 2)
                if edge_value == mt.floor(K / 2):
                    G.remove_edge(i, j)
                    rewire(G, i, rnd.randint(0, G.number_of_nodes() - 2))

    return G
