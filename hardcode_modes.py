
nodes = ['v_9/prod_lightnaptha.F_ln', 'distil_1/prod_slurry.F_slurry', 'comp_1/v_6.F_7', 'react_1.L_sp', 'Pos_7', 'Pos_3', 'comp_2/prod_lpg.F_lpg', 'Pos_8', 'react_1/v_2.F_rgc', 
         'feed_feedstream/furn_1.F_3', 'Pos_1', 'react_2/v_3.F_sc', 'feed_air/comp_1.P_1', 'v_11/prod_lightoil.F_lco', 'comp_1/v_6.P_2', 'react_1.T_reg', 'distil_1.T_20', 'AWGC', 
         'distil_1.P_5', 'feed_feedstream/furn_1.T_1', 'v_7/prod_stack.X_co2', 'furn_1/react_2.T_2', 'distil_1.T_fra', 'Pos_2', 'ACAB', 'react_2.P_4', 'react_2.T_r', 
         'react_1/v_7.T_cyc', 'v_8/distil_1.F_reflux', 'v_10/prod_heavynaptha.F_hn', 'Pos_11', 'react_1.P_6', 'distil_1.T_10', 'feed_fuel/v_1.F_5', 'furn_1.T_3', 'Pos_6', 'Pos_10', 
         'react_1/v_7.F_sg', 'Pos_9', 'v_7/prod_stack.X_co', 'Pos_4']



# Vessels - sequential, reactions - reactants, flow through - param controlled (no difference), cross unit links - none
g1 = {}
g1['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g1['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g1['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('react_2/v_3.F_sc', 'react_1.T_reg'), ('react_2/v_3.F_sc', 'react_1.L_sp'), 
           ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), ('react_1.L_sp', 'react_1/v_2.F_rgc'), 
           ('react_1.P_6', 'react_1/v_7.F_sg'), ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2')]
g1['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g1['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g1['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g1['v_1'] = ('Pos_1', 'feed_fuel/v_1.F_5')
g1['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g1['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
           ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g1['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g1['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g1['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g1['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g1['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g1['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]



# Vessels - in and out controlling, reactions - reactants (no edges), flow through - param controlled (no difference), cross unit links - none
g2 = {}
g2['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g2['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g2['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('react_2/v_3.F_sc', 'react_1.T_reg'), ('react_2/v_3.F_sc', 'react_1.L_sp'), 
           ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), ('react_1/v_2.F_rgc', 'react_1.L_sp'), 
           ('react_1/v_7.F_sg', 'react_1.P_6'), ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2')]
g2['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g2['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g2['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g2['v_1'] = ('Pos_1', 'feed_fuel/v_1.F_5')
g2['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g2['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
                 ('feed_feedstream/furn_1.F_3', 'react_2.P_4'), ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc')]
g2['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g2['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g2['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g2['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g2['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g2['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]



# Vessels - in controlling, reactions - reactants (no edges), flow through - param controlled (no difference), cross unit links - none
g3 = {}
g3['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g3['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g3['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('comp_1/v_6.F_7', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1.T_reg'), 
                 ('react_2/v_3.F_sc', 'react_1.L_sp'), ('react_2/v_3.F_sc', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'),
                 ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), 
                 ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2')]
g3['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g3['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g3['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g3['v_1'] = [('Pos_1', 'feed_fuel/v_1.F_5')]
g3['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g3['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
                 ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g3['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g3['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g3['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g3['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g3['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g3['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]



# Vessels - direct and indirect (unit controlled), reactions - reactants (no edges), flow through - param controlled (no difference), cross unit links - none
g4 = {}
g4['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g4['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g4['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('comp_1/v_6.F_7', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1.T_reg'), 
                 ('react_2/v_3.F_sc', 'react_1.L_sp'), ('react_2/v_3.F_sc', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'),
                 ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), 
                 ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2'), ('react_1.P_6', 'react_1/v_7.F_sg'), ('react_1.L_sp', 'react_1/v_2.F_rgc')]
g4['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g4['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g4['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g4['v_1'] = [('Pos_1', 'feed_fuel/v_1.F_5')]
g4['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g4['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
                 ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g4['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g4['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g4['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g4['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g4['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g4['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]



# Vessels - direct and indirect (out controlled), reactions - reactants (no edges), flow through - param controlled (no difference), cross unit links - none
g5 = {}
g5['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g5['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g5['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('comp_1/v_6.F_7', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1.T_reg'), 
                 ('react_2/v_3.F_sc', 'react_1.L_sp'), ('react_2/v_3.F_sc', 'react_1/v_7.F_sg'), ('react_2/v_3.F_sc', 'react_1/v_2.F_rgc'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'),
                 ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), 
                 ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2'), ('react_1/v_7.F_sg', 'react_1.P_6'), ( 'react_1/v_2.F_rgc', 'react_1.L_sp')]
g5['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g5['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g5['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g5['v_1'] = [('Pos_1', 'feed_fuel/v_1.F_5')]
g5['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g5['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
                 ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g5['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g5['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g5['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g5['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g5['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g5['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]




# Vessels - sequential, reactions - reactants, flow through - param controlled (no difference), cross unit links - cluster
g6 = {}
g6['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g6['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g6['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('react_2/v_3.F_sc', 'react_1.T_reg'), ('react_2/v_3.F_sc', 'react_1.L_sp'), 
           ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), ('react_1.L_sp', 'react_1/v_2.F_rgc'), 
           ('react_1.P_6', 'react_1/v_7.F_sg'), ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2')]
g6['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g6['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g6['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g6['v_1'] = ('Pos_1', 'feed_fuel/v_1.F_5')
g6['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g6['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
           ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g6['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g6['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g6['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g6['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g6['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g6['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]
g6['cross_unit'] = [('react_2.P_4', 'distil_1.P_5'), ('distil_1.P_5', 'AWGC'), ('distil_1.P_5', 'comp_2/prod_lpg.F_lpg'), ('distil_1.P_5', 'v_9/prod_lightnaptha.F_ln'),
                    ('distil_1.P_5', 'v_8/distil_1.F_reflux'), ('distil_1.T_fra', 'comp_2/prod_lpg.F_lpg'), ('distil_1.T_fra', 'v_9/prod_lightnaptha.F_ln'),
                    ('distil_1.T_fra', 'v_8/distil_1.F_reflux')]



# Vessels - sequential, reactions - reactants, flow through - param controlled (no difference), cross unit links - general
g7 = {}
g7['comp_1'] = [('feed_air/comp_1.P_1', 'ACAB'), ('comp_1/v_6.P_2', 'ACAB'), ('ACAB', 'comp_1/v_6.P_2')]
g7['v_6'] = [('Pos_6', 'comp_1/v_6.P_2'), ('comp_1/v_6.P_2', 'comp_1/v_6.F_7')]
g7['react_1'] = [('comp_1/v_6.F_7', 'react_1.T_reg'), ('comp_1/v_6.F_7', 'react_1.P_6'), ('react_2/v_3.F_sc', 'react_1.T_reg'), ('react_2/v_3.F_sc', 'react_1.L_sp'), 
           ('react_1.T_reg', 'react_1/v_7.T_cyc'), ('react_1.T_reg', 'v_7/prod_stack.X_co'), ('react_1.T_reg', 'v_7/prod_stack.X_co2'), ('react_1.L_sp', 'react_1/v_2.F_rgc'), 
           ('react_1.P_6', 'react_1/v_7.F_sg'), ('react_1.P_6', 'v_7/prod_stack.X_co'), ('react_1.P_6', 'v_7/prod_stack.X_co2')]
g7['v_7'] = [('Pos_7', 'react_1/v_7.F_sg')]
g7['v_2'] = [('Pos_2', 'react_1/v_2.F_rgc')]
g7['v_3'] = [('Pos_3', 'react_2/v_3.F_sc')]
g7['v_1'] = ('Pos_1', 'feed_fuel/v_1.F_5')
g7['furn_1'] = [('feed_feedstream/furn_1.F_3', 'furn_1/react_2.T_2'), ('feed_feedstream/furn_1.T_1', 'furn_1/react_2.T_2'), ('feed_fuel/v_1.F_5', 'furn_1.T_3'), 
          ('furn_1.T_3', 'furn_1/react_2.T_2')]
g7['react_2'] = [('furn_1/react_2.T_2', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2.T_r'), ('react_1/v_2.F_rgc', 'react_2/v_3.F_sc'), ('feed_feedstream/furn_1.F_3', 'react_2.T_r'), 
           ('feed_feedstream/furn_1.F_3', 'react_2.P_4')]
g7['distil_1'] = [('distil_1.P_5', 'distil_1/prod_slurry.F_slurry'), ('distil_1.P_5', 'v_11/prod_lightoil.F_lco'), ('distil_1.P_5', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_fra', 'distil_1.T_10'), ('distil_1.T_10', 'distil_1.T_fra'), ('distil_1.T_10', 'distil_1.T_20'), ('distil_1.T_10', 'v_10/prod_heavynaptha.F_hn'), 
            ('distil_1.T_20', 'distil_1.T_10'), ('distil_1.T_20', 'distil_1/prod_slurry.F_slurry'), ('distil_1.T_20', 'v_11/prod_lightoil.F_lco'), 
            ('v_8/distil_1.F_reflux', 'distil_1.T_fra')]
g7['v_4'] = [('Pos_4', 'comp_2/prod_lpg.F_lpg')]
g7['v_9'] = [('Pos_9', 'v_9/prod_lightnaptha.F_ln')]
g7['v_8'] = [('Pos_8', 'v_8/distil_1.F_reflux')]
g7['v_10'] = [('Pos_10', 'v_10/prod_heavynaptha.F_hn')]
g7['v_11'] = [('Pos_11', 'v_11/prod_lightoil.F_lco')]
g7['cross_unit'] = [('comp_1/v_6.P_2', 'react_1.P_6'), ('react_1.T_reg', 'react_2.T_r'), ('react_2.T_r', 'react_1.T_reg'), ('react_2.T_r', 'distil_1.T_20'),
                    ('react_2.P_4', 'distil_1.P_5'), ('distil_1.P_5', 'AWGC'), ('distil_1.P_5', 'comp_2/prod_lpg.F_lpg'), 
                    ('distil_1.P_5', 'v_9/prod_lightnaptha.F_ln'), ('distil_1.P_5', 'v_8/distil_1.F_reflux'), ('distil_1.T_fra', 'comp_2/prod_lpg.F_lpg'), 
                    ('distil_1.T_fra', 'v_9/prod_lightnaptha.F_ln'), ('distil_1.T_fra', 'v_8/distil_1.F_reflux')]



graph = []
for itr_edges in g4.values():

    graph.extend(itr_edges)


import pandas as pd

data = pd.read_csv('NOC_stableFeedFlow_outputs.csv')
additional_vars = ['Time', 'T_atm', 'deltaP', 'Fair', 'T_cyc-T_reg', 'FV11']
data = data.drop(columns = additional_vars)

var_mapping = {
                'feed_air/comp_1.P_1' : 'P1',
                'comp_1/v_6.F_7' : 'F7',
                'comp_1/v_6.P_2' : 'P2',
                'react_1.T_reg' : 'T_reg',
                'react_1.L_sp' : 'L_sp',
                'react_1.P_6' : 'P6',
                'react_1/v_7.F_sg' : 'F_sg',
                'react_1/v_7.T_cyc' : 'T_cyc',
                'v_7/prod_stack.X_co' : 'C_cosg',
                'v_7/prod_stack.X_co2' : 'C_co2sg',
                'react_1/v_2.F_rgc' : 'F_rgc',
                'react_2.T_r' : 'T_r',
                'react_2.P_4' : 'P4',
                'react_2/v_3.F_sc' : 'F_sc',
                'feed_feedstream/furn_1.F_3' : 'F3',
                'feed_feedstream/furn_1.T_1' : 'T1',
                'feed_fuel/v_1.F_5' : 'F5',
                'furn_1.T_3' : 'T3',
                'furn_1/react_2.T_2' : 'T2',
                'distil_1.T_20' : 'T_20',
                'distil_1.T_10' : 'T_10',
                'distil_1.T_fra' : 'T_fra',
                'distil_1.P_5' : 'P5',
                'v_11/prod_lightoil.F_lco' : 'F_LCO',
                'v_10/prod_heavynaptha.F_hn' : 'F_HN',
                'v_9/prod_lightnaptha.F_ln' : 'F_LN',
                'v_8/distil_1.F_reflux' : 'F_Reflux',
                'comp_2/prod_lpg.F_lpg' : 'F_LPG',
                'distil_1/prod_slurry.F_slurry' : 'F_Slurry',
                'ACAB' : 'ACAB',
                'AWGC' : 'AWGC',
                'Pos_1' : 'V1',
                'Pos_2' : 'V2',
                'Pos_3' : 'V3',
                'Pos_4' : 'V4',
                'Pos_6' : 'V6',
                'Pos_7' : 'V7',
                'Pos_8' : 'V8',
                'Pos_9' : 'V9',
                'Pos_10' : 'V10',
                'Pos_11' : 'V11',
                }






from run_BIC import run_BIC

BIC = run_BIC(graph, data, var_mapping)
BIC.calc_BIC()
























