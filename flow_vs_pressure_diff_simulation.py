# author: dylan
# github: @dylanhudson

# version: last tested with python 3.7

import math


#initalize bernoulli flow variables
mass_flow = 0.0
pipe_diameter = .0208
internal_orifice_diameter = 0.005
discharge_coefficient = 0.8
fluid_density = 1000 # constant if substance is a liquid; this value is for water.
pressure_diff = 4000

orifice_diameter_ratio = internal_orifice_diameter / pipe_diameter


# calculation and simulation functions #

def calculate_discharge_coefficient(flow_rate, internal_orifice_diameter, pressure_diff):
        C_d = ((flow_rate * 476) / (pow((internal_orifice_diameter *1000), 2) * math.sqrt(pressure_diff *133)))
        return C_d

def calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, internal_orifice_diameter, pressure_diff, fluid_density):
    mass_flow = (discharge_coefficient / (1 - pow(orifice_diameter_ratio, 4))) * (math.pi / 4) * pow(
        internal_orifice_diameter, 2) * (math.sqrt((2 * pressure_diff) * fluid_density))
    return mass_flow

def calculate_reynolds_number(mass_flow, pipe_diameter, fluid_viscosity, pipe_xsection_area):
    return ((mass_flow * pipe_diameter) / (fluid_viscosity * pipe_xsection_area))

#takes diameters as a list of floats, returns dictionary with key,value -> diameter,mass_flow
def calculate_mass_flow_for_list_of_orifice_place_diameters(diameters, curr_pipe_diameter, discharge_coefficient, pressure_diff, fluid_density):
    mass_flows = {}
    for elem in diameters:
        orifice_diameter_ratio = elem / curr_pipe_diameter
        mass_flow = calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, elem, pressure_diff, fluid_density)
        mass_flows[str(elem)] = mass_flow
    return mass_flows

#takes list of floats representing pressure deltas, returns mass_flows in dict with deltas as key
def simulate_pressure_differentials(pressure_deltas, discharge_coefficient, orifice_diameter_ratio, internal_orifice_diameter, fluid_density):
    mass_flows = []
    for elem in pressure_deltas:
        mass_flow_kgs = calculate_mass_flow_in_kg_per_sec(discharge_coefficient, orifice_diameter_ratio, internal_orifice_diameter, elem, fluid_density)
        #convert to L/min flow rate for easier visualization later
        mass_flow_lpm = mass_flow_kgs * 60
        my_tuple = (mass_flow_lpm, elem, internal_orifice_diameter)
        mass_flows.append(my_tuple)
    return mass_flows


# helper functions #

def print_dictionary(my_dict):
    for key in my_dict:
        print(f'{key},{my_dict[key]}')

def output_dict_to_csv(my_dict, output_file_name, headers):
    with open(output_file_name, 'w') as f:
        f.write(headers + "\n")
        for key in my_dict.keys():
            f.write("%s,%s\n" % (key, my_dict[key]))

#helper function to populate array with incremental data for simulations
def populate_array(start, increment, end):
    my_list = []
    my_list.append(start)
    while start < end:
        start += increment
        new = round(start, 4)
        my_list.append(new)
    return my_list

def list_of_tuples_to_csv(output_file_name, list_of_data_tuples, headers):
    with open(output_file_name, "w") as outfile:
        outfile.write(headers)
        for each in list_of_data_tuples:
            for elem in each:
                csv_string = str(elem).strip("(")
                csv_string = csv_string.strip(")")
                csv_string = csv_string.strip(" ")
                outfile.write('\n')
                outfile.write(csv_string)


### Simulation Driver ###

int_diameters = populate_array(0.001, 0.001, 0.008)

results = calculate_mass_flow_for_list_of_orifice_place_diameters(int_diameters, pipe_diameter, discharge_coefficient, pressure_diff, fluid_density)
my_pressure_deltas = populate_array(1,10,10000)

# for flow vs pressure diff by orifice size simulations
sim_list = []
for elem in int_diameters:
    orifice_diameter_ratio = elem / pipe_diameter
    results = simulate_pressure_differentials(my_pressure_deltas, discharge_coefficient, orifice_diameter_ratio, elem, fluid_density)
    sim_list.append(results)

sim_flow_headers = "flow_rate, pressure_diff, int_diameter"
list_of_tuples_to_csv("simulated_flow_rates_by_pressure_diff.csv", sim_list, sim_flow_headers)

