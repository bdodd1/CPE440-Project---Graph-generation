
import importlib
import matplotlib.pyplot as plt
import networkx as nx


class graph_builder_class:

    def __init__(graph, data, topology, configuration, var_mapping):
        
        graph.data = data
        graph.topology = topology
        graph.configuration = configuration
        graph.var_mapping = var_mapping 
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
        
    def build_graph(graph):

        from parse_inputs import parse_inputs
        inputs = parse_inputs(graph)
        inputs.parse_inputs_ctrl()

        graph.topology = inputs.topology
        graph.units = inputs.units
        graph.adj_mat = inputs.adj_mat
        graph.unit_sensors = inputs.unit_sensors

        graph.subgraphs = {}
        for unit_cat, unit_list in graph.units.items():

            if unit_cat not in ['mix', 'split', 'tank', 'abs', 'str']:

                for itr_unit in unit_list:
                    
                    file_class_name = 'model_' + unit_cat
                    model_module = importlib.import_module(file_class_name)
                    model_class = getattr(model_module, file_class_name)

                    unit_model = model_class(graph, itr_unit)
                    unit_model.model_ctrl()
                    graph.subgraphs[itr_unit] = {}
                    graph.subgraphs[itr_unit]['nodes'] = unit_model.present_sensors
                    graph.subgraphs[itr_unit]['edges'] = unit_model.actual_structure
                    graph.subgraphs[itr_unit]['sensor name mapping'] = unit_model.sensor_name_mapping

        graph.fuse_subgraphs()


    def fuse_subgraphs(graph):

        subgraphs = graph.subgraphs 
        whole_graph = {'nodes' : [] , 'edges' : []}
        for itr_subgraph in subgraphs.values():

            sensor_mapping = itr_subgraph['sensor name mapping']
            for node in itr_subgraph['nodes']:

                whole_graph['nodes'].append(sensor_mapping[node])

            for edge in itr_subgraph['edges']:

                source_node = sensor_mapping[edge[0]]
                dest_node = sensor_mapping[edge[1]]
                whole_graph['edges'].append((source_node, dest_node))


        whole_graph['nodes'] = list(set(whole_graph['nodes']))
        whole_graph['edges'] = list(set(whole_graph['edges']))
        graph.whole_graph = whole_graph


        vis_graph = nx.DiGraph()
        plt.figure(figsize=[5, 5])
        vis_graph.add_nodes_from(whole_graph['nodes'])
        vis_graph.add_edges_from(whole_graph['edges'])
        pos = nx.spring_layout(vis_graph)
        nx.draw(vis_graph, pos, with_labels = True)
        plt.show()
