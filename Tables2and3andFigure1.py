import sys
import subprocess
import math
import re
import matplotlib.pyplot as plt
import numpy as np
import helpers

## Case variables

case_vars = {1: [3., 0.6, 3., 0.6],
             2: [1.2, 0.6, 3., 0.6],
             3: [3., 0.6, 5., 0.5],
             4: [3., 0.6, 1., 0.8]}

case_range = {1: [60, 60, 0.05],
              2: [60, 60, 0.15],
              3: [500, 450, 0.02],
              4: [60, 60, 0.2]}

article_errors_table_2 = {1: {2: [1.34e-16, 1.48e-16, 2.74e-16, 8.88e-16, 9.64e-16],
                              3: [1.41e-16, 1.48e-16, 2.74e-16, 8.88e-16, 9.64e-16, 2.03e-16, 3.56e-16],
                              4: [4.36e-16, 1.47e-16, 2.74e-16, 8.88e-16, 9.64e-16, 2.03e-16, 3.56e-16, 2.18e-16, 4.12e-16]},
                          2: {2: [1.35e-16, 1.27e-16, 2.67e-16, 8.84e-16, 9.63e-16],
                              3: [1.37e-16, 1.27e-16, 2.67e-16, 8.84e-16, 9.63e-16, 2.03e-16, 1.78e-16],
                              4: [4.35e-16, 1.27e-16, 2.67e-16, 8.84e-16, 9.63e-16, 2.03e-16, 1.78e-16, 2.19e-16, 4.12e-15]},
                          3: {2: [1.48e-16, 1.47e-16, 2.22e-16, 4.36e-16, 6.08e-16],
                              3: [1.97e-16, 1.48e-16, 2.22e-16, 4.36e-16, 6.08e-16, 7.81e-16, 8.21e-16],
                              4: [2.71e-16, 1.48e-16, 2.22e-16, 4.36e-16, 6.08e-16, 7.81e-16, 8.21e-16, 1.30e-16, 1.87e-16]},
                          4: {2: [1.34e-15, 1.28e-14, 2.66e-14, 8.81e-14, 9.61e-14],
                              3: [1.40e-15, 1.28e-14, 2.66e-14, 8.81e-14, 9.61e-14, 2.02e-14, 3.56e-14],
                              4: [4.36e-15, 1.27e-12, 2.66e-12, 8.81e-12, 9.61e-12, 2.02e-12, 3.56e-12, 2.19e-12, 4.12e-12]}}

article_errors_table_3 = {1: {2: 1.90e-13, 3: 2.21e-14, 4: 6.04e-16},
                          2: {2: 2.88e-12, 3: 3.93e-14, 4: 3.90e-14},
                          3: {2: 2.68e-2, 3: 6.68e-3, 4: 2.03e-3},
                          4: {2: 2.76e-1, 3: 1.10e-1, 4: 1.07e-1}}

def calc_err(expected, got):
    return 100.*abs(expected-got)/expected

case_analytic_moments = {}
case_numerical_nodes = {}
case_numerical_moments = {}

Node_nums = [2, 3, 4]

for case in case_vars:
    # Build analytic moments for the case.
    analytic_moments = []
    for k in range(0, 2*Node_nums[-1]+1):
        analytic_moments.append(helpers.lognormal_analytic_moment(k, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3]))
    case_analytic_moments[case] = analytic_moments

    # Calculate numerical moments for each set of node numbers
    numerical_nodes = {}
    numerical_moments = {}

    for node_num in Node_nums:
        node_definitions = helpers.perform_moment_inversion(node_num, analytic_moments)

        # Calculate numerical moments
        num_moments = []
        for k in range(0, 2*node_num+1):
            moment = 0
            for n in range(0, node_num):
                moment += node_definitions[n]['w']*helpers.lognormal_moment(k, node_definitions[n]['ab'], node_definitions['sig'])
            num_moments.append(moment)

        numerical_nodes[node_num] = node_definitions
        numerical_moments[node_num] = num_moments

    case_numerical_nodes[case] = numerical_nodes
    case_numerical_moments[case] = numerical_moments

# Calculate values in Table2
print("Table 2")
print("Case\tN=2\tN=3\tN=4")
for case in case_analytic_moments:
    for k in range(0, 2*Node_nums[-1]+1):
        report_string = ""
        if k == 0:
            report_string += "%i\t" % case
        else:
            report_string += " \t"

        for num in case_numerical_moments[case]:
            if k >= 2*case_numerical_nodes[case][num]['n']+1:
                report_string += "            \t"
            else:
                mom_err = abs(case_analytic_moments[case][k]-case_numerical_moments[case][num][k])/case_analytic_moments[case][k]
                report_string += "E_%i %.2e (%.1f%%)\t" % (k, mom_err, calc_err(article_errors_table_2[case][num][k],mom_err))
        print(report_string)
    print()


# Calculate values in Table3
# We will numerically integrate the expression.

Title_line = ["Case"]
for num_nodes in case_numerical_nodes[1]:
    Title_line.append("N={}".format(num_nodes))
case_lines = [Title_line]
for case in case_vars:
    case_line = [case]
    for num_nodes in case_numerical_nodes[case]:
        node_definitions = case_numerical_nodes[case][2]
        F = lambda x: helpers.f_lognormal(x, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3])
        P = lambda x: helpers.f_num_lognormal(x, node_definitions)

        d = helpers.l2diff(F, P, 1e-12, 500, 5000)/case_analytic_moments[case][0]
        case_line.append(d)
        case_line.append(calc_err(article_errors_table_3[case][num_nodes],d))
    case_lines.append(case_line)

print("Table 3")
for line in case_lines:
    if type(line[0]) is str:
        print("%s\t%s\t%s\t%s" % (line[0], line[1], line[2], line[3]))
    else:
        print("%i\t%e (%.2f%%)\t%e (%.2f%%)\t%e (%.2f%%)" % (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))

# Produce Figures 1a-d
plt.figure(1, figsize=(12,8), dpi=80)

Num_smooth = 1000
Num_point = 40
for case in case_vars:
    plt.subplot(220+int(case))

    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")
    plt.plot([], color="#007F00", linestyle="--", label="EQMOM each nodes")
    plt.plot([], color="#D82900", marker="o", markerfacecolor="white", linestyle="None", label="Approximation Distribution")

    x = np.linspace(1e-12,case_range[case][1], Num_smooth)
    y = np.array([helpers.f_lognormal(x, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3]) for x in x])
    plt.plot(x, y, color="#0A246A", linestyle="-")

    for i in range(0,4):
        node_definition = case_numerical_nodes[case][4][i]
        y = np.array([helpers.f_num_single_lognormal(x, case_numerical_nodes[case][4], i) for x in x])
        plt.plot(x, y, color="#007F00", linestyle="--")


    x = np.linspace(1e-12, case_range[case][1], Num_point)
    y = np.array([helpers.f_num_lognormal(x, case_numerical_nodes[case][4]) for x in x])
    plt.plot(x, y, color="#D82900", marker="o", markerfacecolor="white", linestyle="None")

    plt.legend()
    plt.ylabel(r"$n(\xi)$")
    plt.xlabel(r"$\xi$")
    plt.xlim(0,case_range[case][0])
    plt.ylim(0,case_range[case][2])

plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig("Figure1.png")
