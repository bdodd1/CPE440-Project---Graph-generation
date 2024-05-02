import matplotlib.pyplot as plt
import networkx as nx 
import numpy as np
import pickle



class ground_truth:


    def ctrl(truth_graph, add_cl_flag, plot_gt_flag):

        truth_graph.build_truth()
        truth_graph.add_cl(add_cl_flag)
        truth_graph.plot_truth_graph(plot_gt_flag)

    def build_truth(truth_graph):

        nodes = ['F3', 'T1', 'P4', 'deltaP', 'P6', 'T3', 'T2', 'T_r', 'T_reg', 'L_sp', 'T_cyc', 'T_cyc-T_reg', 'C_co', 'C_o2', 'P5', 'V4', 'V6', 'V7', 'V3', 'V1', 'V2', 'F_rgc', 
                'F_sc', 'ACAB', 'AWGC', 'F5', 'F7', 'F_sg', 'P1', 'P2', 'F_lpg',
                'F_ln', 'F_hn', 'F_lco', 'F_slurry', 'F_reflux', 'T_fra', 'T_10', 'T_20', 'V9', 'V8', 'V10', 'V11']

        edges = []
        # CAB
        edges.extend([('P1', 'ACAB') , ('ACAB', 'P2') , ('P2', 'ACAB') , ('V6', 'F7') , ('V6', 'P2') , ('F7', 'ACAB')])
        # Preheater
        edges.extend([('V1', 'F5',) , ('F5', 'T3') , ('T3', 'T2') , ('F3', 'T2') , ('T1', 'T2')])
        # Regenerator
        edges.extend([('F7', 'P6') , ('P2', 'P6') , ('F7', 'T_reg') , ('F_sc', 'T_reg') , ('F_sc', 'L_sp') , ('F_rgc', 'L_sp') , ('V3', 'F_sc') , ('V2', 'F_rgc') , ('T_reg', 'C_co') , ('P6', 'C_co') , ('T_reg', 'C_o2') , ('P6', 'C_o2') , ('V7', 'T_cyc'),
                    ('V7', 'F_sg') , ('T_reg', 'T_cyc') , ('F_sg', 'P6') , ('T_reg', 'P6')])
        # Reactor
        edges.extend([('T2', 'T_r') , ('F3', 'P4') , ('F3', 'T_r') , ('F_rgc', 'T_r') , ('T_r', 'P4')])
        # Fractionator 
        edges.extend([('T_20', 'T_10') , ('T_10', 'T_20') , ('T_10', 'T_fra') , ('T_fra', 'T_10') , ('T_fra', 'F_reflux') , ('F_reflux', 'T_fra') , ('P5', 'F_reflux') , ('F_reflux', 'P5') , ('F_hn', 'T_10') , ('F_lco', 'T_20') , 
                    ('F_slurry', 'T_20') , ('V11', 'F_lco') , ('V10', 'F_hn') , ('V8', 'F_reflux') , ('V9', 'F_ln') , ('T_fra', 'P5')])
        # WGC
        edges.extend([('F_lpg', 'AWGC') , ('V4', 'F_lpg')])
        # Cross unit links 
        edges.extend([('T_reg', 'T_r') , ('P4', 'P5') , ('T_r', 'T_20') , ('T_r', 'F_lpg') , ('T_r', 'F_ln') , ('T_r', 'F_hn') , ('T_r', 'F_lco') , ('T_r', 'F_slurry')])
        # Calculated vars 
        edges.extend([('T_cyc', 'T_cyc-T_reg') , ('T_reg', 'T_cyc-T_reg') , ('T_cyc-T_reg', 'T_r') , ('P4', 'deltaP') , ('P6', 'deltaP') , ('deltaP', 'F_rgc') , ('deltaP', 'F_sc')])

        truth_graph.nodes = nodes
        truth_graph.edges = edges


    def add_cl(truth_graph, activate):

        pass


    def plot_truth_graph(truth_graph, activate):

        if activate:

            fig = plt.figure()
            g = nx.DiGraph()
            g.add_nodes_from(truth_graph.nodes)
            g.add_edges_from(truth_graph.edges)
            pos = nx.planar_layout(g)
            # pos = nx.kamada_kawai_layout(g)
            nx.draw(g, pos, with_labels=True)
            plt.show()



            adj_mat = np.zeros((len(truth_graph.nodes), len(truth_graph.nodes)))
            for itr_edge in truth_graph.edges:

                source = itr_edge[0]
                source_ind = truth_graph.nodes.index(source)
                dest = itr_edge[1]
                dest_ind = truth_graph.nodes.index(dest)

                adj_mat[source_ind, dest_ind] = 1

                

            plt.figure()
            plt.imshow(adj_mat, interpolation='nearest')
            plt.xticks(range(len(truth_graph.nodes)), truth_graph.nodes, rotation='vertical')
            plt.yticks(range(len(truth_graph.nodes)), truth_graph.nodes)
            # plt.gca().tick_params(axis='x', bottom=True, top=True)
            # plt.gca().tick_params(axis='y', bottom=True, top=True)
            plt.ylabel('cause')
            plt.xlabel('effect')
            plt.grid(True)
            plt.show()
