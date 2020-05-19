import sys
import os
proj = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
sys.path.append(proj)
from SCLP import SCLP, SCLP_settings
from doe.data_generators.simple_reentrant_gideon import generate_simple_reentrant_data
from doe.doe_utils import path_utils





K = 400
I = 20
seed = 1002
solver_settings = SCLP_settings()
solver_settings.suppress_printing = True
solver_settings.memory_management = False
settings = {"c_scale": 0, "cost_scale": 10, "alpha_rate1": 0.08, "alpha_rate2": 0.045}
import time
G, H, F, gamma, c, d, alpha, a, b, TT, total_buffer_cost, buffer_cost = generate_simple_reentrant_data(seed, K, I, **settings)
start_time = time.time()
solution, STEPCOUNT, Tres, res = SCLP(G, H, F, a, b, c, d, alpha, gamma, TT, solver_settings)
t, x, q, u, p, pivots, obj, err, NN, tau, maxT = solution.get_final_solution(False)
print(obj, err)
print("--- %s seconds ---" % (time.time() - start_time))