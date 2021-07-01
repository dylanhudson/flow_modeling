import math
import pandas as pd
import csv
import matplotlib.pyplot as plt


mass_flow = 0.0
pipe_diameter = .0208
internal_orifice_diameter = 0.005
discharge_coefficient = 0.8
fluid_density = 1000
pressure_diff = 4000

#reynolds variables
fluid_viscosity = 8.9 * pow(10,-4)
pipe_xsection_area = 0.0

orifice_diameter_ratio = internal_orifice_diameter / pipe_diameter

mass_flow = (discharge_coefficient / (1 - pow(orifice_diameter_ratio, 4))) * (math.pi / 4) * pow(internal_orifice_diameter, 2) * (math.sqrt((2*pressure_diff) * fluid_density))

print(f'mass_flow in kg/s: {mass_flow}')

mass_flow_kgpm = mass_flow * 60

print(f'mass flow in kg/min {mass_flow_kgpm}')


#reynolds_number = (mass_flow * pipe_diameter() / (fluid_viscosity * pipe_xsection_area)

def calculate_discharge_coefficient(flow_rate, internal_orifice_diameter, pressure_diff):
        C_d = ((flow_rate * 476) / (pow((internal_orifice_diameter *1000), 2) * math.sqrt(pressure_diff *133)))
        return C_d



def calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, internal_orifice_diameter, pressure_diff, fluid_density):
    mass_flow = (discharge_coefficient / (1 - pow(orifice_diameter_ratio, 4))) * (math.pi / 4) * pow(
        internal_orifice_diameter, 2) * (math.sqrt((2 * pressure_diff) * fluid_density))
    return mass_flow

def simulate_orifice_place_diameters(diameters, curr_pipe_diameter):
    mass_flows = {}
    for elem in diameters:
        orifice_diameter_ratio = elem / curr_pipe_diameter
        mass_flow = calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, elem, pressure_diff, fluid_density)
        mass_flows[str(elem)] = mass_flow
    return mass_flows

def simulate_pressure_differentials(pressure_deltas):
    mass_flows = {}
    for elem in pressure_deltas:
        mass_flow = calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, internal_orifice_diameter, elem, fluid_density)
        mass_flows[str(elem)] = mass_flow
    return mass_flows

def print_dictionary(my_dict):
    for key in my_dict:
        print(f'input: {key} result: {my_dict[key]}')

def output_dict_to_csv(my_dict, test_name):
    with open(test_name, 'w') as f:
        for key in my_dict.keys():
            f.write("%s,%s\n" % (key, my_dict[key]))

def populate_array(start, increment, end):
    my_list = []
    my_list.append(start)
    while start < end:
        start += increment
        my_list.append(start)
    return my_list


int_diameters = populate_array(0.001, 0.001, 0.02)

results = simulate_orifice_place_diameters(int_diameters, pipe_diameter)
print("Results:")
print_dictionary(results)

my_pressure_deltas = populate_array(0,100,7000)

results = simulate_pressure_differentials(my_pressure_deltas)

print_dictionary(results)

sim_list = []
for elem in int_diameters:
    orifice_diameter_ratio = elem / pipe_diameter
    results = simulate_pressure_differentials(my_pressure_deltas)
    sim_list.append(results)

#print(sim_list)

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("flow rates")
for i in range(len(sim_list)):
    plt.title("flow rates by int diameter")
    lists = sorted(sim_list[i].items())  # sorted by key, return a list of tuples
    x, y = zip(*lists)  # unpack a list of pairs into two tuples
    plt.plot(x, y)

#plt.show()

# read in flow rate csv
discharge_coefficients = {}
with open('5mm.csv') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        c_d = calculate_discharge_coefficient(float(row['flow_rate']), internal_orifice_diameter, float(row['pressure_diff']))
        flow_rate = row['flow_rate']
        print(f' flow rate : {flow_rate} | coefficient: {c_d}')

print_dictionary(discharge_coefficients)


