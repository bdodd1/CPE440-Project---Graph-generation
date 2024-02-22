
import re 
import pandas as pd

##### Data tracker for graph object #####
# data - whole data set
# topology - topology dict. Input is pipes, control loops and sensors. These are parsed to produce units and streams additionally 
# supported_units - dict containing units modelled in this libray and their naming convention
# adj_mat - adj matrix for units and feed/prod streams 
# units - list of units categorised into type of unit with available model
# unit_sensors - dict storing inlet, outlet and unit mounted sensors for each unit 
# 





class unit_lib:

    def __init__(graph, topology, data):
        
        # Errors if topology or data not entered 
        graph.data = data
        graph.topology = topology
        graph.supported_units = {'reactor' : 'react', 
                                'distilltion column' : 'distil', 
                                'absorption column' : 'abs',
                                'stripping column' : 'str',
                                'heat exchanger' : 'hex',
                                'compressor' : 'comp',
                                'flash drum' : 'flash',
                                'control valve' : 'v'}
        
                                # Pumps? May be similar to comp
                                # abs and str likely get combined 
                                # mixer?
                                # tank?
        

    def check_inputs(graph):

        # Make sure input is correct - error handling
        A=1
        

    def build_graph():
    
        # Executes functions  
        A=1


    def classify_units(graph):
        
        # Gets a list of units and feed/prod streams from the pipes input
        units_present = []
        streams_present = []
        stream_pattern = re.compile(r'(feed|prod)_')
        for itr_pipes in graph.topology['pipes']:

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
        graph.topology['units'] = units_present
        graph.topology['streams'] = streams_present


        # Builds regex from modelled unit list 
        units = {}
        pattern = '('
        for itr_unit in graph.supported_units.values():

            units[itr_unit] = []
            pattern += f'{itr_unit}|'
    
        pattern = pattern[:-1] + ')_'
        pattern = re.compile(rf'{pattern}')


        # Classifies units provided by topology into modelled categories 
        for itr_unit in graph.topology['units']:

            match = re.match(pattern, itr_unit)
            if match:

                units[match.group(1)].append(itr_unit)
            else:

                raise ValueError(f'{itr_unit} is an incompatable unit.')

        graph.units = units

        # print(units)
        # print('***')
        # print(streams_present)
            

    def build_adj_mat(graph):

        streams = graph.topology['streams']
        units = graph.topology['units']
        pipes = graph.topology['pipes']

        adj_mat_ax = streams + units
        adj_mat = pd.DataFrame(columns=adj_mat_ax, index = adj_mat_ax)
        adj_mat.iloc[:,:] = 0

        for itr_ax in adj_mat_ax:

            for itr_pipe in pipes:

                source_unit = itr_pipe[0]
                if source_unit == itr_ax:

                    dest_unit = itr_pipe[1]            
                    adj_mat.loc[source_unit,dest_unit] = 1

        # print(adj_mat)
        graph.adj_mat = adj_mat


    def get_unit_sensors(graph):

        units = graph.topology['units']
        streams = graph.topology['streams']
        sensors = graph.topology['sensors']

        # Create unit sensor store 
        unit_sensors = {}
        for itr_unit in units:

            unit_sensors[itr_unit] = {'in streams' : [],
                                      'unit' : [],
                                      'out streams' : []}
            

        # Classify sensors by their location reltive to each unit 
        for itr_sensor in sensors:

            stop_index = itr_sensor.find('.')
            sensor_loc = itr_sensor[:stop_index]
            sensor_name = itr_sensor[stop_index+1:]
            fs_index = sensor_loc.find('/')

            if fs_index == -1:
                
                # Have to get more complicated when there is multiple of the same sensor on one unit 
                unit_sensors[sensor_loc]['unit'] = itr_sensor
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

        
        # Get flow sensors from non-adjacent streams 
        adj_mat = graph.adj_mat
        for itr_unit in units:

            # Inlet streams 
            inlet_streams = adj_mat.index[adj_mat[itr_unit] == 1].to_list()
            for itr_in_stream in inlet_streams:

                curr_stream = itr_in_stream
                next_streams = adj_mat.index[adj_mat[itr_in_stream] == 1].to_list()
                while len(next_streams) == 1:

                    stream_name_pattern = rf'{next_streams[0]}/{curr_stream}.F_'
                    for itr_sensor in sensors:

                        if re.match(stream_name_pattern, itr_sensor):

                            unit_sensors[itr_unit]['in streams'].append((itr_sensor, itr_in_stream))

                    curr_stream = next_streams[0]
                    next_streams = adj_mat.index[adj_mat[next_streams[0]] == 1].to_list()

            # Outlet streams 
            outlet_streams = adj_mat.columns[adj_mat.loc[itr_unit] == 1].to_list()
            for itr_out_stream in outlet_streams:

                curr_stream = itr_out_stream
                next_streams = adj_mat.columns[adj_mat.loc[itr_out_stream] == 1].to_list()
                while len(next_streams) == 1:

                    stream_name_pattern = rf'{curr_stream}/{next_streams[0]}.F_'
                    for itr_sensor in sensors:

                        if re.match(stream_name_pattern, itr_sensor):

                            unit_sensors[itr_unit]['out streams'].append((itr_sensor, itr_out_stream))

                    curr_stream = next_streams[0]
                    next_streams = adj_mat.columns[adj_mat.loc[next_streams[0]] == 1].to_list()


                    
        # Composition changes only across reactors and columns - leave this for now as its dependent on how the reactors are modelled 


        graph.unit_sensors = unit_sensors
        # print(unit_sensors)


    def model_comp(graph):

        # Hardcoding latent structure 
        all_vars = ['T_in', 'T_out', 'F in', 'F_out', 'P_in', 'P_out', 'X_in', 'X_out', 'W']
        latent_struct = [('P_in', 'W') , ('W', 'P_out') , ('P_out', 'W') , ('P_out', 'T_out') , ('F_in', 'F_out') , ('X_in', 'X_out')]

        
        # For every compressor 
        compressors = graph.units['comp']
        sens_type_pattern = re.compile(r'.(T|F|P|X)_')
        for itr_comp in compressors:

            present_sensors = []

            # Get inlet sensors 
            inlet_sensors = graph.unit_sensors[itr_comp]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(sens_type_pattern, sensor_name)
                if match:

                    present_sensors.append(match.group(1) + '_in')

            # Get outlet sensors 
            outlet_sensors = graph.unit_sensors[itr_comp]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(sens_type_pattern, sensor_name)
                if match:

                    present_sensors.append(match.group(1) + '_out')



            print(present_sensors)
            print('***')

            

















