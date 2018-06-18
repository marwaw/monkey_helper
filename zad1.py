import pandas as pd
import numpy as np


def read_csv(file_name):
    return pd.read_csv(file_name, sep=',', header=0).values

def sprint_planning_helper(file, velocity):
    ID_STORY_POINTS = 1
    ID_KSP = 2

    data = read_csv(file)
    number_of_items, weight = data.shape[0], velocity+1
    matrix = np.zeros((number_of_items, weight))

    for i in range(number_of_items):
        for j in range(weight):
            if j == 0:
                result = 0
            elif data[i, ID_STORY_POINTS] > j:
                result = matrix[i-1, j]
            else:
                tmp1 = matrix[i-1, j]
                tmp2 = matrix[i-1, j-data[i, ID_STORY_POINTS]]+data[i, ID_KSP]
                result = max(tmp1, tmp2)
            matrix[i, j] = result
    print(matrix)
    tasks = find_tasks(matrix, data)

    return tasks

def find_tasks(calculated_matrix, tasks_data):
    row, col = calculated_matrix.shape
    tasks = []

    while row > 0 and col > 0:
        max_ind = np.argmax(calculated_matrix[:row,:col])
        x, y = int(max_ind/col), int(max_ind/row)
        print(x, y)
        tasks.append(x)
        task_weight = tasks_data[x, 1]
        print(task_weight)
        col -= task_weight
        row -= 1

    return tasks
