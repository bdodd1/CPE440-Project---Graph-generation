
import pyinform
import pandas as pd
import numpy as np

# data = pd.read_csv('NOC_stableFeedFlow_outputs.csv')
# source_node = data['L_sp'].to_numpy()
# dest_node = data['F_rgc'].to_numpy()

source_node = np.array([2*x**2 + 4*x + 10 for x in range(10)])
dest_node = np.array([2*(x+1)**2 + 4*(x+1) + 10 for x in range(10)])
print(pyinform.transfer_entropy(source_node, dest_node, k=1))



class handle_cycles:

    def __init__(graph_cyc, graph):

        graph_cyc.nodes = graph.whole_graph['nodes']
        graph_cyc.edges = graph.whole_graph['edges']
        graph_cyc.data = graph.data
        graph_cyc.var_mapping = graph.var_mapping

    
    def handle_cycles_ctrl(graph_cyc):

        graph_cyc.build_reach_mat()
        graph_cyc.categorise_cycles()
        graph_cyc.split_cycles()
        graph_cyc.calc_transfer_entropy()

    
    def build_reach_mat(graph_cyc):
    
        nodes = graph_cyc.nodes
        edges = graph_cyc.edges

        adj_mat = build_latent_adj_mat(nodes, edges)
        graph_cyc.adj_mat = adj_mat

        reach_mat = pd.DataFrame(0, index = nodes, columns = nodes)

        for itr_node in nodes:

            visited_nodes = set()
            adj_nodes = adj_mat.columns[adj_mat.loc[itr_node] == 1].to_list()
            while adj_nodes:

                next_node = adj_nodes.pop(0)
                if next_node not in visited_nodes:

                    reach_mat.loc[itr_node, next_node] = 1
                    visited_nodes.add(next_node)
                    adj_nodes.extend(adj_mat.columns[adj_mat.loc[next_node] == 1].to_list())

        graph_cyc.reach_mat = reach_mat


    def categorise_cycles(graph_cyc):

        reach_mat = graph_cyc.reach_mat
        adj_mat = graph_cyc.adj_mat
        nodes = adj_mat.columns

        cycle_nodes = []
        for itr, itr_node in enumerate(nodes):

            if reach_mat.iloc[itr,itr] == 1:

                cycle_nodes.append(itr_node)

        bidirectionals = set()
        for itr_cycle_node in cycle_nodes:

            for itr_cycle_node_next in cycle_nodes:
            
                if adj_mat.loc[itr_cycle_node, itr_cycle_node_next] == 1 and adj_mat.loc[itr_cycle_node_next, itr_cycle_node] == 1:

                    bidirectionals.add(itr_cycle_node)

        cycle_nodes = [node for node in cycle_nodes if node not in bidirectionals]

        # print(cycle_nodes)

        graph_cyc.cycle_nodes = cycle_nodes
        graph_cyc.bidirectionals = bidirectionals


    def split_cycles(graph_cyc):

        cycle_nodes = graph_cyc.cycle_nodes
        adj_mat = graph_cyc.adj_mat

        cycles = {}
        key_count = 1
        nodes_remaining = cycle_nodes
        while nodes_remaining:

            initial_node = nodes_remaining[0]
            nodes_remaining.remove(initial_node)
            cycles = cycles | {key_count : {'nodes' : [initial_node],
                                            'edges' : []}}

            curr_node = initial_node
            loop_incomplete = True
            while loop_incomplete:

                for itr_rem_node in nodes_remaining:

                    if adj_mat.loc[curr_node, itr_rem_node] == 1:
                        
                        cycles[key_count]['nodes'].append(itr_rem_node)
                        cycles[key_count]['edges'].append((curr_node, itr_rem_node))
                        nodes_remaining.remove(itr_rem_node)
                        curr_node = itr_rem_node

                        if adj_mat.loc[curr_node, initial_node] == 1:

                            cycles[key_count]['edges'].append((curr_node, initial_node))
                            loop_incomplete = False

                        break

            key_count += 1

        graph_cyc.cycles = cycles
        # print(cycles)


    def calc_transfer_entropy(graph_cyc):

        for itr_cycle in graph_cyc.cycles.values():

            test_edges = itr_cycle['edges']
            transfer_entropy = []
            for itr_test_edge in test_edges:

                source_node = graph_cyc.data[graph_cyc.var_mapping[itr_test_edge[0]]]
                dest_node = graph_cyc.data[graph_cyc.var_mapping[itr_test_edge[1]]]
                transfer_entropy.append(pyinform.transfer_entropy(source_node.to_numpy(), dest_node.to_numpy(), k=5))

                print(transfer_entropy[-1])








##### This will not be in final release. Will hard code adj matrix to save time #####
def build_latent_adj_mat(all_sensors, latent_struct):

    latent_adj_mat = pd.DataFrame(columns=all_sensors, index = all_sensors)
    latent_adj_mat.iloc[:,:] = 0

    for itr_edge in latent_struct:
        
        latent_adj_mat.loc[itr_edge[0] ,itr_edge[1] ] = 1

    return latent_adj_mat