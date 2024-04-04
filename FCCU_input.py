import networkx as nx
import re
import matplotlib.pyplot as plt
import pandas as pd





# Topology neglected 
# - v5 as it is not involved in any control loop and has no sensors around it 


topology = {}


topology['pipes'] = [('feed_air','comp_1') , ('comp_1','v_6') , ('v_6','react_1') , ('react_1','v_7') , ('v_7','prod_stack') , ('react_1','v_2') ,
                     ('v_2','react_2') , ('react_2','v_3') , ('v_3','react_1') , ('feed_feedstream','furn_1') , ('feed_fuel','v_1') , ('v_1','furn_1'), ('feed_airin', 'furn_1') , 
                     ('furn_1','react_2') , ('furn_1', 'prod_furnstack') , ('react_2','distil_1') , ('distil_1','prod_slurry') , ('distil_1','hex_1') , ('hex_1','distil_1') , ('feed_uthex1', 'hex_1') , 
                     ('hex_1', 'prod_uthex1') , ('distil_1','v_11') , ('v_11','prod_lightoil') , ('distil_1','v_10') , ('v_10','prod_heavynaptha') , ('distil_1','hex_2') , 
                     ('hex_2','flash_1') , ('feed_uthex2', 'hex_1') , ('hex_1', 'prod_uthex2') , ('flash_1','split_liq') , ('split_liq', 'v_8') , ('v_8','distil_1') , ('split_liq','v_9') , 
                     ('v_9','prod_lightnaptha') , ('flash_1','split_gas') , ('split_gas', 'v_4') , ('v_4','comp_2') , ('comp_2','prod_lpg') , ('split_gas','prod_flare')]

topology['sensors'] = ['feed_air/comp_1.P_1', 'comp_1/v_6.F_7', 'comp_1/v_6.P_2', 'react_1.T_reg', 'react_1.L_sp', 'react_1.P_6', 'react_1/v_7.F_sg', 
                       'react_1/v_7.T_cyc', 'v_7/prod_stack.X_co', 'v_7/prod_stack.X_co2', 'react_1/v_2.F_rgc', 'react_2.T_r', 'react_2.P_4', 
                       'react_2/v_3.F_sc' , 'feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5', 'furn_1.T_3', 'furn_1/react_2.T_2', 
                       'distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 
                       'v_9/prod_lightnaptha.F_ln', 'v_8/distil_1.F_reflux', 'comp_2/prod_lpg.F_lpg', 'distil_1/prod_slurry.F_slurry']

topology['control_loops'] = {'v_6' : ['react_1.T_reg'] , 'v_1' : ['furn_1/react_2.T_2'] , 'v_3' : [('L', 'react_1')] , 'v_2' : ['react_2.T_r'] , 'v_7' : ['react_1.P_6'] , 'v_4' : ['distil_1.P_5'] , 
                             'v_9' : [('L', 'flash_1')] , 'v_8' : ['distil_1.T_fra'] , 'v_10' : ('T', 'distill_1') , 'v_11' : ('T', 'distill_1')}


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



# Need to handle default values 
configuration = {
                'furn_1' : 
                    {'process streams' : ['feed_feedstream/furn_1', 'furn_1/react_2'],
                     'fuel stream' : 'v_1/furn_1'}, 
                'comp_1' :
                    {'duty var' : 'ACAB'},
                'comp_2' : 
                    {'duty var' : 'AWGC'},
                'react_1' :
                    {'stream phases' : 
                        {'v_6/react_1' : 'gas',
                         'v_3/react_1' : 'sol',
                         'react_1/v_7' : 'gas',
                         'react_1/v_2' : 'sol'},
                     'utility streams' : None,
                     'reactants' : None},
                'react_2' :
                    {'stream phases' : 
                        {'furn_1/react_2' : 'gas',
                         'v_2/react_2' : 'sol',
                         'react_2/distil_1' : 'gas',
                         'react_2/v_3' : 'sol'},
                     'utility streams' : None,
                     'reactants' : None}, 
                'flash_1' :
                    {'gas stream' : 'flash_1/split_gas'},
                'distil_1' :
                    {'stream locations' :
                        {'react_2/distil_1' : 20,
                         'v_8/distil_1' : 0,
                         'hex_1/distil_1' : 20,
                         'distil_1/hex_2' : 0,
                         'distil_1/hex_1' : 20,
                         'distil_1/prod_slurry' : 20,
                         'distil_1/v_11' : 17,
                         'distil_1/v_10' : 8},
                     'stream tags' :
                        {'react_2/distil_1' : 'feed',
                         'v_8/distil_1' : 'reflux',
                         'hex_1/distil_1' : 'reboil',
                         'distil_1/hex_2' : 'top',
                         'distil_1/hex_1' : 'bot',
                         'distil_1/prod_slurry' : 'prod',
                         'distil_1/v_11' : 'prod',
                         'distil_1/v_10' : 'prod'},
                     'sensor locations' : 
                        {'distil_1.T_fra' : 0,
                         'distil_1.T_10' : 10,
                         'distil_1.T_20' : 20,
                         'distil_1.P_5' : 0}},
                'hex_1' :
                    {'process streams' : ['distil_1/hex_1', 'hex_1/distil_1']},
                'hex_2' :
                    {'process streams' : ['distil_1/hex_2', 'distil_1/flash_1']}
                }




from graph_builder_class import graph_builder_class

graph = graph_builder_class(data, topology, configuration, var_mapping)
graph.build_graph()

