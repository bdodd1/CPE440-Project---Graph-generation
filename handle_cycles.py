
import pyinform
import pandas as pd
import numpy as np
from PyIF import te_compute as te
from tools import tools 


class handle_cycles:

    def __init__(graph, graph_struct, data, var_mapping):

        graph.nodes = graph_struct['nodes']
        graph.edges = graph_struct['edges']
        graph.data = data
        graph.var_mapping = var_mapping

    
    def handle_cycles_ctrl(graph):

        graph.build_reach_mat()
        graph.find_bidirectionals()
        graph.handle_bidirectionals()
        graph.build_reach_mat()
        graph.split_cycles()
        # graph.calc_transfer_entropy()

    
    def build_reach_mat(graph):
    
        nodes = graph.nodes
        edges = graph.edges

        adj_mat = tools.build_adj_mat(nodes, edges)
        graph.adj_mat = adj_mat

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

        graph.reach_mat = reach_mat


    def find_bidirectionals(graph):

        reach_mat = graph.reach_mat
        adj_mat = graph.adj_mat
        nodes = adj_mat.columns

        cycle_nodes = []
        for itr, itr_node in enumerate(nodes):

            if reach_mat.iloc[itr,itr] == 1:

                cycle_nodes.append(itr_node)

        bidirectional_edges = []
        for itr_cycle_node in cycle_nodes:

            for itr_cycle_node_next in cycle_nodes:
            
                if adj_mat.loc[itr_cycle_node, itr_cycle_node_next] == 1 and adj_mat.loc[itr_cycle_node_next, itr_cycle_node] == 1 and (itr_cycle_node_next, itr_cycle_node) not in bidirectional_edges:

                    bidirectional_edges.append((itr_cycle_node, itr_cycle_node_next))

        
        graph.bidirectional_edges = bidirectional_edges
        print(bidirectional_edges)
        # graph.bidirectional_nodes = list(set([]))


    def handle_bidirectionals(graph):

        for itr_biedge in graph.bidirectional_edges:

            arb_node = itr_biedge[0]   
            dummy_var = arb_node+'_DUMMY'
            col_name = graph.var_mapping[arb_node]   
            dummy_col = col_name+'_DUMMY'

            graph.nodes.append(dummy_var)
            graph.edges.append((itr_biedge[1], dummy_var))
            graph.edges.remove((itr_biedge[1], arb_node))
            graph.data[dummy_col] = graph.data[col_name]
            graph.var_mapping[dummy_var] = dummy_col



    def split_cycles(graph):

        reach_mat = graph.reach_mat
        adj_mat = graph.adj_mat
        nodes = adj_mat.columns

        cycle_nodes = []
        for itr, itr_node in enumerate(nodes):

            if reach_mat.iloc[itr,itr] == 1:

                cycle_nodes.append(itr_node)

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

        graph.cycles = cycles
        print(cycles)


    def calc_transfer_entropy(graph):

        for itr_cycle in graph.cycles.values():

            test_edges = itr_cycle['edges']
            transfer_entropy = []
            for itr_test_edge in test_edges:

                source_node = graph.data[graph.var_mapping[itr_test_edge[0]]]
                dest_node = graph.data[graph.var_mapping[itr_test_edge[1]]]
                transfer_entropy.append(te.te_compute(source_node.to_numpy(), dest_node.to_numpy(), safetyCheck=False, k=4))

                print(transfer_entropy[-1])

