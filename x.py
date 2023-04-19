import numpy as np
import matplotlib.pyplot as plt

# define x and y values
x = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
y = np.array([0.03, 0.028, 0.0275, 0.0263, 0.0254, 0.0249, 0.0241, 0.0238, 0.0235, 0.022, 0.02, 0.018, 0.016, 0.0156, 0.0138, 0.0128, 0.01, 0.0091, 0.0085, 0.0075, 0.007, 0.005, 0.0038, 0.0031, 0.00254, 0.0023, 0.0018, 0.00161, 0.0015])

# create log scale plots
fig, ax = plt.subplots()
ax.set_xscale('log')
ax.set_yscale('log')

# plot the data
ax.plot(x, y)

# add labels and title
ax.set_xlabel('X Values (log scale)')
ax.set_ylabel('Y Values (log scale)')
ax.set_title('Eckert Curve')

# set the x-value you want to find the corresponding y-value for
x_target = 3.016

# find the index of the closest x-value
index = np.abs(x - x_target).argmin()

# get the corresponding y-value
y_target = y[index]

# print the result
print(f"The corresponding y-value for x={x_target} is y={y_target}")

# plot a marker at the x_target and y_target coordinates
ax.plot(x_target, y_target, 'ro', label=f'x={x_target:.3f}, y={y_target:.3f}')
ax.legend()

plt.show()