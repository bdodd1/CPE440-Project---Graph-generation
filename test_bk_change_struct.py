
from test_fci_furn import run_fci_class
# from handle_cycles import handle_cycles
from run_BIC import run_BIC
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 


import random

class test_models:

    def __init__(model, data, var_mapping):

        model.data = data
        model.var_mapping = var_mapping
        model.nodes = ['comp_1/v_6.F_7', 'react_1.T_reg', 'react_1.L_sp', 'react_1.P_6', 'react_1/v_7.F_sg', 'react_1/v_7.T_cyc', 'v_7/prod_stack.X_co', 
                       'v_7/prod_stack.X_co2', 'react_1/v_2.F_rgc', 'react_2/v_3.F_sc']


    def model_ctrl(model):

        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]

        struct_store = {}
        key_count = 1

        new_struct_count = 0
        while new_struct_count <= 10:

            new_struct_found = False
            struct = []
            for itr, itr_node in enumerate(model.nodes):

                num_edges = random.randint(0, 3)                
                node_ind = []
                while len(node_ind) <= num_edges-1 or not node_ind:

                    new_ind = random.randint(0, len(model.nodes)-1)
                    if new_ind in node_ind or new_ind == itr:

                        pass
                    else:
                        node_ind.append(new_ind)

                struct.extend([(itr_node, model.nodes[ind]) for ind in node_ind])


            graph = {'nodes' : model.nodes,
                     'edges' : struct}
            
            # graph_cyc = handle_cycles(graph, model.required_data, model.var_mapping)
            # graph_cyc.handle_cycles_ctrl()

            # while graph_cyc.cycle_nodes or graph_cyc.bidirectionals:
            
            #     if graph_cyc.cycle_nodes:
            #         cycle_node = graph_cyc.cycle_nodes[0]
            #         for itr_cycle_node in graph_cyc.cycle_nodes:

            #             if graph_cyc.adj_mat.loc[cycle_node, itr_cycle_node] == 1:

            #                 graph['edges'].remove((cycle_node, itr_cycle_node))
            #                 break

            #     if graph_cyc.bidirectionals:
            #         bi_edges = graph_cyc.bidirectionals
            #         while bi_edges:

            #             bi_edge = bi_edges.pop(0)
            #             for itr_bi_edge in bi_edges:

            #                 if graph_cyc.adj_mat.loc[bi_edge, itr_bi_edge] == 1:

            #                     graph['edges'].remove((bi_edge, itr_bi_edge))
            #                     bi_edges.remove(itr_bi_edge)
            #                     break
            
            #     graph_cyc = handle_cycles(graph, model.required_data, model.var_mapping)
            #     graph_cyc.handle_cycles_ctrl()


            graph_fci = run_fci_class(graph, model.required_data, model.var_mapping, 'hi')
            graph_fci.run_fci_ctrl()

            struct_store[key_count] = graph_fci.fci_edges_tup
            if key_count > 1:

                comp_struct = struct_store[1]
                for itr_edge in graph_fci.fci_edges_tup:

                    if itr_edge not in comp_struct and (itr_edge[1], itr_edge[0]) not in comp_struct:

                        new_struct_found = True 
                        new_struct_count += 1
                        break 

            knowledge_ret_cnt = 0
            for itr_edge in graph_fci.fci_edges_tup:

                if itr_edge in graph['edges']:

                    knowledge_ret_cnt += 1

            print(f'Knowledge retained = {100*knowledge_ret_cnt/len(graph["edges"])}')

            # if new_struct_found:

            #     print('****************************')
            #     print('****************************')
            #     print('****************************')
            #     print(f'New struct = {struct_store[key_count]}')
            #     print(f'Knowlegde = {graph["edges"]}')
            #     print(f'Same struct = {struct_store[1]}')
            #     print('****************************')
            #     print('****************************')
            #     print('****************************')

            # else:
            #     print('****************************')
            #     print(f' Run {key_count} : Not found')
            #     print('****************************')


            key_count += 1
            









            



