"""
Authors: Sandy Johnstone
This script takes input from the user and creates a random network
according to the Erdos-Renyi model.
"""
import networkx as nx
import matplotlib.pyplot as plt
import random as rnd
import math as mt


def get_input():
    # Take N number of nodes from user
    print("Enter number of nodes")
    N = int(input())

    # Take P probability value for edges
    print("Enter value of probability of every edge")
    P = float(input())
    return N, P


def generate():
    """
    DEPRECATED make an ER graph using terminal input
    :return: a networkx graph
    """
    N, P = get_input();
    # Create graph of N nodes
    G = nx.Graph()
    G.add_nodes_from(range(0, N))

    # Add edges to the graph randomly.
    for i in range(G.number_of_nodes()):
        for j in range(i, G.number_of_nodes()):
            # Take random number R.
            R = rnd.random()

            # Use R and P to determine edge
            if (R < P):
                G.add_edge(i, j)
    return G


def generate_web(N, P):
    """
    Create an Erdos-Renyi graph using input parameters
    :param N: number of nodes
    :param P: probability of an edge
    :return: G a networkx graph
    """
    print("Graph Building")
    # Create graph of N nodes
    G = nx.Graph()
    G.add_nodes_from(range(0, N))

    # Add edges to the graph randomly.
    for i in range(G.number_of_nodes()):
        for j in range(i, G.number_of_nodes()):
            # Take random number R.
            R = rnd.random()

            # Use R and P to determine edge
            if (R < P):
                G.add_edge(i, j)
    return G
