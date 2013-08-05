# This module simulates time-based epidemic simulation

import networkx as nx
import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import module_struct_12June2013 as gr
import epidemic_calculations as ec

def run_timebased_epidemic(G,N, beta,sigma):
    """N=network size, T=transmissibility, tau=recovery probability"""
    infected_list=[0]*N
    recovered_list = [0]*N
    track_infection=[0]*N
    track_recovery=[0]*N
    p_zero = rnd.choice(G.nodes())
    infected_list[p_zero] = 1
    time = 0
    track_infected=[0]*N
    track_infected[p_zero]=1
    pos = nx.spring_layout(G)
    while sum(infected_list)>0:
        print ("time=="), time
        visualize_epidemic(G, pos, infected_list, recovered_list, time)
        time += 1
        infected_list_new = [1 if infected_list[node]==0 and recovered_list[node]==0 and rnd.random()< (1- np.exp(-beta*infected_neighbors(node, infected_list))) else infected_list[node] for node in xrange(N)]       
        recovered_list_new=[1 if infected_list[node]==1 and rnd.random()<sigma else recovered_list[node] for node in xrange (N) ]
        infected_list_new=[0 if recovered_list_new[node]==1 else infected_list_new[node] for node in xrange(N)]
        track_infection=[time if list(np.array(infected_list_new)-np.array(infected_list))[node]==1 and recovered_list[node]==0 else track_infected[node] for node in xrange(N)]
        track_recovery=[time if list(np.array(infected_list_new)-np.array(infected_list))[node]==1 else track_recovery[node] for node in xrange(N)]  
        infected_list=infected_list_new
        recovered_list=recovered_list_new
    return track_infection, track_recovery   
        
        
def visualize_epidemic(G, pos, infected_list, recovered_list, time):
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
    return sum([infected_list[node_i] for node_i in G.neighbors(node)])   
    
        
if __name__ == "__main__":
    G=gr.generate_mod_networks("poisson", 0.6, 120,3,5)
    time, track_infected = run_timebased_epidemic(G, 120, 0.061, 0.1)
    #print ("time to extinction"), time
    #print ("tracked infection"), track_infected
    #incidence= ec.calculate_incidence (time, track_infected)
    #print ("incidence"), incidence
        
