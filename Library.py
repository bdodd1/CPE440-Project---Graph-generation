
import re 
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

##### Data tracker for graph object #####
# data - whole data set
# topology - topology dict. Input is pipes, control loops and sensors. These are parsed to produce units and streams additionally 
# supported_units - dict containing units modelled in this libray and their naming convention
# adj_mat - adj matrix for units and feed/prod streams 
# units - list of units categorised into type of unit with available model
# unit_sensors - dict storing inlet, outlet and unit mounted sensors for each unit 
# subgraphs - a dict containing each unit and the nodes and edges associated with it. Also includes sensor name mapping between local unit and global dataset names





class unit_lib:

    def __init__(graph, topology, data, configuraton, mode):
        
        graph.data = data
        graph.topology = topology
        graph.configuraton = configuraton
        graph.mode = mode 
        graph.subgraphs = {}
        graph.supported_units = {'reactor' : 'react', 
                                'distilltion column' : 'distil', 
                                'absorption column' : 'abs',
                                'stripping column' : 'str',
                                'heat exchanger' : 'hex',
                                'furnace' : 'furn',
                                'compressor' : 'comp',
                                'flash drum' : 'flash',
                                'control valve' : 'v',
                                'splitter' : 'split',
                                'mixer' : 'mix',
                                'tank' : 'tank'}
        
                                # Pumps? Same as comp
                                # abs and str likely get combined 
                                # tank?
                                # Probs combine mis and split to junc 
        

    def check_inputs(graph):

        # Make sure input is correct - error handling
        A=1
        

    def build_graph(graph):
    
        # Executes functions  
        graph.classify_units()
        graph.build_adj_mat()
        graph.get_unit_sensors()

        # Fill as I go and remove at end 
        modelled_units = ['comp', 'furn', 'v', 'hex', 'react', 'flash']     
        #   

        for unit_cat, unit_list in graph.units.items():

            if unit_list and unit_cat in modelled_units:

                method_name = 'model_' + unit_cat
                getattr(graph, method_name)()

        graph.fuse_subgraphs()


        A=1




    def classify_units(graph):
        
        # Gets a list of units and feed/prod streams from the pipes input
        units_present = []
        streams_present = []
        stream_pattern = r'(feed|prod)_'
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
        pattern = rf'{pattern}'


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
        adj_mat = graph.adj_mat
        for itr_unit in units:

            # Inlet streams
            adj_in_units = adj_mat.index[adj_mat[itr_unit] == 1]
            for itr_in_unit in adj_in_units:

                curr_unit = itr_in_unit
                match_unit = re.match(r'(comp|v|furn|hex)_', curr_unit)
                while match_unit:

                    if match_unit.group(1) == 'furn' or match_unit.group(1) == 'hex':

                        inlet_process_stream = graph.configuraton[curr_unit]['process streams'][0]
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

                        outlet_process_stream = graph.configuraton[curr_unit]['process streams'][1]
                        next_unit = outlet_process_stream[outlet_process_stream.find('/')+1:]

                    else:
                        next_unit = adj_mat.columns[adj_mat.loc[curr_unit] == 1][0]

                    sens_pattern = rf'{curr_unit}/{next_unit}.(F|X)_'
                    for itr_sensor in sensors:

                        if re.match(sens_pattern, itr_sensor):

                            unit_sensors[itr_unit]['out streams'].append((itr_sensor, itr_out_unit))
                    
                    match_unit = re.match(r'(comp|v|furn|hex)_', next_unit)
                    curr_unit = next_unit
            

        graph.unit_sensors = unit_sensors
        # print(unit_sensors)


    def model_comp(graph):

        # Hardcoding latent structure 
        if graph.mode['PT change'] == 1:

            latent_struct = [('T_in', 'T_out') , ('P_in', 'W') , ('W', 'P_out') , ('P_out', 'W') , ('P_out', 'T_out') , ('F_in', 'F_out') , ('X_in', 'X_out')]

        elif graph.mode['PT change'] == 2:

            latent_struct = [('T_in', 'T_out') , ('P_in', 'W') , ('W', 'P_out') , ('P_out', 'W') , ('W', 'T_out') , ('F_in', 'F_out') , ('X_in', 'X_out')]

        all_sensors = ['T_in', 'T_out', 'F_in', 'F_out', 'P_in', 'P_out', 'X_in', 'X_out', 'W']
        latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)
        

        # For every compressor 
        compressors = graph.units['comp']
        for itr_comp in compressors:
            
            present_sensors = []
            sensor_name_mapping = {}

            # Get inlet sensors 
            inlet_sensors = graph.unit_sensors[itr_comp]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    local_sensor = match.group(1) + '_in'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            # Get outlet sensors 
            outlet_sensors = graph.unit_sensors[itr_comp]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    local_sensor = match.group(1) + '_out'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            # Obtain user defined work variable 
            if graph.configuraton[itr_comp]['duty var']:

                present_sensors.append('W')
                sensor_name_mapping['W'] = graph.configuraton[itr_comp]['duty var']

            graph.subgraphs[itr_comp] = {'sensor name mapping' : sensor_name_mapping}
            graph.build_actual_structure(itr_comp, latent_adj_mat, present_sensors)

            # print(sensor_name_mapping)


    def model_v(graph):

        all_sensors = ['T_in', 'T_out', 'F_in', 'F_out', 'P_in', 'P_out', 'X_in', 'X_out', 'Pos']
        latent_struct = [('P_in', 'P_out') , ('Pos', 'P_out') , ('Pos', 'P_in') , ('P_in', 'T_in') , ('P_out', 'T_out') , ('T_in', 'T_out') , ('P_in', 'F_in') , ('P_out', 'F_out') ,
                         ('F_in', 'F_out') , ('X_in', 'X_out')]
        latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)     

        # For every valve 
        valves = graph.units['v']
        for itr_valve in valves:
            
            # Assume valve position variables are in dataset
            present_sensors = ['Pos']
            sensor_name_mapping = {'Pos' : f'Pos_{itr_valve[2:]}'}

            # Get inlet sensors 
            inlet_sensors = graph.unit_sensors[itr_valve]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    local_sensor = match.group(1) + '_in'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            # Get outlet sensors 
            outlet_sensors = graph.unit_sensors[itr_valve]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    local_sensor = match.group(1) + '_out'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            graph.subgraphs[itr_valve] = {'sensor name mapping' : sensor_name_mapping}
            graph.build_actual_structure(itr_valve, latent_adj_mat, present_sensors)  


    def model_furn(graph):
        
        adj_mat = graph.adj_mat
        furnaces = graph.units['furn']
        for itr_furnace in furnaces:

            config = graph.configuraton[itr_furnace]
            num_in_streams = adj_mat[itr_furnace].sum()
            num_out_streams = adj_mat.loc[itr_furnace].sum()

            # Determine latent structure from how many of the utility streams are of interest
            if num_in_streams == 2 and num_out_streams == 1:

                # Fuel, feed and product streams
                if config['fuel stream']:

                    all_sensors = ['T_fuel', 'P_fuel', 'F_fuel', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                    latent_struct = [('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]

                # Air, feed and product streams
                else:

                    all_sensors = ['T_air', 'P_air', 'F_air', 'T_stack', 'P_stack', 'F_stack', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                    latent_struct = [('T_air', 'T_unit') , ('P_air', 'P_unit') , ('F_air', 'T_unit') , ('F_air', 'P_unit') , ('T_unit', 'T_stack') , ('P_unit', 'P_stack') , ('P_unit', 'F_stack') , 
                                     ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]


            elif num_in_streams == 2 and num_out_streams == 2:

                # Fuel, stack, feed and product streams
                if config['fuel stream']:

                    all_sensors = ['T_fuel', 'P_fuel', 'F_fuel', 'T_stack', 'P_stack', 'F_stack', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                    latent_struct = [('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_stack') , ('P_unit', 'P_stack') , ('P_unit', 'F_stack') , ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , 
                                    ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]

                # Air, stack, feed and product streams
                else:

                    all_sensors = ['T_air', 'P_air', 'F_air', 'T_fuel', 'P_fuel', 'F_fuel', 'T_stack', 'P_stack', 'F_stack', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                    latent_struct = [('T_air', 'T_unit') , ('P_air', 'P_unit') , ('F_air', 'T_unit') , ('F_air', 'P_unit') , ('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_stack') , 
                                    ('P_unit', 'P_stack') , ('P_unit', 'F_stack') , ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]


            # Fuel, air, feed and prod streams 
            elif num_in_streams == 3 and num_out_streams == 1:

                all_sensors = ['T_air', 'P_air', 'F_air', 'T_fuel', 'P_fuel', 'F_fuel', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                latent_struct = [('T_air', 'T_unit') , ('P_air', 'P_unit') , ('F_air', 'T_unit') , ('F_air', 'P_unit') , ('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_out') , ('T_out', 'P_out') , 
                                 ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]


            # Fuel, air, stack, feed and prod streams     
            elif num_in_streams == 3 and num_out_streams == 2:

                all_sensors = ['T_air', 'P_air', 'F_air', 'T_fuel', 'P_fuel', 'F_fuel', 'T_stack', 'P_stack', 'F_stack', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out', 'T_unit', 'P_unit']
                latent_struct = [('T_air', 'T_unit') , ('P_air', 'P_unit') , ('F_air', 'T_unit') , ('F_air', 'P_unit') , ('F_fuel', 'P_unit') , ('F_fuel', 'T_unit') , ('T_unit', 'T_stack') , 
                                 ('P_unit', 'P_stack') , ('P_unit', 'F_stack') , ('T_unit', 'T_out') , ('T_out', 'P_out') , ('T_in', 'T_out') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('X_in', 'X_out')]

            else:

                A=1
                # Error handling? Or do it all prior to this 

            latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)

            present_sensors = []
            sensor_name_mapping = {}

            # Get inlet sensors 
            inlet_sensors = graph.unit_sensors[itr_furnace]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                source_unit = itr_sens_tup[1]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    inlet_stream = f'{source_unit}/{itr_furnace}'
                    if inlet_stream in config['process streams']:

                        local_sensor = match.group(1) + '_in'
                    
                    elif inlet_stream == config['fuel stream']:

                        local_sensor = match.group(1) + '_fuel'

                    else:
                        local_sensor = match.group(1) + '_air'

                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name
  
            # Get outlet sensors 
            outlet_sensors = graph.unit_sensors[itr_furnace]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                dest_unit = itr_sens_tup[1]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    outlet_stream = f'{itr_furnace}/{dest_unit}'
                    if outlet_stream in config['process streams']:

                        local_sensor = match.group(1) + '_out'
                    
                    else:
                        local_sensor = match.group(1) + '_stack'

                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            # Get unit sensors
            unit_sensors = graph.unit_sensors[itr_furnace]['unit']
            for itr_sensor in unit_sensors:

                match = re.search(r'.(T|L|P)_', itr_sensor)
                if match:

                    local_sensor = match.group(1) + '_unit'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = itr_sensor

            graph.subgraphs[itr_furnace] = {'sensor name mapping' : sensor_name_mapping}
            graph.build_actual_structure(itr_furnace, latent_adj_mat, present_sensors)
                         
    
    def model_hex(graph):

        # Hardcoding latent structure 
        all_sensors = ['T_uin', 'P_uin', 'F_uin', 'X_uin', 'T_uout', 'P_uout', 'F_uout', 'T_in', 'P_in', 'F_in', 'X_in', 'T_out', 'P_out', 'F_out', 'X_out']
        latent_struct = [('T_in', 'T_out') , ('T_in', 'T_uout') , ('P_in', 'P_out') , ('F_in', 'F_out') , ('F_in', 'T_out') , ('F_in', 'T_uout') , ('T_uin', 'T_uout') , ('T_uin', 'T_out') , ('P_uin', 'P_uout') , 
                         ('F_uin', 'F_uout') , ('F_uin', 'T_uout') , ('F_uin', 'T_out') , ('T_out', 'P_out') , ('T_uout', 'P_uout') , ('X_uin', 'X_uout') , ('X_in', 'X_out')]
        latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)


        hex = graph.units['hex']
        for itr_hex in hex:

            config = graph.configuraton[itr_hex]
            present_sensors = []
            sensor_name_mapping = {}

            # Get inlet sensors 
            inlet_sensors = graph.unit_sensors[itr_hex]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                source_unit = itr_sens_tup[1]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    inlet_stream = f'{source_unit}/{itr_hex}'
                    if inlet_stream in config['process streams']:

                        local_sensor = match.group(1) + '_in'

                    else:
                        local_sensor = match.group(1) + '_uin'
                    
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

            # Get outlet sensors 
            outlet_sensors = graph.unit_sensors[itr_hex]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                dest_unit = itr_sens_tup[1]
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    outlet_stream = f'{itr_hex}/{dest_unit}'
                    if outlet_stream in config['process streams']:

                        local_sensor = match.group(1) + '_out'

                    else:
                        local_sensor = match.group(1) + '_uout'

                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name


            graph.subgraphs[itr_hex] = {'sensor name mapping' : sensor_name_mapping}
            graph.build_actual_structure(itr_hex, latent_adj_mat, present_sensors)


    def model_flash(graph):

        all_sensors = ['T_in', 'P_in', 'F_in', 'T_unit', 'P_unit', 'L_unit', 'T_gas', 'P_gas', 'F_gas', 'T_liq', 'P_liq', 'F_liq']
        latent_struct = [('F_in', 'P_unit') , ('F_in', 'L_unit') , ('T_in', 'T_unit') , ('P_in', 'P_unit') , ('T_unit', 'L_unit') , ('P_unit', 'L_unit') , ('T_unit', 'T_gas') , ('T_unit', 'T_liq') , 
                         ('P_unit', 'P_gas') , ('P_unit', 'F_gas') , ('L_unit', 'F_liq') , ('L_unit', 'P_liq')]
        latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)

        
        flash = graph.units['flash']
        for itr_flash in flash:

            config = graph.configuraton[itr_flash]
            present_sensors = []
            sensor_name_mapping = {}
          
            # Get sensors and adjust latent structure for present composition sensors
            inlet_sensors = graph.unit_sensors[itr_flash]['in streams']
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]

                # Get inlet sensors 
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    local_sensor = match.group(1) + '_in'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

                # Composition effects - inlet
                match = re.search(r'.X_', sensor_name)
                if match:

                    sens_id = sensor_name[match.span()[1]+1:]
                    X_sens = 'X_' + sens_id + 'In'
                    all_sensors.append(X_sens)
                    latent_struct.extend([(X_sens, 'P_unit') , (X_sens, 'L_unit')])

                    present_sensors.append(X_sens)
                    sensor_name_mapping[X_sens] = sensor_name
                
            outlet_sensors = graph.unit_sensors[itr_flash]['out streams']
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                dest_unit = itr_sens_tup[1]

                # Get outlet sensors 
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    outlet_stream = f'{itr_flash}/{dest_unit}'
                    if outlet_stream == config['gas stream']:

                        local_sensor = match.group(1) + '_gas'
                    
                    else:
                        local_sensor = match.group(1) + '_liq'

                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

                # Unit conditions effect on composition 
                match = re.search(r'.X_', sensor_name)
                if match:

                    outlet_stream_name = f'{itr_flash}/{dest_unit}'
                    sens_id = sensor_name[match.span()[1]+1:]
                    if outlet_stream_name == config['gas stream']:

                        X_sens = 'X_' + sens_id + 'Gas'

                    else:

                        X_sens = 'X_' + sens_id + 'Liq'

                    all_sensors.append(X_sens)
                    latent_struct.extend([('P_unit', X_sens) , (X_sens, 'L_unit')])

                    present_sensors.append(X_sens)
                    sensor_name_mapping[X_sens] = sensor_name


            # Get unit sensors
            unit_sensors = graph.unit_sensors[itr_flash]['unit']
            for itr_sensor in unit_sensors:

                match = re.search(r'.(T|L|P)_', itr_sensor)
                if match:

                    local_sensor = match.group(1) + '_unit'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = itr_sensor


            graph.subgraphs[itr_flash] = {'sensor name mapping' : sensor_name_mapping}
            latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)
            graph.build_actual_structure(itr_flash, latent_adj_mat, present_sensors)


    def model_tank(graph):

        A=1


    def model_react(graph):

        adj_mat = graph.adj_mat
        reactors = graph.units['react']
        for itr_react in reactors:

            inlet_stream_source = adj_mat.index[adj_mat[itr_react] == 1]
            outlet_stream_dest = adj_mat.columns[adj_mat.loc[itr_react] == 1]

            config = graph.configuraton[itr_react]
            stream_phases = config['stream phase']

            # Convert user input to an empty list if reactor is not jacketed 
            if config['utility streams']:

                jacketed = True
                utility_streams = config['utility streams']
            else:
                jacketed = False
                utility_streams = []

            all_sensors = ['T_unit', 'P_unit', 'L_unit']
            latent_struct = []

            # Modelling how inlet stream phase effects unit T, L and P
            inlet_streams = []
            in_phases = [] 
            for itr_stream_num, itr_source_unit in enumerate(inlet_stream_source):

                curr_inlet_stream = f'{itr_source_unit}/{itr_react}'
                if curr_inlet_stream not in utility_streams:

                    T_sens = 'T_in'+str(itr_stream_num)
                    P_sens = 'P_in'+str(itr_stream_num)
                    F_sens = 'F_in'+str(itr_stream_num)
                    all_sensors.extend([T_sens, P_sens, F_sens])

                    latent_struct.append((F_sens, 'T_unit'))

                    inlet_streams.append(curr_inlet_stream)
                    curr_in_phase = stream_phases[curr_inlet_stream]
                    in_phases.append(curr_in_phase)

                    if curr_in_phase == 'gas':

                        latent_struct.extend([(T_sens, 'T_unit') , (P_sens, 'P_unit') , (F_sens, 'P_unit')])

                    elif curr_in_phase == 'liq' or curr_in_phase == 'sol' or curr_in_phase == 'SL':

                        latent_struct.extend([(T_sens, 'T_unit') , (F_sens, 'L_unit')])

                    elif curr_in_phase == 'GL' or curr_in_phase == 'GS':

                        latent_struct.extend([(T_sens, 'T_unit') , (P_sens, 'P_unit') , (F_sens, 'P_unit') , (F_sens, 'L_unit')])


            # If there is no gas/liquid inlet stream, but a P/L unit sensor, then the liquid/gas streams must be causing P/L
            if not any(phase in in_phases for phase in ['gas', 'GL', 'GS']):

                for itr_stream_num in range(len(inlet_streams)):

                    latent_struct.extend([('F_in'+str(itr_stream_num), 'P_unit') , ('P_in'+str(itr_stream_num), 'P_unit')])

            if all(phase == 'gas' for phase in in_phases):

                for itr_stream_num in range(len(inlet_streams)):

                    latent_struct.append([('F_in'+str(itr_stream_num), 'L_unit')])


            # Modelling how unit T, L and P effects outlet stream           
            outlet_streams = []
            out_phases = []
            for itr_stream_num, itr_dest_unit in enumerate(outlet_stream_dest):

                curr_outlet_stream = f'{itr_react}/{itr_dest_unit}'
                if curr_outlet_stream not in utility_streams:

                    T_sens = 'T_out'+str(itr_stream_num)
                    P_sens = 'P_out'+str(itr_stream_num)
                    F_sens = 'F_out'+str(itr_stream_num)
                    all_sensors.extend([T_sens, P_sens, F_sens])

                    outlet_streams.append(curr_outlet_stream)
                    curr_out_phase = stream_phases[curr_outlet_stream]
                    out_phases.append(curr_out_phase)
                    if curr_out_phase == 'gas':

                        latent_struct.extend([('T_unit', T_sens) , ('P_unit', P_sens) , ('P_unit', F_sens)])

                    elif curr_out_phase == 'liq' or curr_out_phase == 'sol' or curr_out_phase == 'SL' or curr_out_phase == 'GL' or curr_out_phase == 'GS':

                        latent_struct.extend([('T_unit', T_sens) , ('L_unit', P_sens) , ('L_unit', F_sens)])


            # If reactor is jacketed 
            if jacketed:

                all_sensors.extend(['T_uin', 'P_uin', 'F_uin', 'T_uout', 'P_uout', 'F_uout'])
                latent_struct.extend([('F_uin', 'F_uout') , ('P_uin', 'P_uout') , ('F_uin', 'T_unit') , ('T_uin', 'T_unit') , ('T_unit', 'T_uout') , ('T_uout', 'P_uout')])


            sensor_name_mapping = {}
            present_sensors = []

            reactants = config['reactants']
            inlet_sensors = graph.unit_sensors[itr_react]['in streams']
            outlet_sensors = graph.unit_sensors[itr_react]['out streams']

            # Get sensors and adjust latent structure for present composition sensors
            for itr_sens_tup in inlet_sensors:

                sensor_name = itr_sens_tup[0]
                source_unit = itr_sens_tup[1]

                # Get inlet sensors 
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    inlet_stream_name = f'{source_unit}/{itr_react}'
                    if inlet_stream_name in utility_streams:

                        local_sensor = match.group(1) + '_uin'

                    else:
                        stream_num = inlet_streams.index(inlet_stream_name)
                        local_sensor = match.group(1) + '_in' + str(stream_num)
                    
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name

                # Composition effects on T - inlet
                match = re.search(r'.X_', sensor_name)
                if match:

                    inlet_stream_name = f'{source_unit}/{itr_react}'
                    sens_id = sensor_name[match.span()[1]+1:]
                    stream_num = inlet_streams.index(inlet_stream_name)
                    X_sens = 'X_' + sens_id + 'In' + str(stream_num)
                    all_sensors.append(X_sens)

                    sensor_name_mapping[X_sens] = sensor_name
                    present_sensors.append(X_sens)

                    if reactants[sensor_name]:

                        latent_struct.append((X_sens, 'T_unit'))

             
            for itr_sens_tup in outlet_sensors:

                sensor_name = itr_sens_tup[0]
                dest_unit = itr_sens_tup[1]

                # Get outlet sensors
                match = re.search(r'.(T|F|P)_', sensor_name)
                if match:

                    outlet_stream_name = f'{itr_react}/{dest_unit}'
                    if outlet_stream_name in utility_streams:

                        local_sensor = match.group(1) + '_uout'

                    else:
                        stream_num = outlet_streams.index(outlet_stream_name)
                        local_sensor = match.group(1) + '_out' + str(stream_num)

                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = sensor_name
                        
                # T effects on composition - outlet
                match = re.search(r'.X_', sensor_name)
                if match:

                    outlet_stream_name = f'{itr_react}/{dest_unit}'
                    sens_id = sensor_name[match.span()[1]+1:]
                    stream_num = outlet_streams.index(outlet_stream_name)
                    X_sens = 'X_' + sens_id + 'out' + str(stream_num)
                    all_sensors.append(X_sens)
                    latent_struct.extend([('T_unit', X_sens) , ('P_unit', X_sens)])

                    present_sensors.append(X_sens)
                    sensor_name_mapping[X_sens] = sensor_name


            # Get unit sensors
            unit_sensors = graph.unit_sensors[itr_react]['unit']
            for itr_sensor in unit_sensors:

                match = re.search(r'.(T|L|P)_', itr_sensor)
                if match:

                    local_sensor = match.group(1) + '_unit'
                    present_sensors.append(local_sensor)
                    sensor_name_mapping[local_sensor] = itr_sensor


            graph.subgraphs[itr_react] = {'sensor name mapping' : sensor_name_mapping}
            latent_adj_mat = build_latent_adj_mat(all_sensors, latent_struct)
            graph.build_actual_structure(itr_react, latent_adj_mat, present_sensors)
    

    def model_distil(graph):

        A=1






                







    def build_actual_structure(graph, unit, latent_adj_mat, present_sensors):

        actual_structure = []
        for itr_sensor in present_sensors:

            sensor_queue = latent_adj_mat.columns[latent_adj_mat.loc[itr_sensor] == 1].to_list()
            while sensor_queue:

                next_sensor = sensor_queue.pop(0)
                if next_sensor == itr_sensor:

                    continue

                if next_sensor in present_sensors:

                    actual_structure.append((itr_sensor, next_sensor))

                else:
                    sensor_queue.extend(latent_adj_mat.columns[latent_adj_mat.loc[next_sensor] == 1].to_list())


        # subgraph = nx.DiGraph()
        # plt.figure(figsize=[5, 5])
        # subgraph.add_nodes_from(present_sensors)
        # subgraph.add_edges_from(actual_structure)
        # nx.draw(subgraph, with_labels = True)
        # plt.show()

        graph.subgraphs[unit]['nodes'] = present_sensors
        graph.subgraphs[unit]['edges'] = actual_structure


    def fuse_subgraphs(graph):

        subgraphs = graph.subgraphs 
        whole_graph = {'nodes' : [] , 'edges' : []}
        for itr_subgraph in subgraphs.values():

            sensor_mapping = itr_subgraph['sensor name mapping']
            for edge in itr_subgraph['edges']:

                source_node = sensor_mapping[edge[0]]
                dest_node = sensor_mapping[edge[1]]
                whole_graph['nodes'].extend([source_node, dest_node])
                whole_graph['edges'].append((source_node, dest_node))

        whole_graph['nodes'] = list(set(whole_graph['nodes']))

        vis_graph = nx.DiGraph()
        plt.figure(figsize=[5, 5])
        vis_graph.add_nodes_from(whole_graph['nodes'])
        vis_graph.add_edges_from(whole_graph['edges'])
        pos = nx.spring_layout(vis_graph)
        nx.draw(vis_graph, pos, with_labels = True)
        plt.show()
                












##### This will not be in final release. Will hard code adj matrix to save time #####
def build_latent_adj_mat(all_sensors, latent_struct):

    latent_adj_mat = pd.DataFrame(columns=all_sensors, index = all_sensors)
    latent_adj_mat.iloc[:,:] = 0

    for itr_sensor in all_sensors:

        for itr_edge in latent_struct:

            source_sensor = itr_edge[0]
            if source_sensor == itr_sensor:

                dest_sensor = itr_edge[1]            
                latent_adj_mat.loc[source_sensor,dest_sensor] = 1

    return latent_adj_mat


















