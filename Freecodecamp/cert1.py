import numpy as np


def calculate(alist):
    if len(alist) != 9:
        raise ValueError("List must contain nine numbers.")
    arr = np.array(alist).reshape(3, 3)
    mean_row = np.mean(arr, axis=1).tolist()
    mean_column = np.mean(arr, axis=0).tolist()
    var_row = np.var(arr, axis=1).tolist()
    var_column = np.var(arr, axis=0).tolist()
    sd_row = np.std(arr, axis=1).tolist()
    sd_colum = np.std(arr, axis=0).tolist()
    max_row = np.max(arr, axis=1).tolist()
    max_column = np.max(arr, axis=0).tolist()
    min_row = np.min(arr, axis=1).tolist()
    min_column = np.min(arr, axis=0).tolist()
    sum_row = np.sum(arr, axis=1).tolist()
    sum_column = np.sum(arr, axis=0).tolist()
    calc = {'mean': [mean_column, mean_row, np.mean(alist)],
            'variance': [var_column, var_row, np.var(alist)],
            'standard deviation': [sd_colum, sd_row, np.std(alist)],
            'max': [max_column, max_row, np.max(alist)],
            'min': [min_column, min_row, np.min(alist)],
            'sum': [sum_column, sum_row, np.sum(alist)]}
    return calc


if __name__ == '__main__':
    print(calculate([2, 6, 2, 8, 4, 0, 1, 5, 7]))
