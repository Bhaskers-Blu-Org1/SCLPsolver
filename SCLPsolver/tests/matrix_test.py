from subroutines.matrix import matrix
import numpy as np
import timeit

a = 8
b = 6
test_matrix = matrix(a, b)
print(test_matrix.get_matrix())

index = 0
row_vector = np.asarray([1, 1])
column_vector = np.asarray([1, 1])
test_matrix.insert(index, row_vector, column_vector)
print(test_matrix.get_matrix())

index = 1
row_vector = np.asarray([2,2,2])
column_vector = np.asarray([2,2,2])
test_matrix.insert(index, row_vector, column_vector)
print(test_matrix.get_matrix())

index = 2
row_vector = np.asarray([3,3,3,3])
column_vector = np.asarray([3,3,3,3])
test_matrix.insert(index, row_vector, column_vector)
print(test_matrix.get_matrix())

index = 3
test_matrix.delete(index)
print(test_matrix.get_matrix())

index = 1
row_vector = np.asarray([4,4,4])
column_vector = np.asarray([4,4,4])
test_matrix.overwrite(index, row_vector, column_vector)
print(test_matrix.get_matrix())


matrix_a_size = 200
times_to_run = 100
# comparing numpy inverse speed to new algorithm speed
# 1st testing the numpy implementation
matrix_a = np.random.randint(10, size=(matrix_a_size, matrix_a_size))
vector_b = np.random.randint(10, size=(matrix_a_size))
vector_c = np.random.randint(10, size=(matrix_a_size))
scalar_d = 4

matrix_to_inverse = np.zeros((matrix_a_size + 1, matrix_a_size + 1))
matrix_to_inverse[0:matrix_a_size, 0:matrix_a_size] = matrix_a
matrix_to_inverse[0:matrix_a_size, matrix_a_size] = vector_b
matrix_to_inverse[matrix_a_size, 0:matrix_a_size] = vector_c
matrix_to_inverse[matrix_a_size, matrix_a_size] = scalar_d

numpy_inverse_update_matrix = np.linalg.inv(matrix_to_inverse)

numpy_inverse_time=timeit.timeit(lambda: 'np.linalg.inv(matrix_a)', number=times_to_run)
print("Numpy iverse took ",numpy_inverse_time," seconds")
inversed_matrix_a = np.linalg.inv(matrix_a)

c = matrix(None, len(inversed_matrix_a)*2)

new_algorithm_time = timeit.timeit(lambda: 'c.inverseUpdate2(inversed_matrix_a, vector_b, vector_c, scalar_d)', number=times_to_run)
improved_algorithm_inverse_update_matrix = c.inverseUpdate2(inversed_matrix_a, vector_b, vector_c, scalar_d)

print("New algorithm took ",new_algorithm_time," seconds")
diff_between_algorithms = numpy_inverse_time-new_algorithm_time
print("** New algorithm is",'faster' if (diff_between_algorithms >= 0) else 'slower', "by : ", abs(diff_between_algorithms)," seconds")
#print("Numpy result:\n",numpy_inverse_update_matrix)
#print("New Algorithm result:\n",improved_algorithm_inverse_update_matrix)
print("Are Numpy and new Algotithm results the same? :",  np.allclose(numpy_inverse_update_matrix,improved_algorithm_inverse_update_matrix))

