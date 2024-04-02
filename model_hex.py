
from tools import tools
import re

class model_hex:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.config = graph.configuration[unit] 

    
    def model_ctrl(model):

        model.hardcode_struct()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        
        model.present_sensors = []
        model.sensor_name_mapping = {}
        model.get_in_sensors()
        model.get_out_sensors()

        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)


    def hardcode_struct(model):

        model.all_sensors = ['T_uin', 'P_uin', 'F_uin', 'X_uin', 'T_uout', 'P_uout', 'F_uout', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out']
        model.latent_struct = [('T_in', 'T_out') , ('T_in', 'T_uout') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('F_in', 'T_uout') , ('T_uin', 'T_uout') , ('T_uin', 'T_out') , ('P_uin', 'P_uout') , 
                         ('F_uin', 'F_uout') , ('F_uin', 'T_uout') , ('F_uin', 'T_out') , ('T_out', 'P_out') , ('T_uout', 'P_uout') , ('X_uin', 'X_uout') , ('X_in', 'X_out')]
        

    def get_in_sensors(model):

        inlet_sensors = model.unit_sensors['in streams']
        for itr_sens_tup in inlet_sensors:

            sensor_name = itr_sens_tup[0]
            source_unit = itr_sens_tup[1]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                inlet_stream = f'{source_unit}/{model.unit_name}'
                if inlet_stream in model.config['process streams']:

                    local_sensor = match.group(1) + '_in'

                else:
                    local_sensor = match.group(1) + '_uin'
                
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name


    def get_out_sensors(model):

        outlet_sensors = model.unit_sensors['out streams']
        for itr_sens_tup in outlet_sensors:

            sensor_name = itr_sens_tup[0]
            dest_unit = itr_sens_tup[1]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                outlet_stream = f'{model.unit_name}/{dest_unit}'
                if outlet_stream in model.config['process streams']:

                    local_sensor = match.group(1) + '_out'

                else:
                    local_sensor = match.group(1) + '_uout'

                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name

