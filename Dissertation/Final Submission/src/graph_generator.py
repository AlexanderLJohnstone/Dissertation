import er_generator as ER
from networkx import graph
import ba_generator as BA
import ws_generator as WS
import rpn_generator as RPN


class GraphMaker:
    selection: int
    G: graph
    received_values = []

    def set_selection(self, selection):
        '''
        Set the selection from user
        :param selection: integer representing the graph
        '''
        self.selection = selection

    def set_received_values(self, received_values):
        '''
        Set the paramaters for the network
        :param received_values: list of parameters from the user
        '''
        self.received_values = received_values

    def make_er(self):
        '''
        Generate an ER graph according to user input
        '''
        global G
        n = int(float(self.received_values[0]))
        p = float(self.received_values[1])
        G = ER.generate_web(n, p)
        return G

    def make_ws(self):
        '''
        Generate a WS graph according to user input
        '''
        global G
        N = int(float(self.received_values[0]))
        K = int(float(self.received_values[1]))
        B = float(self.received_values[2])
        G = WS.generate_web(N, K, B)
        return G

    def make_ba(self):
        '''
        Generate a BA graph according to user input
        '''
        global G
        n = int(float(self.received_values[0]))
        m = int(float(self.received_values[1]))
        lim = int(float(self.received_values[2]))
        G = BA.generate_web(n, m, lim)
        return G

    def make_rpn(self):
        '''
        Generate an RPN graph according to user input
        '''
        global G
        N = int(float(self.received_values[0]))
        M = int(float(self.received_values[1]))
        G = RPN.generate_web(N, M)
        return G

    def make_graph(self):
        '''
        Generate graph according to selection
        '''
        selection = self.selection
        if selection == 1:
            self. G = self.make_er()
        if selection == 2:
            self. G = self.make_ws()
        if selection == 3:
            self.G = self.make_ba()
        if selection == 4:
            self.G = self.make_rpn()

    def get_G(self):
        '''
        Return generated graph
        '''
        return self.G