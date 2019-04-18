import numpy as np
from .extract_rates import extract_rates
from .pivot import full_pivot
from .matlab_utils import find


def SCLP_subproblem(pbaseDD,dbaseDD,DD, N1,N2,v1,v2,Kexclude,Jexclude,pbaseB1,pbaseB2,
                     AAN1,AAN2, KK, JJ, NN, totalK, totalJ, DEPTH, STEPCOUNT, ITERATION, settings, tolerance):


    #[~, NN] = size(prim_name)
    # Excluding the k's and j's which are > 0
    lKDDin = np.logical_not(np.in1d(pbaseDD, Kexclude, assume_unique=True))
    lJDDin = np.logical_not(np.in1d(dbaseDD, -Jexclude, assume_unique=True))
    # size(pbaseDD)
    # size(dbaseDD)
    pbaseDDred = pbaseDD[lKDDin]
    dbaseDDred = dbaseDD[lJDDin]
    DDred = DD[find(np.hstack(([True],lKDDin)))[:,None], find(np.hstack(([True],lJDDin)))]
    if len(pbaseB1) > 0:
        pbaseB1red = pbaseB1[np.logical_not(np.in1d(pbaseB1,Kexclude, assume_unique=True))]
    else:
        pbaseB1red = []
    if len(pbaseB2) > 0:
        pbaseB2red = pbaseB2[np.logical_not(np.in1d(pbaseB2,Kexclude, assume_unique=True))]
    else:
        pbaseB2red = []

    klist = np.sort(np.append(pbaseDDred[pbaseDDred > 0], dbaseDDred[dbaseDDred > 0]))
    jlist = np.sort(-np.append(pbaseDDred[pbaseDDred < 0], dbaseDDred[dbaseDDred < 0]))

    lk = np.size(klist)
    lj = np.size(jlist)

    # The starting sequence
    pn1 = np.vstack(pbaseDDred)
    dn1 = np.vstack(dbaseDDred)
    dx, dq = extract_rates(pbaseDDred, dbaseDDred, DDred, lk, lj, totalK, totalJ)
    new_base_sequence = {'dx': [dx], 'dq': [dq], 'bases': [{'prim_name': pbaseDDred, 'dual_name': dbaseDDred,'A': DDred.copy()}],
                         'places': [0]}
    pivots=[]
    # performing the left and right first pivots
    #		the right pivot:
    if np.size(pbaseB2red) > 0:
        if not isinstance(v1, list):
            if v1 > 0:
                K_0 = [v1]
                J_N = []
            else:
                K_0 = []
                J_N = [-v1]
        else:
            K_0 = []
            J_N = []
        if not isinstance(v2, list):
            if v2 < 0:
                J_N.append(-v2)
        from .SCLP_pivot4 import SCLP_pivot
        pn1,dn1,pivots,new_base_sequence, STEPCOUNT, ITERATION = SCLP_pivot(K_0,J_N,pn1,dn1,0,1,[],v1,pivots, new_base_sequence,
                                                                            lk, lj, 1, totalK, totalJ, DEPTH, STEPCOUNT, ITERATION, settings, tolerance)
    #		the left pivot:
    if np.size(pbaseB1red) > 0:
        if not isinstance(v2, list):
            if v2 > 0:
                K_0 = [v2]
                J_N = []
            else:
                K_0 = []
                J_N = [-v2]
        else:
            K_0 = []
            J_N = []
        if not isinstance(v1, list):
            if v1 > 0:
                K_0.append(v1)
        from .SCLP_pivot4 import SCLP_pivot
        pn1,dn1,pivots,new_base_sequence, STEPCOUNT, ITERATION = SCLP_pivot(K_0,J_N,pn1,dn1,-1,0,v2,[],pivots,new_base_sequence,
                                                                            lk, lj, 1, totalK, totalJ, DEPTH, STEPCOUNT, ITERATION, settings, tolerance)
    # prepare the boundaries
    T = 1
    del_T = 0

    x_0=np.zeros((lk,1))
    q_N=np.zeros((lj,1))
    del_x_0=np.zeros((lk,1))
    del_q_N=np.zeros((lj,1))

    # Boundary values for one sided subproblem, collision at t=0
    if N1 == -1:
        # The case of v1 > 0, collision case iv_a
        if not isinstance(v1, list) and v1 > 0:
            dx_DD_v1 = DD[1:,0][pbaseDD == v1][0]
            lk1 = klist == v1
            x_0[lk1] = -dx_DD_v1
            del_x_0[lk1] = dx_DD_v1
        # The case of v1 < 0, collision case iii_a
        if not isinstance(v1, list) and v1 < 0:
            #dq_B2_v1 = AA( 1, j1B2 + 1, N2 )
            dq_B2_v1 = AAN2['A'][0,1:][AAN2['dual_name'] == v1][0]
            lj1 = jlist == -v1
            #q_N[lj1] = 0
            del_q_N[lj1] = -dq_B2_v1
    #
    #
    # Boundary values for one sided subproblem, collision at t=T
    elif N2 == NN:
        # The case of v2 > 0, collision case iii_b
        if not isinstance(v2, list) and v2 > 0:
            #dx_B1_v2 = AA( i2B1 + 1, 1, N1 )
            dx_B1_v2 = AAN1['A'][1:,0][AAN1['prim_name'] == v2][0]
            lk2 = klist == v2
            #x_0[lk2] = 0
            del_x_0[lk2] = -dx_B1_v2
        # The case of v2 < 0, collision case iv_b
        if not isinstance(v2, list) and v2 < 0:
            dq_DD_v2 = DD[0,1:][dbaseDD == v2][0]
            lj2 = jlist == -v2
            q_N[lj2] = -dq_DD_v2
            del_q_N[lj2] = dq_DD_v2
    #
    #
    # Boundary values for two sided subproblem, collision at 0<t<T
    #  setting boundaries for the second exiting variable v1
    else:
        if not isinstance(v1, list) and v1 > 0:
            dx_DD_v1 = DD[1:,0][pbaseDD == v1][0]
            lk1 = klist == v1
            x_0[lk1] = -dx_DD_v1
            #dx_B1_v1 = AA( i1B1 + 1, 1, N1 )
            dx_B1_v1 = AAN1['A'][1:,0][AAN1['prim_name'] == v1][0]
            del_x_0[lk1] = -0.5*dx_B1_v1 + dx_DD_v1
        if not isinstance(v1, list) and v1 < 0:
            #dq_B2_v1 = AA( 1, j1B2 + 1, N2 )
            dq_B2_v1 = AAN2['A'][0,1:][AAN2['dual_name'] == v1][0]
            lj1 = jlist == -v1
            #q_N(j1) = 0
            del_q_N[lj1] = -0.5*dq_B2_v1
        #  setting boundaries for the first exiting variable v2
        if not isinstance(v2, list) and v2 > 0:
            #dx_B1_v2 = AA( i2B1 + 1, 1, N1 )
            dx_B1_v2 = AAN1['A'][1:,0][AAN1['prim_name'] == v2][0]
            lk2 = klist == v2
            #x_0[lk2] = 0
            del_x_0[lk2] = -0.5*dx_B1_v2
        if not isinstance(v2, list) and v2 < 0:
            dq_DD_v2 = DD[0,1:][dbaseDD == v2][0]
            lj2 = jlist == -v2
            q_N[lj2] = -dq_DD_v2
            #dq_B2_v2 = AA(1, j2B2 + 1, N2 )
            dq_B2_v2 = AAN2['A'][0,1:][AAN2['dual_name'] == v2][0]
            del_q_N[lj2] = -0.5*dq_B2_v2 + dq_DD_v2

    #############################################
    # solving the subproblem
    from .SCLP_solver4 import SCLP_solver
    pn1,dn1, x_0, q_N, T, pivots,\
    new_base_sequence, STEPCOUNT = SCLP_solver( x_0, del_x_0, q_N, del_q_N, T, del_T, pn1,dn1, 1,'sub_prob', pbaseB1red,
                                                pbaseB2red, pivots, new_base_sequence, totalK, totalJ, DEPTH, STEPCOUNT, ITERATION, settings, tolerance)
    #############################################
    # the list of pivots:
    #[~, ~, pivots] = calc_pivots3(pn1, dn1)
    Npivots = len(pivots)
    #Warning this based on assumption that first basis in new_base_sequence is equal to the AAN1 and/or last basis is equal to the AAN2
    if N1 != -1 and Npivots > 0:
        pm1 = AAN1['prim_name']
        dm1 = AAN1['dual_name']
        pp1 = np.setdiff1d(pn1[:,0], pm1)
        pp2 = np.setdiff1d(dn1[:,0], dm1)
        if len(pp1) > 1 or len(pp2) > 1:
            print('Incomplete pivot...')
            raise Exception()
        elif len(pp1) == 0 and len(pp2) == 0:
            pass
        elif len(pp1) == 1 and len(pp2) == 1:
            if pivots[0][0] == pp2[0] and pivots[0][1] == pp1[0]:
                pass
            elif pivots[0][0] != pp2[0] and pivots[0][1] != pp1[0]:
                piv = [[pp2[0],pp1[0]]]
                pivots = piv + pivots
            else:
                print('Incompatible pivots...')
                raise Exception()
        else:
            print('Undefined pivot...')
            raise Exception()
        DD1 = AAN1['A'].copy()
        k1 = len(pm1)
        l1 = len(dm1)
        if N2 != NN:
            pp1 = np.setdiff1d(pn1[:, -1], AAN2['prim_name'])
            pp2 = np.setdiff1d(dn1[:, -1], AAN2['dual_name'])
            if len(pp1) > 1 or len(pp2) > 1:
                print('Incomplete pivot...')
                raise Exception()
            elif len(pp1) == 0 and len(pp2) == 0:
                pivots = pivots[:-1]
                Npivots -= 1
            elif len(pp1) == 1 and len(pp2) == 1:
                pass
        pn_new=np.empty(shape=(k1,len(pivots)), dtype=int)
        #pn_new =np.union1d(pn1, Kexclude)
        dn_new=np.empty(shape=(l1,len(pivots)), dtype=int)
        new_base_sequence = {'dx': [], 'dq': [], 'bases': [], 'places': []}
        zz1 = np.zeros(k1)
        zz2 = np.zeros(l1)
        for i,piv1 in enumerate(pivots):
            DD1,pm1,dm1,zz1,zz2 = full_pivot(DD1,find(pm1==piv1[0])[0],find(dm1==piv1[1])[0],pm1.copy(),dm1.copy(),zz1.copy(),zz2.copy())
            pn_new[:,i] = pm1
            dn_new[:,i] = dm1
            dx, dq = extract_rates(pm1, dm1, DD1, KK, JJ, totalK, totalJ)
            new_base_sequence['dx'].append(dx)
            new_base_sequence['dq'].append(dq)
    elif Npivots >0:
        pm1 = AAN2['prim_name']
        dm1 = AAN2['dual_name']
        DD1 = AAN2['A'].copy()
        k1 = len(pm1)
        l1 = len(dm1)
        pn_new = np.empty(shape=(k1, Npivots), dtype=int)
        dn_new = np.empty(shape=(l1, Npivots), dtype=int)
        new_base_sequence = {'dx': [], 'dq': [], 'bases': [], 'places': []}
        zz1 = np.zeros(k1)
        zz2 = np.zeros(l1)
        for i,piv1 in enumerate(reversed(pivots)):
            [DD1,pm1,dm1,zz1,zz2] = full_pivot(DD1,find(pm1==piv1[1]),find(dm1==piv1[0]),pm1.copy(),dm1.copy(),zz1.copy(),zz2.copy())
            pn_new[:, Npivots-i-1] = pm1
            dn_new[:, Npivots-i-1] = dm1
            dx, dq = extract_rates(pm1, dm1, DD1, KK, JJ, totalK, totalJ)
            new_base_sequence['dx'].append(dx)
            new_base_sequence['dq'].append(dq)
        new_base_sequence['dx'].reverse()
        new_base_sequence['dq'].reverse()
    else:
        pn_new = np.vstack(np.union1d(pn1[:,0], Kexclude))
        dn_new = np.vstack(np.union1d(dn1[:,0], -Jexclude))
    return  pn_new,dn_new, new_base_sequence, STEPCOUNT, ITERATION