import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Read the CSV file using pandas
# /file path/home/location
csv_file_path = '/home/murtaza/catkin_ws/src/my_rosbag_processor/delay_vs_distance_231219_103504.csv'

df = pd.read_csv(csv_file_path)

# Filter out values less than -10000 and greater than 10000
filtered_df = df[(df['v2x_delay'] >= -10000) & (df['v2x_delay'] <= 10000) & (df['e2e_delay'] >= -10000) & (df['e2e_delay'] <= 10000)]

# Group data by distance intervals (assuming the column name for distance is 'distance')
distance_intervals = pd.cut(filtered_df['distance'], bins=range(0, int(filtered_df['distance'].max()) + 10, 10), right=False)

# Calculate average v2x_delay and e2e_delay for each interval
average_delay_by_distance = filtered_df.groupby(distance_intervals)['v2x_delay'].mean()
average_e2e_delay_by_distance = filtered_df.groupby(distance_intervals)['e2e_delay'].mean()

# Calculate max, min, and average values
max_v2x_delay = filtered_df['v2x_delay'].max()
min_v2x_delay = filtered_df['v2x_delay'].min()
avg_v2x_delay = filtered_df['v2x_delay'].mean()
std_v2x_delay = filtered_df['v2x_delay'].std()

max_e2e_delay = filtered_df['e2e_delay'].max()
min_e2e_delay = filtered_df['e2e_delay'].min()
avg_e2e_delay = filtered_df['e2e_delay'].mean()
std_e2e_delay = filtered_df['e2e_delay'].std()

print('Max v2x_delay: {}'.format(max_v2x_delay))
print('Min v2x_delay: {}'.format(min_v2x_delay))
print('Avg v2x_delay: {}'.format(avg_v2x_delay))
print('Std v2x_delay: {:.2f}'.format(std_v2x_delay))
print('Variance v2x_delay: {:.2f}'.format(filtered_df['v2x_delay'].var()))

print('Max e2e_delay: {}'.format(max_e2e_delay))
print('Min e2e_delay: {}'.format(min_e2e_delay))
print('Avg e2e_delay: {}'.format(avg_e2e_delay))
print('Std e2e_delay: {:.2f}'.format(std_e2e_delay))
print('Variance e2e_delay: {:.2f}'.format(filtered_df['e2e_delay'].var()))

# Get the interval edges as strings for better x-axis labels
interval_labels = [f'{interval.left}-{interval.right}' for interval in average_delay_by_distance.index]

# Plot bar graph for v2x_delay
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
average_delay_by_distance.plot(kind='bar', color='blue', alpha=0.7)
plt.title('Average v2x_delay for Every 10m Distance Interval')
plt.xlabel('Distance Interval (m)')
plt.ylabel('Average v2x_delay (ms)')
plt.xticks(range(0, len(average_delay_by_distance), 5), interval_labels[::5], rotation=45, ha='right')

# Plot bar graph for e2e_delay
plt.subplot(2, 1, 2)
average_e2e_delay_by_distance.plot(kind='bar', color='red', alpha=0.7)
plt.title('Average e2e_delay for Every 10m Distance Interval')
plt.xlabel('Distance Interval (m)')
plt.ylabel('Average e2e_delay (ms)')
plt.xticks(range(0, len(average_e2e_delay_by_distance), 5), interval_labels[::5], rotation=45, ha='right')

plt.subplots_adjust(hspace=0.5)

# Scatter plot distance vs v2x_delay
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.scatter(filtered_df['distance'], filtered_df['v2x_delay'], color='blue', label='v2x_delay', alpha=0.7)
plt.title('Scatter Plot: Distance vs v2x_delay')
plt.xlabel('Distance (m)')
plt.ylabel('v2x_delay (ms)')
plt.legend()
plt.xticks(np.arange(0, filtered_df['distance'].max() + 1, 50))  # Set x-axis ticks for every 20m

# Scatter plot distance vs e2e_delay
plt.subplot(2, 1, 2)
plt.scatter(filtered_df['distance'], filtered_df['e2e_delay'], color='red', label='e2e_delay', alpha=0.7)
plt.title('Scatter Plot: Distance vs e2e_delay')
plt.xlabel('Distance (m)')
plt.ylabel('e2e_delay (ms)')
plt.legend()
plt.xticks(np.arange(0, filtered_df['distance'].max() + 1, 50))  # Set x-axis ticks for every 20m

plt.subplots_adjust(hspace=0.5)

# Plot the PDF for v2x_delay
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)

plt.hist(filtered_df['v2x_delay'], bins=30, density=True, alpha=0.7, color='blue', label='v2x_delay')
mu_v2x, std_v2x = norm.fit(filtered_df['v2x_delay'])
xmin_v2x, xmax_v2x = plt.xlim()
x_v2x = np.linspace(xmin_v2x, xmax_v2x, 100)
p_v2x = norm.pdf(x_v2x, mu_v2x, std_v2x)
plt.plot(x_v2x, p_v2x, 'k', linewidth=2, label='Normal Distribution Fit')
plt.title('Probability Density Function (PDF) - v2x_delay')
plt.xlabel('v2x_delay (ms)')
plt.ylabel('Probability Density')
plt.legend()
plt.xticks(np.arange(0, xmax_v2x + 1, 100))

# Plot the PDF for e2e_delay
plt.subplot(2, 1, 2)
plt.hist(filtered_df['e2e_delay'], bins=30, density=True, alpha=0.7, color='red', label='e2e_delay')
mu_e2e, std_e2e = norm.fit(filtered_df['e2e_delay'])
xmin_e2e, xmax_e2e = plt.xlim()
x_e2e = np.linspace(xmin_e2e, xmax_e2e, 100)
p_e2e = norm.pdf(x_e2e, mu_e2e, std_e2e)
plt.plot(x_e2e, p_e2e, 'k', linewidth=2, label='Normal Distribution Fit')
plt.title('Probability Density Function (PDF) - e2e_delay')
plt.xlabel('e2e_delay (ms)')
plt.ylabel('Probability Density')
plt.legend()
plt.xticks(np.arange(0, xmax_e2e + 1, 100))

plt.subplots_adjust(hspace=0.5)

plt.tight_layout()
plt.show()

