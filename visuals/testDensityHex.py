
import matplotlib.pyplot as plot

import numpy as np

 

# Set the random seed for data generation using numpy

np.random.seed(1)

 

# Create random X data using numpy random module

xData = np.random.random_integers(1, 10, 100)

 

# Create random Y data using numpy random module

#yData = np.random.random_integers(1, 50, 500)

yData = np.arange(0, 100, 1)

 

# Plot the hexbin using the data genererated by numpy

plot.hexbin(xData, yData, gridsize=50)

 

# Provide the title for the plot

plot.title('Hexagonal binning using Python Matplotlib')

 

# Give x axis label for the spike raster plot

plot.xlabel('XData')

 

# Give y axis label for the spike raster plot

plot.ylabel('YData')

 

# Display the plot

plot.show()