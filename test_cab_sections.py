from test_run_fges import run_fges
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
import pandas as pd
from itertools import combinations, product
import re
from handle_cycles import handle_cycles





class test_cab_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping_orig = var_mapping
        



    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()


        ### INPUT ###
        test_log = [4, 6]
        valves = ['V6']
        


        # Initialise data stores
        model.knowledge_scores = {}
        for itr_test in range(len(test_log)):
            
            model.knowledge_scores = model.knowledge_scores | {'test'+str(itr_test) : {'mode'+str(itr_mode) : None for itr_mode in range(test_log[itr_test])}}

        model.comb_data_store = []


        comb = list(product(*(range(itr) for itr in test_log)))
        for itr_comb in comb:

            model.comb_data_store.append({'combination' : itr_comb,
                                     'knowledge score' : None,
                                     'data score' : None,
                                     'graph score' : None,
                                     'knowledge count' : None,
                                     r'% of max degree' : None,
                                     'graph' : None,
                                     'edges cat' : None})
            model.reset_fges_inputs()

            # Build structure from section combinations and score section if necassary (method called from within test method)
            for test, mode in enumerate(itr_comb):

                getattr(model, 'test'+str(test))(mode)

            # Remove duplicates 
            model.nodes = list(set(model.nodes))
            model.dummy_nodes_struct = list(set(model.dummy_nodes_struct))
            model.edges = list(set(model.edges))

            graph = {'nodes' : model.nodes,
                     'edges' : model.edges}
            cycle_obj = handle_cycles(graph, model.required_data, model.var_mapping_orig)
            cycle_obj.handle_cycles_ctrl()

            # Skip if there any cycles as this will always lose
            if cycle_obj.cycle_nodes:

                continue


            # Score compiled sections / overall knowledge 
            total_kn_score = 0
            for test, mode in enumerate(itr_comb):

                total_kn_score += model.knowledge_scores['test'+str(test)]['mode'+str(mode)]
            model.comb_data_store[-1]['knowledge score'] = total_kn_score
            model.comb_data_store[-1]['knowledge count'] = len(model.edges)

            # Forbidden edges stay the same every time
            model.forbid_backwards(True)
            model.forbid_valves(True, valves)

            # Run FGES over knowledge struct and find best DAG
            graph = {'nodes' : model.nodes,
                     'dummy vars' : model.dummy_nodes_struct,
                     'edges' : model.edges,
                     'forbidden' : model.forbid_edges}
            fges_obj = run_fges(graph, model.required_data, 'run fges')
            fges_obj.run_fges_ctrl()

            # Plot best DAG of MEC
            model.plot_best_dag_in_class(itr_comb, fges_obj, False)

            graph = fges_obj.trim_graph
            graph['edges'] = fges_obj.best_dag

            # Populate data store 
            model.comb_data_store[-1]['graph score'] = fges_obj.best_score
            model.comb_data_store[-1]['data score'] = model.comb_data_store[-1]['graph score'] - model.comb_data_store[-1]['knowledge score']
            model.comb_data_store[-1][r'% of max degree'] = fges_obj.pc_degree
            model.comb_data_store[-1]['graph'] = graph
            model.comb_data_store[-1]['edges cat'] = fges_obj.edges_cat

            
        pass

  

        # unit_model_ind = model.find_best_model()
        # model.unit_model_ind = unit_model_ind
        # print(f'Best score: {model.best_dags[unit_model_ind]["score"]}')


        # ### Visualise best DAG from all CPDAGs for each struct ###
        # model.plot_best_dag_for_model(unit_model_ind, fges_obj, True)


        # ### Save best model for unit ###
        # name = f'struct{str(itr_model)}_furn_test_best'
        # location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
        # model.save_graphs(model.best_dags[unit_model_ind], name, location, False)



    # Test 0: Relationship between P1, W and P2. 
    def test0(model, test0_mode):


        if test0_mode == 0:

            nodes = ['P1', 'ACAB', 'P2']
            dummy_nodes_struct = []
            edges = [('P1', 'ACAB') , ('ACAB', 'P2')]

        elif test0_mode == 1:

            nodes = ['P1', 'ACAB', 'P2']
            dummy_nodes_struct = []
            edges = [('P1', 'ACAB') , ('P2', 'ACAB')]

        elif test0_mode == 2:

            nodes = ['P1', 'ACAB', 'P2']
            dummy_nodes_struct = []
            edges = [('P1', 'ACAB')]

        elif test0_mode == 3:

            nodes = ['P1', 'ACAB', 'P2']
            dummy_nodes_struct = []
            edges = []

        else:

            raise ValueError('Invalid test mode.')


        if not model.knowledge_scores['test0']['mode'+str(test0_mode)]:
            
            score = model.score_knowledge(nodes, dummy_nodes_struct, edges)
            model.knowledge_scores['test0']['mode'+str(test0_mode)] = score

        model.add_fges_inputs(nodes, dummy_nodes_struct, edges)
                     

    # Test 1: Valve intercation with comp. 
    def test1(model, test1_mode):

        if test1_mode == 0:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'F7') , ('V6', 'P2') , ('F7', 'ACAB')]

        elif test1_mode == 1:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'P2') , ('P2', 'F7') , ('F7', 'ACAB')]

        elif test1_mode == 2:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'P2') , ('P2', 'F7') , ('ACAB', 'F7')]

        elif test1_mode == 3:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'F7') , ('V6', 'P2')]

        elif test1_mode == 4:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'F7') , ('V6', 'P2')]

        elif test1_mode == 5:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = [('V6', 'F7')]

        elif test1_mode == 6:

            nodes = ['V6', 'ACAB', 'P2', 'F7']
            dummy_nodes_struct = []
            edges = []
        else:

            raise ValueError('Invalid test mode.')


        if not model.knowledge_scores['test1']['mode'+str(test1_mode)]:
            
            score = model.score_knowledge(nodes, dummy_nodes_struct, edges)
            model.knowledge_scores['test1']['mode'+str(test1_mode)] = score

        model.add_fges_inputs(nodes, dummy_nodes_struct, edges)


    def reset_fges_inputs(model):

        model.required_data = pd.DataFrame()
        model.nodes = []
        model.edges = []
        model.dummy_nodes_struct = []
        model.forbid_edges = []


    def score_knowledge(model, nodes, dummy_nodes_struct, edges):

        knowledge_data = model.data_orig[nodes]
        kn_nodes = nodes.copy()
        kn_nodes += dummy_nodes_struct
        for itr_dummy_node in dummy_nodes_struct:

            var_name = itr_dummy_node[:re.search(r'_(?=DUMMY)', itr_dummy_node).start()]
            knowledge_data[itr_dummy_node] = model.data_orig[var_name]

        graph = {'nodes' : kn_nodes,
                 'dummy vars' : dummy_nodes_struct,
                 'edges' : edges,
                 'forbidden' : []}
        
        fges_obj = run_fges(graph, knowledge_data, 'score kn')
        fges_obj.remove_no_variance()
        score = fges_obj.score_dag(fges_obj.trim_graph['edges'])

        return score



    def add_fges_inputs(model, nodes, dummy_nodes_struct, edges):
        
        model.required_data[nodes] = model.data_orig[nodes]
        nodes += dummy_nodes_struct
        for itr_dummy_node in dummy_nodes_struct:

            var_name = itr_dummy_node[:re.search(r'_(?=DUMMY)', itr_dummy_node).start()]
            model.required_data[itr_dummy_node] = model.data_orig[var_name]

        model.nodes += nodes
        model.dummy_nodes_struct += dummy_nodes_struct
        model.edges += edges


    def forbid_backwards(model, activate):

        if activate:

            model.forbid_edges.extend([('ACAB', 'P1') , ('F7', 'P1') , 
                                       ('P2', 'P1') , ('V6', 'P1') , ('V6', 'ACAB')])


    def forbid_valves(model, activate, valves):

        if activate:

            for itr_valve in valves:

                model.forbid_edges.extend([(node, itr_valve) for node in model.nodes])

            
    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def plot_CPDAG(model, itr_model, fges_obj, activate):

        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'CPDAG: {str(itr_model)}')
            vis_graph.add_nodes_from(fges_obj.graph['nodes'])
            vis_graph.add_edges_from(fges_obj.fges_edges)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['data'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.indirect_edges, edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def plot_best_dag_in_class(model, itr_model, fges_obj, activate):

        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'best DAG of MEC: {str(itr_model)}')
            vis_graph.add_nodes_from(model.nodes)
            vis_graph.add_edges_from(fges_obj.best_dag)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['data'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=[edge for edge in fges_obj.best_dag if edge in fges_obj.indirect_edges], edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def plot_best_dag_for_model(model, unit_model_ind, fges_obj, activate):
        
        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'Best DAG for unit: {str(unit_model_ind)}')
            vis_graph.add_nodes_from(model.best_dags[unit_model_ind]['nodes'])
            vis_graph.add_edges_from(model.best_dags[unit_model_ind]['all edges'])
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['data directed'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['redirected CPDAG'], edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def save_graphs(model, graph, name, location, activate):

        if activate:

            save_path = rf'{location}\{name}.xlsx'
            tools.print_to_excel(graph, save_path)


    def forbid_control_loops(model):

        # Prevents connections from dummy vars to anything other than the valve pos, and only dummy vars can cause valve pos

        model.forbid_edges = []
        for valve, dummy_vars in model.dummy_valve_mapping.items():

            model.forbid_edges.extend([(node, valve) for node in model.nodes if node not in dummy_vars])
            for itr_dummy_var in dummy_vars:

                model.forbid_edges.extend([(node, itr_dummy_var) for node in model.nodes])
                model.forbid_edges.extend([(itr_dummy_var, node) for node in model.nodes if node != valve])

