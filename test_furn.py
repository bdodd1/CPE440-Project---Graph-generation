
from test_fci_furn import run_fci_class
from run_BIC import run_BIC
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
import pandas as pd




class test_furn_models:

    def __init__(model, data, var_mapping):

        model.data = data
        model.var_mapping = var_mapping
        model.nodes = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5', 'furn_1.T_3', 'furn_1/react_2.T_2']


    def model_ctrl(model):

        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]
        model.best_dags = []
        graph_store = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()


        node_tiers = {}
        node_tiers['out'] = ['furn_1/react_2.T_2']
        node_tiers['unit'] = ['furn_1.T_3']
        node_tiers['in'] = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5']
        
        node_tiers_names = ['out', 'unit', 'in']
        model.forbid_edges = []
        for itr_tier in range(len(node_tiers_names)-1):

            curr_tier = node_tiers_names[itr_tier]
            next_tier = node_tiers_names[itr_tier+1]
            for itr_tier_node in node_tiers[curr_tier]:

                model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[next_tier]])


        num_models = 9
        for itr_model in range(num_models):

            # model.forbid_edges = []
            getattr(model, 'struct_'+str(itr_model))()
            graph  ={'nodes' : model.nodes,
                     'edges' : model.edges,
                     'forbidden' : model.forbid_edges}
            
            graph_fci = run_fci_class(graph, model.required_data, model.var_mapping, itr_model)
            graph_fci.run_fci_ctrl()




            ### For plotting CPDAG
            # vis_graph = nx.DiGraph()
            # plt.figure(figsize=[5, 5])
            # vis_graph.add_nodes_from(graph['nodes'])
            # vis_graph.add_edges_from(graph_fci.fci_edges_tup)
            # pos = nx.spring_layout(vis_graph)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.edges_cat['data'], edge_color='red', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.edges_cat['knowledge'], edge_color='black', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.undirect_edges, edge_color='blue', width=2)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            # plt.show()


            ### For plotting best DAG
            knowledge = graph_fci.edges_cat['knowledge']
            redirected_pdag = [edge for edge in graph_fci.best_dag if edge in graph_fci.undirect_edges or (edge[1], edge[0]) in graph_fci.undirect_edges]
            directed_data = [edge for edge in graph_fci.best_dag if edge not in knowledge and edge not in redirected_pdag]
            # vis_graph = nx.DiGraph()
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
            # save_loc = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
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
        # vis_graph = nx.DiGraph()
        # plt.figure(figsize=[5, 5])
        # vis_graph.add_nodes_from(model.nodes)
        # vis_graph.add_edges_from(model.best_dags[unit_model_ind]['all edges'])
        # pos = nx.spring_layout(vis_graph)
        # nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['data directed'], edge_color='red', width=2)
        # nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['knowledge'], edge_color='black', width=2)
        # nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['redirected CPDAG'], edge_color='blue', width=2)
        # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
        # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
        # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
        # plt.show()


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

    

            

    
    # My opinion
    def struct_0(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2')]

    # TEMP
    # def struct_1(model):

    #     model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2')]

        # node_tiers = {}
        # node_tiers['out'] = ['furn_1/react_2.T_2']
        # node_tiers['unit'] = ['furn_1.T_3']
        # node_tiers['in'] = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5']
        
        # node_tiers_names = ['out', 'unit', 'in']
        # model.forbid_edges = []
        # for itr_tier in range(len(node_tiers_names)-1):

        #     curr_tier = node_tiers_names[itr_tier]
        #     next_tier = node_tiers_names[itr_tier+1]
        #     for itr_tier_node in node_tiers[curr_tier]:

        #         model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[next_tier]])


    # Addition of fuel flow to outlet temp (direct + indirect)
    def struct_1(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , 
                       ('feed_fuel/v_1.F_5', 'furn_1/react_2.T_2')]


    # Inlet temp sufficient to cause a change in furnace temp and outlet temp
    def struct_2(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , 
                       ('feed_feedstream/furn_1.T_1', 'furn_1.T_3')]
        

    # Inlet temp sufficient to cause a change in furnace temp 
    def struct_3(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1.T_3')]
        

    # Inlet flow sufficient to cause a change in furnace temp and outlet temp
    def struct_4(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2'),
                       ('feed_feedstream/furn_1.F_3', 'furn_1.T_3')]
        

    # Inlet flow sufficient to cause a change in furnace temp 
    def struct_5(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2'),
                       ('feed_feedstream/furn_1.F_3', 'furn_1.T_3')]
        

    ### Lower knolwedge content ###
    # 3 most important
    def struct_6(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2')]


    # 2 most important 
    def struct_7(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('furn_1.T_3', 'furn_1/react_2.T_2')]

    
    # data only
    def struct_8(model):

        model.edges = []