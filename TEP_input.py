import networkx as nx
import re
import matplotlib.pyplot as plt
import pandas as pd




# Topology neglected 



topology = {}


topology['pipes'] = [('feed_A', 'v_1') , ('v_1', 'mix_react1') , ('mix_react1', 'mix_react2') , ('feed_D', 'v_2') , ('v_2', 'mix_react2') , ('mix_react2', 'mix_react3') , ('feed_E', 'v_3') , 
                     ('v_3', 'mix_react3') , ('mix_react3', 'react_1') , ('feed_coolreact', 'react_1') , ('react_1', 'v_12') , ('v_12', 'prod_coolreact') , ('react_1', 'hex_1') , 
                     ('hex_1', 'flash_1') , ('feed_coolhex', 'hex_1') , ('hex_1', 'v_13') , ('v_13', 'prod_coolhex') , ('flash_1', 'split_flashgas') , ('split_flashgas', 'v_9') , ('v_9', 'prod_purge') , 
                     ('split_flashgas', 'mix_comp') , ('mix_comp', 'comp_1') , ('comp_1', 'split_comp') , ('split_1', 'v_comp') , ('v_comp', 'mix_comp') , ('split_comp', 'mix_recyc') , 
                     ('mix_recyc', 'mix_react1') , ('flash_1', 'v_10') , ('v_10', 'str_1') , ('str_1', 'mix_recyc') , ('feed_C', 'v_4') , ('v_4', 'str_1') , ('str_1', 'split_botliq') , 
                     ('split_botliq', 'hex_reboil') , ('hex_reboil', 'str_1') , ('feed_steam', 'v_steam') , ('v_steam', 'hex_reboil') , ('hex_reboil', 'prod_steam') , ('split_botliq', 'v_11') , 
                     ('v_11', 'prod_product')]

# Missed J sensor on comp
topology['sensors'] = ['feed_A/v_1.F_Afeed', 'feed_D/v_2.F_Dfeed', 'feed_E/v_3.F_Efeed', 'feed_C/v_4.F_Cfeed', 'mix_react3/react_1.X_A', 'mix_react3/react_1.X_B', 'mix_react3/react_1.X_C',
                       'mix_react3/react_1.X_D', 'mix_react3/react_1.X_E', 'mix_react3/react_1.X_F', 'mix_react3/react_1.F_react1', 'react_1.L_react1', 'react_1.T_react1', 'react_1/hex_1.P_react1',
                       'react_1/v_12.T_coolreact', 'split_comp/mix_recyc.F_recyc', 'hex_1/v_13.T_coolhex', 'split_flashgas'
                       
                       ]

topology['control_loops'] = 



# Need to handle default values 
configuration = {'furn_1' : 
                    {'process streams' : ['feed_feedstream/furn_1', 'furn_1/react_2'],
                    'fuel stream' : 'feed_fuel/v_1'}, 
                'comp_1' :
                    {'duty var' : 'ACAB'},
                'comp_2' : 
                    {'duty var' : 'AWGC'} 
                }

# hex: process streams



from Library import unit_lib

graph = unit_lib(topology, data, configuration)
# graph.classify_units()
# graph.build_adj_mat()
# graph.get_unit_sensors()
# graph.model_comp()

graph.build_graph()









