from test_fci_furn import run_fges
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
import pandas as pd
from itertools import combinations




class test_cab_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping_orig = var_mapping
        



    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()




        num_models = 10
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


            best_dag_data = {'nodes' : model.nodes,
                            'all edges' : fges_obj.best_dag,
                            'knowledge' : fges_obj.edges_cat['knowledge'],
                            'data directed' : fges_obj.edges_cat['data'],
                            'redirected CPDAG' : [edge for edge in fges_obj.best_dag if edge in fges_obj.indirect_edges],
                            'score' : fges_obj.best_score}
            model.best_dags.append(best_dag_data)
            print(fges_obj.best_score)


            ### Plot best DAG of MEC ###
            model.plot_best_dag_in_class(itr_model, fges_obj, True)

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

        model.edges = [('feed_air/comp_1.P_1', 'ACAB') , ('ACAB', 'comp_1/v_6.P_2') , ('comp_1/v_6.P_2', 'ACAB_sDUMMY')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])
        model.add_dummy('ACAB')
        model.forbid_edges.extend([('comp_1/v_6.P_2', 'ACAB')])
        model.forbid_edges.extend([('ACAB_DUMMY', 'ACAB') , ('ACAB_DUMMY', 'feed_air/comp_1.P_1') , ('ACAB_DUMMY', 'comp_1/v_6.P_2') , 
                                   ('ACAB_DUMMY', 'Pos_6') , ('ACAB_DUMMY', 'react_1.T_reg_DUMMY') , ('ACAB_DUMMY', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('ACAB', 'ACAB_DUMMY') , ('feed_air/comp_1.P_1', 'ACAB_DUMMY') , ('Pos_6', 'ACAB_DUMMY') , 
                                   ('react_1.T_reg_DUMMY', 'ACAB_DUMMY') , ('comp_1/v_6.F_7', 'ACAB_DUMMY')])
                                   


    # Don't enforce outlet P control - see which way data thinks edge is 
    def struct_1(model):

        model.edges = [('feed_air/comp_1.P_1', 'ACAB') , ('ACAB', 'comp_1/v_6.P_2')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('comp_1/v_6.F_7', 'ACAB')])


    # Don't enforce outlet P control - don't constrain outlet flow 
    def struct_2(model):

        model.edges = [('feed_air/comp_1.P_1', 'ACAB') , ('ACAB', 'comp_1/v_6.P_2')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])
        

    # Outlet P controlled, valve causes P as well
    def struct_3(model):

        model.edges = [('feed_air/comp_1.P_1', 'ACAB') , ('ACAB', 'comp_1/v_6.P_2') , ('comp_1/v_6.P_2', 'ACAB_DUMMY')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7') , ('Pos_6', 'comp_1/v_6.P_2')])
        model.add_dummy('ACAB')
        model.forbid_edges.extend([('comp_1/v_6.P_2', 'ACAB') , ('comp_1/v_6.F_7', 'ACAB')])
        model.forbid_edges.extend([('ACAB_DUMMY', 'ACAB') , ('ACAB_DUMMY', 'feed_air/comp_1.P_1') , ('ACAB_DUMMY', 'comp_1/v_6.P_2') , 
                                   ('ACAB_DUMMY', 'Pos_6') , ('ACAB_DUMMY', 'react_1.T_reg_DUMMY') , ('ACAB_DUMMY', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('ACAB', 'ACAB_DUMMY') , ('feed_air/comp_1.P_1', 'ACAB_DUMMY') , ('Pos_6', 'ACAB_DUMMY') , 
                                   ('react_1.T_reg_DUMMY', 'ACAB_DUMMY') , ('comp_1/v_6.F_7', 'ACAB_DUMMY')])
    

    # Outlet P controlled, P in doesn't cause work
    def struct_4(model):

        model.edges = [('ACAB', 'comp_1/v_6.P_2') , ('comp_1/v_6.P_2', 'ACAB_DUMMY')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7') , ('Pos_6', 'comp_1/v_6.P_2')])
        model.add_dummy('ACAB')
        model.forbid_edges.extend([('comp_1/v_6.P_2', 'ACAB') , ('comp_1/v_6.F_7', 'ACAB')])
        model.forbid_edges.extend([('ACAB_DUMMY', 'ACAB') , ('ACAB_DUMMY', 'feed_air/comp_1.P_1') , ('ACAB_DUMMY', 'comp_1/v_6.P_2') , 
                                   ('ACAB_DUMMY', 'Pos_6') , ('ACAB_DUMMY', 'react_1.T_reg_DUMMY') , ('ACAB_DUMMY', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('ACAB', 'ACAB_DUMMY') , ('feed_air/comp_1.P_1', 'ACAB_DUMMY') , ('Pos_6', 'ACAB_DUMMY') , 
                                   ('react_1.T_reg_DUMMY', 'ACAB_DUMMY') , ('comp_1/v_6.F_7', 'ACAB_DUMMY')])
        

    # Prevent all backwards and no outlet P control
    def struct_5(model):

        model.edges = [('feed_air/comp_1.P_1', 'ACAB') , ('ACAB', 'comp_1/v_6.P_2')]
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('comp_1/v_6.F_7', 'ACAB') , ('comp_1/v_6.P_2', 'ACAB')])


    # Prevent all backwards and just valves
    def struct_6(model):

        model.edges = []
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])
        model.forbid_edges.extend([('comp_1/v_6.F_7', 'ACAB') , ('comp_1/v_6.P_2', 'ACAB')])


    # Allow some backwards and just valves 
    def struct_7(model):

        model.edges = []
        model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('Pos_6', 'comp_1/v_6.F_7')])


    # Prevent all backwards and just valves
    def struct_8(model):

        model.edges = []
        model.forbid_edges.extend([('comp_1/v_6.F_7', 'ACAB') , ('comp_1/v_6.P_2', 'ACAB')])


    # Allow some backwards and just valves 
    def struct_9(model):

        model.edges = []


    def add_dummy(model, var):

        dummy_name = var+'_sDUMMY'
        model.nodes.append(dummy_name)
        col_name = model.var_mapping[var]
        col_dummy_name = col_name + '_sDUMMY'
        model.data[col_dummy_name] = model.data[col_name]
        model.var_mapping[dummy_name] = col_dummy_name



    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def reset_fges_inputs(model):

        model.nodes = ['feed_air/comp_1.P_1', 'comp_1/v_6.F_7', 'comp_1/v_6.P_2', 'ACAB']
        model.dummy_vars = ['react_1.T_reg_DUMMY']
        model.valve_pos = ['Pos_6']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data = model.data_orig
        model.data['T_reg_DUMMY'] = model.data['T_reg']
        model.var_mapping = model.var_mapping_orig
        model.var_mapping['react_1.T_reg_DUMMY'] = 'T_reg_DUMMY'

        model.dummy_valve_mapping = {'Pos_6': ['react_1.T_reg_DUMMY']}


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

            model.forbid_edges.extend([('ACAB', 'feed_air/comp_1.P_1') , ('comp_1/v_6.F_7', 'feed_air/comp_1.P_1') , 
                                       ('comp_1/v_6.P_2', 'feed_air/comp_1.P_1') , ('Pos_6', 'feed_air/comp_1.P_1') , ('Pos_6', 'ACAB')])

            

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




