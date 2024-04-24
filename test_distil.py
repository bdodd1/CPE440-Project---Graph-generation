
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




class test_distil_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping = var_mapping



    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()


        # Test which variables should be dummy to the valve that is controlling an unmeasured var
        model.control_loop_test(False)


        num_models = 9
        for itr_model in range(num_models):

            model.reset_fges_inputs()
            unmeas_dummy = ['distil_1.T_10', 'distil_1.T_fra']
            test_valve = 'Pos_10'
            model.add_additional_nodes(unmeas_dummy, test_valve)
            test_valve = 'Pos_11'
            model.add_additional_nodes(unmeas_dummy, test_valve)
            model.forbid_control_loops()


            # Additional filters 
            model.forbid_diff_streams(True)

            getattr(model, 'struct_'+str(itr_model))()
            model.edges.extend([('distil_1.T_fra_DUMMY', 'Pos_8') , ('distil_1.T_10_DUMMY', 'Pos_10') , ('distil_1.T_fra_DUMMY', 'Pos_10') , ('distil_1.T_10_DUMMY', 'Pos_11') , ('distil_1.T_fra_DUMMY', 'Pos_11')])

            # Define required data
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




    # T psuedonodes - worst, extra dimensionality 
    def struct_0(model):

        model.edges = [('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra') , ('distil_1.T_fra', 'distil_1.T_10_DUMMYloop') , ('distil_1.T_10_DUMMYloop', 'distil_1.T_20_DUMMYloop'),
                        ('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.add_dummy('distil_1.T_20')
        model.add_dummy('distil_1.T_10')
        model.forbid_backwards([], True)
        model.forbid_edges.extend([('distil_1.T_10_DUMMYloop', node) for node in model.nodes if node != 'distil_1.T_20_DUMMYloop'])
        model.forbid_edges.extend([(node, 'distil_1.T_10_DUMMYloop') for node in model.nodes if node != 'distil_1.T_fra'])
        model.forbid_edges.extend([('distil_1.T_20_DUMMYloop', node) for node in model.nodes])
        model.forbid_edges.extend([(node, 'distil_1.T_20_DUMMYloop') for node in model.nodes if node != 'distil_1.T_10_DUMMYloop'])


    # Reboil/ in controlled with reflux affecting T - next worst
    def struct_1(model):

        model.edges = [('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra') ,
                        ('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([], True)


    # Reflux controlled - joint best 
    def struct_2(model):

        model.edges = [('distil_1.T_fra', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_20') , 
                        ('v_8/distil_1.F_reflux', 'distil_1.T_fra') , ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([], True)


    # In controlled - F reflux doesnt affect T - same struct as 1
    def struct_3(model):

        model.edges = [('distil_1.T_20', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_fra') ,
                        ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([], True)
        

    # Let data decide - same struct as 2
    def struct_4(model):

        model.edges = [('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn') , ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn') , 
                        ('distil_1.T_20', 'v_11/prod_lightoil.F_lco') , ('distil_1.P_5', 'v_11/prod_lightoil.F_lco') , ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry') , 
                        ('distil_1.P_5', 'distil_1/prod_slurry.F_slurry')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([], True)


    # Gone with best temp strat - reflux controlled

    # Product flows affect closest T and P (no reflux knowledge)
    def struct_5(model):

        model.edges = [('v_10/prod_heavynaptha.F_hn', 'distil_1.T_10') , ('v_10/prod_heavynaptha.F_hn', 'distil_1.P_5') , 
                        ('v_11/prod_lightoil.F_lco', 'distil_1.T_20') , ('v_11/prod_lightoil.F_lco', 'distil_1.P_5') , ('distil_1/prod_slurry.F_slurry', 'distil_1.T_20') , 
                        ('distil_1/prod_slurry.F_slurry', 'distil_1.P_5')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([('v_10/prod_heavynaptha.F_hn', 'distil_1.T_10') , ('v_10/prod_heavynaptha.F_hn', 'distil_1.P_5') , 
                        ('v_11/prod_lightoil.F_lco', 'distil_1.T_20') , ('v_11/prod_lightoil.F_lco', 'distil_1.P_5') , ('distil_1/prod_slurry.F_slurry', 'distil_1.T_20') , 
                        ('distil_1/prod_slurry.F_slurry', 'distil_1.P_5')], True)
        
    
    # Product flows affect closest T and P (reflux knowledge)
    def struct_6(model):

        model.edges = [('distil_1.T_fra', 'distil_1.T_10') , ('distil_1.T_10', 'distil_1.T_20') , ('v_8/distil_1.F_reflux', 'distil_1.T_fra') , 
                       ('v_10/prod_heavynaptha.F_hn', 'distil_1.T_10') , ('v_10/prod_heavynaptha.F_hn', 'distil_1.P_5') , 
                        ('v_11/prod_lightoil.F_lco', 'distil_1.T_20') , ('v_11/prod_lightoil.F_lco', 'distil_1.P_5') , ('distil_1/prod_slurry.F_slurry', 'distil_1.T_20') , 
                        ('distil_1/prod_slurry.F_slurry', 'distil_1.P_5')]
        model.edges.extend([('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')])
        model.forbid_backwards([('v_10/prod_heavynaptha.F_hn', 'distil_1.T_10') , ('v_10/prod_heavynaptha.F_hn', 'distil_1.P_5') , 
                        ('v_11/prod_lightoil.F_lco', 'distil_1.T_20') , ('v_11/prod_lightoil.F_lco', 'distil_1.P_5') , ('distil_1/prod_slurry.F_slurry', 'distil_1.T_20') , 
                        ('distil_1/prod_slurry.F_slurry', 'distil_1.P_5')], True)



    def struct_7(model):

        model.edges = [('Pos_8', 'v_8/distil_1.F_reflux') , ('Pos_10', 'v_10/prod_heavynaptha.F_hn') , ('Pos_11', 'v_11/prod_lightoil.F_lco')]
        model.forbid_backwards([], True)

    
    def struct_8(model):

        model.edges = []
        model.forbid_backwards([], True) 



    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def add_dummy(model, var):

        dummy_name = var+'_DUMMYloop'
        model.nodes.append(dummy_name)
        col_name = model.var_mapping[var]
        col_dummy_name = col_name + '_DUMMYloop'
        model.data[col_dummy_name] = model.data[col_name]
        model.var_mapping[dummy_name] = col_dummy_name


    def reset_fges_inputs(model):

        # Adding things that don't change 
        model.nodes = ['distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 'v_8/distil_1.F_reflux', 
                       'distil_1/prod_slurry.F_slurry']
        # model.dummy_vars = ['distil_1.T_fra_DUMMY', 'distil_1.T_10_DUMMY']
        model.dummy_vars = ['distil_1.T_fra_DUMMY']
        # model.valve_pos = ['Pos_8', 'Pos_11']
        model.valve_pos = ['Pos_8']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data = model.data_orig
        model.data['T_fra_DUMMY'] = model.data['T_fra']
        # model.data['T_10_DUMMY'] = model.data['T_10']
        model.var_mapping['distil_1.T_fra_DUMMY'] = 'T_fra_DUMMY'
        # model.var_mapping['distil_1.T_10_DUMMY'] = 'T_10_DUMMY'


        # model.dummy_valve_mapping = {'Pos_8': ['distil_1.T_fra_DUMMY'],
        #                              'Pos_11' : ['distil_1.T_10_DUMMY']}
        model.dummy_valve_mapping = {'Pos_8': ['distil_1.T_fra_DUMMY']}



    def add_additional_nodes(model, node_list, test_valve):

        model.dummy_valve_mapping[test_valve] = []
        dup_dummy_var = []
        for itr_var in node_list:

            dummy_var_name = itr_var+'_DUMMY'
            if dummy_var_name not in model.dummy_vars:

                column_name = model.var_mapping[itr_var]
                dummy_col_name = column_name+'_DUMMY'
                # if dummy_var_name in model.dummy_vars:
                    
                #     dummy_var_name += '2'
                #     dummy_col_name += '2'

                model.dummy_vars.append(dummy_var_name)
                model.nodes.append(dummy_var_name)            
                model.data[dummy_col_name] = model.data[column_name]
                model.var_mapping[dummy_var_name] = dummy_col_name

            else:

                dup_dummy_var.append(dummy_var_name)

            model.dummy_valve_mapping[test_valve].append(dummy_var_name)

        model.valve_pos.append(test_valve)
        model.nodes.append(test_valve)

        return dup_dummy_var


    def control_loop_test(model, activate):

        if activate: 

            potential_vars = ['distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 'v_8/distil_1.F_reflux', 
                              'distil_1/prod_slurry.F_slurry']
            test_valve = 'Pos_10'
            # test_valve = 'Pos_11'
            model.test_valve = test_valve

            # Get combinations of potential dummy vars 
            all_combinations = []
            #for itr in range(1, len(potential_vars) + 1):
            for itr in range(1, 4):

                comb_at_itr = list(combinations(potential_vars, itr))
                all_combinations.extend(comb_at_itr)

            # Check score of every combination
            scores = []
            for itr_comb in all_combinations:

                # Reset things inputs to thngs that don't change - more long winded but its safer 
                model.reset_fges_inputs()

                # Add things which are changing every test
                dup_dummy_var = model.add_additional_nodes(itr_comb, test_valve)
                model.forbid_control_loops()

                # Define required data
                columns = [model.var_mapping[sensor] for sensor in model.nodes]
                model.required_data = model.data[columns]

                # Arbitrary comparison struct with appended dummy var-valve reationships 
                model.struct_3()
                connect_dummy_vars = model.dummy_vars[2:] + dup_dummy_var
                model.edges.extend([(dummy_var, test_valve) for dummy_var in connect_dummy_vars])
                model.edges.extend([('distil_1.T_fra_DUMMY', 'Pos_8') , ('distil_1.T_10_DUMMY', 'Pos_11')])

                graph = {'nodes' : model.nodes,
                        'dummy vars' : model.dummy_vars,
                        'edges' : model.edges,
                        'forbidden' : model.forbid_edges}
                fges_obj = run_fges(graph, model.required_data, model.var_mapping, 'CL test')
                fges_obj.run_fges_ctrl()
                scores.append(fges_obj.best_score)

                print(itr_comb)
                print(fges_obj.best_score)
                print('*****')
                model.plot_CPDAG(str(len(itr_comb)), fges_obj, False)


            highest_score = max(scores)
            best_comb_ind = [itr for itr, score in enumerate(scores) if score == highest_score]
            len_best_combs = [len(all_combinations[comb]) for comb in best_comb_ind]
            model.unmeas_dummy = all_combinations[best_comb_ind[len_best_combs.index(min(len_best_combs))]]

            print('***')
            print(f'Best combination: {model.unmeas_dummy}')
            print(f'Best score: {highest_score}')
            print('***')

            pass




    def forbid_control_loops(model):

        # Prevents connections from dummy vars to anything other than the valve pos, and only dummy vars can cause valve pos

        model.forbid_edges = []
        for valve, dummy_vars in model.dummy_valve_mapping.items():

            model.forbid_edges.extend([(node, valve) for node in model.nodes if node not in dummy_vars])
            for itr_dummy_var in dummy_vars:

                model.forbid_edges.extend([(node, itr_dummy_var) for node in model.nodes])
                model.forbid_edges.extend([(itr_dummy_var, node) for node in model.nodes if node != valve])


    def forbid_backwards(model, exclude_list, activate):

        if activate:

            # Forbids all going backwards 
            node_tiers = {}
            node_tiers['out'] = ['v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 'distil_1/prod_slurry.F_slurry', 'Pos_10', 'Pos_11']
            node_tiers['unit'] = ['distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5']
            node_tiers['in'] = ['v_8/distil_1.F_reflux', 'Pos_8']
            
            node_tiers_names = ['out', 'unit', 'in']
            for itr_tier in range(len(node_tiers_names)-1):

                curr_tier = node_tiers_names[itr_tier]
                next_tiers = node_tiers_names[itr_tier+1:]
                for itr_next_tier in next_tiers:
                    
                    for itr_tier_node in node_tiers[curr_tier]:

                        model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[itr_next_tier] if (itr_tier_node, next_tier_node) not in exclude_list])

            

    def forbid_diff_streams(model, activate):

        if activate:            
            
            model.forbid_edges.extend([('v_10/prod_heavynaptha.F_hn', 'v_11/prod_lightoil.F_lco') , ('v_11/prod_lightoil.F_lco', 'v_10/prod_heavynaptha.F_hn') , 
                                       ('v_10/prod_heavynaptha.F_hn', 'distil_1/prod_slurry.F_slurry') , ('distil_1/prod_slurry.F_slurry', 'v_10/prod_heavynaptha.F_hn') ,
                                       ('v_11/prod_lightoil.F_lco', 'distil_1/prod_slurry.F_slurry') , ('distil_1/prod_slurry.F_slurry', 'v_11/prod_lightoil.F_lco') , 
                                       ('Pos_10' , 'v_11/prod_lightoil.F_lco') , ('Pos_10' , 'distil_1/prod_slurry.F_slurry') , 
                                       ('Pos_11' , 'v_10/prod_heavynaptha.F_hn') , ('Pos_11' , 'distil_1/prod_slurry.F_slurry')])
            


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

        

