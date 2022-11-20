import networkx as nx
import DAG_generator as DG
import top_sort_DFS as TS_DFS
import top_sort_Kahns as TS_Kahns


class TestTopSort():
    """
    Class for managing the regression 
    """

    _debug = 0

    def __init__(self, debug):
        self._debug = debug
        self._TS_DFS = TS_DFS.TopSort_DFS(self._debug)
        self._TS_Kahns = TS_Kahns.TopSort_Kahns(self._debug)
        self._DG =  DG.DAG_generator()

    def plot_sorted_graph(self, G, sorted):
        pos = {n: (i+3, 0) for i, n in enumerate(sorted)}
        self._DG.plot_graph(G,pos)
        
       
    def run_avg_point(self, n=10, alg='dfs', samples=5, max_out=3, alpha=1):
        list_exect_times = []
        for i in range(samples):
            G = nx.DiGraph()
            (edges,into_degree,out_degree,position) = self._DG.DAG_generator(n=n, max_out=max_out, alpha=alpha)
            G = nx.DiGraph()
            G.add_edges_from(edges)
            if alg=='dfs':
                (sorted, exec_t) = self._TS_DFS.DeepFirstSearch(G)
            else: 
                (sorted, exec_t) = self._TS_Kahns.KahnsAlgorithm(G)
            if self._debug:
                print('Execution Time: ',exec_t)
            list_exect_times.append(exec_t)
        avg = sum(list_exect_times)/samples
        return avg
    
    def run_regression(self, file_name='results.txt'):
        set_dag_size = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 900000]  
        #set_dag_size = [1000]      
        #set_dag_size = [900000]      
        set_max_out = [1,10, 100, 1000]
        #set_max_out = [900]
        set_alpha = [0.5, 0.75, 1.0, 1.5, 2.0]
        set_beta = [0.0,0.5,1.0,2.0]
        f = open(file_name, "w")
        f.write('Alpha, Max_out, Size , DFS, KAHNS \n')
        for alpha in set_alpha:
            for max_out in set_max_out:
                for n in set_dag_size:
                    dfs_avg = self.run_avg_point(n=n, alg='dfs', samples=3, max_out=max_out, alpha=alpha)
                    kahn_avg = self.run_avg_point(n=n, alg='kahn', samples=3, max_out=max_out, alpha=alpha)
                    f.write('{}, {}, {}, {}, {}\n'.format(alpha, max_out, n, dfs_avg, kahn_avg))
        f.close()

            

TS = TestTopSort(0)
TS.run_regression('results.txt')

# TS = TestTopSort(0)
# (edges,into_degree,out_degree,position) = TS._DG.DAG_generator(n=10, max_out=5, alpha=2)
# G = nx.DiGraph()
# G.add_edges_from(edges)
# #TS._DG.plot_graph(G,position)
# (edges,into_degree,out_degree,position) = TS._DG.DAG_generator(n=10, max_out=3, alpha=0.5)
# G = nx.DiGraph()
# G.add_edges_from(edges)
# TS._DG.plot_graph(G,position)
# (sorted, t) = TS._TS_DFS.DeepFirstSearch(G)
# print(sorted)
# TS.plot_sorted_graph(G,sorted)
# G1 = G.copy()
# (sorted, t) = TS._TS_Kahns.KahnsAlgorithm(G1)
# print(sorted)
# TS.plot_sorted_graph(G,sorted)
