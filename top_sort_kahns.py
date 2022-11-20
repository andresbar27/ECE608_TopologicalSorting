import time

class TopSort_Kahns():
    _debug = 0
    
    def __init__(self, debug):
        self._debug = debug

    def KahnsAlgorithm(self, G):
        sorted = []
        kahn_time_start = time.process_time() 
        while G.number_of_nodes() > 0:
            for node in list(G.nodes()):
                if G.in_degree(node) == 0:
                    G.remove_node(node)
                    sorted.append(node)
        kahn_time_end = time.process_time()
        kahn_exec_t = kahn_time_end - kahn_time_start
        if self._debug:
            print('Kahns Execution Time:', kahn_exec_t)
        if self._debug:
            print(sorted)
        return sorted, kahn_exec_t