# SIR as a compartmented model
#
# Copyright (C) 2017--2020 Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import CompartmentedModel
import sys
import random as rnd
import numpy as np
from networkx import community

if sys.version_info >= (3, 8):
    from typing import Final, Dict, Any
else:
    # backport compatibility with older typing
    from typing import Dict, Any
    from typing_extensions import Final


class SIR_Q(CompartmentedModel):
    '''The Susceptible-Infected-Removed :term:`compartmented model of disease`.
    Susceptible nodes are infected by infected neighbours, and recover to
    removed.'''

    # Model parameters
    P_INFECTED: Final[str] = 'epydemic.SIR.pInfected'  #: Parameter for probability of initially being infected.
    P_INFECT: Final[str] = 'epydemic.SIR.pInfect'  #: Parameter for probability of infection on contact.
    P_REMOVE: Final[str] = 'epydemic.SIR.pRemove'  #: Parameter for probability of removal (recovery).

    # Possible dynamics states of a node for SIR dynamics
    SUSCEPTIBLE: Final[str] = 'epydemic.SIR.S'  #: Compartment for nodes susceptible to infection.
    INFECTED: Final[str] = 'epydemic.SIR.I'  #: Compartment for nodes infected.
    REMOVED: Final[str] = 'epydemic.SIR.R'  #: Compartment for nodes recovered/removed.

    # Locus containing the edges at which dynamics can occur
    SI: Final[str] = 'epydemic.SIR.SI'  #: Edge able to transmit infection.

    # Dict of infected individuals
    infections = dict()
    # Dict of new cases by day
    cases = dict()
    # Lockdown thresholds
    thresh_r: int
    thresh_c: int
    # List of removed edges by a lockdown
    removed_edges = []
    # Lockdown Obedience Parameters
    variance: bool
    mean: float
    deviation = 0.1
    cluster: bool

    # State tracking variables
    locked_down_c: bool
    locked_down_r: bool
    isolation: float
    tracing: float

    trace_dict = dict()

    communities: list

    def __init__(self):
        super(SIR_Q, self).__init__()
        self.locked_down_c = False
        self.locked_down_r = False
        self.thresh_r = -1
        self.thresh_c = -1
        self.removed_edges = []
        self.cases = dict()
        self.infections = dict()
        self.trace_dict = dict()
        self.variance = False
        self.cluster = False
        self.deviation = 0.1
        self.communities = []
        self.isolation = -1
        self.tracing = -1

    def set_r(self, thresh_r):
        self.thresh_r = float(thresh_r)

    def set_cases(self, thresh_c):
        self.thresh_c = float(thresh_c)

    def set_isolation(self, iso):
        self.isolation = iso

    def set_tracing(self, tracing):
        self.tracing = tracing

    def check_variance(self, mean):
        self.variance = True
        self.cluster = False
        self.mean = mean

    def check_cluster(self, mean, G):
        self.cluster = True
        self.variance = False
        self.get_communities(G)
        self.mean = mean

    def build(self, params: Dict[str, Any]):
        '''Build the SIR model.

        :param params: the model parameters'''
        super(SIR_Q, self).build(params)

        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        pRemove = params[self.P_REMOVE]

        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)
        self.addCompartment(self.REMOVED, 0.0)

        self.trackEdgesBetweenCompartments(self.SUSCEPTIBLE, self.INFECTED, name=self.SI)
        self.trackNodesInCompartment(self.INFECTED)

        self.addEventPerElement(self.SI, pInfect, self.infect)
        self.addEventPerElement(self.INFECTED, pRemove, self.remove)

        if self.thresh_c >= 0:
            self.postRepeatingEvent(1, 1, self.SI, self.check_cases)
        if self.thresh_r >= 0:
            self.postRepeatingEvent(1, 1, self.SI, self.check_r)

    def infect(self, t: float, e: Any):
        '''Perform an infection event. This changes the compartment of
        the susceptible-end node to :attr:`INFECTED`. It also marks the edge
        traversed as occupied.

        :param t: the simulation time
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, _) = e
        self.changeCompartment(n, self.INFECTED)
        self.markOccupied(e, t)
        self.update_tracking(t, e)
        if self.isolation > 0:
            self.postEvent(t + 5, e, self.isolate)

    def remove(self, t: float, n: Any):
        '''Perform a removal event. This changes the compartment of
        the node to :attr:`REMOVED`.

        :param t: the simulation time (unused)
        :param n: the node'''
        self.changeCompartment(n, self.REMOVED)
        self.remove_tracking(t, n)

    def isolate(self, t: float, e: any):
        '''Perform an isolation event. This removes all contacts
        from the node and posts a tracing event if appropriate.

        :param t: the simulation time (unused)
        :param e: the edge'''
        (n, _) = e
        r = rnd.random()
        if r < self.isolation:
            neighbors = list(self.network().neighbors(n))
            for each in neighbors:
                self.removeEdge(n, each)
            if self.tracing > 0:
                pass_param = [n, neighbors]
                self.postEvent(t + 1, pass_param, self.trace)

    def trace(self, t: float, e: any):
        '''Perform a Trace event. This traces the percentage
        of contacts input by the user. Traced contacts lose
        all contacts.

        :param t: the simulation time (unused)
        :param e: an object containing the node and its neighbours'''
        n = e[0]
        neighbours = e[1]
        edges = self.network()
        remove_int = round(len(neighbours) * self.tracing)
        to_remove = rnd.sample(neighbours, remove_int)
        for each in to_remove:
            self.quarantine(t, each)
        self.postEvent(t + 14, to_remove, self.undo_trace)

    def quarantine(self, t: float, n: any):
        '''Perform a quarantine. This function removes all the
        neighbours of a single node.

        :param t: the simulation time (unused)
        :param n: the node'''
        neighbors = list(self.network().neighbors(n))
        for each in neighbors:
            self.removeEdge(n, each)
        self.trace_dict[n] = neighbors

    def undo_trace(self, t: float, neighbours: any):
        '''Perform an trace reversal. This mimics the end of a quarantine
        for a node. Add back edges using trace dictionary.

        :param t: the simulation time (unused)
        :param n: the node'''
        for each in neighbours:
            if each in self.trace_dict:
                child_neighbours = self.trace_dict.pop(each)
                for i in child_neighbours:
                    self.addEdge(each, i)

    def update_tracking(self, t: float, e: Any):
        '''Update the tracking of infections

        :param t: the simulation time
        :param e: the edge between infected nodes'''
        (n, x) = e
        self.infections[n] = []
        # Update tracking of a single infection for R
        if x in self.infections:
            val = self.infections[x]
            val.append(n)
            self.infections[x] = val
        time = int(t)
        # Update daily number of infections
        if time in self.cases:
            self.cases[time] += 1
        else:
            self.cases[time] = 1

    def remove_tracking(self, t: float, n: Any):
        '''Perform a removal from tracking. Don't track
            removed nodes for R
        :param t: the simulation time (unused)
        :param n: the node to remove from tracking'''
        if n in self.infections:
            self.infections.pop(n)

    def check_r(self, t: float, n: Any):
        '''Perform an R check. Use r information calculated from tracking to dictate
                lockdowns.

        :param t: the simulation time
        :param n: the node (unused)'''
        # Calculate total infections per infected node
        total = 0
        r = 0
        if len(self.infections) > 0:
            for key, value in self.infections.items():
                total += len(self.infections[key])
            r = total / len(self.infections)
        if len(self.infections) > self.network().number_of_nodes() * 0.01:
            if r > self.thresh_r and not self.locked_down_r and not self.locked_down_c and len(
                    self.removed_edges) == 0:  # Instigate a lockdown
                self.postEvent(t + 7, self.SI, self.lockdown)
                self.locked_down_r = True
            if r < self.thresh_r and self.locked_down_r and 0 < len(self.removed_edges):  # Remove a lockdown
                self.postEvent(t + 7, self.SI, self.ease_lockdown)
                self.locked_down_r = False

    def check_cases(self, t: float, n: Any):
        '''Perform a cases check. Use new case information calculated from tracking to dictate
                lockdowns.

        :param t: the simulation time
        :param n: the node (unused)'''
        if 1 <= len(self.cases):
            if len(self.cases) < t:
                self.fix_cases(t)
            cases = self.cases[int(t) - 1]
            size = self.network().number_of_nodes()
            if (cases / size) > self.thresh_c and not self.locked_down_c and not self.locked_down_r and \
                    len(self.removed_edges) == 0:  # Instigate a lockdown
                self.postEvent(t + 7, self.SI, self.lockdown)
                self.locked_down_c = True
            if (cases / size) < self.thresh_c and self.locked_down_c and 0 < len(self.removed_edges):  # Remove a lockdown
                flag = True
                for each in range(2, 14):  # Check several days as this is a volatile metric
                    if int(t) - each >= 0:
                        if self.cases[int(t) - each] / size > self.thresh_c:
                            flag = False
                if flag:
                    self.postEvent(t + 7, self.SI, self.ease_lockdown)
                    self.locked_down_c = False

    def lockdown(self, t: float, n: Any):
        '''Perform a lockdown. Remove and record edge removals

        :param t: the simulation time (unused)
        :param n: the node (unused)'''
        if self.variance:
            self.lockdown_obedience_variance()
        elif self.cluster:
            self.lockdown_obedience_cluster()
        else:
            edges = self.network().edges
            remove_number = round(len(edges) * 0.9)
            to_remove = rnd.sample(edges, remove_number)
            for edge in to_remove:
                x = edge[0]
                y = edge[1]
                self.removeEdge(x, y)
                self.removed_edges.append(edge)

    def ease_lockdown(self, t: float, n: Any):
        '''Perform a lockdown removal. Add back any removed edges

        :param t: the simulation time (unused)
        :param n: the node (unused)'''
        for edge in self.removed_edges:
            self.network().add_edge(edge[0], edge[1])
        self.removed_edges = []

    def lockdown_obedience_variance(self):
        '''
        This event begins a lockdown. This lockdown is dictated by the individual nodes
        and the variance selected.
        '''
        nodes = self.network().number_of_nodes()
        remove_list = []
        for i in range(0, nodes):
            remove_percentage = np.random.normal(self.mean, self.deviation)
            if remove_percentage > 1:
                remove_percentage = 1
            if remove_percentage < 0:
                remove_percentage = 0
            self.remove_set(i, remove_percentage, remove_list)
        self.remove_edges(remove_list)

    def lockdown_obedience_cluster(self):
        '''
        This event begins a lockdown. This lockdown is dictated by the communities
        and the variance selected.
        '''
        remove_list = []
        for i in self.communities:
            remove_percentage = np.random.normal(self.mean, self.deviation)
            if remove_percentage > 1:
                remove_percentage = 1
            if remove_percentage < 0:
                remove_percentage = 0
            remove_list.extend(self.community_removal(list(i), remove_percentage))
        self.remove_edges(remove_list)

    def community_removal(self, com: list, percentage: float):
        '''
        This function creates a list of edges in a community and then takes a random sample
        that are to later be removed

        :param com: list of nodes in the communites
        :param percentage: percentage of edges to remove
        :return: list of edges to be removed
        '''
        edges = []
        for i in com:
            neighbours = self.network().neighbors(i)
            for j in neighbours:
                if j <= i:
                    if [j, i] not in edges:
                        edges.append([j, i])
                else:
                    if [i, j] not in edges:
                        edges.append([i, j])
        edges = rnd.sample(edges, int(percentage * len(edges)))
        return edges

    def remove_set(self, node: int, to_remove: int, remove_set: list):
        '''
        This method take a number and node and creates a list of edges
        to be removed of size 'to_remove'.

        :param node: the node to remove nodes
        :param to_remove: number of edges to remove
        :param remove_set: the list to be updated
        '''
        edges = list(self.network().neighbors(node))
        remove_int = round(to_remove * len(edges))
        remove_list = rnd.sample(edges, remove_int)
        for i in remove_list:
            remove_set.append([node, i])

    def remove_edges(self, edge_list: list):
        '''
        This is a simple function that removes the edges passed to it

        :param edge_list: the list of edges to remove
        '''
        for edge in edge_list:
            if self.network().has_edge(edge[0], edge[1]):
                self.removeEdge(edge[0], edge[1])
                self.removed_edges.append([edge[0], edge[1]])

    def get_communities(self, g):
        '''
        This function splits the graph into communities. The communities are determined
        by the size of the input graph.

        :param g: the input graph
        '''
        size = g.number_of_nodes()
        if size > 50000:
            k = int(size / 500)
        elif size < 5000:
            k = int(size / 50)
        else:
            k = 100
        self.communities = community.asyn_fluidc(g, k)

    def fix_cases(self, t):
        '''
        Fix cases is a function that fills missing points in the cases array.
        If nobody s infected on a given day then the dictionary entry is not
        created. The function finds these days and inserts them.
        :param t: the point in time
        '''
        for i in range(0, t):
            if i not in self.cases:
                self.cases[i] = 0

