import numpy as np
import pandas
import os


def parse_series(filename: str):  # filename with .csv
    """Parse several spectra."""
    i1 = 0
    while (i1 <= 100):
        try:
            data = pandas.read_csv(filename, skiprows=(i1),
                                   index_col=False, usecols=[0, 1],
                                   header=None, skip_blank_lines=False)
            break
        except:
            if (i1 >= 100):
                raise SystemExit('cant read data')
            i1 += 1
    # print(filename+' created, i1 = ', i1)
    data[0] = data[0].replace(np.nan, 'n')
    i2 = data[0].str.match(r'\b\d{4}\.\d+').values.nonzero()[0][0]
    # print(filename+' created, i2 = ', i2+i1)
    data = pandas.read_csv(filename, skiprows=int(i1 + i2),
                           index_col=False, usecols=[0, 1],
                           header=None, skip_blank_lines=False)
    # print(filename+' type is ', type(data), data.dtype)

    # parse other spectra, make list
    data[0] = data[0].replace(np.nan, 'n')
    N_points = data[0].str.match(r'\b\d{4}\.\d+').eq(0).values.nonzero()[0][0]
    N_skip = i1 + i2
    N_spectra = int((data.shape[0] - N_points) / (N_points + N_skip))
    spec_list = ([data[0:N_points].to_numpy(dtype=float)])
    if (np.mean(spec_list[0][:, 1]) < 0):
        log_flag = True
    else:
        log_flag = False
    if log_flag:
        spec_list[0][:, 1] = 10 ** (spec_list[0][:, 1] / 10)
    for ii in range(N_spectra):
        ii_start = (N_points + N_skip) * (ii + 1)
        ii_end = ii_start + N_points
        temp = data[ii_start:ii_end].to_numpy(dtype=float)
        if log_flag:
            temp[:, 1] = 10 ** (temp[:, 1] / 10)
        spec_list.append(temp.copy())

    return spec_list
