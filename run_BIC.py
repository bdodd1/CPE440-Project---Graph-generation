
from pgmpy.estimators import BayesianEstimator
from pgmpy.metrics import log_likelihood_score
from pgmpy.models import BayesianNetwork
import math



class run_BIC:

    def __init__(model, graph, data, var_mapping):

        model.graph = graph
        model.data = data
        model.var_mapping = var_mapping

    
    def calc_BIC(model):

        edges_col = [(model.var_mapping[itr_edge[0]], model.var_mapping[itr_edge[1]]) for itr_edge in model.graph['edges']]
        nodes_col = [model.var_mapping[sensor] for sensor in model.graph['nodes']]

        bayes_net = BayesianNetwork()
        bayes_net.add_nodes_from(nodes_col)
        bayes_net.add_edges_from(edges_col)

        # estimator = BayesianEstimator(bayes_net, model.data)
        # bayes_net.fit(model.data, estimator=BayesianEstimator, prior_type='BDeu')
        bayes_net.fit(model.data, n_jobs=4) 
 

        log_likelihood = log_likelihood_score(bayes_net, model.data)
        num_params = len(model.graph['nodes'])
        n = len(model.data)
        model.BIC_score = -2 * log_likelihood + num_params * math.log(n)
