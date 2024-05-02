import networkx as nx
import matplotlib.pyplot as plt
from openpyxl import Workbook, load_workbook
from itertools import product
from handle_cycles import handle_cycles
from test_run_fges import run_fges


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
    def amount_kn_vs_graph_score(data_store):

        kn_amount = []
        graph_scores = []
        for itr_comb in data_store:

            graph_scores.append(itr_comb['graph score'])
            kn_amount.append(itr_comb['knowledge count'])

        plt.figure()
        plt.scatter(kn_amount, graph_scores)
        plt.xlabel('amount of knowledge')
        plt.ylabel('graph scores')
        plt.show()


    @staticmethod
    def pc_max_degree_vs_graph_score(data_store):

        pc_max_degree = []
        graph_scores = []
        for itr_comb in data_store:

            graph_scores.append(itr_comb['graph score'])
            pc_max_degree.append(itr_comb[r'% of max degree'])

        plt.figure()
        plt.scatter(pc_max_degree, graph_scores)
        plt.xlabel(r'% of max degree')
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


    @staticmethod
    def avg_graph_score_vs_mode_bar(data_store, test):

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

            plt.bar(itr_mode, sum(itr_mode_data)/len(itr_mode_data))

        plt.xlabel('mode')
        plt.ylabel('avg graph score')
        plt.show()
    

    @staticmethod
    def find_pc_unique_graphs(data_store):

        scores = []
        for itr_comb in data_store:

            scores.append(itr_comb['graph score'])

        return 100*len(set(scores)) / len(scores)


    @staticmethod
    def find_top_three_graphs(data_store):

        scores = []
        for itr_comb in data_store:

            scores.append(itr_comb['graph score'])

        unique_scores = list(set(scores))
        if len(unique_scores) < 3:
            top_score_count = len(unique_scores)
        else:
            top_score_count = 3
        top_three_scores = sorted(unique_scores, reverse=True)[:top_score_count]

        top_three_store = []
        for _ in range(len(top_three_scores)):
            top_three_store.append([])


        for itr_comb, itr_score in enumerate(scores):

            if itr_score == top_three_scores[0]:

                top_three_store[0].append(data_store[itr_comb])

            if len(unique_scores) > 1:

                if itr_score == top_three_scores[1]:

                    top_three_store[1].append(data_store[itr_comb])

            if len(unique_scores) > 2:
                
                if itr_score == top_three_scores[2]:

                    top_three_store[2].append(data_store[itr_comb])

        return top_three_store
    

    @staticmethod
    def find_top_three_closest_to_gt(data_store, ground_truth):

        pc_mismatch = []
        pc_match = []
        overall_metric = []
        for itr_comb in data_store:

            nodes = itr_comb['graph']['nodes']
            gt_edges = []
            for itr_gt_edge in ground_truth['edges']:

                if itr_gt_edge[0] in nodes and itr_gt_edge[1] in nodes:

                    gt_edges.append(itr_gt_edge)

            edge_match_count = 0
            edge_mismatch_count = 0
            edges = itr_comb['graph']['edges']
            for itr_edge in edges:

                if itr_edge in gt_edges:

                    edge_match_count += 1

                else:

                    edge_mismatch_count += 1
            
            pc_mismatch.append(100*edge_mismatch_count/len(edges))
            pc_match.append(100*edge_match_count/len(gt_edges))
            overall_metric.append(pc_match[-1] - pc_mismatch[-1])
            pass


        unique_scores = list(set(overall_metric))
        if len(unique_scores) < 3:
            top_score_count = len(unique_scores)
        else:
            top_score_count = 3
        top_three_scores = sorted(unique_scores, reverse=True)[:top_score_count]

        top_three_store = []
        for _ in range(len(top_three_scores)):
            top_three_store.append([])

        for itr_comb, itr_score in enumerate(overall_metric):

            if itr_score == top_three_scores[0]:

                top_three_store[0].append(itr_comb)

            if len(unique_scores) > 1:

                if itr_score == top_three_scores[1]:

                    top_three_store[1].append(itr_comb)

            if len(unique_scores) > 2:
                
                if itr_score == top_three_scores[2]:

                    top_three_store[2].append(itr_comb)

        return top_three_store, overall_metric, pc_match, pc_mismatch

            

    @staticmethod
    def remove_cycle_datapoints(data_store):

        cyclic_graphs = []
        for itr, itr_comb in enumerate(data_store):

            if not itr_comb['graph score']:

                cyclic_graphs.append(itr)

        data_store = [data for itr, data in enumerate(data_store) if itr not in cyclic_graphs] 

        return data_store, cyclic_graphs



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

        return vis_graph


    @staticmethod
    def write_pydot(data_store, name):

        vis_graph = analyse_graphs.visualise_graph(data_store)
        vis_graph = nx.drawing.nx_pydot.to_pydot(vis_graph)
        vis_graph.write_png(name+'.png')


    @staticmethod
    def write_data_store(data_store, filepath):

        wb = Workbook()
        for itr_data in data_store:

            wb = analyse_graphs.write_excel_sheet(wb, itr_data, str(itr_data['combination']))
            
        wb.save(filepath)

        
    @staticmethod
    def write_top_three(data_store, filepath):

        wb = Workbook()
        for itr_place, itr_place_graphs in enumerate(data_store, start=1):

            for itr_graph in itr_place_graphs:

                wb = analyse_graphs.write_excel_sheet(wb, itr_graph, str(itr_place) + '--' + str(itr_graph['combination']))

        wb.save(filepath)

 
    @staticmethod
    def write_excel_sheet(wb, data, sheet_name):

        sheet = wb.create_sheet(title=sheet_name)
            
        nodes = data['graph']['nodes']
        knowledge = data['edges cat']['knowledge']
        data_edges = data['edges cat']['data']
        undirected = data['edges cat']['undirected']

        for itr, itr_node in enumerate(nodes, start=1):

            sheet.cell(row=itr, column=1, value=itr_node)

        for itr, itr_kn in enumerate(knowledge, start=1):

            sheet.cell(row=itr, column=2, value=itr_kn[0])
            sheet.cell(row=itr, column=3, value=itr_kn[1])

        for itr, itr_data_edges in enumerate(data_edges, start=1):

            sheet.cell(row=itr, column=4, value=itr_data_edges[0])
            sheet.cell(row=itr, column=5, value=itr_data_edges[1])

        for itr, itr_undi in enumerate(undirected, start=1):

            sheet.cell(row=itr, column=6, value=itr_undi[0])
            sheet.cell(row=itr, column=7, value=itr_undi[1])

        sheet.cell(row=1, column=8, value='graph score')
        sheet.cell(row=2, column=8, value='kn score')
        sheet.cell(row=3, column=8, value='pc max degree')
        sheet.cell(row=1, column=9, value=data['graph score'])
        sheet.cell(row=2, column=9, value=data['knowledge score'])
        sheet.cell(row=3, column=9, value=data[r'% of max degree'])
    
        return wb
    

    @staticmethod
    def read_data_store(filepath):

        wb = load_workbook(filepath)
        sheets = wb.sheetnames

        data_store = []
        for itr_sheet in sheets[1:]:

            nodes = []
            data = []
            knowledge = []
            undi = []

            sheet_obj = wb[itr_sheet]
            for itr_row_num, itr_row in enumerate(sheet_obj.iter_rows(values_only=True)):

                if itr_row_num == 0:

                    graph_score = itr_row[8]
                
                elif itr_row_num == 1:

                    kn_score = itr_row[8]

                elif itr_row_num == 2:

                    pc_max_deg = itr_row[8]  

                if itr_row[0]:
                    nodes.append(itr_row[0])
                if itr_row[1] and itr_row[2]:
                    knowledge.append((itr_row[1], itr_row[2]))
                if itr_row[3] and itr_row[4]:
                    data.append((itr_row[3], itr_row[4]))
                if itr_row[5] and itr_row[6]:
                    undi.append((itr_row[5], itr_row[6]))

            graph_store = {'combination' : itr_sheet,
                           'knowledge score' : kn_score,
                           'data score' : graph_score-kn_score,
                           'graph score' : graph_score,
                           'knowledge count' : len(knowledge),
                           r'% max degree' : pc_max_deg,
                           'graph' : {'nodes' : nodes,
                                      'edges' : data+knowledge+undi},
                            'edges cat' : {'data' : data,
                                           'knowledge' : knowledge,
                                           'undirected' : undi}}
            
            data_store.append(graph_store)

        return data_store
            

    @staticmethod
    def compile_graphs(top_three_score, data):

        units = list(top_three_score.keys())
        comb = list(product(*(range(2) for _ in units)))

        whole_graph_score = []
        for itr_comb in comb:

            graph_data = {'combination' : itr_comb,
                        'nodes' : [],
                        'edges' : []}
            
            for itr, itr_place in enumerate(itr_comb):

                unit = units[itr]
                unit_graph = top_three_score[unit][itr_place][0]['graph']
                graph_data['nodes'].extend(unit_graph['nodes'])
                graph_data['edges'].extend(unit_graph['edges'])

            # Add flash sensors
            graph_data['nodes'].extend(['V9', 'F_ln'])
            graph_data['edges'].extend([('V9', 'F_ln')])

            graph_data['nodes'] = list(set(graph_data['nodes']))
            graph_data['edges'] = list(set(graph_data['edges'])) 


            cyc_obj = handle_cycles(graph_data, 'hi', 'hi')
            cyc_obj.handle_cycles_ctrl()


            # All loops go through F_rgc so direct all parents to a dummy
            graph_data['nodes'].append('F_rgc_DUMMY')
            for itr_cycle_edge in cyc_obj.cycle_edges:

                if itr_cycle_edge[1] == 'F_rgc':

                    graph_data['edges'].remove(itr_cycle_edge)
                    graph_data['edges'].append((itr_cycle_edge[0], 'F_rgc_DUMMY'))


            
            # Sorting out the F7 <--> P2
            if ('P2', 'F7') in graph_data['edges'] and ('F7', 'P2') in graph_data['edges']:

                P2_parents = []
                F7_parents = []
                for itr_edge in graph_data['edges']:

                    if itr_edge[1] == 'P2':

                        P2_parents.append(itr_edge[0])

                    elif itr_edge[1] == 'F7':

                        F7_parents.append(itr_edge[0])
                        

                trim_P2_parents = [parent for parent in P2_parents if parent != 'F7']
                P2_child_graph = {'nodes' : ['P2']+P2_parents,
                                'edges' : [(parent, 'P2') for parent in P2_parents],
                                'dummy vars' : [],
                                'forbidden' : []}
                fges_obj = run_fges(P2_child_graph, data, 'score kn')
                fges_obj.remove_no_variance()
                P2_score_prior = fges_obj.local_score(['P2'] , P2_parents)
                P2_score_after = fges_obj.local_score(['P2'] , trim_P2_parents)
                P2_penalty = P2_score_prior - P2_score_after

                trim_F7_parents = [parent for parent in F7_parents if parent != 'P2']
                F7_child_graph = {'nodes' : ['F7']+F7_parents,
                                'edges' : [(parent, 'F7') for parent in F7_parents],
                                'dummy vars' : [],
                                'forbidden' : []}
                fges_obj = run_fges(F7_child_graph, data, 'score kn')
                fges_obj.remove_no_variance()
                F7_score_prior = fges_obj.local_score(['F7'] , F7_parents)
                F7_score_after = fges_obj.local_score(['F7'] , trim_F7_parents)
                F7_penalty = F7_score_prior - F7_score_after

                if F7_penalty < P2_penalty:

                    graph_data['edges'].remove(('P2', 'F7'))

                elif F7_penalty > P2_penalty:

                    graph_data['edges'].remove(('F7', 'P2'))

                else:

                    raise ValueError('GIVE UP NOW')

            cyc_obj = handle_cycles(graph_data, 'hi', 'hi')
            cyc_obj.handle_cycles_ctrl()

            if cyc_obj.cycle_edges:

                print(cyc_obj.cycle_edges)

            whole_graph_score.append(graph_data)

        return whole_graph_score


    @staticmethod
    def score_whole_graphs(best_graph_scores, data):

        scores = []
        for itr_graph in best_graph_scores:

            graph = {'nodes' : itr_graph['nodes'],
                    'edges' : itr_graph['edges'],
                    'dummy vars' : [], # there is one but irrelevant at this point
                    'forbidden' : []}
            fges_obj = run_fges(graph, data, 'hi')
            fges_obj.remove_no_variance()
            scores.append(fges_obj.score_dag(itr_graph['edges']))

        for itr, score in enumerate(scores):

            best_graph_scores[itr]['score'] = score

        return best_graph_scores
    

    @staticmethod
    def write_excel_whole_graph(data_store, filepath):

        wb = Workbook()
        for itr_data in data_store:
            
            sheet = wb.create_sheet(title=str(itr_data['combination']))
                
            nodes = itr_data['nodes']
            edges = itr_data['edges']

            for itr, itr_node in enumerate(nodes, start=1):

                sheet.cell(row=itr, column=1, value=itr_node)

            for itr, itr_edge in enumerate(edges, start=1):

                sheet.cell(row=itr, column=2, value=itr_edge[0])
                sheet.cell(row=itr, column=3, value=itr_edge[1])

            sheet.cell(row=1, column=4, value='graph score')
            sheet.cell(row=1, column=5, value=itr_data['score'])

        
        wb.save(filepath)


    @staticmethod
    def read_excel_whole_graph(filepath):

        wb = load_workbook(filepath)
        sheets = wb.sheetnames

        data_store = []
        for itr_sheet in sheets[1:]:

            nodes = []
            edges = []

            sheet_obj = wb[itr_sheet]
            for itr_row_num, itr_row in enumerate(sheet_obj.iter_rows(values_only=True)):

                if itr_row_num == 0:

                    graph_score = itr_row[4]
 

                if itr_row[0]:
                    nodes.append(itr_row[0])
                if itr_row[1] and itr_row[2]:
                    edges.append((itr_row[1], itr_row[2]))

            graph_store = {'combination' : itr_sheet,
                           'score' : graph_score,
                           'nodes' : nodes,
                           'edfes' : edges}

            
            data_store.append(graph_store)

        return data_store


    @staticmethod
    def forbid_within_units(forbid_edges):

        unit_sensors = {'cab' : ['P1', 'F7', 'P2', 'ACAB', 'V6'],
                        'reg' : ['F7', 'P2', 'V6', 'T_reg', 'L_sp', 'P6', 'F_sg', 'T_cyc', 'C_co', 'C_o2', 'V7', 'F_rgc', 'V2', 'F_sc', 'V3'],
                        'react' : ['F_sc', 'V3', 'F_rgc', 'V2', 'F3', 'T2', 'T_r', 'P4'],
                        'furn' : ['F3', 'T1', 'F5', 'V1', 'T3', 'T2'],
                        'distil' : ['T_20', 'T_10', 'T_fra', 'P5', 'F_slurry', 'F_lco', 'V11', 'F_hn', 'V10', 'F_reflux', 'V8'],
                        'wgc' : ['V4', 'AWGC', 'F_lpg'],
                        'flash' : ['V9', 'F_ln']}

        for itr_unit in unit_sensors.values():

            for sensor in itr_unit:
            
                forbid_edges.extend([(sensor, next) for next in itr_unit])
                forbid_edges.extend([(next, sensor) for next in itr_unit])

        return forbid_edges


    @staticmethod
    def forbid_units(forbid_edges):

        unit_sensors = {'cab' : ['P1', 'F7', 'P2', 'ACAB', 'V6'],
                        'reg' : ['F7', 'P2', 'V6', 'T_reg', 'L_sp', 'P6', 'F_sg', 'T_cyc', 'C_co', 'C_o2', 'V7', 'F_rgc', 'V2', 'F_sc', 'V3'],
                        'react' : ['F_sc', 'V3', 'F_rgc', 'V2', 'F3', 'T2', 'T_r', 'P4'],
                        'furn' : ['F3', 'T1', 'F5', 'V1', 'T3', 'T2'],
                        'distil' : ['T_20', 'T_10', 'T_fra', 'P5', 'F_slurry', 'F_lco', 'V11', 'F_hn', 'V10', 'F_reflux', 'V8'],
                        'wgc' : ['V4', 'AWGC', 'F_lpg'],
                        'flash' : ['V9', 'F_ln']}
        
        forbid_pairs = [('reg', 'cab') , ('react', 'cab') , ('furn', 'cab') , ('distil', 'cab') , ('wgc', 'cab') , ('flash', 'cab') , 
                        ('reg', 'furn') , ('react', 'furn') , ('cab', 'furn') , ('distil', 'furn') , ('wgc', 'furn') , ('flash', 'furn') , 
                        ('distil', 'reg') , ('wgc', 'reg') , ('flash', 'reg'),
                        ('distil', 'react') , ('wgc', 'react') , ('flash', 'react') , 
                        ('wgc', 'distil') , ('flash', 'distil') , 
                        ('wgc', 'flash')]
        
        for itr_pair in forbid_pairs:

            unit1_sensors = unit_sensors[itr_pair[0]]
            unit2_sensors = unit_sensors[itr_pair[1]]
            for unit1 in unit1_sensors:

                forbid_edges.extend([(unit1, unit2) for unit2 in unit2_sensors])

        return forbid_edges


    @staticmethod
    def forbid_valves(forbid_edges):

        unit_sensors = {'cab' : ['P1', 'F7', 'P2', 'ACAB', 'V6'],
                'reg' : ['F7', 'P2', 'V6', 'T_reg', 'L_sp', 'P6', 'F_sg', 'T_cyc', 'C_co', 'C_o2', 'V7', 'F_rgc', 'V2', 'F_sc', 'V3'],
                'react' : ['F_sc', 'V3', 'F_rgc', 'V2', 'F3', 'T2', 'T_r', 'P4'],
                'furn' : ['F3', 'T1', 'F5', 'V1', 'T3', 'T2'],
                'distil' : ['T_20', 'T_10', 'T_fra', 'P5', 'F_slurry', 'F_lco', 'V11', 'F_hn', 'V10', 'F_reflux', 'V8'],
                'wgc' : ['V4', 'AWGC', 'F_lpg'],
                'flash' : ['V9', 'F_ln']}
        nodes = []
        for itr in unit_sensors.values():
            nodes += list(itr)
        
        valves = ['V1', 'V2', 'V3', 'V4', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11']

        for itr in valves:

            forbid_edges.extend([(node, itr) for node in nodes])

        return forbid_edges

    

    @staticmethod
    def data_only(best_graph_scores, data, forbid_edges):

        new_data = []
        for itr_data in best_graph_scores:

            graph = {'nodes' : itr_data['nodes'] + ['deltaP', 'T_cyc-T_reg'],
                     'edges' : itr_data['edges'],
                    'dummy vars' : [], # there is one but irrelevant at this point
                    'forbidden' : forbid_edges}
            fges_obj = run_fges(graph, data, 'hi')
            fges_obj.run_fges_ctrl()
            added_edges = fges_obj.edges_cat['data'] + fges_obj.edges_cat['undirected']
            new_data.append([added_edges, fges_obj.best_score])

        for itr in range(len(best_graph_scores)):

            best_graph_scores[itr]['data mode'] = new_data[itr]

        return best_graph_scores


    @ staticmethod
    def cluster_mode(best_graph_scores, data, forbid_edges):

        cluster_edges = [('T_r', 'T_20') , ('P4', 'P5') , ('T_fra', 'F_ln') , ('P5', 'F_ln')]

        new_data = []
        for itr_data in best_graph_scores:

            
            graph = {'nodes' : itr_data['nodes'] + ['deltaP', 'T_cyc-T_reg'],
                     'edges' : itr_data['edges'] + cluster_edges,
                    'dummy vars' : [], # there is one but irrelevant at this point
                    'forbidden' : forbid_edges}
            fges_obj = run_fges(graph, data, 'hi')
            fges_obj.run_fges_ctrl()
            added_edges = fges_obj.edges_cat['data'] + fges_obj.edges_cat['undirected']
            new_data.append([added_edges, fges_obj.best_score])

        for itr in range(len(best_graph_scores)):

            best_graph_scores[itr]['cluster mode'] = new_data[itr]

        return best_graph_scores



    def rigorous_mode(best_graph_scores, data, forbid_edges):

        rigorous_edges = []




    @staticmethod
    def write_cross_unit_graph(data_store, mode, filepath):

        wb = Workbook()
        for itr_data in data_store:
            
            sheet = wb.create_sheet(title=str(itr_data['combination']))
                
            nodes = itr_data['nodes'] + ['deltaP', 'T_cyc-T_reg']
            edges = itr_data['edges']

            for itr, itr_node in enumerate(nodes, start=1):

                sheet.cell(row=itr, column=1, value=itr_node)

            for itr, itr_edge in enumerate(edges, start=1):

                sheet.cell(row=itr, column=2, value=itr_edge[0])
                sheet.cell(row=itr, column=3, value=itr_edge[1])

            for itr, itr_edge in enumerate(itr_data[mode][0], start=1):

                sheet.cell(row=itr, column=4, value=itr_edge[0])
                sheet.cell(row=itr, column=5, value=itr_edge[1])

            sheet.cell(row=1, column=6, value='graph score')
            sheet.cell(row=1, column=7, value=itr_data[mode][1])

        
        wb.save(filepath)


    @staticmethod
    def read_cross_unit_graph(filepath):

        wb = load_workbook(filepath)
        sheets = wb.sheetnames

        data_store = []
        for itr_sheet in sheets[1:]:

            nodes = []
            edges = []
            cross_unit = []

            sheet_obj = wb[itr_sheet]
            for itr_row_num, itr_row in enumerate(sheet_obj.iter_rows(values_only=True)):

                if itr_row_num == 0:

                    graph_score = itr_row[6]
 

                if itr_row[0]:
                    nodes.append(itr_row[0])
                if itr_row[1] and itr_row[2]:
                    edges.append((itr_row[1], itr_row[2]))
                if itr_row[3] and itr_row[4]:
                    cross_unit.append((itr_row[3], itr_row[4]))

            graph_store = {'combination' : itr_sheet,
                           'score' : graph_score,
                           'nodes' : nodes,
                           'edges' : edges,
                           'cross unit' : cross_unit}

            
            data_store.append(graph_store)

        return data_store
                    

    @staticmethod
    def compile_knowledge_graphs(top_three_score, data):

        units = list(top_three_score.keys())
        comb = list(product(*(range(2) for _ in units)))

        whole_graph_score = []
        for itr_comb in comb:

            graph_data = {'combination' : itr_comb,
                        'nodes' : [],
                        'edges' : []}
            
            for itr, itr_place in enumerate(itr_comb):

                unit = units[itr]
                unit_graph = top_three_score[unit][itr_place][0]['graph']
                graph_data['nodes'].extend(unit_graph['nodes'])
                graph_data['edges'].extend(top_three_score[unit][itr_place][0]['edges cat']['knowledge'])

            # Add flash sensors
            graph_data['nodes'].extend(['V9', 'F_ln'])
            graph_data['edges'].extend([('V9', 'F_ln')])

            graph_data['nodes'] = list(set(graph_data['nodes']))
            graph_data['edges'] = list(set(graph_data['edges'])) 


            cyc_obj = handle_cycles(graph_data, 'hi', 'hi')
            cyc_obj.handle_cycles_ctrl()


            # All loops go through F_rgc so direct all parents to a dummy
            graph_data['nodes'].append('F_rgc_DUMMY')
            for itr_cycle_edge in cyc_obj.cycle_edges:

                if itr_cycle_edge[1] == 'F_rgc':

                    graph_data['edges'].remove(itr_cycle_edge)
                    graph_data['edges'].append((itr_cycle_edge[0], 'F_rgc_DUMMY'))


            
            # # Sorting out the F7 <--> P2
            # if ('P2', 'F7') in graph_data['edges'] and ('F7', 'P2') in graph_data['edges']:

            #     P2_parents = []
            #     F7_parents = []
            #     for itr_edge in graph_data['edges']:

            #         if itr_edge[1] == 'P2':

            #             P2_parents.append(itr_edge[0])

            #         elif itr_edge[1] == 'F7':

            #             F7_parents.append(itr_edge[0])
                        

            #     trim_P2_parents = [parent for parent in P2_parents if parent != 'F7']
            #     P2_child_graph = {'nodes' : ['P2']+P2_parents,
            #                     'edges' : [(parent, 'P2') for parent in P2_parents],
            #                     'dummy vars' : [],
            #                     'forbidden' : []}
            #     fges_obj = run_fges(P2_child_graph, data, 'score kn')
            #     fges_obj.remove_no_variance()
            #     P2_score_prior = fges_obj.local_score(['P2'] , P2_parents)
            #     P2_score_after = fges_obj.local_score(['P2'] , trim_P2_parents)
            #     P2_penalty = P2_score_prior - P2_score_after

            #     trim_F7_parents = [parent for parent in F7_parents if parent != 'P2']
            #     F7_child_graph = {'nodes' : ['F7']+F7_parents,
            #                     'edges' : [(parent, 'F7') for parent in F7_parents],
            #                     'dummy vars' : [],
            #                     'forbidden' : []}
            #     fges_obj = run_fges(F7_child_graph, data, 'score kn')
            #     fges_obj.remove_no_variance()
            #     F7_score_prior = fges_obj.local_score(['F7'] , F7_parents)
            #     F7_score_after = fges_obj.local_score(['F7'] , trim_F7_parents)
            #     F7_penalty = F7_score_prior - F7_score_after

            #     if F7_penalty < P2_penalty:

            #         graph_data['edges'].remove(('P2', 'F7'))

            #     elif F7_penalty > P2_penalty:

            #         graph_data['edges'].remove(('F7', 'P2'))

            #     else:

            #         raise ValueError('GIVE UP NOW')

            cyc_obj = handle_cycles(graph_data, 'hi', 'hi')
            cyc_obj.handle_cycles_ctrl()

            if cyc_obj.cycle_edges:

                print(cyc_obj.cycle_edges)

            whole_graph_score.append(graph_data)

        return whole_graph_score



    @staticmethod
    def forbid_unit_edges(forbid_edges):

        # backwards forbids
        backwards_store = {}

        node_tiers = {}
        node_tiers['exclude'] = [('F_rgc', 'L_sp') , ('F_sg', 'P6')]
        node_tiers['out'] = ['T_cyc', 'C_co', 'F_sg', 'C_o2', 'F_rgc', 'V7', 'V2']
        node_tiers['unit'] = ['T_reg', 'L_sp', 'P6']
        node_tiers['in'] = ['F7', 'F_sc', 'V6', 'V3', 'P2']
        backwards_store['reg'] = node_tiers

        node_tiers = {}
        node_tiers['exclude'] = [('F_sc', 'T_r')]
        node_tiers['out'] = ['F_sc', 'V3']
        node_tiers['unit'] = ['P4', 'T_r']
        node_tiers['in'] = ['F_rgc', 'V2', 'T2', 'F3']
        backwards_store['react'] = node_tiers

        node_tiers = {}
        node_tiers['exclude'] = [('F_slurry', 'T_20') , ('F_lco', 'T_20') , ('F_hn', 'T_10')]
        node_tiers['out'] = ['F_slurry', 'F_lco', 'F_hn', 'V11', 'V10']
        node_tiers['unit'] = ['T_20', 'T_10', 'T_fra', 'P5']
        node_tiers['in'] = ['F_reflux', 'V8']
        backwards_store['frac'] = node_tiers

        node_tiers = {}
        node_tiers['exclude'] = []
        node_tiers['out'] = ['T2']
        node_tiers['unit'] = ['T3']
        node_tiers['in'] = ['T1', 'F3', 'F5', 'V1']
        backwards_store['furn'] = node_tiers
    
        for unit in backwards_store.values():

            node_tiers_names = ['out', 'unit', 'in']
            for itr_tier in range(len(node_tiers_names)-1):

                curr_tier = node_tiers_names[itr_tier]
                next_tiers = node_tiers_names[itr_tier+1:]
                for itr_next_tier in next_tiers:
                    
                    for itr_tier_node in node_tiers[curr_tier]:

                        forbid_edges.extend([(itr_tier_node, next_tier_node) for next_tier_node in node_tiers[itr_next_tier] if (itr_tier_node, next_tier_node) not in unit['exclude']])

        #cab
        forbid_edges.extend([('ACAB', 'P1') , ('F7', 'P1') , 
                            ('P2', 'P1') , ('V6', 'P1') , ('V6', 'ACAB')])
        

        # forbid diff streams
        #reg
        forbid_edges.extend([('F7', 'F_sc') , ('F_sc', 'F7') , ('P2', 'F_sc') , ('F_sc', 'P2') , ('V6', 'F_sc') , 
                                    ('V3', 'F7') , ('V7', 'F_rgc') , ('V2', 'F_sg') , ('V2', 'T_cyc') , 
                                    ('V2', 'C_co') , ('V2', 'C_o2') ,
                                    ('T_cyc','F_rgc') , ('C_co','F_rgc') , 
                                    ('C_o2', 'F_rgc') , ('F_sg', 'F_rgc') , ('F_rgc', 'T_cyc') , 
                                    ('F_rgc', 'X_co') , ('F_rgc', 'C_o2') , ('F_rgc', 'F_sg')])
        #react
        forbid_edges.extend([('T2', 'F_rgc') , ('F_rgc', 'T2') , ('T2', 'V2') , ('V2', 'T2') , 
                                       ('F3', 'F_rgc') , ('F_rgc', 'F3') , ('F3', 'V2') , ('V2', 'F3')])
        #furn
        forbid_edges.extend([('T1', 'F5') , ('F5', 'T1') , ('F3', 'F5') , ('F5', 'F3') , 
                                       ('V1', 'T1') , ('V1', 'F3')])
        #frac
        forbid_edges.extend([('F_hn', 'F_lco') , ('F_lco', 'F_hn') , 
                                       ('F_hn', 'F_slurry') , ('F_slurry', 'F_hn') ,
                                       ('F_lco', 'F_slurry') , ('F_slurry', 'F_lco') , 
                                       ('V10' , 'F_lco') , ('V10' , 'F_slurry') , 
                                       ('V11' , 'F_hn') , ('V11' , 'F_slurry')])
        
        return forbid_edges
        

    @staticmethod
    def compare_cul_modes(modes):

        for mode_name, itr_mode in modes.items():

            combination = []
            score = []
            for itr_comb in itr_mode:

                combination.append(itr_comb['combination'])
                score.append(itr_comb['score'])

            plt.plot(combination, score, label=mode_name)

        plt.xlabel('combination')
        plt.ylabel('score')
        plt.legend()
        plt.xticks(rotation='vertical')
        plt.show()


    @staticmethod
    def run_fges_no_knowledge(data, forbid_edges):

        unit_sensors = {'cab' : ['P1', 'F7', 'P2', 'ACAB', 'V6'],
                'reg' : ['F7', 'P2', 'V6', 'T_reg', 'L_sp', 'P6', 'F_sg', 'T_cyc', 'C_co', 'C_o2', 'V7', 'F_rgc', 'V2', 'F_sc', 'V3'],
                'react' : ['F_sc', 'V3', 'F_rgc', 'V2', 'F3', 'T2', 'T_r', 'P4'],
                'furn' : ['F3', 'T1', 'F5', 'V1', 'T3', 'T2'],
                'distil' : ['T_20', 'T_10', 'T_fra', 'P5', 'F_slurry', 'F_lco', 'V11', 'F_hn', 'V10', 'F_reflux', 'V8'],
                'wgc' : ['V4', 'AWGC', 'F_lpg'],
                'flash' : ['V9', 'F_ln']}
        nodes = []
        for itr in unit_sensors.values():
            nodes += list(itr)

        graph = {'nodes' : nodes + ['deltaP', 'T_cyc-T_reg'],
                    'edges' : [],
                'dummy vars' : [], # there is one but irrelevant at this point
                'forbidden' : forbid_edges}
        fges_obj = run_fges(graph, data, 'hi')
        fges_obj.run_fges_ctrl()

        return nodes, fges_obj.best_dag, fges_obj.best_score
        

    @staticmethod
    def write_no_knowledge_graph(graph, score, filepath):

        wb = Workbook() 
        sheet = wb.active
        nodes = graph['nodes']
        edges = graph['edges']

        for itr, itr_node in enumerate(nodes, start=1):

            sheet.cell(row=itr, column=1, value=itr_node)

        for itr, itr_edge in enumerate(edges, start=1):

            sheet.cell(row=itr, column=2, value=itr_edge[0])
            sheet.cell(row=itr, column=3, value=itr_edge[1])

        sheet.cell(row=1, column=4, value='graph score')
        sheet.cell(row=1, column=5, value=score)

        wb.save(filepath)


    def get_mode_gt_similarity_score(modes, ground_truth):

        new_modes = {}
        for itr_mode, itr_comb in modes.items():

            data_store = itr_comb

            for itr in range(len(data_store)):

                data_store[itr]['graph'] = {'nodes' : data_store['nodes'],
                                            'edges' : data_store['edges'] + data_store['cross unit']}

            _, overall_metric, pc_match, pc_mismatch = analyse_graphs.find_top_three_closest_to_gt(data_store, ground_truth)

            for itr in range(len(data_store)):

                del data_store[itr]['graph']
                data_store[itr]['overall metric'] = overall_metric[itr]
                data_store[itr]['pc match'] = pc_match[itr]
                data_store[itr]['pc mismatch'] = pc_mismatch[itr]

            new_modes[itr_mode] = data_store




    def plot_whole_graph(nodes, kn, data):

        plt.figure(figsize=[10, 10])
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        graph.add_edges_from(kn+data)
        pos = nx.circular_layout(graph)
        nx.draw_networkx_edges(graph, pos, edgelist=kn, edge_color='black', width=2)
        nx.draw_networkx_edges(graph, pos, edgelist=data, edge_color='red', width=2)
        nx.draw_networkx_nodes(graph, pos, node_color='black')
        nx.draw_networkx_labels(graph, pos, font_color='blue')
        nx.draw(graph, pos=pos)
        plt.show()

            
