import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plt


predicted_value = 80
lower_confidence_interval_value = 0
upper_confidence_interval_value = 100


# Set the range based on the 95% confidence intervals
lower = lower_confidence_interval_value
upper = upper_confidence_interval_value

# Calculate the mean and standard deviation based on the predicted value
mean = predicted_value
std = (upper - lower) / (2 * 1.96)  # 1.96 is the z-score for 95% confidence

# Create the distribution variable
dist = truncnorm(
    (lower - mean) / std, 
    (upper - mean) / std, 
    loc=mean, 
    scale=std
)
# Generate a sample of 1000 values from this distribution
samples = dist.rvs(size=1000)

# Plot the distribution function
x = np.linspace(dist.ppf(0.01), dist.ppf(0.99), 100)
plt.plot(x, dist.pdf(x), 'r-', lw=5, alpha=0.6, label='gamma pdf')

# Plot the histogram of generated samples within the confidence interval range
plt.hist(samples[(samples >= lower_confidence_interval_value) & (samples <= upper_confidence_interval_value)], bins='auto', density=True, label='generated samples')

# Add labels and legend to the plot
plt.xlabel('Values')
plt.ylabel('Probability density')
plt.title('Gamma distribution and generated samples')
plt.legend()

# Show the plot
plt.show()