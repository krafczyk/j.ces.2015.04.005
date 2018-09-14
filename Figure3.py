import csv
import helpers
import matplotlib.pyplot as plt
import numpy as np
import math

node_num = 3

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

x = np.linspace(1, 10, 300)

time_end = 200.0

# Produce Figures 3a-d
plt.figure(3, figsize=(12,8), dpi=80)

# Produce Figure 3a
plt.subplot(221)

plt.plot([], color="#007F00", linestyle="-.", label="LnEQMOM N=3, $N_\\alpha$ = 20")
plt.plot([], color="#956363", linestyle="--", label="EQMOM each nodes")
plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")

plt.plot(x_analytic, y_analytic, color="#0A246A", linestyle="-")

node_definitions = {'n': node_num}
sigma = None
for i in range(0, node_num):
    node_name = "node%i" % i

    case_dir = "case5N%i" % node_num

    sigma_data = helpers.load_probe_data("%s/postProcessing/probes/0/sigma.%s.populationBalance" % (case_dir, node_name))
    if sigma is None:
        sigma = sigma_data[time_end]
    else:
        if sigma_data[time_end] != sigma:
            print("ERROR!!! sigma is different!!")
            sys.exit(-1)
        else:
            sigma = sigma_data[time_end]

    abscissa_data = helpers.load_probe_data("%s/postProcessing/probes/0/abscissa.%s.populationBalance" % (case_dir, node_name))
    weight_data = helpers.load_probe_data("%s/postProcessing/probes/0/weight.%s.populationBalance" % (case_dir, node_name))
    node_definitions[i] = {'w': weight_data[time_end], 'ab': math.log(abscissa_data[time_end])}
node_definitions['sig'] = sigma

moment0_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.0.populationBalance" % case_dir)

for i in range(0, node_num):
    y = [node_definitions[i]['w']*helpers.lognormal_kern(x, node_definitions[i]['ab'], node_definitions['sig'])/moment0_data[200.0] for x in x]

    plt.plot(x, y, color="#956363", linestyle="--")

y = [helpers.f_num_lognormal(x, node_definitions)/moment0_data[200.0] for x in x]

plt.plot(x, y, color="#007F00", linestyle="--")

plt.legend()
plt.ylabel(r"$n(\xi)$")
plt.xlabel(r"$\xi$")
plt.xlim(1., 10.)
plt.ylim(0., 0.65)

# Produce Figure 3d
plt.subplot(224)

plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")
plt.plot([], color="#007F00", linestyle="None", marker="o", markerfacecolor="white", label="LnEQMOM N=3, $N_\\alpha$ = 20")
plt.plot([], color="#D82900", linestyle="None", marker="s", markerfacecolor="white", label="QMOM N=3")

d43_data = helpers.load_probe_data("Vanni2000_d43_Case5.dat")

x = d43_data.keys()
y = d43_data.values()

plt.plot(x, y, color="#0A246A", linestyle="-") 

moment3_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.3.populationBalance" % case_dir)
moment4_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.4.populationBalance" % case_dir)

# Build set of position values to use
x_all = sorted(list(moment3_data.keys()))
x = []
x = x + [x_all[i] for i in range(0,10, 2) ]
x = x + [x_all[i] for i in range(10,50, 10) ]
x = x + [x_all[i] for i in range(50,100, 25) ]
x = x + [x_all[i] for i in range(100,1000, 45) ]
x = x + [x_all[len(x_all)-1]]

y = [moment4_data[x]/moment3_data[x] for x in x]

plt.plot(x, y, color="#007F00", linestyle="None", marker="o", markerfacecolor="white")

plt.legend()
plt.ylabel(r"$d_{43}$")
plt.xlabel(r"$t$")
plt.xlim(0., 200.)
plt.ylim(1., 5.)

# Finished, adjust and save

plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig("Figure3.png")