
from test_fci_furn import run_fci_class
from run_BIC import run_BIC
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
from PyIF import te_compute as te
import numpy as np
import pandas as pd




class test_distil_models:

    def __init__(model, data, var_mapping):

        model.data = data
        model.var_mapping = var_mapping
        model.nodes = ['distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 'v_8/distil_1.F_reflux', 'distil_1/prod_slurry.F_slurry']


    def model_ctrl(model):

        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]
        model.best_dags = []
        graph_store = []



        num_models = 9
        for itr_model in range(1,num_models):

            getattr(model, 'struct_'+str(itr_model))()
            graph  ={'nodes' : model.nodes,
                     'edges' : model.edges}
            
            graph_fci = run_fci_class(graph, model.required_data, model.var_mapping, itr_model)
            graph_fci.run_fci_ctrl()




            ### For plotting CPDAG
            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            vis_graph.add_nodes_from(graph['nodes'])
            vis_graph.add_edges_from(graph_fci.fci_edges_tup)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.edges_cat['data'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.edges_cat['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.undirect_edges, edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


            ### For plotting best DAG
            knowledge = graph_fci.edges_cat['knowledge']
            redirected_pdag = [edge for edge in graph_fci.best_dag if edge in graph_fci.undirect_edges or (edge[1], edge[0]) in graph_fci.undirect_edges]
            directed_data = [edge for edge in graph_fci.best_dag if edge not in knowledge and edge not in redirected_pdag]
            vis_graph = nx.DiGraph()
            # plt.figure(figsize=[5, 5])
            # vis_graph.add_nodes_from(graph['nodes'])
            # vis_graph.add_edges_from(graph_fci.best_dag)
            # pos = nx.spring_layout(vis_graph)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=directed_data, edge_color='red', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=knowledge, edge_color='black', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=redirected_pdag, edge_color='blue', width=2)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            # plt.show()


            ### For plotting direct CPDAG
            # knowledge = graph_fci.edges_cat['knowledge']
            # directed_data = [edge for edge in graph_fci.direct_edges if edge not in knowledge]
            # vis_graph = nx.DiGraph()
            # plt.figure(figsize=[5, 5])
            # vis_graph.add_nodes_from(graph['nodes'])
            # vis_graph.add_edges_from(graph_fci.direct_edges)
            # pos = nx.spring_layout(vis_graph)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=directed_data, edge_color='red', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=knowledge, edge_color='black', width=2)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            # plt.show()


            ### For saving graphs - edit edges and save name 
            # graph = {'nodes' : model.nodes,
            #          'edges' : graph_fci.fci_edges_tup}
            # trial_name = f'furn_test_{str(itr_model)}'
            # save_loc = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\furn test fges semBIC pen 5'
            # save_path = rf'{save_loc}\{trial_name}.xlsx'
            # tools.print_to_excel(graph, save_path)


           

            ### For finding best dag 
            model.best_dags.append({'all edges' : graph_fci.best_dag,
                                      'knowledge' : knowledge,
                                      'data directed' : directed_data,
                                      'redirected CPDAG' : redirected_pdag,
                                    'score' : graph_fci.best_score})
            print(graph_fci.best_score)


            ### For direct CPDAG
            # model.best_dags.append({'all edges' : graph_fci.direct_edges,
            #                         'knowledge' : knowledge,
            #                         'data directed' : directed_data,
            #                         'score' : graph_fci.dag_score})
            # print(graph_fci.dag_score)


            if itr_model == 0:

                model.nodes.remove('distil_1.T_20_DUMMY')
                model.nodes.remove('distil_1.T_10_DUMMY')
                del model.var_mapping['distil_1.T_20_DUMMY']
                del model.var_mapping['distil_1.T_10_DUMMY']
                model.required_data = model.required_data.drop(columns = ['T_20_DUMMY', 'T_10_DUMMY'])



        unit_model_ind = model.find_best_model()


        print(f'Best score: {model.best_dags[unit_model_ind]["score"]}')


        ### Visualise best DAG for all directed CPDAGs for each struct
        # vis_graph = nx.DiGraph()
        # plt.figure(figsize=[5, 5])
        # vis_graph.add_nodes_from(model.nodes)
        # vis_graph.add_edges_from(model.best_dags[unit_model_ind]['all edges'])
        # pos = nx.spring_layout(vis_graph)
        # nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['data directed'], edge_color='red', width=2)
        # nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['knowledge'], edge_color='black', width=2)
        # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
        # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
        # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
        # plt.show()

        ### Visualise best DAG from all CPDAGs for each struct
        vis_graph = nx.DiGraph()
        plt.figure(figsize=[5, 5])
        vis_graph.add_nodes_from(model.nodes)
        vis_graph.add_edges_from(model.best_dags[unit_model_ind]['all edges'])
        pos = nx.spring_layout(vis_graph)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['data directed'], edge_color='red', width=2)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['knowledge'], edge_color='black', width=2)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['redirected CPDAG'], edge_color='blue', width=2)
        nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
        nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
        nx.draw_networkx_labels(vis_graph, pos, font_color='green')
        plt.show()


        ### Save best model for unit
        # graph = {'nodes' : model.nodes,
        #          'edges' : unit_model_struct}
        # trial_name = 'furn_test_best_1_1'
        # save_loc = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs'
        # save_path = rf'{save_loc}\{trial_name}.xlsx'
        # tools.print_to_excel(graph, save_path)




    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind

    

            
# ['distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 'v_8/distil_1.F_reflux', 'distil_1/prod_slurry.F_slurry']
    
    # My opinion psuedonodes
    def struct_0(model):

        model.dummy_list = ['distil_1.T_20_DUMMY', 'distil_1.T_10_DUMMY']
        model.nodes.extend(['distil_1.T_20_DUMMY', 'distil_1.T_10_DUMMY'])
        model.edges = [('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra') , ('distil_1.T_fra', 'distil_1.T_10_DUMMY') , ('distil_1.T_10_DUMMY', 'distil_1.T_20_DUMMY'),
                        ('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]


        model.required_data.loc[:,'T_10_DUMMY'] = model.required_data['T_10']
        model.required_data.loc[:,'T_20_DUMMY'] = model.required_data['T_20']

        model.var_mapping['distil_1.T_20_DUMMY'] = 'T_20_DUMMY'
        model.var_mapping['distil_1.T_10_DUMMY'] = 'T_10_DUMMY'
        



    # My opinion psuedonodes TE
    def struct_1(model):

        model.edges = [('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        
        # T20_T10_te = te.te_compute(model.required_data['T_20'].to_numpy(), model.required_data['T_10'].to_numpy(), safetyCheck=False) 
        # T10_T20_te = te.te_compute(model.required_data['T_10'].to_numpy(), model.required_data['T_20'].to_numpy(), safetyCheck=False) 
        # T10_Tfra_te = te.te_compute(model.required_data['T_10'].to_numpy(), model.required_data['T_fra'].to_numpy(), safetyCheck=False) 
        # Tfra_T10_te = te.te_compute(model.required_data['T_fra'].to_numpy(), model.required_data['T_10'].to_numpy(), safetyCheck=False) 

        model.edges.extend([('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra')])



    # Reflux has greater effect
    def struct_2(model):

        model.edges = [('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.T_fra', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_20')]
        

    # Reboil has a greater effect excluded but put in main 

    # Try a struct where F relfux doesn't affect things as much 

    # Let data dictate temp direction 
    def struct_3(model):

        model.edges = [('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        

    # Only certain about T,P effects on prod flow
    def struct_4(model):

        model.edges = [('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , 
                       ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]        


    # Only certain about T
    def struct_5(model):

        model.edges = [('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry')]  
        

    # Only certain about P
    def struct_6(model):

        model.edges = [('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]  


    # Only certain about T up the column 
    def struct_7(model):

        model.edges = [('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra')]

    
    # data only
    def struct_8(model):

        model.edges = []