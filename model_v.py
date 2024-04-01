
from tools import tools
import re

class model_v:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]

    
    def model_ctrl(model):

        model.hardcode_struct()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        
        model.present_sensors = ['Pos']
        model.sensor_name_mapping = {'Pos' : f'Pos_{model.unit_name[2:]}'}
        model.get_in_out_sensors('in')
        model.get_in_out_sensors('out')

        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)


    def hardcode_struct(model):

        model.all_sensors = ['T_in', 'T_out', 'F_in', 'F_out', 'P_in', 'P_out', 'X_in', 'X_out', 'Pos']
        model.latent_struct = [('P_in', 'P_out') , ('Pos', 'P_out') , ('Pos', 'P_in') , ('P_in', 'T_in') , ('P_out', 'T_out') , ('T_in', 'T_out') , ('P_in', 'F_in') , ('P_out', 'F_out') ,
                         ('F_in', 'F_out') , ('X_in', 'X_out')]
        

    def get_in_out_sensors(model, stream):

        sensors = model.unit_sensors[stream + ' streams']
        for itr_sens_tup in sensors:

            sensor_name = itr_sens_tup[0]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                local_sensor = match.group(1) + '_' + stream
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name