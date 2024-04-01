
from tools import tools
import re

class model_flash:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.configuration = graph.configuration[unit] 

    
    def model_ctrl(model):

        model.hardcode_struct()
        
        model.present_sensors = []
        model.sensor_name_mapping = {}
        model.get_in_sensors()
        model.get_out_sensors()
        model.get_unit_sensors()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)
        
        
    def hardcode_struct(model):

        model.all_sensors = ['T_in', 'P_in', 'F_in', 'T_unit', 'P_unit', 'L_unit', 'T_gas', 'P_gas', 'F_gas', 'T_liq', 'P_liq', 'F_liq']
        model.latent_struct = [('F_in', 'P_unit') , ('F_in', 'L_unit') , ('T_in', 'T_unit') , ('P_in', 'P_unit') , ('T_unit', 'L_unit') , ('P_unit', 'L_unit') , ('T_unit', 'T_gas') , ('T_unit', 'T_liq') , 
                               ('P_unit', 'P_gas') , ('P_unit', 'F_gas') , ('L_unit', 'F_liq') , ('L_unit', 'P_liq')]
        

    def get_in_sensors(model):

        inlet_sensors = model.unit_sensors['in streams']
        for itr_sens_tup in inlet_sensors:

            sensor_name = itr_sens_tup[0]

            # Get inlet sensors 
            match = re.search(r'.(T|F|P)_', sensor_name)
            match_X = re.search(r'.X_', sensor_name)
            if match:

                local_sensor = match.group(1) + '_in'
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name
            
            elif match_X:

                sens_id = sensor_name[match_X.span()[1]+1:]
                X_sens = 'X_' + sens_id + 'In'
                model.all_sensors.append(X_sens)
                model.latent_struct.extend([(X_sens, 'P_unit') , (X_sens, 'L_unit')])

                model.present_sensors.append(X_sens)
                model.sensor_name_mapping[X_sens] = sensor_name


    def get_out_sensors(model):

        outlet_sensors = model.unit_sensors['out streams']
        for itr_sens_tup in outlet_sensors:

            sensor_name = itr_sens_tup[0]
            dest_unit = itr_sens_tup[1]

            # Get outlet sensors 
            match = re.search(r'.(T|F|P)_', sensor_name)
            match_X = re.search(r'.X_', sensor_name)
            if match:

                outlet_stream = f'{model.unit_name}/{dest_unit}'
                if outlet_stream == model.configuration['gas stream']:

                    local_sensor = match.group(1) + '_gas'
                
                else:
                    local_sensor = match.group(1) + '_liq'

                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name

            elif match_X:

                outlet_stream_name = f'{model.unit_name}/{dest_unit}'
                sens_id = sensor_name[match_X.span()[1]+1:]
                if outlet_stream_name == model.configuration['gas stream']:

                    X_sens = 'X_' + sens_id + 'Gas'

                else:

                    X_sens = 'X_' + sens_id + 'Liq'

                model.all_sensors.append(X_sens)
                model.latent_struct.extend([('P_unit', X_sens) , (X_sens, 'L_unit')])

                model.present_sensors.append(X_sens)
                model.sensor_name_mapping[X_sens] = sensor_name


    def get_unit_sensors(model):

        unit_sensors = model.unit_sensors['unit']
        for itr_sensor in unit_sensors:

            match = re.search(r'.(T|P|L)_', itr_sensor)
            if match:

                local_sensor = match.group(1) + '_unit'
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = itr_sensor