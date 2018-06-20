#!/usr/bin/env python3
import sys

import numpy as np
import pandas as pd


def sprint_planning_helper(file, velocity):
    data = read_csv(file)

    matrix = make_matrix(data, velocity)
    tasks = find_tasks(matrix, data)
    return tasks


def make_matrix(data, velocity):
    ID_STORY_POINTS = 1
    ID_KSP = 2

    number_of_items, weight = data.shape[0], velocity + 1
    matrix = np.zeros((number_of_items, weight))

    for i in range(number_of_items):
        for j in range(weight):
            if j == 0:
                result = 0
            elif data[i, ID_STORY_POINTS] > j:
                result = matrix[i - 1, j]
            else:
                prev_value = matrix[i - 1, j]
                current_value = matrix[i - 1, j - data[i, ID_STORY_POINTS]] + data[i, ID_KSP]
                result = max(prev_value, current_value)
            matrix[i, j] = result
    return matrix


def find_tasks(calculated_matrix, tasks_data):
    row, col = calculated_matrix.shape
    tasks = []
    weight = np.max(calculated_matrix)

    while weight:
        max_ind_x, max_ind_y = np.unravel_index(np.argmax(calculated_matrix[:row, :col]),
                                                calculated_matrix[:row, :col].shape)

        if max_ind_y == 0:
            break
        tasks.append(max_ind_x)
        task_weight = tasks_data[max_ind_x, 1]
        weight -= task_weight
        col -= task_weight
        row -= 1

    return tasks


def read_csv(file_name):
    return pd.read_csv(file_name, sep=',', header=0).values

if __name__ == '__main__':
    tasks = sprint_planning_helper(sys.argv[1], int(sys.argv[2]))
    print(tasks)