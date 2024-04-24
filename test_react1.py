
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




class test_react1_models:

    def __init__(model, data, var_mapping):

        model.data_orig = data
        model.var_mapping = var_mapping



    def model_ctrl(model):


        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()

        # model.forbid_diff_streams(True)


        # Test which variables should be dummy to the valve that is controlling an unmeasured var
        model.control_loop_test(False)

        # Use the output of this to reset the fges inputs and forbid all control loops 
        model.reset_fges_inputs()
        unmeas_dummy = ['react_2.T_r', 'feed_feedstream/furn_1.F_3']
        test_valve = 'Pos_3'
        model.add_additional_nodes(unmeas_dummy, test_valve)
        model.forbid_control_loops()

        # Additional filters 
        model.forbid_diff_streams(True)

        num_models = 10
        for itr_model in range(num_models):

            getattr(model, 'struct_'+str(itr_model))()
            model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('react_1.P_6_DUMMY', 'Pos_7') , ('react_2.T_r_DUMMY', 'Pos_2') , ('react_2.T_r_DUMMY', 'Pos_3') , ('feed_feedstream/furn_1.F_3_DUMMY', 'Pos_3')])


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



    # Graph 1
    def struct_0(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , ('react_2/v_3.F_sc', 'react_1.T_reg') , ('react_1.L_sp', 'react_1/v_2.F_rgc') , 
                       ('react_1.P_6', 'react_1/v_7.F_sg') , ('react_1.T_reg', 'react_1/v_7.T_cyc') , ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , 
                       ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2')]
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        model.forbid_backwards([], True)


    # Out flow controls unit 
    def struct_1(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , ('react_2/v_3.F_sc', 'react_1.T_reg') , 
                       ('react_1/v_2.F_rgc', 'react_1.L_sp') , 
                       ('react_1/v_7.F_sg', 'react_1.P_6') , ('react_1.T_reg', 'react_1/v_7.T_cyc') , ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , 
                       ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2')]
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        exclude_list = [('react_1/v_7.F_sg', 'react_1.P_6') , ('react_1/v_2.F_rgc', 'react_1.L_sp')]
        model.forbid_backwards(exclude_list, True)



    # In causes out and unit (except T)
    def struct_2(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('comp_1/v_6.F_7', 'react_1/v_7.F_sg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , 
                       ('react_2/v_3.F_sc', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc') , ('react_2/v_3.F_sc', 'react_1/v_7.F_sg') , ('react_1.T_reg', 'react_1/v_7.T_cyc') ,
                       ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2')]
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        model.forbid_backwards([], True)

        

    # In causes out and unit, out causes unit (except T)
    def struct_3(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('comp_1/v_6.F_7', 'react_1/v_7.F_sg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , 
                       ('react_2/v_3.F_sc', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc') , ('react_2/v_3.F_sc', 'react_1/v_7.F_sg') , ('react_1.T_reg', 'react_1/v_7.T_cyc') ,
                       ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2') , 
                       ('react_1/v_2.F_rgc', 'react_1.L_sp') , ('react_1/v_7.F_sg', 'react_1.P_6')]
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        exclude_list = [('react_1/v_7.F_sg', 'react_1.P_6') , ('react_1/v_2.F_rgc', 'react_1.L_sp')]
        model.forbid_backwards(exclude_list, True)
        

    # In causes out and unit, unit causes out (except T)
    def struct_4(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('comp_1/v_6.F_7', 'react_1/v_7.F_sg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , 
                       ('react_2/v_3.F_sc', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc') , ('react_2/v_3.F_sc', 'react_1/v_7.F_sg') , ('react_1.T_reg', 'react_1/v_7.T_cyc') ,
                       ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2') , 
                       ('react_1.L_sp', 'react_1/v_2.F_rgc') , ( 'react_1.P_6', 'react_1/v_7.F_sg')]    
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')]) 
        model.forbid_backwards([], True)


    # Drop outlet vars. unit -> out won. Going with this going forward.
    def struct_5(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('comp_1/v_6.F_7', 'react_1.T_reg') , ('react_2/v_3.F_sc', 'react_1.L_sp') , 
                       ('react_2/v_3.F_sc', 'react_1.T_reg') , ('react_1.T_reg', 'react_1/v_7.T_cyc') ,
                       ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2')]
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        model.forbid_backwards([], True) 
        

    # uncertain about all flows affecting T
    def struct_6(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('react_2/v_3.F_sc', 'react_1.L_sp') , ('react_1.T_reg', 'react_1/v_7.T_cyc') ,
                       ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2') , ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2')] 
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        model.forbid_backwards([], True)


    # Uncertain about T,P causing comp out  
    def struct_7(model):

        model.edges = [('comp_1/v_6.F_7', 'react_1.P_6') , ('react_2/v_3.F_sc', 'react_1.L_sp') , ('react_1.T_reg', 'react_1/v_7.T_cyc')] 
        model.edges.extend([('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')])
        model.forbid_backwards([], True)

    
    # Only certain of valves affectinf flows 
    def struct_8(model):

        model.edges = [('Pos_6', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_7.F_sg') , ('Pos_3', 'react_2/v_3.F_sc') , ('Pos_2', 'react_1/v_2.F_rgc')]
        model.forbid_backwards([], True) 


    # data only
    def struct_9(model):

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


    def reset_fges_inputs(model):

        # Adding things that don't change 
        model.nodes = ['comp_1/v_6.F_7', 'react_1.T_reg', 'react_1.L_sp', 'react_1.P_6', 'react_1/v_7.F_sg', 'react_1/v_7.T_cyc', 'v_7/prod_stack.X_co', 'v_7/prod_stack.X_co2', 
                       'react_1/v_2.F_rgc', 'react_2/v_3.F_sc']
        model.dummy_vars = ['react_1.T_reg_DUMMY', 'react_1.P_6_DUMMY', 'react_2.T_r_DUMMY']
        model.valve_pos = ['Pos_6', 'Pos_7', 'Pos_2']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data = model.data_orig
        model.data['T_reg_DUMMY'] = model.data['T_reg']
        model.data['P6_DUMMY'] = model.data['P6']
        model.data['T_r_DUMMY'] = model.data['T_r']
        model.var_mapping['react_1.T_reg_DUMMY'] = 'T_reg_DUMMY'
        model.var_mapping['react_1.P_6_DUMMY'] = 'P6_DUMMY'
        model.var_mapping['react_2.T_r_DUMMY'] = 'T_r_DUMMY'

        model.dummy_valve_mapping = {'Pos_6': ['react_1.T_reg_DUMMY'],
                               'Pos_7' : ['react_1.P_6_DUMMY'],
                               'Pos_2' : ['react_2.T_r_DUMMY']}



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

        # Define required data
        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]

        return dup_dummy_var



    def control_loop_test(model, activate):

        if activate: 

            potential_vars = ['react_2.P_4', 'react_2.T_r', 'feed_feedstream/furn_1.F_3', 'react_1/v_2.F_rgc']
            test_valve = 'Pos_3'
            model.test_valve = test_valve

            # Get combinations of potential dummy vars 
            all_combinations = []
            for itr in range(1, len(potential_vars) + 1):

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

                # Arbitrary comparison struct with appended dummy var-valve reationships 
                model.struct_0()
                connect_dummy_vars = model.dummy_vars[3:] + dup_dummy_var
                model.edges.extend([(dummy_var, test_valve) for dummy_var in connect_dummy_vars])
                model.edges.extend([('react_1.T_reg_DUMMY', 'Pos_6') , ('react_1.P_6_DUMMY', 'Pos_7') , ('react_2.T_r_DUMMY', 'Pos_2')])

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
                model.plot_CPDAG(str(len(itr_comb)), fges_obj, True)


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
            node_tiers['out'] = ['react_1/v_7.T_cyc', 'v_7/prod_stack.X_co', 'react_1/v_7.F_sg', 'v_7/prod_stack.X_co2', 'react_1/v_2.F_rgc', 'Pos_7', 'Pos_2']
            node_tiers['unit'] = ['react_1.T_reg', 'react_1.L_sp', 'react_1.P_6']
            node_tiers['in'] = ['comp_1/v_6.F_7', 'react_2/v_3.F_sc', 'Pos_6', 'Pos_3']
            
            node_tiers_names = ['out', 'unit', 'in']
            for itr_tier in range(len(node_tiers_names)-1):

                curr_tier = node_tiers_names[itr_tier]
                next_tiers = node_tiers_names[itr_tier+1:]
                for itr_next_tier in next_tiers:
                    
                    for itr_tier_node in node_tiers[curr_tier]:

                        model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[itr_next_tier] if (itr_tier_node, next_tier_node) not in exclude_list])

            




    def forbid_diff_streams(model, activate):

        if activate:            
            
            model.forbid_edges.extend([('comp_1/v_6.F_7', 'react_2/v_3.F_sc') , ('react_2/v_3.F_sc', 'comp_1/v_6.F_7') , ('Pos_6', 'react_2/v_3.F_sc') , 
                                       ('Pos_3', 'comp_1/v_6.F_7') , ('Pos_7', 'react_1/v_2.F_rgc') , ('Pos_2', 'react_1/v_7.F_sg') , ('Pos_2', 'react_1/v_7.T_cyc') , 
                                       ('Pos_2', 'v_7/prod_stack.X_co') , ('Pos_2', 'v_7/prod_stack.X_co2') ,
                                       ('react_1/v_7.T_cyc','react_1/v_2.F_rgc') , ('v_7/prod_stack.X_co','react_1/v_2.F_rgc') , 
                                       ('v_7/prod_stack.X_co2', 'react_1/v_2.F_rgc') , ('react_1/v_7.F_sg', 'react_1/v_2.F_rgc') , ('react_1/v_2.F_rgc', 'react_1/v_7.T_cyc') , 
                                       ('react_1/v_2.F_rgc', 'v_7/prod_stack.X_co') , ('react_1/v_2.F_rgc', 'v_7/prod_stack.X_co2') , ('react_1/v_2.F_rgc', 'react_1/v_7.F_sg')])
            


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

        

