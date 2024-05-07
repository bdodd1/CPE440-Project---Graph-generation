import numpy as np
import pandas as pd
from tools import tools
import matplotlib.pyplot as plt


# source_node = np.array([0]+[2*x**2 + 4*x + 10 for x in range(500)])
# dest_node = np.array([0]+[2*(x-1)**2 + 4*(x-1) + 10 for x in range(500)])
# source_node = np.array([0,1,1,1,1,0,0,0,0,1,1,1,1,1,1])
# dest_node = np.array([0,0,1,1,1,1,0,0,0,0,1,1,1,1,1])
# print(te.te_compute(source_node, dest_node, safetyCheck=True))
# print(pyinform.transfer_entropy(source_node, dest_node, k=1))


# xs = [0,1,1,1,1,0,0,0,0,1,1,1,1,1,1]
# ys = [0,0,1,1,1,1,0,0,0,0,1,1,1,1,1]
# print(pyinform.transfer_entropy(xs, ys, k=2))





# files = ['furn_test_0',
#          'furn_test_1',
#          'furn_test_2',
#          'furn_test_3',
#          'furn_test_4',
#          'furn_test_5',
#          'furn_test_6',
#          'furn_test_7',
#          'furn_test_8']
# location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\furn test fges 1,2 best dags'

# tools.compare_graphs(files, location)










# files = [#'react1_test_0',
#          'react1_test_1',
#          'react1_test_2',
#          'react1_test_3',
#          'react1_test_4',
#          'react1_test_5',
#          'react1_test_6',
#          'react1_test_7',
#          'react1_test_8']

# path1 = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\react1 test fges 1,3 forbid backwards'
# path2 = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\react1 test fges 1,3 no forbid'

# tools.compare_parallel_graphs(files, files, path1, path2)




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


from ground_truth import ground_truth
truth_graph_obj = ground_truth()
truth_graph_obj.ctrl(False, False)
truth_graph = {'nodes' : truth_graph_obj.nodes,
               'edges' : truth_graph_obj.edges}


from analyse_graphs import analyse_graphs





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
data = pd.read_csv(rf'C:\Users\fcb19bd\Documents\CPE440-Project---Graph-generation-main\Data\{data_files[file_ind]}')
# additional_vars = ['Time', 'T_atm', 'deltaP', 'Fair', 'T_cyc-T_reg', 'FV11']
# data = data.drop(columns = additional_vars)

# pd.plotting.scatter_matrix(data, figsize=(10, 10))
# plt.show()






# from test_furn import test_furn_models

# model = test_furn_models(data, var_mapping)
# model.model_ctrl()

# from test_furn_sections import test_furn_models

# model = test_furn_models(data, var_mapping)
# model.model_ctrl()




# from test_distil import test_distil_models

# model = test_distil_models(data, var_mapping)
# model.model_ctrl()

# from test_distil_sections import test_distil_models

# model = test_distil_models(data, var_mapping)
# model.model_ctrl()




# from test_react1 import test_react1_models

# model = test_react1_models(data, var_mapping)
# model.model_ctrl()

# from test_react1_sections import test_react1_models

# model = test_react1_models(data, var_mapping)
# model.model_ctrl()





# from test_react2 import test_react2_models

# model = test_react2_models(data, var_mapping)
# model.model_ctrl()

# from test_react2_sections import test_react2_models

# model = test_react2_models(data, var_mapping)
# model.model_ctrl()





# from test_cab import test_cab_models

# model = test_cab_models(data, var_mapping)
# model.model_ctrl()

# from test_cab_sections import test_cab_models

# model = test_cab_models(data, var_mapping)
# model.model_ctrl()




# from test_wgc import test_wgc_models

# model = test_wgc_models(data, var_mapping)
# model.model_ctrl()

from test_wgc_sections import test_wgc_models

model = test_wgc_models(data, var_mapping)
model.model_ctrl()