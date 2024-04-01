
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from causallearn.graph.GraphNode import GraphNode
import numpy as np

class run_fci:

    def __init__(graph_fci, graph):

        graph_fci.data = graph.data.to_numpy()
        graph_fci.vars = graph.data.columns.tolist()
        graph_fci.whole_graph = graph.whole_graph
        graph_fci.var_mapping = graph.var_mapping


    def run_fci_ctrl(graph_fci):

        graph_fci.fci_no_knowledge()
        graph_fci.build_background_knowledge()
        graph_fci.fci_with_knowledge()


    def fci_no_knowledge(graph_fci):

        g = fci(graph_fci.data, independence_test_method='kci')
        graph_fci.nodes_obj = g[0].get_nodes()


    def build_background_knowledge(graph_fci):

        knowledge = BackgroundKnowledge()
        for itr_edge in graph_fci.whole_graph['edges']:

            source_node_var = graph_fci.var_mapping[itr_edge[0]]
            source_node_ind = graph_fci.vars.index(source_node_var)
            source_node_obj = graph_fci.nodes_obj[source_node_ind]

            dest_node_var = graph_fci.var_mapping[itr_edge[1]]
            dest_node_ind = graph_fci.vars.index(dest_node_var)
            dest_node_obj = graph_fci.nodes_obj[dest_node_ind]

            knowledge.add_required_by_node(source_node_obj, dest_node_obj)

        graph_fci.knowledge = knowledge


    def fci_with_knowledge(graph_fci):

        g, edges = fci(graph_fci.data, independence_test_method='kci', background_knowledge=graph_fci.knowledge)

        A=1



    