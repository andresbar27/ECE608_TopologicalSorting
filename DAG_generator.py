import random,math,argparse
import numpy as np
from numpy.random.mtrand import sample
from matplotlib import pyplot as plt
import networkx as nx

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default='default', type=str)#parameters setting
parser.add_argument('--n', default=10, type=int)          #number of DAG  nodes
parser.add_argument('--max_out', default=2, type=float)   #max out_degree of one node
parser.add_argument('--alpha',default=1,type=float)       #shape 
parser.add_argument('--beta',default=1.0,type=float)      #regularity
args = parser.parse_args()

set_dag_size = [20,30,40,50,60,70,80,90]             #random number of DAG  nodes       
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
        nx.draw_networkx(G)
        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()
    
    def DAGs_generate(mode = 'default',n = 10,max_out = 2,alpha = 1,beta = 1.0):
        ##############################################initialize###########################################
        args.mode = mode
        if args.mode != 'default':
            args.n = random.sample(set_dag_size,1)[0]
            args.max_out = random.sample(set_max_out,1)[0]
            args.alpha = random.sample(set_alpha,1)[0]
            args.beta = random.sample(set_alpha,1)[0]
        else: 
            args.n = n
            args.max_out = max_out
            args.alpha = alpha
            args.beta = beta

        length = math.floor(math.sqrt(args.n)/args.alpha)
        mean_value = args.n/length
        random_num = np.random.normal(loc = mean_value, scale = args.beta,  size = (length,1))    
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

        if generate_num != args.n:
            if generate_num<args.n:
                for i in range(args.n-generate_num):
                    index = random.randrange(0,length,1)
                    dag_list[index].append(len(dag_list[index]))
            if generate_num>args.n:
                i = 0
                while i < generate_num-args.n:
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
        into_degree = [0]*args.n            
        out_degree = [0]*args.n             
        edges = []                          
        pred = 0

        for i in range(length-1):
            sample_list = list(range(len(dag_list_update[i+1])))
            for j in range(len(dag_list_update[i])):
                od = random.randrange(1,args.max_out+1,1)
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


#G = nx.DiGraph([(0, 3), (1, 3), (2, 4), (3, 5), (3, 6), (4, 6), (5, 6)])

# # group nodes by column
# left_nodes = [1, 2, 3]
# middle_nodes = [4 ,5, 6]
# right_nodes = [7 ,8, 9]

# # set the position according to column (x-coord)
# pos = {n: (0, i) for i, n in enumerate([0])}
# pos.update({n: (1, i + 0.5) for i, n in enumerate(left_nodes)})
# pos.update({n: (2, i + 0.5) for i, n in enumerate(middle_nodes)})
# pos.update({n: (3, i + 0.5) for i, n in enumerate(right_nodes)})
