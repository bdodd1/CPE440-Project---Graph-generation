
import pandas as pd
from openpyxl import load_workbook


class tools:

    @staticmethod
    def build_adj_mat(nodes, edges):
    
        adj_mat = pd.DataFrame(0, columns=nodes, index = nodes)
        for itr_edge in edges:

            adj_mat.loc[itr_edge[0], itr_edge[1]] = 1

        return adj_mat


    @staticmethod
    def build_actual_structure(latent_adj_mat, present_sensors):

        actual_structure = []
        for itr_sensor in present_sensors:

            sensor_queue = latent_adj_mat.columns[latent_adj_mat.loc[itr_sensor] == 1].to_list()
            while sensor_queue:

                next_sensor = sensor_queue.pop(0)
                if next_sensor == itr_sensor:

                    continue

                if next_sensor in present_sensors:

                    actual_structure.append((itr_sensor, next_sensor))

                else:
                    sensor_queue.extend(latent_adj_mat.columns[latent_adj_mat.loc[next_sensor] == 1].to_list())


        return actual_structure
    

    @staticmethod
    def compare_graphs(files, store_location):

        graph_store = {}
        for itr, itr_graph in enumerate(files):

            filepath = rf'{store_location}\{itr_graph}.xlsx'
            nodes, edges = tools.read_graph_excel(filepath)
            graph_store[itr] = {}
            graph_store[itr]['nodes'] = nodes 
            graph_store[itr]['edges'] = edges 

        comparison = {}
        for itr, itr_graph in graph_store.items():

            for itr_comp in range(itr+1, len(files)):
            
                comparison = {'equivalent': [],
                                'reoriented' : [],
                                'additional' : []}

                for itr_edge in graph_store[itr]['edges']:

                    if itr_edge in graph_store[itr_comp]['edges']:

                        comparison['equivalent'].append(itr_edge)

                    elif (itr_edge[1], itr_edge[0]) in graph_store[itr_comp]['edges']:

                        comparison['reoriented'].append(itr_edge)

                    elif itr_edge not in graph_store[itr_comp]['edges']:

                        comparison['additional'].append(itr_edge)

                dropped_knowledge = []
                for itr_edge in graph_store[itr_comp]['edges']:

                    if itr_edge not in graph_store[itr]['edges'] and (itr_edge[1], itr_edge[0]) not in graph_store[itr]['edges']:

                        dropped_knowledge.append(itr_edge)

                print('-------------------------------------------------------------------------------------------------')
                print(f'Comparison - {itr} and {itr_comp}')
                print('-------------------------------------------------------------------------------------------------')
                print(f'Edges present in both: {comparison["equivalent"]}')
                print('*************************************************************************************************')
                print(f'Edges reoriented: {comparison["reoriented"]}')
                print('*************************************************************************************************')
                print(f'Edges not in {itr_comp}: {comparison["additional"]}')
                print('*************************************************************************************************')
                print(f'Edges not in {itr}: {dropped_knowledge}')
                print('*************************************************************************************************')
            


    @staticmethod
    def read_graph_excel(filepath):

        wb = load_workbook(filepath)
        ws = wb.active

        nodes = []
        edges = []

        for row in ws.iter_rows(values_only=True):
            nodes.append(row[0]) 
            edges.append((row[1], row[2]))  

        return nodes, edges
    
