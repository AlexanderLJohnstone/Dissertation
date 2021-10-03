"""
Authors: Sandy Johnstone
This script takes input from the user and creates a random network
according to the Watts-Strogatz model.
"""
import networkx as nx
import matplotlib.pyplot as plt
import random as rnd
import math as mt


# Get network specification from user
def get_input():
    # Take N number of nodes from user
    print("Enter number of nodes")
    N = int(input())

    # Take M number of edges per new node
    print("Enter number of edges for new nodes")
    M = int(input())
    return N, M


def generate():
    """
    DEPRECATED Create an rpn graph using terminal input
    :return: a networkx graph
    """
    N, M = get_input()
    G = nx.Graph()
    G.add_nodes_from(range(0, 1))
    G.add_edge(0, 1)
    count = 2

    while G.number_of_nodes() != N:
        sample_size = M
        if G.number_of_edges() < M:
            sample_size = G.number_of_edges()
        edge = rnd.sample(list(G.edges()), sample_size)
        G.add_node(count)
        for i in range(0, sample_size):
            G.add_edge(count, edge[i][0])
            G.add_edge(count, edge[i][1])
        count += 1
    return G


def generate_web(N, M):
    """
    Given input parameters create a graph acording to the RPN algorithm
    :param N: number of nodes
    :param M: Number of edges per new node
    :return:
    """
    G = nx.Graph()
    G.add_nodes_from(range(0, 1))
    G.add_edge(0, 1)
    count = 2

    while G.number_of_nodes() != N:
        sample_size = M
        if G.number_of_nodes() < M:
            sample_size = G.number_of_nodes()
        G.add_node(count)
        edge_list = list(G.edges())
        while G.degree(count) < sample_size:
            edge = rnd.choice(edge_list)
            if G.degree(edge[0]) < 30 and G.degree(edge[1]) < 30:
                G.add_edge(count, edge[0])
                G.add_edge(count, edge[1])
                edge_list.append((count, edge[0]))
                edge_list.append((count, edge[0]))
            else:
                edge_list.remove(edge)
        count += 1
    return G


