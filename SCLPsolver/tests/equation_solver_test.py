from subroutines.matrix import matrix
from subroutines.equation_solver import equation_solver
import numpy as np
import random
import time

matrix_size = 3
times_to_run = 5
print('\n test replace_equation')

numpy_algorithm_time = 0
new_algorithm_time = 0
vector_2 = 10 * np.random.normal(size=matrix_size)

for i in range(times_to_run):

    if i == 0:
        matrix_1 = 10 * np.random.rand(matrix_size, matrix_size)

        matrix_3 = np.linalg.inv(matrix_1)
        result_4 = np.dot(matrix_3, vector_2)

        # step 9
        equation_solver_9 = equation_solver(matrix_size)
        equation_solver_9.set_inverse_matrix(matrix_3)

    index_to_replace = random.randint(0, matrix_size - 1)

    random_row_vector_5_1 = 10 * np.random.normal(size=matrix_size)
    random_column_vector_5_2 = 10 * np.random.normal(size=matrix_size)
    # step 6
    matrix_1[:, index_to_replace] = random_column_vector_5_2
    matrix_1[index_to_replace, :] = random_row_vector_5_1

    # step 7
    start_time = time.time()
    matrix_7 = np.linalg.inv(matrix_1)
    # step 8
    result_8 = np.dot(matrix_7, vector_2)
    numpy_algorithm_time += time.time() - start_time

    start_time = time.time()
    #step 10
    equation_solver_9._replace_equation(index_to_replace,index_to_replace,random_row_vector_5_1,random_column_vector_5_2)
    #result10 = equation_solver_9.get_inverse()
    #print(np.allclose(result10, matrix_7))
    result_11 = equation_solver_9.resolve(vector_2)
    new_algorithm_time += time.time() - start_time

    print("Are Numpy and new Algorithm results the same? :", np.allclose(result_8, result_11))


print("Numpy algorithm took ", numpy_algorithm_time, " seconds")
print("New algorithm took ", new_algorithm_time, " seconds")
# size_comparison = numpy_algorithm_time/new_algorithm_time
# print("** New algorithm is ",abs(round((size_comparison-1)*100,1)), "%" ,'faster' if (size_comparison >= 1) else 'slower')

#print(result_8)
#print(result_11)

print('\n test add_equation')

numpy_algorithm_time = 0
new_algorithm_time = 0
vector_2 = 10 * np.random.normal(size=matrix_size+1)

matrix_1 = 10 * np.random.rand(matrix_size, matrix_size)

matrix_3 = np.linalg.inv(matrix_1)
# result_4 = np.dot(matrix_3, vector_2)

index_to_replace = random.randint(0, matrix_size - 1)

random_row_vector_5_1 = 10 * np.random.normal(size=matrix_size+1)
random_column_vector_5_2 = 10 * np.random.normal(size=matrix_size+1)
#random_column_vector_5_2[index_to_replace] = random_row_vector_5_1[index_to_replace]

# expand matrix by 1 row and 1 column
matrix_2 = np.eye(matrix_1.shape[0]+1)
matrix_2[:matrix_size, :matrix_size] = matrix_1
res22 = np.linalg.inv(matrix_2)
matrix_2[:,matrix_size] = random_column_vector_5_2
matrix_2[matrix_size,:] = random_row_vector_5_1


# matrix_2[:index_to_replace, :index_to_replace] = matrix_1[:index_to_replace, :index_to_replace]
# matrix_2[:index_to_replace, index_to_replace+1:] = matrix_1[:index_to_replace, index_to_replace:]
# matrix_2[index_to_replace+1:, :index_to_replace] = matrix_1[index_to_replace:,:index_to_replace]
# matrix_2[index_to_replace+1:,index_to_replace+1:] = matrix_1[index_to_replace:,index_to_replace:]
#
# matrix_2[index_to_replace,:] = random_row_vector_5_1
# matrix_2[:,index_to_replace] = random_column_vector_5_2


# step 7
start_time = time.time()
matrix_7 = np.linalg.inv(matrix_2)
# step 8
result_8 = np.dot(matrix_7, vector_2)
numpy_algorithm_time += time.time() - start_time


# step 9
equation_solver_9 = equation_solver(matrix_size*2)
equation_solver_9.set_inverse_matrix(matrix_3)
equation_solver_10 = equation_solver(matrix_size*2)
equation_solver_10.set_inverse_matrix(res22)
equation_solver_10._replace_equation(3, 3, random_row_vector_5_1.copy(), random_column_vector_5_2.copy())
result_12 = equation_solver_10.resolve(vector_2.copy())

start_time = time.time()

#equation_solver_9.add_equation(index_to_replace,index_to_replace,random_row_vector_5_1,random_column_vector_5_2)
equation_solver_9.add_equation(matrix_size,matrix_size,random_row_vector_5_1.copy(),random_column_vector_5_2.copy())

result_11 = equation_solver_9.resolve(vector_2.copy())

new_algorithm_time += time.time() - start_time

print("Are Numpy and new Algorithm results the same? :", np.allclose(result_8, result_11))


print("Numpy algorithm took ", numpy_algorithm_time, " seconds")
print("New algorithm took ", new_algorithm_time, " seconds")
size_comparison = numpy_algorithm_time/new_algorithm_time
print("** New algorithm is ",abs(round((size_comparison-1)*100,1)), "%" ,'faster' if (size_comparison >= 1) else 'slower')

print("results using numpy:\n",result_8)
print("results using add equation:\n",result_11)

# test remove equation

# test that do replace, add and remove several times









