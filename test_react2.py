
from test_fci_furn import run_fges
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
from PyIF import te_compute as te
import numpy as np
import pandas as pd



from test_fci_furn import run_fges
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
import pandas as pd
from itertools import combinations




class test_react2_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping = var_mapping



    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()


        # Use the output of this to reset the fges inputs and forbid all control loops 
        model.reset_fges_inputs()
        model.forbid_control_loops()

        # Define required data
        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]

        # Additional filters 
        model.forbid_backwards(True)
        model.forbid_diff_streams(True)

        num_models = 8
        for itr_model in range(num_models):

            getattr(model, 'struct_'+str(itr_model))()
            model.edges.extend([('feed_feedstream/furn_1.F_3_DUMMY', 'Pos_3') , ('react_2.T_r_DUMMY', 'Pos_3') , ('react_2.T_r_DUMMY', 'Pos_2')])


            graph = {'nodes' : model.nodes,
                     'dummy vars' : model.dummy_vars,
                     'edges' : model.edges,
                     'forbidden' : model.forbid_edges}
            
            fges_obj = run_fges(graph, model.required_data, model.var_mapping, itr_model)
            fges_obj.run_fges_ctrl()


            ### Plot CPDAG for struct ###
            model.plot_CPDAG(itr_model, fges_obj, False)


            best_dag_data = {'all edges' : fges_obj.best_dag,
                            'knowledge' : fges_obj.edges_cat['knowledge'],
                            'data directed' : fges_obj.edges_cat['data'],
                            'redirected CPDAG' : [edge for edge in fges_obj.best_dag if edge in fges_obj.indirect_edges],
                            'score' : fges_obj.best_score}
            model.best_dags.append(best_dag_data)
            print(fges_obj.best_score)


            ### Plot best DAG of MEC ###
            model.plot_best_dag_in_class(itr_model, fges_obj, False)

            ### Save best graph of MEC ###
            name = f'struct{str(itr_model)}_furn_test'
            location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
            model.save_graphs(best_dag_data, name, location, False)
  

        unit_model_ind = model.find_best_model()
        model.unit_model_ind = unit_model_ind
        print(f'Best score: {model.best_dags[unit_model_ind]["score"]}')


        ### Visualise best DAG from all CPDAGs for each struct ###
        model.plot_best_dag_for_model(unit_model_ind, fges_obj, True)


        ### Save best model for unit ###
        name = f'struct{str(itr_model)}_furn_test_best'
        location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
        model.save_graphs(model.best_dags[unit_model_ind], name, location, False)


    # My opinion  
    def struct_0(model):

        model.edges = [('feed_feedstream/furn_1.F_3', 'react_2.P_4') , ('furn_1/react_2.T_2', 'react_2.T_r')]
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])


    # Temp in causes P
    def struct_1(model):

        model.edges = [('feed_feedstream/furn_1.F_3', 'react_2.P_4') , ('furn_1/react_2.T_2', 'react_2.T_r') , ('furn_1/react_2.T_2', 'react_2.P_4')]
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])


    # Additionally solid flow in causes solid flow out
    def struct_2(model):

        model.edges = [('feed_feedstream/furn_1.F_3', 'react_2.P_4') , ('furn_1/react_2.T_2', 'react_2.T_r') , ('furn_1/react_2.T_2', 'react_2.P_4') , ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc')]
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        

    # Solid flow in causes solid flow out without T in causing P
    def struct_3(model):

        model.edges = [('feed_feedstream/furn_1.F_3', 'react_2.P_4') , ('furn_1/react_2.T_2', 'react_2.T_r') , ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc')]
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])


    # Only T in causes T unit
    def struct_4(model):

        model.edges = [('furn_1/react_2.T_2', 'react_2.T_r')]    
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')]) 


    # Only flow in causes P unit 
    def struct_5(model):

        model.edges = [('feed_feedstream/furn_1.F_3', 'react_2.P_4')]    
        model.edges.extend([('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')]) 
        

    # Only flow and valves 
    def struct_6(model):

        model.edges = [('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')] 


    # Data only  
    def struct_7(model):

        model.edges = [] 

    


    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def reset_fges_inputs(model):

        # Adding things that don't change 
        model.nodes = ['react_1/v_2.F_rgc', 'react_2/v_3.F_sc', 'react_2.P_4', 'feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2', 'react_2.T_r']
        model.dummy_vars = ['react_2.T_r_DUMMY', 'feed_feedstream/furn_1.F_3_DUMMY']
        model.valve_pos = ['Pos_3', 'Pos_2']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data = model.data_orig
        model.data['T_r_DUMMY'] = model.data['T_r']
        model.data['F3_DUMMY'] = model.data['F3']
        model.var_mapping['react_2.T_r_DUMMY'] = 'T_r_DUMMY'
        model.var_mapping['feed_feedstream/furn_1.F_3_DUMMY'] = 'F3_DUMMY'

        model.dummy_valve_mapping = {'Pos_3': ['react_2.T_r_DUMMY', 'feed_feedstream/furn_1.F_3_DUMMY'],
                                     'Pos_2' : ['react_2.T_r_DUMMY']}


    def forbid_control_loops(model):

        # Prevents connections from dummy vars to anything other than the valve pos, and only dummy vars can cause valve pos
        model.forbid_edges = []
        for valve, dummy_vars in model.dummy_valve_mapping.items():

            model.forbid_edges.extend([(node, valve) for node in model.nodes if node not in dummy_vars])
            for itr_dummy_var in dummy_vars:

                model.forbid_edges.extend([(node, itr_dummy_var) for node in model.nodes])
                model.forbid_edges.extend([(itr_dummy_var, node) for node in model.nodes if node != valve])


    def forbid_backwards(model, activate):

        if activate:

            # All structures abide by the forbidden backwards rule
            node_tiers = {}
            node_tiers['out'] = ['react_2/v_3.F_sc', 'Pos_3']
            node_tiers['unit'] = ['react_2.T_r', 'react_2.P_4']
            node_tiers['in'] = ['feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2', 'react_1/v_2.F_rgc', 'Pos_2']
            
            node_tiers_names = ['out', 'unit', 'in']
            for itr_tier in range(len(node_tiers_names)-1):

                curr_tier = node_tiers_names[itr_tier]
                next_tiers = node_tiers_names[itr_tier+1:]
                for itr_next_tier in next_tiers:
                    
                    for itr_tier_node in node_tiers[curr_tier]:

                        model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[itr_next_tier]])


    def forbid_diff_streams(model, activate):

        if activate:            
            
            model.forbid_edges.extend([('feed_feedstream/furn_1.F_3', 'react_1/v_2.F_rgc') , ('furn_1/react_2.T_2', 'react_1/v_2.F_rgc') , ('react_1/v_2.F_rgc', 'feed_feedstream/furn_1.F_3') , 
                                       ('react_1/v_2.F_rgc', 'furn_1/react_2.T_2') , ('Pos_2', 'furn_1/react_2.T_2') , ('Pos_2', 'feed_feedstream/furn_1.F_3')])
            


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
            vis_graph.add_nodes_from(fges_obj.graph['nodes'])
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
            vis_graph.add_nodes_from(model.nodes)
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
