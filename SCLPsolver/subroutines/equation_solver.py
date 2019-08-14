import numpy as np
import subroutines.matrix as mm

class equation_solver():

    def __init__(self, alloc_size):
        self._steps = 0
        self._eta_rows = []
        self._eta_cols = []
        self._row_places = []
        self._col_places = []
        self._matrix = mm.matrix(1, alloc_size)
        self._inv_matrix = mm.matrix(1, alloc_size)
        self._row_order = [0] # use this to save order of equations set -1 if we remove equation
        self._col_order = [0] # use this to save order of variables set -1 if we remove variable

    def add_equation(self, n_row, n_col, row, col):
        self._steps += 1
        if -1 not in self._row_order:
            self._inv_matrix.enlarge() #new method to implement should increase row and column count of matrix and set 1 at the corner
            self._row_order.append(n_row)
            self._col_order.append(n_col)
            self._replace_equation(len(self._row_places),len(self._col_places), row, col)
        else:
            i_row = self._row_places.index(-1)
            i_col = self._col_places.index(-1)
            self._replace_equation(i_row, i_col, row, col)
            self._row_order[i_row] = n_row
            self._col_order[i_col] = n_col

    def remove_equation(self, n_row, n_col):
        self._steps += 1
        i_row = self._row_places.index(n_row)
        i_col = self._col_places.index(n_col)
        row = np.zeros(len(self._col_places))
        col = np.zeros(len(self._row_places))
        row[i_col] = 1
        col[i_row] = 1
        # should utilize sparsity in btran!!!
        self._replace_equation(i_row, i_col, row, col)
        self._row_order[i_row] = -1
        self._col_order[i_col] = -1

    def replace_equation(self, n_row, n_col, row, col):
        self._replace_equation(self._row_places.index(n_row), self._col_places.index(n_col), row, col)

    def _replace_equation(self, i_row, i_col, row, col):
        self._steps += 1
        for i, r in enumerate(self._eta_rows):
            col = btran(col, r, self._row_places[i])
        col = np.dot(self._inv_matrix.get_matrix(), col)
        for i, c in enumerate(self._eta_cols):
            col = ftran(col, c, self._col_places[i])
        self._col_places.append(i_col)
        self._eta_cols.append(to_eta(col, i_row))
        for i, c in zip(reversed(range(len(self._eta_cols))), reversed(self._eta_cols)):
            row = btran(row, c, self._col_places[i])
        row = np.dot(self._inv_matrix.get_matrix().T, row)
        for i, r in enumerate(self._eta_rows):
            row = ftran(row, r, self._row_places[i])
        self._row_places.append(i_row)
        self._eta_rows.append(to_eta(row, i_col))


    def _get_row_etm(self, index):
        etm = np.eye(len(self._eta_rows[index]))
        etm[self._row_places[index], :] = self._eta_rows[index]
        return etm

    def _get_col_etm(self, index):
        etm = np.eye(len(self._eta_cols[index]))
        etm[:, self._col_places[index]] = self._eta_cols[index]
        return etm

    def _get_inverse(self):
        return np.dot(self._get_col_etm(-1),np.dot(self._inv_matrix.get_matrix(), self._get_row_etm(-1)))

    def _resolve(self, rhs):
        for i, r in zip(reversed(range(len(self._eta_rows))), reversed(self._eta_rows)):
            rhs = btran(rhs, r, self._row_places[i])
        rhs = np.dot(self._inv_matrix.get_matrix(), rhs)
        for i, c in enumerate(self._eta_cols):
            rhs = ftran(rhs, c, self._col_places[i])
        return rhs

    def resolve(self, rhs):
        res = self._resolve(rhs)
        # should update res by removing 0 from indexes of -1 in col order and ordering elements
        return res

    def set_inverse_matrix(self, inverse_matrix):
        self._inv_matrix.set_matrix(inverse_matrix)

def to_eta(values, index_to_pivot):
    pivot_val = values[index_to_pivot]
    values /= -values[index_to_pivot]
    values[index_to_pivot] = 1/pivot_val
    return values

def ftran(values, eta, index_to_pivot):
    pivot_val = values[index_to_pivot] * eta[index_to_pivot]
    values[:len(eta)] += values[index_to_pivot] * eta
    values[index_to_pivot] = pivot_val
    return values

def btran(values, eta, index_to_pivot):
    pivot_val = np.inner(values[:len(eta)], eta)
    values[index_to_pivot] = pivot_val
    return values