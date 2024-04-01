
import re
import pandas as pd
from tools import tools


class parse_inputs:

    def __init__(inputs, graph):
        
        inputs.supported_units = graph.supported_units
        inputs.topology = graph.topology
        inputs.configuration = graph.configuration
        

    def parse_inputs_ctrl(inputs):
        
        inputs.classify_units()
        inputs.topology_adj_mat()
        inputs.get_unit_sensors()
    

    def classify_units(inputs):
        
        # Gets a list of units and feed/prod streams from the pipes input
        units_present = []
        streams_present = []
        stream_pattern = r'(feed|prod)_'
        for itr_pipes in inputs.topology['pipes']:

            source_unit = itr_pipes[0]
            if re.match(stream_pattern, source_unit):

                streams_present.append(source_unit)

            else: 
                units_present.append(source_unit)

            dest_unit = itr_pipes[1]
            if re.match(stream_pattern, dest_unit):

                streams_present.append(dest_unit)

            else: 
                units_present.append(dest_unit)

        units_present = list(set(units_present))
        streams_present = list(set(streams_present))
        inputs.topology['units'] = units_present
        inputs.topology['streams'] = streams_present


        # Builds regex from modelled unit list 
        units = {}
        pattern = '('
        for itr_unit in inputs.supported_units.values():

            units[itr_unit] = []
            pattern += f'{itr_unit}|'
    
        pattern = pattern[:-1] + ')_'
        pattern = rf'{pattern}'


        # Classifies units provided by topology into modelled categories 
        for itr_unit in inputs.topology['units']:

            match = re.match(pattern, itr_unit)
            if match:

                units[match.group(1)].append(itr_unit)
                
            else:

                raise ValueError(f'{itr_unit} is an incompatable unit.')

        inputs.units = units

        # print(units)
        # print('***')
        # print(streams_present)
            

    def topology_adj_mat(inputs):

        streams = inputs.topology['streams']
        units = inputs.topology['units']
        pipes = inputs.topology['pipes']

        adj_mat_ax = streams + units
        inputs.adj_mat = tools.build_adj_mat(adj_mat_ax, pipes)


    def get_unit_sensors(inputs):

        units = inputs.topology['units']
        streams = inputs.topology['streams']
        sensors = inputs.topology['sensors']

        # Create unit sensor store 
        unit_sensors = {}
        for itr_unit in units:

            unit_sensors[itr_unit] = {'in streams' : [],
                                      'unit' : [],
                                      'out streams' : []}
            

        # Classify sensors by their location relative to each unit 
        for itr_sensor in sensors:

            stop_index = itr_sensor.find('.')
            sensor_loc = itr_sensor[:stop_index]
            fs_index = sensor_loc.find('/')

            if fs_index == -1:
                
                # Have to get more complicated when there is multiple of the same sensor on one unit 
                unit_sensors[sensor_loc]['unit'].append(itr_sensor)

            else:

                source_unit = sensor_loc[:fs_index]
                dest_unit = sensor_loc[fs_index+1:]
                if source_unit in streams:

                    unit_sensors[dest_unit]['in streams'].append((itr_sensor, source_unit))

                elif dest_unit in streams:

                    unit_sensors[source_unit]['out streams'].append((itr_sensor, dest_unit))

                else:
                    unit_sensors[source_unit]['out streams'].append((itr_sensor, dest_unit))
                    unit_sensors[dest_unit]['in streams'].append((itr_sensor, source_unit))

        
        # Get flow and comp sensors from non-adjacent streams 
        adj_mat = inputs.adj_mat
        for itr_unit in units:

            # Inlet streams
            adj_in_units = adj_mat.index[adj_mat[itr_unit] == 1]
            for itr_in_unit in adj_in_units:

                curr_unit = itr_in_unit
                match_unit = re.match(r'(comp|v|furn|hex)_', curr_unit)
                while match_unit:

                    if match_unit.group(1) == 'furn' or match_unit.group(1) == 'hex':

                        inlet_process_stream = inputs.configuration[curr_unit]['process streams'][0]
                        next_unit = inlet_process_stream[:inlet_process_stream.find('/')]

                    else:
                        next_unit = adj_mat.index[adj_mat[curr_unit] == 1][0]

                    sens_pattern = rf'{next_unit}/{curr_unit}.(F|X)_'
                    for itr_sensor in sensors:

                        if re.match(sens_pattern, itr_sensor):

                            unit_sensors[itr_unit]['in streams'].append((itr_sensor, itr_in_unit))
                    
                    match_unit = re.match(r'(comp|v|furn|hex)_', next_unit)
                    curr_unit = next_unit


            # Outlet streams
            adj_out_units = adj_mat.columns[adj_mat.loc[itr_unit] == 1]
            for itr_out_unit in adj_out_units:

                curr_unit = itr_out_unit
                match_unit = re.match(r'(comp|v|furn|hex)_', curr_unit)
                while match_unit:

                    if match_unit.group(1) == 'furn' or match_unit.group(1) == 'hex':

                        outlet_process_stream = inputs.configuration[curr_unit]['process streams'][1]
                        next_unit = outlet_process_stream[outlet_process_stream.find('/')+1:]

                    else:
                        next_unit = adj_mat.columns[adj_mat.loc[curr_unit] == 1][0]

                    sens_pattern = rf'{curr_unit}/{next_unit}.(F|X)_'
                    for itr_sensor in sensors:

                        if re.match(sens_pattern, itr_sensor):

                            unit_sensors[itr_unit]['out streams'].append((itr_sensor, itr_out_unit))
                    
                    match_unit = re.match(r'(comp|v|furn|hex)_', next_unit)
                    curr_unit = next_unit
            

        inputs.unit_sensors = unit_sensors
        # print(unit_sensors)
