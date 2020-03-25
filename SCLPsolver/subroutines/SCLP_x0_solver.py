from .classification import classification
from .SCLP_pivot import SCLP_pivot
from .collision_info import collision_info
from .parametric_line import parametric_line
from .SCLP_solver import SCLP_solver

#'#@profile
def SCLP_x0_solver(solution, param_line, target_x0, target_T, K_add_set, DEPTH, STEPCOUNT, ITERATION, settings, tolerance, find_alt_line=True, mm=None):

    ITERATION[DEPTH] = 0

    pivot_problem = {'result': 0}
    solution.print_short_status(STEPCOUNT, DEPTH, ITERATION[DEPTH], 0, 0, 'x0')
    solution.clear_collision_stack()
    source_T = param_line.T

    for v1 in K_add_set:
        col_info = collision_info('x0: ' + str(v1), 0, -1, 0, v1, [])
        solution, STEPCOUNT, ITERATION, pivot_problem = SCLP_pivot(param_line.Kset_0, param_line.Jset_N, solution, col_info, DEPTH, STEPCOUNT,
                                                                   ITERATION, settings, tolerance)
        param_line = param_line.get_x0_parline(solution, v1, target_x0[v1-1])
        res = solution.update_state(param_line, settings.check_intermediate_solution, tolerance * 100)
        if not res:
            return solution, STEPCOUNT, {'result': 1}
        col_info, problem = classification(solution, tolerance)
        theta = param_line.theta
        if param_line.is_end(col_info.delta):
            param_line.forward_to_end()
        else:
            param_line.forward_to(col_info.delta/2)
        STEPCOUNT = STEPCOUNT + 1
        ITERATION[DEPTH] = ITERATION[DEPTH] + 1
        solution.print_short_status(STEPCOUNT, DEPTH, ITERATION[DEPTH], theta, param_line.theta, 'x0: ' + str(v1))
    param_line = parametric_line(param_line.x0, param_line.qN, source_T, target_T, 0, target_x0 - param_line.x0, None,
                               param_line.Kset_0, param_line._Jset_N)
    solution, STEPCOUNT, pivot_problem = SCLP_solver(solution, param_line, 'update', DEPTH, STEPCOUNT, ITERATION, settings, tolerance, find_alt_line,
                mm)
    return solution, STEPCOUNT, pivot_problem

