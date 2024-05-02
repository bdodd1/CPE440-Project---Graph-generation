from itertools import combinations
import random
from tools import tools


import pandas as pd
import pydot as py


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
                'react2_1/prod_slurry.F_slurry' : 'F_Slurry',
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
data = pd.read_csv(rf'C:\Users\fcb19bd\Documents\CPE440-Project---Graph-generation-main\Data\{data_files[file_ind]}')
# additional_vars = ['Time', 'T_atm', 'deltaP', 'Fair', 'T_cyc-T_reg', 'FV11']
# data = data.drop(columns = additional_vars)



nodes = ['P2', 'F7', 'V6', 'F_sc', 'L_sp', 'T_reg', 'P6', 'V3']
dummy_nodes_struct = []
graph = {'nodes' : nodes,
'dummy vars' : [],
'edges' : [],
'forbidden' : []}


data = data[nodes]

from test_run_fges import run_fges
obj = run_fges(graph, data, 'hi')
obj.run_fges_ctrl()
data_dag = obj.best_dag

adj_mat = tools.build_adj_mat(nodes, data_dag)
data_dag_v = []
for itr_node in nodes:

    parents = adj_mat.loc[adj_mat[itr_node] == 1].index.to_list()
    v_pairs = combinations(parents, 2)
    for itr_v in v_pairs:

        data_dag_v.append([itr_v[0] , itr_node, itr_v[1]])



for _ in range(20):

    num_entries = random.randint(1, len(data_dag)-1)  # Random number of entries
    random_entries = random.sample(data_dag, num_entries)
    graph = {'nodes' : nodes,
    'dummy vars' : [],
    'edges' : random_entries,
    'forbidden' : []}
    obj = run_fges(graph, data, 'hi')
    obj.run_fges_ctrl()
    random_dag = obj.best_dag

    for 



    match_edges = []
    for itr_edge in random_dag:

        if itr_edge in data_dag:

            match_edges.append(True)

        else:

            match_edges.append(False)


    if len(random_dag) == len(data_dag) and all(match_edges):

        print('Converged')
        print(random_entries)

    else:

        print('***********')
        print(random_entries)
        print('***********')




