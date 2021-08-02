library(ggplot2)

#Sim Graphs

#Basic Pressure vs Flow Rates for each orifice plate size (for a given C_d)
data<-read.csv('~/Downloads/simulated_flow_rates_by_pressure_diff.csv')
data$int_diameter = as.factor(data$int_diameter)

ggplot(data, aes(x=pressure_diff, y=flow_rate, color=int_diameter)) + geom_line() + labs(
       title = "Simulated Flow Rates for Pressure Differentials", 
       subtitle = "Comparing theoretical performance of orifice plate internal diameters",  
       x = "Pressure Differential", y = "Flow Rate (L/m)", color = "Orifice Size ")


# experimental data graphs

#Comparing Different Sensor Types
#get raw source data from python export
diff_comp<-read.csv('~/flow_modeling/flow_modeling/pressure_sensor_diff_comparison.csv')
#create pivot version to view sensors as categories
diff_comp_pivot<-diff_comp %>% pivot_longer(cols=ends_with("diff"), names_to="sensor_type", values_to = "pressure_diff")
ggplot(diff_comp_pivot, aes(x=measured_flow, y=pressure_diff, color=sensor_type)) + 
  geom_line() + labs(title="External and Intra-Catheter Pressure Sensor Concordance", subtitle = "Do different sensor types perform consistently in changing flow conditions?", x="Flow Rate (L/m)", y="Pressure Difference between Distal and Proximal (mmHg)", color="Sensor Type")


#Comparing Sensor Performance in Different Pipe Sizes
#graph for each pipe size, with all orifice plates graphed on each. 
#this should have pressure_diff, (measured)flow_rate, and int_diameter for each orifice plate
#produce one of these for each pipe diameter
pipe_comp<-read.csv('~/CSV_NAME_HERE')
pipe_comp$int_diameter = as.factor(pipe_comp$int_diameter)
ggplot(pipe_comp, aes(x=pressure_diff, y=flow_rate, color=int_diameter)) + geom_line() + labs(
  title = "Pressure Differentials Across Orifice Plates as Flow Rate Increases", 
  subtitle = "",  
  x = "Pressure Differential", y = "Flow Rate", color = "Orifice Size")



