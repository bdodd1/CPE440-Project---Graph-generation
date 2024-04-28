import networkx as nx
import matplotlib.pyplot as plt

class analyse_graphs:


    @staticmethod
    def kn_score_vs_graph_score(data_store):

        kn_scores = []
        graph_scores = []
        for itr_comb in data_store:

            graph_scores.append(itr_comb['graph score'])
            kn_scores.append(itr_comb['knowledge score'])

        plt.figure()
        plt.scatter(kn_scores, graph_scores)
        plt.xlabel('knowledge scores')
        plt.ylabel('graph scores')
        plt.show()



    @staticmethod
    def graph_score_for_mode(data_store, test):

        test_modes_list = []
        for itr_comb in data_store:

            test_modes_list.append(itr_comb['combination'][test])

        test_modes = list(set(test_modes_list))
        mode_data_store = []
        for itr_mode in test_modes:

            mode_data_store.append([])

        for itr_comb in data_store:

            mode = itr_comb['combination'][test]
            mode_data_store[mode].append(itr_comb['graph score'])

        plt.figure()
        for itr_mode, itr_mode_data in enumerate(mode_data_store):

            plt.scatter([itr_mode]*len(itr_mode_data), itr_mode_data)

        plt.xlabel('mode')
        plt.ylabel('graph scores')
        plt.show()


        
    # @staticmethod
    # def kn_score_vs_graph_score_test_comp(data_store, comparison_test, modes):

    #     # If don't sepcify test modes that are staying the same then arbitraility chose 0
    #     if not modes or len(modes) != len(data_store[0]['combinations'])-1:

    #         modes = [0] * len(data_store[0]['combinations'])-1

    #     viewed_modes = []
    #     kn_scores = []
    #     graph_scores = []
    #     for itr_comb in data_store:

    #         if itr_comb['combination']:

    #             graph_scores.append(itr_comb['graph score'])
    #             kn_scores.append(itr_comb['knowledge score'])

    #     plt.figure()
    #     plt.scatter(kn_scores, graph_scores)
    #     plt.xlabel('knowledge scores')
    #     plt.ylabel('graph scores')


    @staticmethod
    def find_top_three_graphs(data_store):

        scores = []
        for itr_comb in data_store:

            scores.append(itr_comb['graph score'])

        unique_scores = list(set(scores))
        top_three_scores = sorted(unique_scores, reverse=True)[:3]
        top_three_store = [[],[],[]]
        for itr_comb, itr_score in enumerate(scores):

            if itr_score == top_three_scores[0]:

                top_three_store[0].append(data_store[itr_comb])

            if itr_score == top_three_scores[1]:

                top_three_store[1].append(data_store[itr_comb])

            if itr_score == top_three_scores[2]:

                top_three_store[2].append(data_store[itr_comb])

        return top_three_store
    

    @staticmethod
    def visualise_graph(data_store):
        
        vis_graph = nx.DiGraph()
        plt.figure(figsize=[5, 5])
        # plt.title()
        vis_graph.add_nodes_from(data_store['graph']['nodes']+data_store['graph']['dropped sensors'])
        vis_graph.add_edges_from(data_store['graph']['edges'])
        pos = nx.circular_layout(vis_graph)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=data_store['edges cat']['data'], edge_color='red', width=2)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=data_store['edges cat']['knowledge'], edge_color='black', width=2)
        nx.draw_networkx_edges(vis_graph, pos, edgelist=data_store['edges cat']['undirected'], edge_color='blue', width=2)
        nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=data_store['graph']['dropped sensors'])
        nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=data_store['graph']['nodes'])
        nx.draw_networkx_labels(vis_graph, pos, font_color='green')
        plt.show()

                




            