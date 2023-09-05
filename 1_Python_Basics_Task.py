import numpy as np
import random

# 1. Create list of 100 random numbers from 0 to 1000

# With numpy
# tolist() method convert numpy array into a python list
random_numbers_n = np.random.randint(0, 1001, 100).tolist()
print(random_numbers_n)

# With random
random_numbers_r = random.sample(range(1001), 100)
print(random_numbers_r)

# 2. Sort list from min to max (without using sort())

# Original list
print("Original List:", random_numbers_r)

# Sorting list using nested loops
# The outer loop iterates through each element of the list
for i in range(0, len(random_numbers_r)):
    # The inner loop iterates through elements to the right of the current element 'i'
    for j in range(i+1, len(random_numbers_r)):
        # Comparing of current element 'i' with the elements to its right
        if random_numbers_r[i] >= random_numbers_r[j]:
            # If the current element is greater than or equal to the next element, swap them
            random_numbers_r[i], random_numbers_r[j] = random_numbers_r[j], random_numbers_r[i]

# Sorted list
print("Sorted List:", random_numbers_r)

# 3. Calculate average for even and odd numbers and print both average result in console

sum_even = 0
count_even = 0
sum_odd = 0
count_odd = 0

for numb in random_numbers_r:
    if numb % 2 == 0:  # Check if the number is even
        sum_even += numb  # Sum of  even number
        count_even += 1   # Count of even numbers
    else:
        sum_odd += numb
        count_odd += 1

# Average calculation
average_even = sum_even / count_even if count_even > 0 else 0
average_odd = sum_odd / count_odd if count_odd > 0 else 0

print("Average even:", round(average_even, 2))
print("Average odd:", round(average_odd, 2))