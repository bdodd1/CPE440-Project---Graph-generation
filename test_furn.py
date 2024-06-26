
from test_fci_furn import run_fges
import networkx as nx
import matplotlib.pyplot as plt 
from tools import tools 
import pandas as pd




class test_furn_models:

    def __init__(model, data, var_mapping):

        model.data = data
        model.var_mapping = var_mapping
        model.nodes = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5', 'furn_1.T_3', 'furn_1/react_2.T_2']

        model.dummy_vars = ['furn_1/react_2.T_2_DUMMY']
        model.valve_pos = ['Pos_1']
        model.nodes += model.dummy_vars + model.valve_pos
        model.data['T2_DUMMY'] = model.data['T2']
        model.var_mapping['furn_1/react_2.T_2_DUMMY'] = 'T2_DUMMY'


    def model_ctrl(model):

        columns = [model.var_mapping[sensor] for sensor in model.nodes]
        model.required_data = model.data[columns]
        model.best_dags = []

        # pd.plotting.scatter_matrix(model.required_data, figsize=(10, 10))
        # plt.show()

        model.forbid_edges = []
        model.forbid_control_loops()
        model.forbid_backwards(True)
        model.forbid_diff_streams(True)


        num_models = 9
        for itr_model in range(num_models):

            getattr(model, 'struct_'+str(itr_model))()

            graph = {'nodes' : model.nodes,
                     'dummy vars' : model.dummy_vars,
                     'edges' : model.edges,
                     'forbidden' : model.forbid_edges}
            
            fges_obj = run_fges(graph, model.required_data, model.var_mapping, itr_model)
            fges_obj.run_fges_ctrl()


            ### Plot CPDAG for struct ###
            model.plot_CPDAG(itr_model, fges_obj, False)


            best_dag_data = {'all edges' : fges_obj.best_dag,
                            'knowledge' : fges_obj.edges_cat['knowledge'],
                            'data directed' : fges_obj.edges_cat['data'],
                            'redirected CPDAG' : [edge for edge in fges_obj.best_dag if edge in fges_obj.indirect_edges],
                            'score' : fges_obj.best_score}
            model.best_dags.append(best_dag_data)
            print(fges_obj.best_score)


            ### Plot best DAG of MEC ###
            model.plot_best_dag_in_class(itr_model, fges_obj, False)

            # Save best graph of MEC
            name = f'struct{str(itr_model)}_furn_test'
            location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
            model.save_graphs(best_dag_data, name, location, False)
  

        unit_model_ind = model.find_best_model()
        model.unit_model_ind = unit_model_ind
        print(f'Best score: {model.best_dags[unit_model_ind]["score"]}')


        ### Visualise best DAG from all CPDAGs for each struct ###
        model.plot_best_dag_for_model(unit_model_ind, fges_obj, True)


        ### Save best model for unit ###
        name = f'struct{str(itr_model)}_furn_test_best'
        location = r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\Graphs\CPDAGs\fur test fges 1,3 forbid backwards'
        model.save_graphs(model.best_dags[unit_model_ind], name, location, False)





    
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
    def struct_8(model):

        model.edges = []




    def find_best_model(model):

        best_dag_score = model.best_dags[0]['score']
        best_model_ind = 0
        for itr, itr_dag_data in enumerate(model.best_dags):

            if itr_dag_data['score'] > best_dag_score:

                best_dag_score = itr_dag_data['score']
                best_model_ind = itr

        return best_model_ind


    def forbid_control_loops(model):

        for itr, itr_dummy in enumerate(model.dummy_vars):
                
            model.forbid_edges.extend([(itr_dummy, node) for node in model.nodes if node != model.valve_pos[itr]])
            model.forbid_edges.extend([(node, itr_dummy) for node in model.nodes])

        for itr, itr_valve in enumerate(model.valve_pos):
                
            model.forbid_edges.extend([(node, itr_valve) for node in model.nodes if node != model.dummy_vars[itr]])

        pass
    

    def forbid_backwards(model, activate):

        if activate:

            # All structures abide by the forbidden backwards rule
            node_tiers = {}
            node_tiers['out'] = ['furn_1/react_2.T_2']
            node_tiers['unit'] = ['furn_1.T_3']
            node_tiers['in'] = ['feed_feedstream/furn_1.F_3', 'feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5']
            
            node_tiers_names = ['out', 'unit', 'in']
            for itr_tier in range(len(node_tiers_names)-1):

                curr_tier = node_tiers_names[itr_tier]
                next_tiers = node_tiers_names[itr_tier+1:]
                for itr_next_tier in next_tiers:
                    
                    for itr_tier_node in node_tiers[curr_tier]:

                        model.forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[itr_next_tier]])


    def forbid_diff_streams(model, activate):

        if activate:

            model.forbid_edges.extend([('feed_feedstream/furn_1.F_3', 'feed_fuel/v_1.F_5') , ('feed_fuel/v_1.F_5', 'feed_feedstream/furn_1.F_3') , ('feed_feedstream/furn_1.T_1', 'feed_fuel/v_1.F_5') ,
                                       ('feed_fuel/v_1.F_5', 'feed_feedstream/furn_1.T_1') , ('feed_feedstream/furn_1.F_3', 'Pos_1') , ('Pos_1', 'feed_feedstream/furn_1.F_3') ,
                                       ('feed_feedstream/furn_1.T_1', 'Pos_1') , ('Pos_1', 'feed_feedstream/furn_1.T_1')])
            


    def plot_CPDAG(model, itr_model, fges_obj, activate):

        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'CPDAG: {str(itr_model)}')
            vis_graph.add_nodes_from(fges_obj.graph['nodes'])
            vis_graph.add_edges_from(fges_obj.fges_edges)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['data'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.indirect_edges, edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def plot_best_dag_in_class(model, itr_model, fges_obj, activate):

        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'best DAG of MEC: {str(itr_model)}')
            vis_graph.add_nodes_from(fges_obj.graph['nodes'])
            vis_graph.add_edges_from(fges_obj.best_dag)
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['data'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=fges_obj.edges_cat['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=[edge for edge in fges_obj.best_dag if edge in fges_obj.indirect_edges], edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def plot_best_dag_for_model(model, unit_model_ind, fges_obj, activate):
        
        if activate:

            vis_graph = nx.DiGraph()
            plt.figure(figsize=[5, 5])
            plt.title(f'Best DAG for unit: {str(unit_model_ind)}')
            vis_graph.add_nodes_from(model.nodes)
            vis_graph.add_edges_from(model.best_dags[unit_model_ind]['all edges'])
            pos = nx.spring_layout(vis_graph)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['data directed'], edge_color='red', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['knowledge'], edge_color='black', width=2)
            nx.draw_networkx_edges(vis_graph, pos, edgelist=model.best_dags[unit_model_ind]['redirected CPDAG'], edge_color='blue', width=2)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            plt.show()


    def save_graphs(model, graph, name, location, activate):

        if activate:

            save_path = rf'{location}\{name}.xlsx'
            tools.print_to_excel(graph, save_path)

        