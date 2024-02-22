import networkx as nx
import re
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('NOC_stableFeedFlow_outputs.csv')

### 2 HEX at fractionator probs need including ###
topology = {}


topology['pipes'] = [('feed_air','comp_1') , ('comp_1','v_6') , ('v_6','react_1') , ('react_1','v_7') , ('v_7','prod_stack') , ('react_1','v_2') ,
                     ('v_2','react_2') , ('react_2','v_3') , ('v_3','react_1') , ('feed_feedstream','hex_1') , ('feed_fuel','v_1') , ('v_1','hex_1') , ('hex_1', 'prod_hex1gas') ,
                     ('hex_1','react_2') , ('react_2','distil_1') , ('distil_1','prod_slurry') , ('distil_1','v_11') , ('v_11','prod_lightoil') , ('distil_1','v_10') , 
                     ('v_10','prod_heavynaptha') , ('distil_1','flash_1') , ('flash_1','v_8') , ('v_8','distil_1') , ('flash_1','v_9') , ('v_9','prod_lightnaptha') , 
                     ('flash_1','v_4') , ('v_4','comp_2') , ('comp_2','prod_lpg') , ('flash_1','v_5') , ('v_5','prod_flare')]

topology['control_loops'] = {'T_C1' : ['hex_1/react_2.T_2', 'v_11'] , 'T_C2' : ['react_2.T_r', 'v_2'] , 'T_C3' : ['react_1.T_reg', 'v_6'] , 'L_C1' : ['react_2', 'v_3'] , 
                             'P_C1' : ['react_1.P_6', 'v_7'] , 'T_C6' : ['distil_1', 'v_11'] , 'T_C5' : ['distil_1', 'v_10'] , 'T_C4' : ['distil_1.T_fra', 'v_8'] , 
                             'P_C2' : ['distil_1.P_5', 'v_4'] , 'L_C2' : ['flash_1', 'v_9']}

topology['sensors'] = ['feed_air/comp_1.P_1', 'comp_1/v_6.F_7', 'comp_1/v_6.P_2', 'react_1.T_reg', 'react_1.L_sp', 'react_1.P_6' , 'react_1/v_7.F_sg', 
                       'react_1/v_7.T_cyc', 'v_7/prod_stack.C_co', 'v_7/prod_stack.C_co2', 'react_1/v_2.F_rgc', 'react_2.T_r', 'react_2.P_4', 
                       'react_2/v_3.F_sc' , 'feed_feedstream/hex_1.F_3', 'feed_feedstream/hex_1.T_1', 'feed_fuel/v_1.F_5', 'hex_1.T_3', 'hex_1/react_2.T_2', 
                       'distil_1.T_20', 'distil_1.T_10', 'distil_1.T_fra', 'distil_1.P_5', 'v_11/prod_lightoil.F_lco' , 'v_10/prod_heavynaptha.F_hn', 
                       'v_9/prod_lightnaptha.F_ln', 'v_8/distil_1.F_reflux', 'comp_2/prod_lpg.F_lpg']



from Library import unit_lib

graph = unit_lib(topology, data)
graph.classify_units()
graph.build_adj_mat()
graph.get_unit_sensors()
graph.model_comp()










