
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




class test_wgc_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping_orig = var_mapping
        

    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()


        # Additional filters 


        num_models = 6
        for itr_model in range(num_models):

            model.reset_fges_inputs()
            model.forbid_control_loops()
            model.forbid_backwards(True)
            getattr(model, 'struct_'+str(itr_model))()

            columns = [model.var_mapping[sensor] for sensor in model.nodes]
            model.required_data = model.data[columns]


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


    def struct_0(model):

        model.edges = [('Pos_4', 'comp_2/prod_lpg.F_lpg') , ('Pos_4', 'AWGC') , ('AWGC', 'comp_2/prod_lpg.F_lpg')]
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))


    def struct_1(model):
        
        model.edges = [('Pos_4', 'AWGC') , ('AWGC', 'comp_2/prod_lpg.F_lpg')]
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))


    def struct_2(model):

        model.edges = [('Pos_4', 'AWGC') , ('Pos_4', 'comp_2/prod_lpg.F_lpg')]
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))
        

    def struct_3(model):

        model.edges = [('Pos_4', 'AWGC')]
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))


    def struct_4(model):

        model.edges = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))


    def struct_5(model):

        model.edges = []
        model.edges.append(('react_2.P_5_DUMMY', 'Pos_4'))




    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def reset_fges_inputs(model):

        model.nodes = ['AWGC', 'comp_2/prod_lpg.F_lpg']
        model.dummy_vars = ['react_2.P_5_DUMMY']
        model.valve_pos = ['Pos_4']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data = model.data_orig
        model.data['P5_DUMMY'] = model.data['P5']
        model.var_mapping = model.var_mapping_orig
        model.var_mapping['react_2.P_5_DUMMY'] = 'P5_DUMMY'

        model.dummy_valve_mapping = {'Pos_4': ['react_2.P_5_DUMMY']}


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

            model.forbid_edges.extend([('comp_2/prod_lpg.F_lpg', 'AWGC') , ('comp_2/prod_lpg.F_lpg', 'Pos_4') , ('AWGC', 'Pos_4')])

            

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




