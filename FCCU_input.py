import networkx as nx
import re
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('NOC_stableFeedFlow_outputs.csv')

### 2 HEX at fractionator probs need including ###
topology = {}

# Try to eliminate these. Unecassarily complicated for user 
topology['units'] = ['comp_1', 'react_1', 'react_2', 'hex_1', 'v_1', 'v_2', 'v_3', 'v_6', 'v_7', 'distil_1', 'v_11', 'v_10', 'v_8', 'v_9', 'v_4', 'v_5', 'flash_1', 'comp_2']

topology['streams'] = ['air', 'stackgas', 'feed', 'fuel', 'slurry', 'lightoil', 'heavynaptha', 'lightnaptha', 'lpg', 'flare']                

topology['sensors'] = ['P_1', 'F_7', 'P_2', 'T_reg', 'L_sp', 'F_sg', 'T_cyc', 'C_co', 'C_o2', 'P_6', 'F_rgc', 'F_sc', 'T_r', 'P_4', 'F_5', 'F_3', 
                'T_1', 'T_2', 'T_3', 'T_20', 'T_10', 'F_lco', 'F_hn', 'F_reflux', 'P_5', 'T_fra', 'F_ln', 'F_lpg']

topology['controllers'] = ['T_C1', 'T_C2', 'T_C3', 'L_C1', 'P_C1', 'T_C6', 'T_C5', 'T_C4', 'P_C2', 'L_C2']
##


topology['pipes'] = [
                    ('air','comp_1') , ('comp_1','v_6') , ('v_6','react_1') , ('react_1','v_7') , ('v_7','stackgas') , ('react_1','v_2') ,
                    ('v_2','react_2') , ('react_2','v_3') , ('v_3','react_1') , ('feed','hex_1') , ('fuel','v_1') , ('v_1','hex_1') , 
                    ('hex_1','react_2') , ('react_2','distil_1') , ('distil_1','slurry') , ('distil_1','v_11') , ('v_11','lightoil') , ('distil_1','v_10') , ('v_10','heavynaptha') , 
                    ('distil_1','flash_1') , ('flash_1','v_8') , ('v_8','distil_1') , ('flash_1','v_9') , ('v_9','lightnaptha') , ('flash_1','v_4') , ('v_4','comp_2') , ('comp_2','lpg') , 
                    ('flash_1','v_5') , ('v_5','flare')]

topology['control_loops'] = []

# Finishing putting this in
topology['sensor_location'] = {'air/comp_1' : ['P_1'] , 'comp_1/react_1': ['F_7', 'P_2'] , 'react_1' : ['T_reg', 'L_sp', 'P_6'] , 'react_1/v_7' : ['F_sg', 'T_cyc'] , 'v_7/stackgas' : ['C_co', 'C_co2'] ,
                          'react_1/v_2' : ['F_rgc'] , 'react_2' : ['T_r', 'P_4'] , 'react_2/v_3' : ['F_sc'] , }



from Library import unit_lib

graph = unit_lib(topology, data)
graph.get_unit_sensors()


A=1










