import numpy as np

from utils import read_csv


def sprint_planning_helper(file, velocity):
    ID_STORY_POINTS = 1
    ID_KSP = 2

    data = read_csv(file)
    number_of_items, weight = data.shape[0], velocity + 1
    matrix = np.zeros((number_of_items, weight))

    for i in range(number_of_items):
        for j in range(weight):
            if j == 0:
                result = 0
            elif data[i, ID_STORY_POINTS] > j:
                result = matrix[i - 1, j]
            else:
                tmp1 = matrix[i - 1, j]
                tmp2 = matrix[i - 1, j - data[i, ID_STORY_POINTS]] + data[i, ID_KSP]
                result = max(tmp1, tmp2)
            matrix[i, j] = result
    print(matrix)
    tasks = find_tasks(matrix, data)

    return tasks


def find_tasks(calculated_matrix, tasks_data):
    row, col = calculated_matrix.shape
    tasks = []
    weight = np.max(calculated_matrix)
    max_ind_y = 10

    while weight and max_ind_y != 0:
        print(f'max col {max_ind_y}')
        max_ind_x, max_ind_y = np.unravel_index(np.argmax(calculated_matrix[:row, :col]),
                                                calculated_matrix[:row, :col].shape)
        print(max_ind_x, max_ind_y)
        tasks.append(max_ind_x)
        task_weight = tasks_data[max_ind_x, 1]
        weight -= task_weight
        col -= task_weight
        row -= 1

    return set(tasks)
