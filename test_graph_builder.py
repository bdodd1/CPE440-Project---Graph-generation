import pyinform
from PyIF import te_compute as te
import numpy as np
import pandas as pd
from tools import tools
import matplotlib.pyplot as plt
import networkx as nx
import re

import sys
import jpype.imports
jpype.startJVM(classpath=[r"C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\py-tetrad\pytetrad\resources\tetrad-current.jar"])
import edu.cmu.tetrad.search as ts
import edu.cmu.tetrad.data as td
import edu.cmu.tetrad.graph.GraphTransforms as gt
import edu.cmu.tetrad.algcomparison.score as score
from edu.cmu.tetrad.util import Params, Parameters
import edu.cmu.tetrad.graph as tg
import java.lang as lang


sys.path.insert(1, r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\py-tetrad\pytetrad\tools')
import translate as tr



class test_build_graph:


    def ctrl(graph_obj):


        # graph_obj.build_graph()
        # tools.print_to_excel(graph, r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\whole_graph.xlsx')

        graph_obj.graph = {}
        graph_obj.graph['nodes'], graph_obj.graph['edges'] = tools.read_graph_excel(r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\whole_graph.xlsx')

        graph_obj.adjust_dummys()
        graph_obj.handle_cycles()
        graph_obj.remove_variance()
        score = graph_obj.score_whole_dag()
        print(score)


    def build_graph(graph_obj):

        graph = {'nodes' : [],
                'edges' : []}


        inputs = graph_obj.set_inputs()
        from test_furn import test_furn_models

        model = test_furn_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.nodes)
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        inputs = graph_obj.set_inputs()
        from test_distil import test_distil_models

        model = test_distil_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.best_dags[model.unit_model_ind]['nodes'])
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        inputs = graph_obj.set_inputs()
        from test_react1 import test_react1_models

        model = test_react1_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.nodes)
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        inputs = graph_obj.set_inputs()
        from test_react2 import test_react2_models

        model = test_react2_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.nodes)
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        inputs = graph_obj.set_inputs()
        from test_cab import test_cab_models

        model = test_cab_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.best_dags[model.unit_model_ind]['nodes'])
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        inputs = graph_obj.set_inputs()
        from test_wgc import test_wgc_models

        model = test_wgc_models(inputs[0], inputs[1])
        model.model_ctrl()
        graph['nodes'].extend(model.nodes)
        graph['edges'].extend(model.best_dags[model.unit_model_ind]['all edges'])


        graph['nodes'].extend(['Pos_9', 'v_9/prod_lightnaptha.F_ln'])
        graph['edges'].append(('Pos_9', 'v_9/prod_lightnaptha.F_ln'))


        graph['nodes'] = list(set(graph['nodes']))
        graph['edges'] = list(set(graph['edges']))

        graph_obj.graph = graph


    def adjust_dummys(graph_obj):

        inputs = graph_obj.set_inputs()
        var_mapping = inputs[1]
        var_mapping['react_2.P_5_DUMMY'] = 'P5_DUMMY'
        var_mapping['react_2.T_r_DUMMY'] = 'T_r_DUMMY'
        var_mapping['feed_feedstream/furn_1.F_3_DUMMY'] = 'F3_DUMMY'
        var_mapping['distil_1.T_10_DUMMY'] = 'T_10_DUMMY'
        var_mapping['distil_1.T_fra_DUMMY'] = 'T_fra_DUMMY'
        var_mapping['react_1.T_reg_DUMMY'] = 'T_reg_DUMMY'
        var_mapping['react_1.P_6_DUMMY'] = 'P6_DUMMY'
        var_mapping['furn_1/react_2.T_2_DUMMY'] = 'T2_DUMMY'

        data = inputs[0]
        data['P5_DUMMY'] = data['P5']
        data['T_r_DUMMY'] = data['T_r']
        data['F3_DUMMY'] = data['F3']
        data['T_10_DUMMY'] = data['T_10']
        data['T_fra_DUMMY'] = data['T_fra']
        data['T_reg_DUMMY'] = data['T_reg']
        data['P6_DUMMY'] = data['P6']
        data['T2_DUMMY'] = data['T2']

        graph_obj.data = data
        graph_obj.var_mapping = var_mapping


    def handle_cycles(graph_obj):
    
        graph_obj.graph['edges'].remove(('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'))
        graph_obj.graph['edges'].remove(('react_1/v_2.F_rgc', 'react_2.T_r'))
        graph_obj.graph['edges'].append(('react_1/v_2.F_rgc', 'react_2/v_3.F_sc_DUMMYcyc'))
        graph_obj.graph['edges'].append(('react_1/v_2.F_rgc', 'react_2.T_r_DUMMYcyc'))

        graph_obj.graph['nodes'].extend(['react_2/v_3.F_sc_DUMMYcyc', 'react_2.T_r_DUMMYcyc'])
        graph_obj.var_mapping['react_2/v_3.F_sc_DUMMYcyc'] = 'F_sc_DUMMYcyc'
        graph_obj.var_mapping['react_2.T_r_DUMMYcyc'] = 'T_r_DUMMYcyc'
        graph_obj.data['F_sc_DUMMYcyc'] = graph_obj.data['F_sc']
        graph_obj.data['T_r_DUMMYcyc'] = graph_obj.data['T_r']
    
        from handle_cycles import handle_cycles
        cyc_obj = handle_cycles(graph_obj.graph, graph_obj.data, graph_obj.var_mapping)
        cyc_obj.handle_cycles_ctrl()



    def remove_variance(graph_obj):

        rev_var_mapping = {column: sensor for sensor, column in graph_obj.var_mapping.items()}
        column_to_drop = []
        for itr_col in graph_obj.data.columns:

            var_col = graph_obj.data[itr_col].var()
            if var_col < 0.00000001:

                column_to_drop.append(itr_col)

        graph_obj.data = graph_obj.data.drop(columns=column_to_drop)

        # dropped_sensors is all sensors, and drop_dummy_sensors is just dummy sensors
        graph_obj.dropped_sensors = [rev_var_mapping[column] for column in column_to_drop]

        graph_obj.trim_graph = {}
        graph_obj.trim_graph['nodes'] = [node for node in graph_obj.graph['nodes'] if node not in graph_obj.dropped_sensors]
        graph_obj.trim_graph['edges'] = [(source,dest) for source, dest in graph_obj.graph['edges'] if source not in graph_obj.dropped_sensors and dest not in graph_obj.dropped_sensors]


    def score_whole_dag(graph_obj):

        score = ts.score.MvpScore(tr.pandas_data_to_tetrad(graph_obj.data), 1, 3, True)
        test = ts.Fges(score)
        dag_obj = tg.Dag()
        node_obj_map = {}
        for itr_node in graph_obj.trim_graph['nodes']:

            string = lang.String(graph_obj.var_mapping[itr_node])
            node = tg.GraphNode(string)
            dag_obj.addNode(node)
            node_obj_map[itr_node] = node
        
        for itr_edge in graph_obj.trim_graph['edges']:

            dag_obj.addDirectedEdge(node_obj_map[itr_edge[0]], node_obj_map[itr_edge[1]])

        return test.scoreDag(dag_obj)


    def set_inputs(graph_obj):

        var_mapping = {
                        'feed_air/comp_1.P_1' : 'P1',
                        'comp_1/v_6.F_7' : 'F7',
                        'comp_1/v_6.P_2' : 'P2',
                        'react_1.T_reg' : 'T_reg',
                        'react_1.L_sp' : 'L_sp',
                        'react_1.P_6' : 'P6',
                        'react_1/v_7.F_sg' : 'F_sg',
                        'react_1/v_7.T_cyc' : 'T_cyc',
                        'v_7/prod_stack.X_co' : 'C_cosg',
                        'v_7/prod_stack.X_co2' : 'C_co2sg',
                        'react_1/v_2.F_rgc' : 'F_rgc',
                        'react_2.T_r' : 'T_r',
                        'react_2.P_4' : 'P4',
                        'react_2/v_3.F_sc' : 'F_sc',
                        'feed_feedstream/furn_1.F_3' : 'F3',
                        'feed_feedstream/furn_1.T_1' : 'T1',
                        'feed_fuel/v_1.F_5' : 'F5',
                        'furn_1.T_3' : 'T3',
                        'furn_1/react_2.T_2' : 'T2',
                        'distil_1.T_20' : 'T_20',
                        'distil_1.T_10' : 'T_10',
                        'distil_1.T_fra' : 'T_fra',
                        'distil_1.P_5' : 'P5',
                        'v_11/prod_lightoil.F_lco' : 'F_LCO',
                        'v_10/prod_heavynaptha.F_hn' : 'F_HN',
                        'v_9/prod_lightnaptha.F_ln' : 'F_LN',
                        'v_8/distil_1.F_reflux' : 'F_Reflux',
                        'comp_2/prod_lpg.F_lpg' : 'F_LPG',
                        'distil_1/prod_slurry.F_slurry' : 'F_Slurry',
                        'ACAB' : 'ACAB',
                        'AWGC' : 'AWGC',
                        'Pos_1' : 'V1',
                        'Pos_2' : 'V2',
                        'Pos_3' : 'V3',
                        'Pos_4' : 'V4',
                        'Pos_6' : 'V6',
                        'Pos_7' : 'V7',
                        'Pos_8' : 'V8',
                        'Pos_9' : 'V9',
                        'Pos_10' : 'V10',
                        'Pos_11' : 'V11',
                        }


        data_files = ['NOC_stableFeedFlow_outputs.csv',
                    'NOC_varyingFeedFlow_outputs.csv',
                    'CAB_valveLeak_outputs.csv',
                    'condEff_decrease_outputs.csv',
                    'deltaP_increase_outputs.csv',
                    'Fhn_sensorDrift_outputs.csv',
                    'UAf_decrease_outputs.csv']
        file_ind = 1
        data = pd.read_csv(rf'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Data\{data_files[file_ind]}')
        additional_vars = ['Time', 'T_atm', 'deltaP', 'Fair', 'T_cyc-T_reg', 'FV11']
        data = data.drop(columns = additional_vars)

        return data, var_mapping









    # vis_graph = nx.DiGraph()
    # plt.figure(figsize=[5, 5])
    # plt.title('Full graph')
    # vis_graph.add_nodes_from(graph['nodes'])
    # vis_graph.add_edges_from(graph['edges'])
    # pos = nx.spring_layout(vis_graph)
    # nx.draw_networkx_edges(vis_graph, pos, edgelist=graph['edges'], edge_color='black', width=2)
    # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph['nodes'])
    # nx.draw_networkx_labels(vis_graph, pos, font_color='blue')
    # plt.show()




obj = test_build_graph()
obj.ctrl()