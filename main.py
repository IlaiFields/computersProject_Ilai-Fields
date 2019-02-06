# this is the program for the final project in 'computers for physicists'
import matplotlib.pyplot as plt


# this function checks if the file is in row or in columns
def row_or_columns(data_list):
    # lets see if the file is in rows or in columns
    first_row = data_list[0].lower().strip().split(' ')
    if first_row[1][0] == 'x' or first_row[1][0] == 'y' or\
            first_row[1][0] == 'd':
        return "columns"   # file is in columns
    else:
        return "rows"   # file is in rows


# this function analyzes the file if its in columns
def analyze_cols(input_data):
    # lets create a dictionary that holds the data and variables of the axes
    dict = {}
    # lets add the y axis to the dictionary and remove it from the data
    y_axis = input_data[-1]
    y_axis_list = y_axis.strip().split(': ')
    dict[y_axis_list[0]] = y_axis_list[1]
    input_data.remove(y_axis)
    # lets do the same for the x axis
    x_axis = input_data[-1]
    x_axis_list = x_axis.strip().split(': ')
    dict[x_axis_list[0]] = x_axis_list[1]
    input_data.remove(x_axis)
    # lets remove the extra line before the x and y axes
    input_data = input_data[:-1]
    # lets create a list of x,y,dx,dy
    first_line_list = input_data[0].lower().strip().split(' ')
    input_data.remove(input_data[0])
    # lets create an empty list for each column
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    # lets add the columns to the lists
    # and check to see if there is a length error in the file
    try:
        for line in input_data:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    # lets add each column to the right dictionary key
    dict[first_line_list[0]] = first_list
    dict[first_line_list[1]] = second_list
    dict[first_line_list[2]] = third_list
    dict[first_line_list[3]] = forth_list
    # lets check if the uncertainties are all positive
    dx_values = dict['dx']
    dy_values = dict['dy']
    for index in range(len(first_list)):
        if float(dx_values[index]) <= 0 or float(dy_values[index]) <= 0:
            return 'Input file error: Not all uncertainties are positive.'
    return dict


# this function analyze the file if its in rows
def analyze_rows(input_data):
    # lets create a dictionary that holds the data and variables of the axis
    dict = {}
    # lets add the y axis to the dictionary and remove it from the data
    y_axis = input_data[-1]
    y_axis_list = y_axis.strip().split(': ')
    dict[y_axis_list[0]] = y_axis_list[1]
    input_data.remove(y_axis)
    # lets do the same for the x_axis
    x_axis = input_data[-1]
    x_axis_list = x_axis.strip().split(': ')
    dict[x_axis_list[0]] = x_axis_list[1]
    input_data.remove(x_axis)
    # lets remove the extra line before the x and y axes
    input_data = input_data[:-1]
    # lets determine the base length of the rows to check the length error
    first_line_list = input_data[0].strip().split(' ')
    base_length = len(first_line_list)
    # lets add to the dictionary the variables
    # and the their values and check for errors
    for line in input_data:
        list_line = line.lower().strip().split(' ')
        # lets see if the length of the row is equal
        # to the the length of the base line
        if len(list_line) != base_length:
            return "Input file error: Data lists are not the same length."
        if list_line[0] == 'x':
            dict['x'] = list_line[1:]
        if list_line[0] == 'dx':
            # lets check if the uncertainties of dx are all positive
            for index in range(1, len(list_line)):
                if float(list_line[index]) <= 0:
                    return 'Input file error: Not all uncertainties' \
                           'are positive.'
            dict['dx'] = list_line[1:]
        if list_line[0] == 'y':
            dict['y'] = list_line[1:]
        if list_line[0] == 'dy':
            # lets check if the uncertainties of dy are all positive
            for index in range(1, len(list_line)):
                if float(list_line[index]) <= 0:
                    return 'Input file error: Not all uncertainties' \
                           'are positive.'
            dict['dy'] = list_line[1:]
    return dict


# this function converts the values of the input dictionary
# from string to float
def convert_dict_to_float(input_dict):
    converted_dict = {}
    x_str = input_dict['x']
    y_str = input_dict['y']
    dx_str = input_dict['dx']
    dy_str = input_dict['dy']
    temp_list_x = []      # to hold the converted values of x
    for value in x_str:
        temp_list_x.append(float(value))
    converted_dict['x'] = temp_list_x
    temp_list_y = []      # to hold the converted values of y
    for value in y_str:
        temp_list_y.append(float(value))
    converted_dict['y'] = temp_list_y
    temp_list_dx = []     # to hold the converted values of dx
    for value in dx_str:
        temp_list_dx.append(float(value))
    converted_dict['dx'] = temp_list_dx
    temp_list_dy = []        # to hold the converted values of dy
    for value in dy_str:
        temp_list_dy.append(float(value))
    converted_dict['dy'] = temp_list_dy
    converted_dict['x axis'] = input_dict['x axis']
    converted_dict['y axis'] = input_dict['y axis']
    return converted_dict


# this function returns the evaluated fitting parameters
def evaluating_fitting_parameters(input_dict):
    x_values = input_dict['x']
    y_values = input_dict['y']
    dy_values = input_dict['dy']
    n = len(input_dict['x'])  # number of data points (constant)
    # this function calculates the average value of an argument

    def calculate_avg(values, dys):
        sum = 0
        sum_dys = 0
        for index in range(n):
            temp_value = (values[index]) / (dys[index] ** 2)
            sum += temp_value
            sum_dys += 1 / (dys[index] ** 2)
        avg = sum / sum_dys
        return avg

    # this function calculates the average value of the squared values
    # (such as <x^2>)
    def calculate_sq_avg(values, dys):
        sum = 0
        sum_dys = 0
        for index in range(n):
            temp_value = values[index]
            sq_temp_value = (temp_value ** 2) / (dys[index] ** 2)
            sum += sq_temp_value
            sum_dys += 1 / (dys[index] ** 2)
        sq_avg = sum / sum_dys
        return sq_avg

    # this function calculates the average value of the product of x and y
    def calculate_xy_avg(values1, values2, dys):
        sum_xy = 0
        sum_dys = 0
        for index in range(n):
            xy = (values1[index] * values2[index]) / (dys[index] ** 2)
            sum_xy += xy
            sum_dys += 1 / (dys[index] ** 2)
        xy_avg = sum_xy / sum_dys
        return xy_avg

    # this function calculates the value of chi^2.
    def calculate_chi_sq(input_dict_2):
        sum_chi_sq = 0
        for index in range(n):
            yi = input_dict_2['y'][index]
            xi = input_dict_2['x'][index]
            dyi = input_dict_2['dy'][index]
            temp_value = ((yi - (a * xi + b))/dyi) ** 2
            sum_chi_sq += temp_value
        return sum_chi_sq

    # these are the values that were returned from the above functions
    # and are used to calculate the a, b, chi^2 and chi^2_reduced values
    x = calculate_avg(x_values, dy_values)
    y = calculate_avg(y_values, dy_values)
    dy_square = calculate_sq_avg(dy_values, dy_values)
    x_square = calculate_sq_avg(x_values, dy_values)
    xy_product = calculate_xy_avg(x_values, y_values, dy_values)
    sum_dy = 0   # the sum of all the dy's is needed for each average function
    for index in range(n):
        sum_dy += dy_values[index]
    x_sq_avg = x ** 2
    a = (xy_product - x * y) / (x_square - x_sq_avg)
    da = (dy_square / (n * (x_square - x_sq_avg))) ** 0.5
    b = y - a * x
    db = ((dy_square * x_square) / (n * (x_square - x_sq_avg))) ** 0.5
    chi_sq = calculate_chi_sq(input_dict)
    chi_sq_red = chi_sq / (n - 2)
    return [a, da, b, db, chi_sq, chi_sq_red]


# this function finds and returns the minimum and maximum
# values of x in the data
def find_x_min_and_max(input_dict):
    x_min = min(input_dict['x'])
    x_max = max(input_dict['x'])
    return [x_min, x_max]


# this function finds and returns the minimum and maximum values of y
# in respect to the found a and b values to plot the linear fit
def calculate_y_min_and_max(x_min_and_max, evaluated_parameters):
    a = evaluated_parameters[0]
    b = evaluated_parameters[2]
    y_min = a * (x_min_and_max[0]) + b
    y_max = a * (x_min_and_max[1]) + b
    return [y_min, y_max]


# this function plots and saves the linear fit
def linear_plot(input_dict, parameters):
    x_min_and_max_values = find_x_min_and_max(input_dict)
    y_min_and_max_values = calculate_y_min_and_max(x_min_and_max_values,
                                                   parameters)
    x = input_dict['x']
    y = input_dict['y']
    dx = input_dict['dx']
    dy = input_dict['dy']
    x_axis = input_dict['x axis']
    y_axis = input_dict['y axis']
    # and now lets plot the data
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue",
                 barsabove=True)
    plt.plot(x_min_and_max_values, y_min_and_max_values, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')


# this is the main program to fit a linear plot
def fit_linear(filename):
    file = open(filename, 'r')
    data = file.readlines()
    # first we need to determine if the file is in rows or columns
    if row_or_columns(data) == "rows":
        input_dict = analyze_rows(data)
    else:
        input_dict = analyze_cols(data)
    # lets see if the 'row or columns' function returned an error
    if type(input_dict) == str:
        print(input_dict)
    else:
        converted_dict = convert_dict_to_float(input_dict)
        evaluated_parameters = evaluating_fitting_parameters(converted_dict)
        linear_plot(converted_dict, evaluated_parameters)
        print('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.format
              (evaluated_parameters[0], evaluated_parameters[1],
               evaluated_parameters[2], evaluated_parameters[3],
               evaluated_parameters[4], evaluated_parameters[5]))
    file.close()

# ##############################---BONUS---###################################


# this function analyzes the BONUS file if its in columns
def bonus_analyze_cols(input_data):
    # lets create a dictionary for the bonus that holds the data
    # and variables of the axis
    bonus_dict = {}
    # lets add the b parameters to the bonus dictionary and
    # remove it from the data
    b_parameters = input_data[-1]
    b_parameters_list = b_parameters.lower().strip().split(' ')
    bonus_dict[b_parameters_list[0]] = b_parameters_list[1],\
        b_parameters_list[2],\
        b_parameters_list[3]
    input_data.remove(b_parameters)
    # lets do the same for the a parameters
    a_parameters = input_data[-1]
    a_parameters_list = a_parameters.lower().strip().split(' ')
    bonus_dict[a_parameters_list[0]] = a_parameters_list[1],\
        a_parameters_list[2],\
        a_parameters_list[3]
    input_data.remove(a_parameters)
    # lets remove the extra line that's after the x and y axes
    input_data = input_data[:-1]
    # lets add the y axis to the dictionary and remove it from the data
    y_axis = input_data[-1]
    y_axis_list = y_axis.strip().split(': ')
    bonus_dict[y_axis_list[0]] = y_axis_list[1]
    input_data.remove(y_axis)
    # lets do the same for the x axis
    x_axis = input_data[-1]
    x_axis_list = x_axis.strip().split(': ')
    bonus_dict[x_axis_list[0]] = x_axis_list[1]
    input_data.remove(x_axis)
    # lets remove the extra line before the axes
    input_data = input_data[:-1]
    # lets create a list of x,y,dx,dy
    first_line_list = input_data[0].lower().strip().split(' ')
    input_data.remove(input_data[0])
    # lets create an empty list for each column
    first_list = []
    second_list = []
    third_list = []
    forth_list = []
    # lets add the columns to the lists
    # and check to see if there is a length error in the file
    try:
        for line in input_data:
            line_list = line.strip().split(' ')
            first_list.append(line_list[0])
            second_list.append(line_list[1])
            third_list.append(line_list[2])
            forth_list.append(line_list[3])
    except:
        return "Input file error: Data lists are not the same length."
    # lets add each column to the right dictionary key
    bonus_dict[first_line_list[0]] = first_list
    bonus_dict[first_line_list[1]] = second_list
    bonus_dict[first_line_list[2]] = third_list
    bonus_dict[first_line_list[3]] = forth_list
    # lets check if the uncertainties are all positive
    dx_values = bonus_dict['dx']
    dy_values = bonus_dict['dy']
    for index in range(len(first_list)):
        if float(dx_values[index]) <= 0 or float(dy_values[index]) <= 0:
            return 'Input file error: Not all uncertainties are positive.'
    return bonus_dict


# this function analyzes the BONUS file if its in rows
def bonus_analyze_rows(input_data):
    # lets create a dictionary that holds the data and variables of the axis
    bonus_dict = {}
    # lets add the b parameters to the bonus dictionary
    # and remove it from the data
    b_parameters = input_data[-1]
    b_parameters_list = b_parameters.lower().strip().split(' ')
    bonus_dict[b_parameters_list[0]] = b_parameters_list[1],\
        b_parameters_list[2],\
        b_parameters_list[3]
    input_data.remove(b_parameters)
    # lets do the same for the a parameters
    a_parameters = input_data[-1]
    a_parameters_list = a_parameters.lower().strip().split(' ')
    bonus_dict[a_parameters_list[0]] = a_parameters_list[1],\
        a_parameters_list[2],\
        a_parameters_list[3]
    input_data.remove(a_parameters)
    # lets remove the extra line that's after the x and y axes
    input_data = input_data[:-1]
    # lets add the y axis to the bonus dictionary and remove it from the data
    y_axis = input_data[-1]
    y_axis_list = y_axis.strip().split(': ')
    bonus_dict[y_axis_list[0]] = y_axis_list[1]
    input_data.remove(y_axis)
    # lets do the same for the x axis
    x_axis = input_data[-1]
    x_axis_list = x_axis.strip().split(': ')
    bonus_dict[x_axis_list[0]] = x_axis_list[1]
    input_data.remove(x_axis)
    # lets remove the extra line before the axes
    input_data = input_data[:-1]
    # lets determine the base length of the rows to check the length error
    first_line_list = input_data[0].strip().split(' ')
    line_length = len(first_line_list)
    # lets add to the bonus dictionary the variables
    # and the their values and check for errors
    for line in input_data:
        list_line = line.lower().strip().split(' ')
        # lets see if the length of the row is equal
        # to the the length of the base line
        if len(list_line) != line_length:
            return "Input file error: Data lists are not the same length."
        if list_line[0] == 'x':
            bonus_dict['x'] = list_line[1:]
        if list_line[0] == 'dx':
            # lets check if the uncertainties of dx are all positive
            for index in range(1, len(list_line)):
                if float(list_line[index]) <= 0:
                    return 'Input file error:' \
                           'Not all uncertainties are positive.'
            bonus_dict['dx'] = list_line[1:]
        if list_line[0] == 'y':
            bonus_dict['y'] = list_line[1:]
        if list_line[0] == 'dy':
            # lets check if the uncertainties of dy are all positive
            for index in range(1, len(list_line)):
                if float(list_line[index]) <= 0:
                    return 'Input file error: ' \
                           'Not all uncertainties are positive.'
            bonus_dict['dy'] = list_line[1:]
    return bonus_dict


# this function converts the values of the bonus input dictionary
# from string to float
def convert_bonus_dict_to_float(input_dict):
    # lets create a new dictionary that holds the converted values
    converted__bonus_dict = {}
    x_str = input_dict['x']
    y_str = input_dict['y']
    dx_str = input_dict['dx']
    dy_str = input_dict['dy']
    a_str = input_dict['a']
    b_str = input_dict['b']
    temp_list_x = []      # to hold the converted values of x
    for value in x_str:
        temp_list_x.append(float(value))
        converted__bonus_dict['x'] = temp_list_x
    temp_list_y = []      # to hold the converted values of y
    for value in y_str:
        temp_list_y.append(float(value))
        converted__bonus_dict['y'] = temp_list_y
    temp_list_dx = []      # to hold the converted values of dx
    for value in dx_str:
        temp_list_dx.append(float(value))
    converted__bonus_dict['dx'] = temp_list_dx
    temp_list_dy = []      # to hold the converted values of dy
    for value in dy_str:
        temp_list_dy.append(float(value))
    converted__bonus_dict['dy'] = temp_list_dy
    temp_list_a = []      # to hold the converted values of a
    for value in a_str:
        temp_list_a.append(float(value))
    converted__bonus_dict['a'] = temp_list_a
    temp_list_b = []      # to hold the converted values of b
    for value in b_str:
        temp_list_b.append(float(value))
    converted__bonus_dict['b'] = temp_list_b
    converted__bonus_dict['x axis'] = input_dict['x axis']
    converted__bonus_dict['y axis'] = input_dict['y axis']
    return converted__bonus_dict


# this function calculates a temporary value for chi^2 using the (1) equation
def calculate_bonus_temp_chi(a_value, b_value, input_dict):
    chi_sq = 0
    for index in range(len(input_dict['x'])):
        temp_x = input_dict['x'][index]
        temp_x_plus = temp_x + input_dict['dx'][index]
        temp_x_minus = temp_x - input_dict['dx'][index]
        temp_y = input_dict['y'][index]
        temp_dy = input_dict['dy'][index]
        temp_chi_sq = ((temp_y - (a_value * temp_x + b_value)) /
                       (temp_dy ** 2 + (a_value * temp_x_plus + b_value -
                        (a_value * temp_x_minus + b_value)) ** 2) ** 0.5)
        chi_sq += (temp_chi_sq ** 2)
    return chi_sq


# this function calculates the minimum value of chi^2.
def calculate_bonus_chi_sq(input_dict):
    min_a = min(float(input_dict['a'][0]), float(input_dict['a'][1]))
    max_a = max(float(input_dict['a'][0]), float(input_dict['a'][1]))
    step_a = abs(float(input_dict['a'][2]))
    min_b = min(float(input_dict['b'][0]), float(input_dict['b'][1]))
    max_b = max(float(input_dict['b'][0]), float(input_dict['b'][1]))
    step_b = abs(float(input_dict['b'][2]))
    a_for_chi_min = min_a
    b_for_chi_min = min_b
    min_chi = calculate_bonus_temp_chi(min_a, min_b, input_dict)
    b = min_b
    # lets find the 'a' and 'b' for the minimum chi^2
    while b <= max_b:
        a = min_a
        while a <= max_a:
            temp_chi = calculate_bonus_temp_chi(a, b, input_dict)
            if temp_chi < min_chi:
                min_chi = temp_chi
                a_for_chi_min = a
                b_for_chi_min = b
            a += step_a
        b += step_b
    return [a_for_chi_min, step_a, b_for_chi_min, step_b, min_chi]


# this function creates lists to all the 'a' and chi^2 for the best 'b'
def parameters_for_non_linear(input_dict, min_b):
    min_a = min(float(input_dict['a'][0]), float(input_dict['a'][1]))
    max_a = max(float(input_dict['a'][0]), float(input_dict['a'][1]))
    step_a = abs(float(input_dict['a'][2]))
    a_list = []
    chi_sq_list = []
    a = min_a
    while a <= max_a:
        a_list.append(a)
        chi_for_a = calculate_bonus_temp_chi(a, min_b, input_dict)
        chi_sq_list.append(chi_for_a)
        a += step_a
    return [a_list, chi_sq_list]


# this function plots and saves the bonus fit for chi^2 in relation to 'a'
def bonus_chi_sq_of_a_plot(non_linear_points, min_b):
    plt.clf()
    x = non_linear_points[0]
    y = non_linear_points[1]
    plt.plot(x, y)
    plt.xlabel("a")
    mini_b = str(min_b)
    plt.ylabel("chi2(a,b="+mini_b+")")
    plt.savefig('numeric_sampling.svg', bbox_inches="tight")


# this function plots and saves the bonus fit
def bonus_linear_plot(input_dict, parameters):
    # lets find the maximum and minimum values of 'x' and their 'y' values
    x_min_and_max_values_bonus = find_x_min_and_max(input_dict)
    y_min_and_max_values_bonus = []
    for xi in x_min_and_max_values_bonus:
        yi = xi * parameters[0] + parameters[2]
        y_min_and_max_values_bonus.append(yi)
    x = input_dict['x']
    y = input_dict['y']
    dx = input_dict['dx']
    dy = input_dict['dy']
    x_axis = input_dict['x axis']
    y_axis = input_dict['y axis']
    plt.errorbar(x, y, xerr=dx, yerr=dy, fmt='none', ecolor="blue",
                 barsabove=True)
    plt.plot(x_min_and_max_values_bonus, y_min_and_max_values_bonus, 'r')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.savefig('linear_fit.svg')


# this is the main program for the bonus section
def search_best_parameter(filename):
    bonus_file = open(filename, 'r')
    bonus_data = bonus_file.readlines()
    # lets determine if the bonus file is in rows or in columns
    if row_or_columns(bonus_data) == "rows":
        bonus_input_dict = bonus_analyze_rows(bonus_data)
    else:
        bonus_input_dict = bonus_analyze_cols(bonus_data)
    # lets see if the 'row or columns' function returned an error
    if type(bonus_input_dict) == str:
        print(bonus_input_dict)
    else:
        converted_bonus_dict = convert_bonus_dict_to_float(bonus_input_dict)
        evaluated_parameters = calculate_bonus_chi_sq(converted_bonus_dict)
        chi_sq_red = evaluated_parameters[4] / \
            ((len(converted_bonus_dict['x']))-2)
        evaluated_parameters.append(chi_sq_red)
        print('a={0}+-{1}\nb={2}+-{3}\nchi2={4}\nchi2_reduced={5}'.format
              (evaluated_parameters[0], evaluated_parameters[1],
               evaluated_parameters[2], evaluated_parameters[3],
               evaluated_parameters[4], evaluated_parameters[5]))
        bonus_linear_plot(converted_bonus_dict, evaluated_parameters)
        graph_parameters = parameters_for_non_linear(converted_bonus_dict,
                                                     evaluated_parameters[2])
        bonus_chi_sq_of_a_plot(graph_parameters, evaluated_parameters[2])
    bonus_file.close()


search_best_parameter('input.txt')