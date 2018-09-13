import csv
import helpers
import matplotlib.pyplot as plt
import numpy as np

Node_nums = [1, 2, 3, 4]
max_nodes = max(Node_nums)

# Read analytic data from file.
x_analytic = []
y_analytic = []
last_y = -1.
with open("Case5_n_analytic.csv", "r") as analytic_file:
    csvreader = csv.reader(analytic_file, delimiter=",", quotechar='"')
    for row in csvreader:
        x = float(row[0])
        y = float(row[1])
        if y != last_y:
            x_analytic.append(x)
            y_analytic.append(y)
            last_y = y

# Extract moments from distribution
analytic_moments = []
for i in range(0,2*max_nodes+1):
    new_moment = 0.
    for j in range(0,len(x_analytic)-1):
        dx = x_analytic[j+1]-x_analytic[j]
        x = (x_analytic[j+1]+x_analytic[j])/2.
        y = (y_analytic[j+1]+y_analytic[j])/2.
        new_moment += y*(x**i)*dx
    analytic_moments.append(new_moment)


print("Moments are: ")
for i in range(0,2*max_nodes+1):
    print("M_%i = %f" % (i, analytic_moments[i]))


x = np.linspace(1, 10, 300)

# Produce Figures 2a-d
plt.figure(2, figsize=(12,8), dpi=80)

for node_num in Node_nums:
    node_definitions = helpers.perform_moment_inversion(node_num, analytic_moments)

    plt.subplot(220+node_num)

    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")
    plt.plot([], color="#007F00", linestyle="--", label="LnEQMOM")

    plt.plot(x_analytic, y_analytic, color="#0A246A", linestyle="-")

    y = [helpers.f_num(x, node_definitions)/analytic_moments[0] for x in x]

    plt.plot(x, y, color="#007F00", linestyle="--")

    plt.legend()
    plt.ylabel(r"$n(\xi)$")
    plt.xlabel(r"$\xi$")
    plt.xlim(1., 10.)
    plt.ylim(0., 1.)

plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig("Figure2.png")
