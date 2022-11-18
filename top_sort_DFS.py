import random,math,argparse
import numpy as np
from numpy.random.mtrand import sample
from matplotlib import pyplot as plt
import networkx as nx
import time 


#set_dag_size = [20,30,40,50,60,70,80,90]             #random number of DAG  nodes       
set_dag_size = [5]
set_max_out = [1,2,3,4,5]                              #max out_degree of one node
set_alpha = [0.5,1.0,2.0]                            #DAG shape
set_beta = [0.0,0.5,1.0,2.0]                         #DAG regularity

class DAG_generator():
    
    def __init__(self) -> None:
        pass
    def generate_DAG(self, n, p):
        G=nx.gnp_random_graph(n,p,directed=True)
        reversed_G = G.reverse()
        DAG = nx.DiGraph([(u,v) for (u,v) in reversed_G.edges() if u<v])
        DAG
        if nx.is_directed_acyclic_graph(DAG):
            return DAG
        else:
            print("Error in DAG_generator")
            return
    def plot_graph(self, G):
        plt.figure()
        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        #pos = {n: (0, i) for i, n in enumerate(G.nodes())}
        #pos.update({n: (1, i + 0.5) for i, n in enumerate(left_nodes)})
        #pos.update({n: (2, i + 0.5) for i, n in enumerate(middle_nodes)})
        #pos.update({n: (3, i + 0.5) for i, n in enumerate(right_nodes)})
        nx.draw_networkx(G)
        plt.show()

    def generate_DAG_complex(mode = 'default',n = 10,max_out = 2,alpha = 1,beta = 1.0):
        ##############################################initialize###########################################

        length = math.floor(math.sqrt(n)/alpha)
        mean_value = n/length
        random_num = np.random.normal(loc = mean_value, scale = beta,  size = (length,1))    
        ###############################################division############################################
        position = {'Start':(0,4),'Exit':(10,4)}
        generate_num = 0
        dag_num = 1
        dag_list = [] 
        for i in range(len(random_num)):
            dag_list.append([]) 
            for j in range(math.ceil(random_num[i])):
                dag_list[i].append(j)
            generate_num += math.ceil(random_num[i])

        if generate_num != n:
            if generate_num<n:
                for i in range(n-generate_num):
                    index = random.randrange(0,length,1)
                    dag_list[index].append(len(dag_list[index]))
            if generate_num>n:
                i = 0
                while i < generate_num-n:
                    index = random.randrange(0,length,1)
                    if len(dag_list[index])==1:
                        i = i-1 if i!=0 else 0
                    else:
                        del dag_list[index][-1]
                    i += 1

        dag_list_update = []
        pos = 1
        max_pos = 0
        for i in range(length):
            dag_list_update.append(list(range(dag_num,dag_num+len(dag_list[i]))))
            dag_num += len(dag_list_update[i])
            pos = 1
            for j in dag_list_update[i]:
                position[j] = (3*(i+1),pos)
                pos += 5
            max_pos = pos if pos > max_pos else max_pos
            position['Start']=(0,max_pos/2)
            position['Exit']=(3*(length+1),max_pos/2)

        ############################################link###################################################
        into_degree = [0]*n            
        out_degree = [0]*n             
        edges = []                          
        pred = 0

        for i in range(length-1):
            sample_list = list(range(len(dag_list_update[i+1])))
            for j in range(len(dag_list_update[i])):
                od = random.randrange(1,max_out+1,1)
                od = len(dag_list_update[i+1]) if len(dag_list_update[i+1])<od else od
                bridge = random.sample(sample_list,od)
                for k in bridge:
                    edges.append((dag_list_update[i][j],dag_list_update[i+1][k]))
                    into_degree[pred+len(dag_list_update[i])+k]+=1
                    out_degree[pred+j]+=1 
            pred += len(dag_list_update[i])


        ######################################create start node and exit node################################
        for node,id in enumerate(into_degree):#给所有没有入边的节点添加入口节点作父亲
            if id ==0:
                edges.append(('Start',node+1))
                into_degree[node]+=1

        for node,od in enumerate(out_degree):#给所有没有出边的节点添加出口节点作儿子
            if od ==0:
                edges.append((node+1,'Exit'))
                out_degree[node]+=1

        #############################################plot##################################################
        return edges,into_degree,out_degree,position



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
        if self._debug:
            #print(nx.get_node_attributes(G,"color"))
            #print(nx.get_node_attributes(G,"d"))
            #print(nx.get_node_attributes(G,"f"))
            print(list(reversed(self._sorted_list)))
        dfs_time_end = time.process_time()
        dfs_exec_t = dfs_time_end - dfs_time_start
        if self._debug:
            print('DFS Execution Time:', dfs_exec_t)
        return dfs_exec_t

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



class TopSort_Kahns():
    _debug = 0
    
    def __init__(self, debug):
        self._debug = debug

    def KahnsAlgorithm(self, G):
        sorted = []
        #G = G.copy()
        kahn_time_start = time.process_time() 
        while G.number_of_nodes() > 0:
            for node in list(G.nodes()):
                if G.in_degree(node) == 0:
                    #degree_0.append(node)
                    G.remove_node(node)
                    sorted.append(node)
        kahn_time_end = time.process_time()
        kahn_exec_t = kahn_time_end - kahn_time_start
        if self._debug:
            print('Kahns Execution Time:', kahn_exec_t)
        if self._debug:
            print(sorted)
        return kahn_exec_t

class TestTopSort():
    _TS_DFS = TopSort_DFS(0)
    _TS_Kahns = TopSort_Kahns(0)
    _DG = DAG_generator()
    _debug = 0

    def __init__(self, debug):
        self._debug = debug
    
    def run_avg_point(self, n=10, alg='dfs', samples=5, max_out=3):
        list_exect_times = []
        for i in range(samples):
            G = nx.DiGraph()
            (edges,into_degree,out_degree,position) = self._DG.generate_DAG_complex(n=n, max_out=max_out)
            G = nx.DiGraph()
            G.add_edges_from(edges)
            if alg=='dfs':
                exec_t = self._TS_DFS.DeepFirstSearch(G)
            else: 
                exec_t = self._TS_Kahns.KahnsAlgorithm(G)
            if self._debug:
                print('Execution Time: ',exec_t)
            list_exect_times.append(exec_t)
        avg = sum(list_exect_times)/samples
        return avg
    
    def run_regression(self):
        set_dag_size = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 900000]      
        #set_dag_size = [10, 100, 500]      
        set_max_out = [1,2,3,4,5,10]
        set_alpha = [0.5,1.0,2.0]
        set_beta = [0.0,0.5,1.0,2.0]
        f = open("results.txt", "w")
        f.write('Max_out, Size , DFS, KAHNS \n')
        for max_out in set_max_out:
            for n in set_dag_size:
                dfs_avg = self.run_avg_point(n=n, alg='dfs', samples=5, max_out=max_out)
                kahn_avg = self.run_avg_point(n=n, alg='kahn', samples=5, max_out=max_out)
                f.write('{}, {}, {}, {}\n'.format(max_out, n, dfs_avg, kahn_avg))
        f.close()

            


TS = TestTopSort(0)
TS.run_regression()