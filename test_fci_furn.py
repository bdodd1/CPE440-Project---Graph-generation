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





class run_fges:

    def __init__(fges_obj, graph, data, var_mapping, struct):

        fges_obj.data_orig = data
        fges_obj.graph = graph
        fges_obj.var_mapping = var_mapping
        fges_obj.rev_var_mapping = {column: sensor for sensor, column in var_mapping.items()}
        fges_obj.struct = struct
        fges_obj.MVP_params = [1, 3, True]


    def run_fges_ctrl(fges_obj):

        fges_obj.remove_no_variance()
        fges_obj.adj_dtype()

        fges_obj.build_knowledge()
        fges_obj.perform_fges()
        fges_obj.categorise_edges()
        fges_obj.calc_avg_deg()

        fges_obj.generate_dags()
        fges_obj.find_best_dag()


    def remove_no_variance(fges_obj):

        column_to_drop = []
        dummy_to_drop = []
        for itr_col in fges_obj.data_orig.columns:

            var_col = fges_obj.data_orig[itr_col].var()
            if var_col < 0.00000001:

                column_to_drop.append(itr_col)
                if itr_col in fges_obj.graph['dummy vars']:

                    dummy_to_drop.append(itr_col)


        fges_obj.data = fges_obj.data_orig.drop(columns=column_to_drop)
        fges_obj.vars = fges_obj.data.columns.tolist()

        # dropped_sensors is all sensors, and drop_dummy_sensors is just dummy sensors
        fges_obj.dropped_sensors = [fges_obj.rev_var_mapping[column] for column in column_to_drop]
        fges_obj.drop_dummy_sensors = [fges_obj.rev_var_mapping[column] for column in dummy_to_drop]

        fges_obj.trim_graph = {}
        fges_obj.trim_graph['nodes'] = [node for node in fges_obj.graph['nodes'] if node not in fges_obj.dropped_sensors]
        fges_obj.trim_graph['dummy vars'] = [node for node in fges_obj.graph['dummy vars'] if node not in fges_obj.drop_dummy_sensors]
        fges_obj.trim_graph['edges'] = [(source,dest) for source, dest in fges_obj.graph['edges'] if source not in fges_obj.dropped_sensors and dest not in fges_obj.dropped_sensors]
        fges_obj.trim_graph['forbidden'] = [(source,dest) for source, dest in fges_obj.graph['forbidden'] if source not in fges_obj.dropped_sensors and dest not in fges_obj.dropped_sensors]


    def adj_dtype(fges_obj):

        for itr_var in fges_obj.vars:

            dtype = fges_obj.data[itr_var].dtype
            if dtype == np.int64 or dtype == np.int32:

                fges_obj.data[itr_var] = fges_obj.data[itr_var].astype('float64')


    def build_knowledge(fges_obj):

        fges_obj.kn = td.Knowledge()
        for itr_edge in fges_obj.trim_graph['edges']:

            fges_obj.kn.setRequired(fges_obj.var_mapping[itr_edge[0]], fges_obj.var_mapping[itr_edge[1]])

        for itr_edge in fges_obj.trim_graph['forbidden']:

            fges_obj.kn.setForbidden(fges_obj.var_mapping[itr_edge[0]], fges_obj.var_mapping[itr_edge[1]])

        # print(fges_obj.kn.getListOfForbiddenEdges())
        # print(fges_obj.kn.getListOfRequiredEdges())


    def perform_fges(fges_obj):

        fges_obj.data_tet = tr.pandas_data_to_tetrad(fges_obj.data)
        score = ts.score.MvpScore(fges_obj.data_tet, fges_obj.MVP_params[0], fges_obj.MVP_params[1], fges_obj.MVP_params[2])
        self = ts.Fges(score)
        self.setKnowledge(fges_obj.kn)
        self.setSymmetricFirstStep(True)
        self.setFaithfulnessAssumed(False)
        # self.setVerbose(True)
        # self.setMeekVerbose(True)
        fges_obj.cpdag = self.search()
        mat = tr.graph_to_matrix(fges_obj.cpdag, nullEpt=0, circleEpt=1, arrowEpt=2, tailEpt=3)
        # print(f'final score: {self.getModelScore()}')
        # print(mat)

        vars = mat.columns
        edges = []
        indirect_edges = []
        for itr in range(len(vars)):

            for itr_next in range(itr+1, len(vars)):

                if mat.loc[itr, vars[itr_next]] == 3 and mat.loc[itr_next, vars[itr]] == 3:

                    edges.extend([(vars[itr], vars[itr_next]), (vars[itr_next], vars[itr])])
                    indirect_edges.extend([(vars[itr], vars[itr_next]) , (vars[itr_next], vars[itr])])

                elif mat.loc[itr, vars[itr_next]] == 2 and mat.loc[itr_next, vars[itr]] == 3:

                    edges.append((vars[itr], vars[itr_next]))

                elif mat.loc[itr, vars[itr_next]] == 3 and mat.loc[itr_next, vars[itr]] == 2:

                    edges.append((vars[itr_next], vars[itr]))

                elif mat.loc[itr, vars[itr_next]] == 2 and mat.loc[itr_next, vars[itr]] == 2:

                    raise Exception('POSSIBLE TO HAVE BIDIRECTIONAL')

                elif mat.loc[itr, vars[itr_next]] == 1 or mat.loc[itr_next, vars[itr]] == 1:

                    raise Exception('POSSIBLE TO HAVE 1 IN MATRIX')

        # Classify into direct and indirect - indirected_edges contains bidirectionals 
        fges_obj.fges_edges = [(fges_obj.rev_var_mapping[edge[0]], fges_obj.rev_var_mapping[edge[1]]) for edge in edges]
        fges_obj.indirect_edges = [(fges_obj.rev_var_mapping[edge[0]], fges_obj.rev_var_mapping[edge[1]]) for edge in indirect_edges]
        fges_obj.direct_edges = [edge for edge in fges_obj.fges_edges if edge not in fges_obj.indirect_edges and (edge[1], edge[0]) not in fges_obj.indirect_edges]


    def categorise_edges(fges_obj):

        edges_cat = {'knowledge': [], 
                     'data' : []}
        
        for itr_edge in fges_obj.direct_edges:

            if itr_edge in fges_obj.trim_graph['edges']:

                edges_cat['knowledge'].append(itr_edge)
            
            else:

                edges_cat['data'].append(itr_edge)

        fges_obj.edges_cat = edges_cat


    def calc_avg_deg(fges_obj):

        max_degree = 0
        # How many non dropped, non dummy nodes present
        non_dummy_node_cnt = len(fges_obj.trim_graph['nodes']) - len(fges_obj.trim_graph['dummy vars'])
        for itr_node in range(non_dummy_node_cnt):

            max_degree+=itr_node

        act_degree = (len(fges_obj.indirect_edges) / 2) + len(fges_obj.direct_edges)
        print(f'Pc of max degree: {100*act_degree/max_degree}')


    def generate_dags(fges_obj):

        # dag_list = gt.generateCpdagDags(fges_obj.cpdag, True)
        pdag_obj = PDAG(nodes=fges_obj.trim_graph['nodes'], edges=fges_obj.indirect_edges, arcs=fges_obj.direct_edges)
        fges_obj.dags = pdag_obj.all_dags()
        fges_obj.dags = [list(dag) for dag in fges_obj.dags]


    def find_best_dag(fges_obj):

        mvp_scores = []
        for itr_dag_edges in fges_obj.dags:
        
            dag_score = fges_obj.score_dag(itr_dag_edges)
            mvp_scores.append(dag_score)

            # vis_graph = nx.DiGraph()
            # plt.figure(figsize=[5, 5])
            # vis_graph.add_nodes_from(fges_obj.graph['nodes'])
            # vis_graph.add_edges_from(itr_dag_edges)
            # pos = nx.spring_layout(vis_graph)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=edges_cat['data'], edge_color='red', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=edges_cat['knowledge'], edge_color='black', width=2)
            # nx.draw_networkx_edges(vis_graph, pos, edgelist=[edge for edge in itr_dag_edges if edge in fges_obj.indirect_edges], edge_color='blue', width=2)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='blue', node_size=500, nodelist=fges_obj.dropped_sensors)
            # nx.draw_networkx_nodes(vis_graph, pos, node_color='black', node_size=500, nodelist=fges_obj.trim_graph['nodes'])
            # nx.draw_networkx_labels(vis_graph, pos, font_color='green')
            # plt.show()

        fges_obj.best_score = max(mvp_scores)
        fges_obj.best_dag = fges_obj.dags[mvp_scores.index(fges_obj.best_score)]


    def score_whole_dag(fges_obj):

        score = ts.score.MvpScore(tr.pandas_data_to_tetrad(fges_obj.data_orig), fges_obj.MVP_params[0], fges_obj.MVP_params[1], fges_obj.MVP_params[2])
        test = ts.Fges(score)
        dag_obj = tg.Dag()
        node_obj_map = {}
        for itr_node in fges_obj.graph['nodes']:

            string = lang.String(fges_obj.var_mapping[itr_node])
            node = tg.GraphNode(string)
            dag_obj.addNode(node)
            node_obj_map[itr_node] = node
        
        for itr_edge in fges_obj.graph['edges']:

            dag_obj.addDirectedEdge(node_obj_map[itr_edge[0]], node_obj_map[itr_edge[1]])

        return test.scoreDag(dag_obj)


    def score_dag(fges_obj, edges):

        score = ts.score.MvpScore(fges_obj.data_tet, fges_obj.MVP_params[0], fges_obj.MVP_params[1], fges_obj.MVP_params[2])
        test = ts.Fges(score)
        dag_obj = tg.Dag()
        node_obj_map = {}
        for itr_node in fges_obj.trim_graph['nodes']:

            string = lang.String(fges_obj.var_mapping[itr_node])
            node = tg.GraphNode(string)
            dag_obj.addNode(node)
            node_obj_map[itr_node] = node
        
        for itr_edge in edges:

            dag_obj.addDirectedEdge(node_obj_map[itr_edge[0]], node_obj_map[itr_edge[1]])

        return test.scoreDag(dag_obj)





