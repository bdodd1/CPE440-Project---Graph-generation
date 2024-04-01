
import importlib


class graph_builder_class:

    def __init__(graph, data, topology, configuration, mode):
        
        graph.data = data
        graph.topology = topology
        graph.configuration = configuration
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
        
    def graph_builder_class_ctrl(graph):

        from parse_inputs import parse_inputs
        inputs = parse_inputs(graph)
        inputs.parse_inputs_ctrl()

        graph.topology = inputs.topology
        graph.units = inputs.units
        graph.adj_mat = inputs.adj_mat
        graph.unit_sensors = inputs.unit_sensors

        for unit_cat, unit_list in graph.units.items():

            for itr_unit in unit_list:
                
                file_class_name = 'model_' + unit_cat
                model_module = importlib.import_module(file_class_name)
                model_class = getattr(model_module, file_class_name)

                unit_model = model_class(graph, itr_unit)
                unit_model.model_ctrl()
                

