
from test_fci_furn import run_fci
from run_BIC import run_BIC
import networkx as nx
import matplotlib.pyplot as plt 

class test_furn_models:

    def __init__(model, data, var_mapping):

        model.data = data
        model.var_mapping = var_mapping
        model.nodes = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5', 'furn_1.T_3', 'furn_1/react_2.T_2']


    def model_ctrl(model):

        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]

        num_models = 9
        for itr_model in range(num_models):

            getattr(model, 'struct_'+str(itr_model))()
            graph  ={'nodes' : model.nodes,
                     'edges' : model.edges}
            
            graph_fci = run_fci(graph, model.required_data, model.var_mapping, itr_model)
            graph_fci.run_fci_ctrl()

            print(len(graph_fci.fci_edges_tup))
            print('**')
            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            vis_graph.add_nodes_from(graph['nodes'])
            vis_graph.add_edges_from(graph_fci.fci_edges_tup)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.data_edges, edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.graph['edges'], edge_color='black', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


            graph['edges'] = graph_fci.fci_edges_tup
            del graph_fci
            del vis_graph

            # BIC = run_BIC(graph, model.required_data, model.var_mapping)
            # BIC.calc_BIC()



    
    # My opinion
    def struct_0(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2')]


    # Addition of fuel flow to outlet temp (direct + indirect)
    def struct_1(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , 
                       ('feed_fuel/v_1.F_5', 'furn_1/react_2.T_2')]


    # Inlet temp sufficient to cause a change in furnace temp and outlet temp
    def struct_2(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , 
                       ('feed_feedstream/furn_1.T_1', 'furn_1.T_3')]
        

    # Inlet temp sufficient to cause a change in furnace temp 
    def struct_3(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1.T_3')]
        

    # Inlet flow sufficient to cause a change in furnace temp and outlet temp
    def struct_4(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2'),
                       ('feed_feedstream/furn_1.F_3', 'furn_1.T_3')]
        

    # Inlet flow sufficient to cause a change in furnace temp 
    def struct_5(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2'),
                       ('feed_feedstream/furn_1.F_3', 'furn_1.T_3')]
        

    ### Lower knolwedge content ###
    # 3 most important
    def struct_6(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2') , ('furn_1.T_3', 'furn_1/react_2.T_2')]


    # 2 most important 
    def struct_7(model):

        model.edges = [('feed_fuel/v_1.F_5', 'furn_1.T_3') , ('furn_1.T_3', 'furn_1/react_2.T_2')]

    
    # data only
    # 2 most important 
    def struct_8(model):

        model.edges = []