import pyinform
import numpy as np
import pandas as pd
from tools import tools


# source_node = np.array([0]+[2*x**2 + 4*x + 10 for x in range(50)])
# dest_node = np.array([0]+[2*(x-1)**2 + 4*(x-1) + 10 for x in range(50)])
# # print(max(source_node))
# print(pyinform.transfer_entropy(source_node, dest_node, k=1))


# xs = [0,1,1,1,1,0,0,0,0,1,1,1,1,1,1]
# ys = [0,0,1,1,1,1,0,0,0,0,1,1,1,1,1]
# print(pyinform.transfer_entropy(xs, ys, k=2))





# files = ['fisherz_cycles_graph1_varyflow',
#          'fisherz_cycles_graph1_varyflow_2']
# location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs'

# from tools import tools
# tools.compare_graphs(files, location)







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
file_ind = 2
data = pd.read_csv(rf'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Data\{data_files[file_ind]}')
additional_vars = ['Time', 'T_atm', 'deltaP', 'Fair', 'T_cyc-T_reg', 'FV11']
data = data.drop(columns = additional_vars)

from test_furn import test_furn_models

model = test_furn_models(data, var_mapping)
model.model_ctrl()


# location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\fisherz_alldata_varyflow.xlsx'
# graph = {}
# graph['nodes'] , graph['edges'] = tools.read_graph_excel(location)
# from run_BIC import run_BIC
# bic = run_BIC(graph, data, var_mapping)
# bic.calc_BIC()

