
from tools import tools
import re

class model_distil:

    def __init__(model, graph, unit):

        model.unit_name = unit
        model.unit_sensors = graph.unit_sensors[unit]
        model.config = graph.configuration[unit] 
        model.adj_mat = graph.adj_mat
        model.stream_tags_rev = {value : key for key, value in model.config['stream tags'].items()}

    
    def model_ctrl(model):

        # Determine latent stucture from column configuration
        model.init_sensor_stores()
        model.order_unit_sensors()
        model.split_TP_sensors()
        model.feed_stream()
        model.reflux_stream()
        model.reboil_stream()
        model.product_streams()
        model.no_reboil_reflux()

        # Get sensors and build actual structure 
        model.get_in_out_sensors('in')
        model.get_in_out_sensors('out')
        model.get_L_sensor()
        model.latent_adj_mat = tools.build_adj_mat(model.all_sensors, model.latent_struct)
        model.actual_structure = tools.build_actual_structure(model.latent_adj_mat, model.present_sensors)


    def init_sensor_stores(model):

        # Hardcode definite relationships 
        model.all_sensors = ['F_feed', 'T_feed', 'P_feed', 'L_unit', 'F_top', 'T_top', 'P_top', 'F_bot', 'T_bot', 'P_bot']
        model.latent_struct = [('L_unit', 'F_bot') , ('L_unit', 'P_bot') , ('F_feed', 'L_unit')]

        # Init other sensor stores
        model.composition_edges = []
        model.present_sensors = []
        model.sensor_name_mapping = {}


    def order_unit_sensors(model):

        TP_sensors = [sensor for sensor in model.unit_sensors['unit'] if not re.search(r'.L_', sensor)]
        sensor_locations = [model.config['sensor locations'][sensor] for sensor in TP_sensors]
        ordered_sensor_store = sorted(zip(TP_sensors, sensor_locations), key=lambda x: x[1])
        model.ordered_sensors = [sens[0] for sens in ordered_sensor_store]
        model.ordered_loations = [sens[1] for sens in ordered_sensor_store]


    def split_TP_sensors(model):

        model.ordered_P_sens = []
        model.local_P_sens = []
        model.ordered_T_sens = []
        model.local_T_sens = []
        for itr, itr_sens in enumerate(model.ordered_sensors):

            if re.search(r'.P_', itr_sens):

                model.ordered_P_sens.append(itr_sens)
                model.local_P_sens.append('P_unit' + str(model.ordered_loations[itr]))

            elif re.search(r'.T_', itr_sens):

                model.ordered_T_sens.append(itr_sens)
                model.local_T_sens.append('T_unit' + str(model.ordered_loations[itr]))


        # Adjust sensor stores
        model.all_sensors.extend(model.local_P_sens)
        model.all_sensors.extend(model.local_T_sens)
        model.present_sensors.extend(model.local_P_sens)
        model.present_sensors.extend(model.local_T_sens)
        model.sensor_name_mapping = model.sensor_name_mapping | {local : actual for local, actual in zip(model.local_P_sens, model.ordered_P_sens)}
        model.sensor_name_mapping = model.sensor_name_mapping | {local : actual for local, actual in zip(model.local_T_sens, model.ordered_T_sens)}


    def feed_stream(model):

        # Find the closest P sensor above feed stream 
        model.feed_adj_P_ind, model.feed_location = model.find_closest_ind('feed', model.ordered_P_sens, 'above')

        # Add in edges between pressure sensors from the feed to the top 
        model.latent_struct.extend([('F_feed', model.local_P_sens[model.feed_adj_P_ind]) , ('P_feed', model.local_P_sens[model.feed_adj_P_ind]) , (model.local_P_sens[0], 'P_top') , (model.local_P_sens[0], 'F_top')])
        model.composition_edges.extend([('X_feed', model.local_P_sens[model.feed_adj_P_ind]) , ('X_feed', 'L_unit') , (model.local_P_sens[0], 'X_top') , (model.local_P_sens[-1], 'X_bot')])
        for itr_P_sens_ind in range(model.feed_adj_P_ind):

            model.latent_struct.append((model.local_P_sens[itr_P_sens_ind+1] , model.local_P_sens[itr_P_sens_ind]))


    def reflux_stream(model):

        # If there is a reflux system on column 
        if any(tag == 'reflux' for tag in model.config['stream tags'].values()):

            model.reflux_flag = True 
            model.all_sensors.extend(['F_reflux', 'T_reflux', 'P_reflux'])

            # Find the closest T sensor below the reflux stream 
            closest_ind, _ = model.find_closest_ind('reflux', model.ordered_T_sens, 'below')

            # Add in edges between temp sensors from the reflux stream to the bottom
            model.latent_struct.extend([('F_reflux', model.local_T_sens[closest_ind]) , ('F_reflux', 'L_unit') , ('T_reflux', model.local_T_sens[closest_ind]) , (model.local_T_sens[-1], 'T_bot')])
            model.composition_edges.append((model.local_T_sens[-1], 'X_bot'))
            for itr_T_sens_ind in range(closest_ind, len(model.local_T_sens)-1):

                model.latent_struct.append((model.local_T_sens[itr_T_sens_ind] , model.local_T_sens[itr_T_sens_ind+1]))

        else:

            model.reflux_flag = False 


    def reboil_stream(model):

        # If there is a reboil system on column  
        if any(tag == 'reboil' for tag in model.config['stream tags'].values()):

            model.reboil_flag = True
            model.all_sensors.extend(['F_reboil', 'T_reboil', 'P_reboil']) 

            # Find the closest P sensor above the reboil stream 
            closest_ind, _ = model.find_closest_ind('reboil', model.ordered_P_sens, 'above')

            # Add in edges between pressure sensors from reboil stream to feed stream (feed to top already covered)
            model.latent_struct.extend([('F_reboil', model.local_P_sens[closest_ind]) , ('P_reboil', model.local_P_sens[closest_ind])])
            if closest_ind > model.feed_adj_P_ind:

                for itr_P_sens_ind in range(model.feed_adj_P_ind, closest_ind):

                    model.latent_struct.append((model.local_P_sens[itr_P_sens_ind+1] , model.local_P_sens[itr_P_sens_ind]))

            # Find the closest T sensor above the reboil stream 
            closest_ind, _ = model.find_closest_ind('reboil', model.ordered_T_sens, 'above')

            # Add in edges between temp sensors from reboil stream to top stream
            model.latent_struct.extend([('F_reboil', model.local_T_sens[closest_ind]) , ('T_reboil', model.local_T_sens[closest_ind]) , (model.local_T_sens[0] , 'T_top')])
            model.composition_edges.append((model.local_T_sens[0] , 'X_top'))
            for itr_T_sens_ind in range(closest_ind):

                model.latent_struct.append((model.local_T_sens[itr_T_sens_ind+1] , model.local_T_sens[itr_T_sens_ind]))

        else:

            model.reboil_flag = False 


    def product_streams(model):

        # For every product stream 
        outlet_stream_dest = model.adj_mat.columns[model.adj_mat.loc[model.unit_name] == 1]
        for itr_dest_unit in outlet_stream_dest:

            stream_name = f'{model.unit_name}/{itr_dest_unit}'
            stream_tag = model.config['stream tags'][stream_name]
            if stream_tag == 'prod':

                # Create latent sensors for current product stream 
                stream_location = model.config['stream locations'][stream_name]
                F_sens = 'F_prod' + str(stream_location)
                P_sens = 'P_prod' + str(stream_location)
                T_sens = 'T_prod' + str(stream_location)
                model.all_sensors.extend([F_sens, P_sens, T_sens])

                # Find closest P sensor
                closest_sens = [0, abs(stream_location - model.config['sensor locations'][model.ordered_P_sens[0]])]
                for itr, itr_P_sens in enumerate(model.ordered_P_sens[1:], start = 1):

                    curr_dist = abs(stream_location - model.config['sensor locations'][itr_P_sens])
                    if curr_dist < closest_sens[1]:

                        closest_sens[0] = itr
                        closest_sens[1] = curr_dist

                closest_P_sens = model.local_P_sens[closest_sens[0]]

                # Find closest T sensor
                closest_sens = [0, abs(stream_location - model.config['sensor locations'][model.ordered_T_sens[0]])]
                for itr, itr_T_sens in enumerate(model.ordered_T_sens[1:], start = 1):

                    curr_dist = abs(stream_location - model.config['sensor locations'][itr_T_sens])
                    if curr_dist < closest_sens[1]:

                        closest_sens[0] = itr
                        closest_sens[1] = curr_dist

                closest_T_sens = model.local_T_sens[(closest_sens[0])]

                # Assign edges between closest T and P unit sensors and product stream sensors 
                model.latent_struct.extend([(closest_P_sens, F_sens) , (closest_T_sens, F_sens) , (closest_P_sens, P_sens) , (closest_T_sens, T_sens)])
                model.composition_edges.extend([(closest_P_sens, 'X_prod'+str(stream_location)) , (closest_T_sens, 'X_prod'+str(stream_location))])


    def no_reboil_reflux(model):

        # If there is no reboil or reflux the feed will affect temperature
        if not model.reboil_flag and not model.reflux_flag:

            # Find the index of the temp sensors that are closest above and below the feed stream
            for itr, itr_T_sens in enumerate(model.ordered_T_sens):

                curr_T_sens_loc = model.config['sensor locations'][itr_T_sens]
                if curr_T_sens_loc < model.feed_location:

                    closest_above_ind = itr

                elif curr_T_sens_loc == model.feed_location:

                    closest_above_ind = itr
                    closest_below_ind = itr
                    break

                elif curr_T_sens_loc > model.feed_location:

                    closest_below_ind = itr
                    break

            # Connect feed temp to closest temp sensors 
            if closest_above_ind == closest_below_ind:

                model.latent_struct.append(('T_feed', model.local_T_sens[closest_above_ind]))

            else:

                model.latent_struct.extend([('T_feed', model.local_T_sens[closest_above_ind]) , ('T_feed', model.local_T_sens[closest_below_ind])])

            # Add in edges connecting unit temp sensors to top and bottom temps 
            model.latent_struct.extend([(model.local_T_sens[0], 'T_top') , (model.local_T_sens[-1], 'T_bot')])
            model.composition_edges.extend([(model.local_T_sens[0], 'X_top') , (model.local_T_sens[-1], 'X_bot')])

            # Add edges between temp sensors above feed 
            for itr_T_sens_ind in range(closest_above_ind):

                curr_T_sens = model.local_T_sens[itr_T_sens_ind]
                next_T_sens = model.local_T_sens[itr_T_sens_ind+1]
                model.latent_struct.append((next_T_sens, curr_T_sens))

            # Add edges between temp sensors below the feed 
            for itr_T_sens_ind in range(closest_below_ind, len(model.ordered_T_sens)):

                curr_T_sens = model.local_T_sens[itr_T_sens_ind]
                next_T_sens = model.local_T_sens[itr_T_sens_ind+1]
                model.latent_struct.append((curr_T_sens, next_T_sens))
    

    def get_in_out_sensors(model, stream):

        # For every in/out sensor
        sensors = model.unit_sensors[stream + ' streams']
        for itr_sens_tup in sensors:

            sensor_name = itr_sens_tup[0]
            next_unit = itr_sens_tup[1]

            # Stream name based on whether the stream is an inlet or outlet
            if stream == 'in':

                stream_name = f'{next_unit}/{model.unit_name}'
            else:
                stream_name = f'{model.unit_name}/{next_unit}'

            # Append stream location to tag if it is a product stream as there could be multiple
            stream_tag = model.config['stream tags'][stream_name]
            stream_location = model.config['stream locations'][stream_name]
            if stream_tag == 'prod':

                stream_tag += str(stream_location)

            # Check if sensor is F,T,P or X
            match = re.search(r'.(F|T|P)_', sensor_name)
            match_X = re.search(r'.X_', sensor_name)
            if match:
                
                local_sensor_name = match.group(1) + '_' + stream_tag 
                model.present_sensors.append(local_sensor_name)
                model.sensor_name_mapping[local_sensor_name] = sensor_name

            elif match_X:

                # Create specific local comp sensor name using the ID
                sens_id = sensor_name[match_X.span()[1]+1:]
                gen_comp_sens = 'X_' + stream_tag
                local_comp_sens = 'X_' + sens_id + stream_tag

                # For every composition edge using general names add in edges to latent struct using specific local sensor names 
                for itr_comp_edge in model.composition_edges:

                    if gen_comp_sens == itr_comp_edge[0]:

                        model.all_sensors.append(local_comp_sens)
                        model.latent_struct.append(local_comp_sens, itr_comp_edge[1])
                        model.present_sensors.append(local_comp_sens)
                        model.sensor_name_mapping[local_comp_sens] = sensor_name

                    elif gen_comp_sens == itr_comp_edge[1]:

                        model.all_sensors.append(local_comp_sens)
                        model.latent_struct.append(itr_comp_edge[1], local_comp_sens)  
                        model.present_sensors.append(local_comp_sens)
                        model.sensor_name_mapping[local_comp_sens] = sensor_name


    def get_L_sensor(model):

        for unit_sensor in model.unit_sensors['unit']:

            if re.search(r'.L_', unit_sensor):

                model.present_sensors.append('L_unit')
                model.sensor_name_mapping['L_unit'] = unit_sensor


    def find_closest_ind(model, stream_tag, sensors, direction):
        
        stream = model.stream_tags_rev[stream_tag]
        location = model.config['stream locations'][stream]
        for itr, itr_sens in enumerate(sensors):

            if location >= model.config['sensor locations'][itr_sens]:

                closest_ind = itr
                if direction == 'below':

                    break

        return closest_ind, location