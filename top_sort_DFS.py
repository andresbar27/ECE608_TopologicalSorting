
import networkx as nx
import time 

class TopSort_DFS():
    _time = 0
    _sorted_list = []
    _debug = 0

    def __init__(self, debug):
        self._debug = debug

    def DeepFirstSearch(self, G):
        self._time = 0
        self._sorted_list = []
        dfs_time_start = time.process_time()
        nx.set_node_attributes(G, 'white', "color")
        nx.set_node_attributes(G, None, "Pi")
        nx.set_node_attributes(G, None, "d")
        nx.set_node_attributes(G, None, "f")
        if self._debug:
            print('Size: ', len(G.nodes()))
            print('Time: ', self._time)
        for u in G.nodes():
            if (G.nodes[u]["color"] == 'white'):
                #print("DFS: Node {} is white".format(u))
                self.DFS_visit(u, G)
        sorted = list(reversed(self._sorted_list))
        if self._debug:
            #print(nx.get_node_attributes(G,"color"))
            #print(nx.get_node_attributes(G,"d"))
            #print(nx.get_node_attributes(G,"f"))
            print(sorted)
        dfs_time_end = time.process_time()
        dfs_exec_t = dfs_time_end - dfs_time_start
        if self._debug:
            print('DFS Execution Time:', dfs_exec_t)
        return sorted, dfs_exec_t

    def DFS_visit(self, u, G):
        #if self._debug:
        #    print('DFS_visit: Entrance for node {}'.format(u))
        G.nodes[u]["color"] = 'gray'
        G.nodes[u]["d"]=self._time
        self._time = self._time +1
        for v in list(nx.neighbors(G, u)):
            if G.nodes[v]["color"] == 'white':
               G.nodes[v]["Pi"] = u
               self.DFS_visit(v, G)
        G.nodes[u]["color"] = 'black'
        G.nodes[u]["f"]=self._time
        self._sorted_list.append(u)
        self._time = self._time +1

