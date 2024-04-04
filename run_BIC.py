
from pgmpy.estimators import BayesianEstimator
from pgmpy.models import BayesianNetwork
import math



class run_BIC:

    def __init__(model, graph, data, var_mapping):

        model.graph = graph
        model.data = data
        model.var_mapping = var_mapping

    
    def calc_BIC(model):

        bayes_net = []
        present_vars = []
        for itr_edge in model.graph['edges']:

            bayes_net.append((model.var_mapping[itr_edge[0]], model.var_mapping[itr_edge[1]]))
            present_vars.append(model.var_mapping[itr_edge[0]])
            present_vars.append(model.var_mapping[itr_edge[1]])

        present_vars = list(set(present_vars))
        vars_to_drop = [var for var in model.data.columns if var not in present_vars]
        model.data = model.data.drop(columns = vars_to_drop)

        bayes_net = BayesianNetwork(bayes_net)

        estimator = BayesianEstimator(bayes_net, model.data)
        bayes_net.fit(model.data, estimator=estimator)

        log_likelihood = bayes_net.log_likelihood(model.data)

        num_params = bayes_net.number_of_parameters()

        n = len(model.data)
        BIC = -2 * log_likelihood + num_params * math.log(n)
        print("BIC Score:", BIC)
