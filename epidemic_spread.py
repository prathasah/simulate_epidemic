# This module simulates time-based epidemic simulation

import networkx as nx
import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import time
import module_struct_12June2013 as gr


def run_timebased_epidemic(G,beta,sigma):
    """N=network size, T=transmissibility, tau=recovery probability"""
    start=time.clock()
    N=len(G.nodes())
    infected_list=[0]*N
    recovered_list = [0]*N
    track_infection=[0]*N
    track_recovery=[0]*N
    p_zero = rnd.choice(G.nodes())
    track_time=1
    infected_list[p_zero] = 1
    track_infection[p_zero]=1
    #pos = nx.spring_layout(G)
    while sum(infected_list)>0:
        #print ("time=="), time
        #visualize_epidemic(G, pos, infected_list, recovered_list, track_time)
        track_time += 1
        infected_list_new = [1 if infected_list[node]==0 and recovered_list[node]==0 and rnd.random()< (1- np.exp(-beta*infected_neighbors(node, infected_list))) else infected_list[node] for node in xrange(N)]       
        track_infection=[track_time if infected_list_new[node]-infected_list[node]==1 and recovered_list[node]==0 else track_infection[node] for node in xrange(N)]
        infected_list=[infected_list_new[x] if infected_list_new[x]==1 else infected_list[x] for x in xrange(N)]
        recovered_list_new=[1 if infected_list[node]==1 and rnd.random()<sigma else 0 for node in xrange (N) ]
        track_recovery=[track_time if recovered_list_new[node]-recovered_list[node]==1 else track_recovery[node] for node in xrange(N)] 
        infected_list=[0 if recovered_list_new[node]==1 else infected_list[node] for node in xrange(N)]
        recovered_list=[recovered_list_new[x] if recovered_list_new[x]==1 else recovered_list[x] for x in xrange(N)]      
    
    print ("time to extinction"),track_time
    print ("time taken infection"), time.clock()-start
    return track_infection, track_recovery   
        
        
def visualize_epidemic(G, pos, infected_list, recovered_list, track_time):
    """ visualize epidemic spread. Red indicates infected node, blue indicate 
    susceptible and black indicate recovered"""
    susceptible_list = [node for node in G.nodes() if infected_list[node] == 0 and recovered_list[node]==0] 
    #print ("susceptible list"), susceptible_list
    nx.draw_networkx_nodes(G, pos,nodelist = [node for node in xrange(len(G.nodes())) if infected_list[node]==1], node_color='r')
    nx.draw_networkx_nodes(G, pos, nodelist = [node for node in xrange(len(G.nodes())) if recovered_list[node]==1], node_color='k')
    nx.draw_networkx_nodes(G, pos, nodelist = susceptible_list, node_color='b')
    nx.draw_networkx_edges(G, pos, edgelist = G.edges())
    plt.title("time=" + str(time) + ", susceptible= " + str(len(susceptible_list))+", infected= "+str(sum(infected_list))+ ", recovered= "+str(sum(recovered_list)))
    plt.savefig('modular_time'+str(time).zfill(3)+'.png')

def infected_neighbors(node, infected_list):
    """Calculated the number of infected neighbors for the node"""
    return sum([infected_list[node_i] for node_i in G.neighbors(node)])   
    
        
if __name__ == "__main__":
    #G=gr.generate_mod_networks("poisson", 0.6, 1000, 10, 5)
    G=nx.read_edgelist("Edge_list_poissonn10000_m10_d10_Q0.0_iter0.txt", nodetype=int, data=False)
    track_infection, track_recovery = run_timebased_epidemic(G,0.061, 0.143)
    #print ("time to extinction"), time
    print ("tracked recovery"), track_recovery
    #print ("track recovery"), track_recovery
    #incidence= ec.calculate_incidence (time, track_infected)
    #print ("incidence"), incidence
        
