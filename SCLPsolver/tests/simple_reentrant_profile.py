# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
proj = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
sys.path.append(proj)
from SCLP import SCLP, SCLP_settings
from doe.data_generators.simple_reentrant_gideon import generate_simple_reentrant_data
from doe.doe_utils import path_utils





K = 1000
I = 200
solver_settings = SCLP_settings()
solver_settings.suppress_printing = True
solver_settings.memory_management = False
settings = {"c_scale": 0, "cost_scale": 10, "alpha_rate1": 0.6, "alpha_rate2": 0.45}
import time
import cProfile, pstats, io
pr = cProfile.Profile()
for seed in range(1000, 1010):
    G, H, F, gamma, c, d, alpha, a, b, TT, total_buffer_cost, buffer_cost = generate_simple_reentrant_data(seed, K, I, **settings)
    start_time = time.time()
    pr.enable()
    solution, STEPCOUNT, param_line, res = SCLP(G, H, F, a, b, c, d, alpha, gamma, TT, solver_settings)
    t, x, q, u, p, pivots, obj, err, NN, tau, maxT = solution.get_final_solution(False)
    pr.disable()
    print(obj, err)
    print("--- %s seconds ---" % (time.time() - start_time))
s = io.StringIO()
ps = pstats.Stats(pr, stream=s)
ps.print_stats()
print(s.getvalue())