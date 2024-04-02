
from tools import tools
import re

class model_react:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.config = graph.configuration[unit] 
        model.adj_mat = graph.adj_mat

    
    def model_ctrl(model):

        model.all_sensors = ['T_unit', 'P_unit', 'L_unit']
        model.latent_struct = []
        model.detect_jacket()
        model.inlet_streams()
        model.single_phase_inlet()
        model.outlet_streams()
        model.single_phase_outlet()
        
        model.present_sensors = []
        model.sensor_name_mapping = {}
        model.get_in_sensors()
        model.get_out_sensors()
        model.get_unit_sensors()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)
        
        
    def detect_jacket(model):

        if model.config['utility streams']:

            model.utility_streams = model.config['utility streams']
            model.all_sensors.extend(['T_uin', 'P_uin', 'F_uin', 'T_uout', 'P_uout', 'F_uout'])
            model.latent_struct.extend([('F_uin', 'F_uout') , ('P_uin', 'P_uout') , ('F_uin', 'T_unit') , ('T_uin', 'T_unit') , ('T_unit', 'T_uout') , ('T_uout', 'P_uout')])

        else:
            model.utility_streams = []


    def inlet_streams(model):

        inlet_stream_source = model.adj_mat.index[model.adj_mat[model.unit_name] == 1]
        model.inlet_streams = []
        model.in_phases = [] 
        for itr_stream_num, itr_source_unit in enumerate(inlet_stream_source):

            curr_inlet_stream = f'{itr_source_unit}/{model.unit_name}'
            if curr_inlet_stream not in model.utility_streams:

                T_sens = 'T_in'+str(itr_stream_num)
                P_sens = 'P_in'+str(itr_stream_num)
                F_sens = 'F_in'+str(itr_stream_num)
                model.all_sensors.extend([T_sens, P_sens, F_sens])

                model.latent_struct.append((F_sens, 'T_unit'))

                model.inlet_streams.append(curr_inlet_stream)
                curr_in_phase = model.config['stream phases'][curr_inlet_stream]
                model.in_phases.append(curr_in_phase)

                if curr_in_phase == 'gas':

                    model.latent_struct.extend([(T_sens, 'T_unit') , (P_sens, 'P_unit') , (F_sens, 'P_unit')])

                elif curr_in_phase == 'liq' or curr_in_phase == 'sol' or curr_in_phase == 'SL':

                    model.latent_struct.extend([(T_sens, 'T_unit') , (F_sens, 'L_unit')])

                elif curr_in_phase == 'GL' or curr_in_phase == 'GS':

                    model.latent_struct.extend([(T_sens, 'T_unit') , (P_sens, 'P_unit') , (F_sens, 'P_unit') , (F_sens, 'L_unit')])


    def single_phase_inlet(model):

        if not any(phase in model.in_phases for phase in ['gas', 'GL', 'GS']):

            for itr_stream_num in range(len(model.inlet_streams)):

                model.latent_struct.extend([('F_in'+str(itr_stream_num), 'P_unit') , ('P_in'+str(itr_stream_num), 'P_unit')])

        if all(phase == 'gas' for phase in model.in_phases):

            for itr_stream_num in range(len(model.inlet_streams)):

                model.latent_struct.append([('F_in'+str(itr_stream_num), 'L_unit')])
        

    def outlet_streams(model):

        outlet_stream_dest = model.adj_mat.columns[model.adj_mat.loc[model.unit_name] == 1]
        model.outlet_streams = []
        model.out_phases = []
        for itr_stream_num, itr_dest_unit in enumerate(outlet_stream_dest):

            curr_outlet_stream = f'{model.unit_name}/{itr_dest_unit}'
            if curr_outlet_stream not in model.utility_streams:

                T_sens = 'T_out'+str(itr_stream_num)
                P_sens = 'P_out'+str(itr_stream_num)
                F_sens = 'F_out'+str(itr_stream_num)
                model.all_sensors.extend([T_sens, P_sens, F_sens])

                model.outlet_streams.append(curr_outlet_stream)
                curr_out_phase = model.config['stream phases'][curr_outlet_stream]
                model.out_phases.append(curr_out_phase)
                if curr_out_phase == 'gas':

                    model.latent_struct.extend([('T_unit', T_sens) , ('P_unit', P_sens) , ('P_unit', F_sens)])

                elif curr_out_phase == 'liq' or curr_out_phase == 'sol' or curr_out_phase == 'SL' or curr_out_phase == 'GL' or curr_out_phase == 'GS':

                    model.latent_struct.extend([('T_unit', T_sens) , ('L_unit', P_sens) , ('L_unit', F_sens)])


    def single_phase_outlet(model):

        pass


    def get_in_sensors(model):

        inlet_sensors = model.unit_sensors['in streams']
        for itr_sens_tup in inlet_sensors:

            sensor_name = itr_sens_tup[0]
            source_unit = itr_sens_tup[1]

            match = re.search(r'.(T|F|P)_', sensor_name)
            match_X = re.search(r'.X_', sensor_name)
            if match:

                inlet_stream_name = f'{source_unit}/{model.unit_name}'
                if inlet_stream_name in model.utility_streams:

                    local_sensor = match.group(1) + '_uin'

                else:
                    stream_num = model.inlet_streams.index(inlet_stream_name)
                    local_sensor = match.group(1) + '_in' + str(stream_num)
                
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name

            elif match_X:

                inlet_stream_name = f'{source_unit}/{model.unit_name}'
                sens_id = sensor_name[match_X.span()[1]+1:]
                stream_num = model.inlet_streams.index(inlet_stream_name)
                X_sens = 'X_' + sens_id + 'In' + str(stream_num)
                model.all_sensors.append(X_sens)

                model.sensor_name_mapping[X_sens] = sensor_name
                model.present_sensors.append(X_sens)

                if model.config['reactants'][sensor_name]:

                    model.latent_struct.append((X_sens, 'T_unit'))


    def get_out_sensors(model):

        outlet_sensors = model.unit_sensors['out streams']
        for itr_sens_tup in outlet_sensors:

            sensor_name = itr_sens_tup[0]
            dest_unit = itr_sens_tup[1]

            match = re.search(r'.(T|F|P)_', sensor_name)
            match_X = re.search(r'.X_', sensor_name)
            if match:

                outlet_stream_name = f'{model.unit_name}/{dest_unit}'
                if outlet_stream_name in model.utility_streams:

                    local_sensor = match.group(1) + '_uout'

                else:
                    stream_num = model.outlet_streams.index(outlet_stream_name)
                    local_sensor = match.group(1) + '_out' + str(stream_num)

                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = sensor_name
                    
            elif match_X:

                outlet_stream_name = f'{model.unit_name}/{dest_unit}'
                sens_id = sensor_name[match_X.span()[1]+1:]
                stream_num = model.outlet_streams.index(outlet_stream_name)
                X_sens = 'X_' + sens_id + 'Out' + str(stream_num)
                model.all_sensors.append(X_sens)
                model.latent_struct.extend([('T_unit', X_sens) , ('P_unit', X_sens)])

                model.present_sensors.append(X_sens)
                model.sensor_name_mapping[X_sens] = sensor_name


    def get_unit_sensors(model):

        unit_sensors = model.unit_sensors['unit']
        for itr_sensor in unit_sensors:

            match = re.search(r'.(T|L|P)_', itr_sensor)
            if match:

                local_sensor = match.group(1) + '_unit'
                model.present_sensors.append(local_sensor)
                model.sensor_name_mapping[local_sensor] = itr_sensor
