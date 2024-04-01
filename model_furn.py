
from tools import tools
import re

class model_furn:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.configuration = graph.configuration[unit] 

    
    def model_ctrl(model):

        model.hardcode_struct()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        
        model.present_sensors = []
        model.sensor_name_mapping = {}
        model.get_in_sensors()
        model.get_out_sensors()
        model.get_unit_sensors()

        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)


    def hardcode_struct(model):

        model.all_sensors = ['T_air', 'P_air', 'F_air', 'T_fuel', 'P_fuel', 'F_fuel', 'T_stack', 'P_stack', 'F_stack', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
        model.latent_struct = [('T_air', 'T_unit') , ('P_air', 'P_unit') , ('F_air', 'T_unit') , ('F_air', 'P_unit') , ('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_stack') , 
                        ('P_unit', 'P_stack') , ('P_unit', 'F_stack') , ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]
        

    def get_in_sensors(model):

        config = model.configuration
        inlet_sensors = model.unit_sensors['in streams']
        for itr_sens_tup in inlet_sensors:

            sensor_name = itr_sens_tup[0]
            source_unit = itr_sens_tup[1]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                inlet_stream = f'{source_unit}/{model.unit_name}'
                if inlet_stream in config['process streams']:

                    local_sensor = match.group(1) + '_in'
                
                elif inlet_stream == config['fuel stream']:

                    local_sensor = match.group(1) + '_fuel'

                else:
                    local_sensor = match.group(1) + '_air'

                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name


    def get_out_sensors(model):

        config = model.configuration
        outlet_sensors = model.unit_sensors['out streams']
        for itr_sens_tup in outlet_sensors:

            sensor_name = itr_sens_tup[0]
            dest_unit = itr_sens_tup[1]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                outlet_stream = f'{model.unit_name}/{dest_unit}'
                if outlet_stream in config['process streams']:

                    local_sensor = match.group(1) + '_out'
                
                else:
                    local_sensor = match.group(1) + '_stack'

 
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name


    def get_unit_sensors(model):

        unit_sensors = model.unit_sensors['unit']
        for itr_sensor in unit_sensors:

            match = re.search(r'.(T|P)_', itr_sensor)
            if match:

                local_sensor = match.group(1) + '_unit'
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = itr_sensor