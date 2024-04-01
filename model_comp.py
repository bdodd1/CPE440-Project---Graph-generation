from tools import tools 
import re

class model_comp:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.configuration = graph.configuration[unit]


    def model_ctrl(model):

        model.hardcode_struct()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        
        model.present_sensors = []
        model.sensor_name_mapping = {}
        model.get_in_out_sensors('in')
        model.get_in_out_sensors('out')
        model.get_unit_sensors()

        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)


    def hardcode_struct(model):

        model.all_sensors = ['T_in', 'T_out', 'F_in', 'F_out', 'P_in', 'P_out', 'X_in', 'X_out', 'W']
        model.latent_struct = [('T_in', 'T_out') , ('P_in', 'W') , ('W', 'P_out') , ('P_out', 'W') , ('P_out', 'T_out') , ('F_in', 'F_out')]


    def get_in_out_sensors(model, stream):

        sensors = model.unit_sensors[stream + ' streams']
        for itr_sens_tup in sensors:

            sensor_name = itr_sens_tup[0]
            match = re.search(r'.(T|F|P)_', sensor_name)
            if match:

                local_sensor = match.group(1) + '_' + stream
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name

    
    def get_unit_sensors(model):

        if model.configuration['duty var']:

            model.present_sensors.append('W')
            model.sensor_name_mapping['W'] = model.configuration['duty var']