# import sys
# sys.path.insert(1, r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\py-tetrad\pytetrad\tools')

# from TetradSearch import TetradSearch as ts



import sys
import jpype.imports
jpype.startJVM(classpath=[r"C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\py-tetrad\pytetrad\resources\tetrad-current.jar"])
import edu.cmu.tetrad.search as ts
import edu.cmu.tetrad.data as td
import edu.cmu.tetrad.graph.GraphTransforms as gt
import edu.cmu.tetrad.algcomparison.score as score
from edu.cmu.tetrad.util import Params, Parameters
import edu.cmu.tetrad.graph as tg
import java.lang as lang


sys.path.insert(1, r'C:\Users\byron\OneDrive\Documents\Year 4\CPE440\Final Project\Code Repositiory\py-tetrad\pytetrad\tools')
import translate as tr

from causaldag import PDAG

import matplotlib.pyplot as plt
import networkx as nx
from openpyxl import Workbook
import numpy as np
from tools import tools 





class run_fci_class:

    def __init__(graph_fci, graph, data, var_mapping, struct):

        graph_fci.data_orig = data
        graph_fci.graph = graph
        graph_fci.var_mapping = var_mapping
        graph_fci.rev_var_mapping = {column: sensor for sensor, column in var_mapping.items()}
        graph_fci.struct = struct
        graph_fci.MVP_params = [1, 3, True]
        graph_fci.SemBIC_pen = 10
        graph_fci.EBIC_gamma = 0.95


    def run_fci_ctrl(graph_fci):

        graph_fci.remove_no_variance()
        graph_fci.adj_dtype()

        graph_fci.kn = td.Knowledge()
        graph_fci.build_knowledge()

        graph_fci.perform_fci()
        graph_fci.categorise_edges()
        # graph_fci.calc_knowledge_retention()
        graph_fci.calc_avg_deg()

        graph_fci.generate_dags()
        graph_fci.find_best_dag()
        # graph_fci.only_direct_dag()


    def remove_no_variance(graph_fci):

        column_to_drop = []
        for itr_col in graph_fci.data_orig.columns:

            var_col = graph_fci.data_orig[itr_col].var()
            if var_col < 0.000001:

                column_to_drop.append(itr_col)

        graph_fci.data = graph_fci.data_orig.drop(columns=column_to_drop)
        graph_fci.data_np = graph_fci.data.to_numpy()
        graph_fci.vars = graph_fci.data.columns.tolist()

        dropped_sensors = [graph_fci.rev_var_mapping[column] for column in column_to_drop]
        graph_fci.dropped_sensors = dropped_sensors
        graph_fci.trim_graph = {}
        graph_fci.trim_graph['nodes'] = [node for node in graph_fci.graph['nodes'] if node not in dropped_sensors]
        graph_fci.trim_graph['edges'] = [(source,dest) for source, dest in graph_fci.graph['edges'] if source not in dropped_sensors and dest not in dropped_sensors]
        graph_fci.trim_graph['forbidden'] = [(source,dest) for source, dest in graph_fci.graph['forbidden'] if source not in dropped_sensors and dest not in dropped_sensors]


    def adj_dtype(graph_fci):

        for itr_var in graph_fci.vars:

            dtype = graph_fci.data[itr_var].dtype
            if dtype == np.int64 or dtype == np.int32:

                graph_fci.data[itr_var] = graph_fci.data[itr_var].astype('float64')


    def build_knowledge(graph_fci):

        for itr_edge in graph_fci.trim_graph['edges']:

            graph_fci.kn.setRequired(graph_fci.var_mapping[itr_edge[0]], graph_fci.var_mapping[itr_edge[1]])

        for itr_edge in graph_fci.trim_graph['forbidden']:

            graph_fci.kn.setForbidden(graph_fci.var_mapping[itr_edge[0]], graph_fci.var_mapping[itr_edge[1]])

        # print(graph_fci.kn.getListOfForbiddenEdges())
        # print(graph_fci.kn.getListOfRequiredEdges())


    def perform_fci(graph_fci):

        graph_fci.data_tet = tr.pandas_data_to_tetrad(graph_fci.data)
        score = ts.score.MvpScore(graph_fci.data_tet, graph_fci.MVP_params[0], graph_fci.MVP_params[1], graph_fci.MVP_params[2])
        # score = ts.score.EbicScore(graph_fci.data_tet, True)
        # score.setGamma(graph_fci.EBIC_gamma)
        # score = ts.score.SemBicScore(graph_fci.data_tet, True)
        # score.setPenaltyDiscount(graph_fci.SemBIC_pen)
        self = ts.Fges(score)
        self.setKnowledge(graph_fci.kn)
        self.setSymmetricFirstStep(True)
        # self.setFaithfulnessAssumed(True)
        # self.setVerbose(True)
        # self.setMeekVerbose(True)
        graph_fci.cpdag = self.search()
        # print(f'final score: {self.getModelScore()}')
        mat = tr.graph_to_matrix(graph_fci.cpdag, nullEpt=0, circleEpt=1, arrowEpt=2, tailEpt=3)
        # print(mat)

        vars = mat.columns
        edges = []
        undirected_edges = []
        for itr in range(len(vars)):

            for itr_next in range(itr+1, len(vars)):

                if mat.loc[itr, vars[itr_next]] == 3 and mat.loc[itr_next, vars[itr]] == 3:

                    edges.extend([(vars[itr], vars[itr_next]), (vars[itr_next], vars[itr])])
                    undirected_edges.append((vars[itr], vars[itr_next]))

                elif mat.loc[itr, vars[itr_next]] == 2 and mat.loc[itr_next, vars[itr]] == 3:

                    edges.append((vars[itr], vars[itr_next]))

                elif mat.loc[itr, vars[itr_next]] == 3 and mat.loc[itr_next, vars[itr]] == 2:

                    edges.append((vars[itr_next], vars[itr]))

                elif mat.loc[itr, vars[itr_next]] == 2 and mat.loc[itr_next, vars[itr]] == 2:

                    raise Exception('POSSIBLE TO HAVE BIDIRECTIONAL')

                elif mat.loc[itr, vars[itr_next]] == 1 or mat.loc[itr_next, vars[itr]] == 1:

                    raise Exception('POSSIBLE TO HAVE 1 IN MATRIX')


        sensor_edges = [(graph_fci.rev_var_mapping[edge[0]], graph_fci.rev_var_mapping[edge[1]]) for edge in edges]
        undirect_sensor_edges = [(graph_fci.rev_var_mapping[edge[0]], graph_fci.rev_var_mapping[edge[1]]) for edge in undirected_edges]
        graph_fci.fci_edges_tup = sensor_edges
        graph_fci.undirect_edges = undirect_sensor_edges
        graph_fci.direct_edges = [edge for edge in graph_fci.fci_edges_tup if edge not in undirect_sensor_edges and (edge[1], edge[0]) not in undirect_sensor_edges]
        # self.clear_knowledge()


    def categorise_edges(graph_fci):

        edges_cat = {'knowledge': [], 
                     'data' : []}
        
        for itr_edge in graph_fci.fci_edges_tup:

            if itr_edge in graph_fci.trim_graph['edges']:

                edges_cat['knowledge'].append(itr_edge)
                
            elif itr_edge not in graph_fci.trim_graph['edges'] and itr_edge not in graph_fci.undirect_edges:

                edges_cat['data'].append(itr_edge)

        graph_fci.edges_cat = edges_cat


    def calc_knowledge_retention(graph_fci):

        if len(graph_fci.trim_graph['edges']) > 1:

            count = 0
            for itr_edge in graph_fci.trim_graph['edges']:

                if itr_edge in graph_fci.fci_edges_tup:

                    count += 1
            
            print(f'Retention: {100*count/len(graph_fci.trim_graph["edges"])}')

        else:
            print('Retention: N/A')


    def calc_avg_deg(graph_fci):

        max_degree = 0
        for itr_node in range(len(graph_fci.trim_graph['nodes'])):

            max_degree+=itr_node

        act_degree = len(graph_fci.undirect_edges) + len(graph_fci.direct_edges)
        print(f'Pc of max degree: {100*act_degree/max_degree}')




    def generate_dags(graph_fci):

        # dag_list = gt.generateCpdagDags(graph_fci.cpdag, True)
        pdag_obj = PDAG(nodes=graph_fci.trim_graph['nodes'], edges=graph_fci.undirect_edges, arcs=graph_fci.direct_edges)
        graph_fci.dags = pdag_obj.all_dags()
        graph_fci.dags = [list(dag) for dag in graph_fci.dags]


    def find_best_dag(graph_fci):

        mvp_scores = []
        for itr_dag_edges in graph_fci.dags:
        
            dag_score = graph_fci.score_dag(itr_dag_edges)
            mvp_scores.append(dag_score)

            # vis_graph = nx.DiGraph()
            # plt.figure(figsize=[5, 5])
            # vis_graph.add_nodes_from(graph_fci.trim_graph['nodes'])
            # vis_graph.add_edges_from(itr_dag_edges)
            # pos = nx.spring_layout(vis_graph)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=graph_fci.trim_graph['edges'], edge_color='black', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=[edge for edge in graph_fci.direct_edges if edge not in graph_fci.trim_graph['edges']], edge_color='blue', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=[edge for edge in itr_dag_edges if edge not in graph_fci.direct_edges], edge_color='red', width=2)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=graph_fci.dropped_sensors)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=graph_fci.trim_graph['nodes'])
            # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            # plt.show()

        graph_fci.best_score = max(mvp_scores)
        graph_fci.best_dag = graph_fci.dags[mvp_scores.index(graph_fci.best_score)]


    def score_dag(graph_fci, edges):

        score = ts.score.MvpScore(graph_fci.data_tet, graph_fci.MVP_params[0], graph_fci.MVP_params[1], graph_fci.MVP_params[2])
        # score = ts.score.SemBicScore(graph_fci.data_tet, True)
        # score.setPenaltyDiscount(graph_fci.SemBIC_pen)
        # score = ts.score.EbicScore(graph_fci.data_tet, True)
        # score.setGamma(graph_fci.EBIC_gamma)
        test = ts.Fges(score)
        dag_obj = tg.Dag()
        node_obj_map = {}
        for itr_node in graph_fci.trim_graph['nodes']:

            string = lang.String(graph_fci.var_mapping[itr_node])
            node = tg.GraphNode(string)
            dag_obj.addNode(node)
            node_obj_map[itr_node] = node
        
        for itr_edge in edges:

            dag_obj.addDirectedEdge(node_obj_map[itr_edge[0]], node_obj_map[itr_edge[1]])

        return test.scoreDag(dag_obj)
        # return ts.score.scoreDag(dag_obj, graph_fci.data_tet, graph_fci.SemBIC_pen, True)



    def only_direct_dag(graph_fci):

        direct_dag = graph_fci.direct_edges
        graph_fci.dag_score = graph_fci.score_dag(direct_dag)

        # if graph_fci.dag_score > graph_fci.best_score:

        #     graph_fci.best_score = graph_fci.dag_score
        #     graph_fci.best_dag = direct_dag
        #     # print(graph_fci.dag_score)




