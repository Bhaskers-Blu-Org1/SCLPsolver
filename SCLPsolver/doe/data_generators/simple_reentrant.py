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

import numpy as np

def generate_simple_reentrant_data(seed, K, I, h_rate1 = 0.08, h_rate2 = 0.045, hdist = np.random.rand, hdist_params = (), alpha_rate1 = 0.8, alpha_rate2 = 0.45,
                            alpha_dist = np.random.rand, alpha_dist_params = (), a_rate = 0.03, a_dist = np.random.rand, a_dist_params = (),
                            cost_scale = 0, cost_dist = np.random.rand,  cost_dist_params = (), last_cost = None, gamma_rate=0,
                            gamma_dist=np.random.rand, gamma_dist_params=(), c_scale = 5, c_dist = np.random.rand,  c_dist_params = ()):

    np.random.seed(seed)
    b = np.ones(I)
    G = np.eye(K) - np.diag(np.ones(K - 1), -1)

    # initial fluid
    cf = round(15 / K, 6)
    alpha_mean = np.arange(cf * (K+0.99), cf, -cf)
    alpha = alpha_rate1 * alpha_mean + alpha_rate2 * alpha_mean * alpha_dist(*alpha_dist_params, K)

    # exogenous input rate
    a_mean = a_rate * alpha_mean
    a = alpha_rate1 * a_mean + alpha_rate2 * a_mean * a_dist(*a_dist_params, K)

    # construct random machine constituency matrix
    cols = np.arange(K)
    rows = np.repeat(np.arange(I), int(K/I))
    H = np.zeros((I, K))
    h_mean = 1/np.arange(1,K+1)
    H[rows, cols] = h_rate1 * h_mean + h_rate2 * h_mean * hdist(*hdist_params, K)

    F = np.empty((K, 0))
    d = np.empty(0)

    if gamma_rate == 0:
        gamma = np.zeros(K)
    else:
        gamma = gamma_rate * gamma_dist(*gamma_dist_params, K)
    if c_scale != 0:
        c = c_scale * c_dist(*c_dist_params, K)
    else:
        c = np.zeros(K)
    cost = None
    if cost_scale != 0:
        cost = cost_scale * cost_dist(*cost_dist_params, K)
        if last_cost is not None:
            cost[-1] = last_cost
        # this produce negative and positive costs!
        c += np.matmul(cost, G)
        total_buffer_cost = (np.inner(cost, alpha), np.inner(cost, a))
    else:
        total_buffer_cost = (0, 0)
    return G, H, F, gamma, c, d, alpha, a, b, 1.5 * K, total_buffer_cost, cost