import numpy as np
#from scipy.linalg.blas import dger


#'#@profile
def base_pivot(A, i, j, pn, dn, tmp):
    nam = pn[i]
    pn[i] = dn[j]
    dn[j] = nam
    i += 1
    j += 1
    p = A[i, j]
    if p == 0:
        raise Exception('pivot on zero')
    rp = A[i,:] / p
    c = A[:, j].copy()
    A -= np.outer(c, rp, out=tmp)
    A[i,:] = rp
    A[:, j] = c / -p
    A[i, j] = 1. / p
    return A, pn, dn


#'#@profile
def full_pivot(A, i, j, pn, dn, ps, ds, tmp):
    nam = pn[i]
    pn[i] = dn[j]
    dn[j] = nam
    sam = ps[i]
    ps[i] = - ds[j]
    ds[j] = - sam
    i += 1
    j += 1
    p = A[i, j]
    if p == 0:
        raise Exception('pivot on zero')
    rp = A[i,:] / p
    c = A[:, j].copy()
    A -= np.outer(c, rp, out=tmp)
    #A = dger(-1.0, c, rp, a=A, overwrite_a= 1)
    A[i,:] = rp
    A[:, j] = c / -p
    A[i, j] = 1. / p
    return A, pn, dn, ps, ds

def ok(a, b):
    return all((m == n) or (m == 1) or (n == 1) for m, n in zip(a.shape[::-1], b.shape[::-1]))

#'#@profile
def dict_pivot(dct, i, j, tmp):
    nam = dct['prim_name'][i]
    dct['prim_name'][i] = dct['dual_name'][j]
    dct['dual_name'][j] = nam
    i += 1
    j += 1
    p = dct['A'][i, j]
    if p == 0:
        raise Exception('pivot on zero')
    if not ok(dct['A'][i, :], p):
        print("=========================================")
        print("dct[A][i,:].shape={}, p.shape={}".format(dct['A'][i, :].shape, p.shape))
        raise Exception("Bad shapes! dct[A][i,:].shape={}, p.shape={}".format(dct['A'][i, :].shape, p.shape))
    rp = dct['A'][i, :] / p
    c = dct['A'][:, j].copy()
    dct['A'] -= np.outer(c, rp, out=tmp)
    dct['A'][i, :] = rp
    dct['A'][:, j] = c / -p
    dct['A'][i, j] = 1. / p
    return dct