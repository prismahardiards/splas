# Library used
import math as mt

# Example dataset
data = [1,5,10,15,20]

# Calculate mean
total = sum(data)
n = len(data)
mean = total / n
print("mean", mean)

# Calculate standard deviation
square = ((x - mean) ** 2 for x in data)
var = sum(square) / (n - 1)
std = mt.sqrt(var)
print("standard deviation", std)

# Calculate kurtosis
quad = sum((x - mean) ** 4 for x in data)
G2 = ((n*(n+1)/((n-1)*(n-2)*(n-3)))*(quad/(std**4))) - (3*(n-1)**2/((n-2)*(n-3)))
print("kurtosis", G2)