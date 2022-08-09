def get_submat(mat, start, size):
    end = tuple(sum(i) for i in zip(start, size))
    return [i[start[0]:end[0]] for i in mat[start[1]:end[1]]]

def multiply_pairwise(mat1, mat2):
    return [[i * j for i, j in zip(k, l)] for k, l in zip(mat1, mat2)]

def reflect_across_diag(mat):
    new_mat = []
    for elem in mat:
        if len(new_mat) != 0:
            for index, num in enumerate(elem):
                new_mat[index].append(num)
        else:
            for i in elem:
                new_mat.append([i])

    return new_mat

def apply_kernel(mat, kernel):
    mat = reflect_across_diag(mat)
    kernel = reflect_across_diag(kernel)
    output_mat_dim = len(mat) - (len(kernel) - 1)
    output_mat = [[0 for i in range(output_mat_dim)] for j in range(output_mat_dim)]
    for i in range(output_mat_dim):
        for j in range(output_mat_dim):
            applied_area = get_submat(mat, (i, j), (len(kernel), len(kernel)))
            new_area = multiply_pairwise(applied_area, kernel)
            new_pixel = sum([sum(i) for i in new_area])
            output_mat[i][j] = new_pixel

    output_mat2 = output_mat.copy()
    for index1, i in enumerate(output_mat):
        for index2, j in enumerate(i):
            val = 255 - int(eval(f'{j}/1' + (len(str(j)))*'0') * 255)
            output_mat2[index1][index2] = (val, val, val)

    return output_mat2

matr = [[]]
kernel = [[0, 0], [1, 1]]

print(apply_kernel(matr, kernel))
