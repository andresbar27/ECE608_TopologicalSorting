"""
DAG_generator: This Class provides two methods for generating a Directed Acyclic Graph,
and a method to plot the graph using matplot libs.
"""
import random,math
import numpy as np
from numpy.random.mtrand import sample
from matplotlib import pyplot as plt
import networkx as nx


class DAG_generator():
    
    def __init__(self) -> None:
        pass

    def generate_DAG(self, n, p):
        G=nx.gnp_random_graph(n,p,directed=True)
        reversed_G = G.reverse()
        #From the random;y Generated Graph, remove any edge that goes backwards
        DAG = nx.DiGraph([(u,v) for (u,v) in reversed_G.edges() if u<v])
        DAG
        if nx.is_directed_acyclic_graph(DAG):
            return DAG
        else:
            print("Error in DAG_generator")
            return
    
    def plot_graph(self, G, pos):
        plt.figure()
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        #pos = {n: (0, i) for i, n in enumerate(G.nodes())}
        #pos.update({n: (1, i + 0.5) for i, n in enumerate(left_nodes)})
        #pos.update({n: (2, i + 0.5) for i, n in enumerate(middle_nodes)})
        #pos.update({n: (3, i + 0.5) for i, n in enumerate(right_nodes)})
        nx.draw_networkx(G, pos)
        plt.show()

    def DAG_generator(mode = 'default',n = 10,max_out = 2,alpha = 1,beta = 1.0):
        """"
        Adapted and modified function from:
        https://github.com/Livioni/DAG_Generator
        """
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
        for node,id in enumerate(into_degree):
            if id ==0:
                edges.append(('Start',node+1))
                into_degree[node]+=1

        for node,od in enumerate(out_degree):
            if od ==0:
                edges.append((node+1,'Exit'))
                out_degree[node]+=1

        #############################################plot##################################################
        return edges,into_degree,out_degree,position
