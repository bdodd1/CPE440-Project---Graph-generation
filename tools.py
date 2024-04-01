
import pandas as pd

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