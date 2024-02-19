
import re 
import pandas as pd

##### Data tracker for graph object #####
# data - Whole data set
# topology - topology dict 
# adj_mat - adj matrix for units and feed/prod streams 
# units - list of units categorised into type of unit with available model
# 








class unit_lib:

    def __init__(graph, topology, data):
        
        # Errors if topology or data not entered 
        graph.data = data
        graph.topology = topology


    def build_graph():
    
        # Executes functions  
        A=1


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

        graph.adj_mat = adj_mat


    def classify_units(graph):

        units = {'react' : [],
                 'distil' : [],
                 'abs' : [],
                 'str' : [],
                 'hex' : [],
                 'comp' : [],
                 'flash' : [],
                 'v' : []
                 }
        
        # Pumps? May be similar to comp
        # abs and str likely get combined 
        # mixer?
        # tank?

        pattern = re.compile(f'^(react|distil|abs|str|hex|comp|flash|v)_')

        for itr_unit in graph.topology['units']:

            match = re.match(pattern, itr_unit)
            
            if match:

                units[match.group(1)].append(itr_unit)
            else:

                raise ValueError(f'{itr_unit} is an incompatable unit.')
            
        graph.units = units
            

    def get_unit_sensors(graph):

        # Have to get more complicated when there is multiple streams in and out as it does not store the stream which the sensor is on

        units = graph.topology['units']
        sensor_location = graph.topology['sensor_location'].key()
        unit_sensors = {}

        for itr_unit in units:

            unit_sensors[itr_unit] = {'in streams' : [],
                                      'unit' : [],
                                      'out streams' : []
                                      }

        for itr_unit in units:

            pattern_unit = re.compile(f'^{itr_unit}$')
            pattern_in_streams = re.compile(f'^{itr_unit}/\w+$')
            pattern_out_streams = re.compile(f'^\w+/{itr_unit}$')

            # if pattern_unit.match




        


    def model_comp():

        A=1



