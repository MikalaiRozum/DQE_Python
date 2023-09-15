import random
import string

'''Task 1. Create a list of random number of dicts (from 2 to 10)
    dict's random numbers of keys should be letter, 
    dict's values should be a number (0-100), 
    example:[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]'''

dicts_list = []

# Determination of the number of dictionaries to be created (between 2 and 10)
num_dicts = random.randint(2, 10)

# Loop 'num_dicts' times to create multiple dictionaries.
for _ in range(num_dicts):
    # Random number of keys between 2 and 10 for the current dictionary
    num_keys = random.randint(2, 10)
    # Creating a dictionary with 'num_keys' key-value pairs:
    # random.choice(string.ascii_lowercase) - choosing of random lowercase letter as the key
    # random.randint(0, 100) - generation of random integer between 0 and 100 as the value
    rand_dict = {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(num_keys)}
    dicts_list.append(rand_dict)

print(dicts_list)

'''Task 2. Get previously generated list of dicts and create one common dict:
    if dicts have same key, we will take max value, and rename key with dict number with max value
    if key is only in one dict - take it as is, 
    example:{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}'''

common_dict = {}
value_max = {}  # Dictionary to store the maximum values for each key
index_of_max = {}  # Dictionary to store the index where the maximum value was found for each key
count_of_max = {}  # Dictionary to store the count of times each key had a maximum value

# Iteration through each dictionary in dicts_list (enumerate - to keep track of the dictionary number (from 1))
for i, dictionary in enumerate(dicts_list, start=1):
    for key, value in dictionary.items():
        if key in value_max:
            # If the current 'value' is greater than the stored maximum value
            # Update 'value_max' with the new maximum value
            # Update 'index_of_max' with the current index 'i'
            # Increment the count of maximum values for this key
            if value > value_max[key]:
                value_max[key] = value
                index_of_max[key] = i
                count_of_max[key] += 1
            # If the current 'value' is not greater, increment the count
            else:
                count_of_max[key] += 1
        # If the key is not in 'value_max', initialize it with the current 'value'
        # Set the index where the maximum value was found to the current index 'i'
        # Initialize the count for this key to 1
        else:
            value_max[key] = value
            index_of_max[key] = i
            count_of_max[key] = 1
# Loop through the keys and maximum values in 'value_max'
for key, value in value_max.items():
    # If the key had more than one maximum value, create a new key in 'final_result' with the format 'key_index'
    if count_of_max[key] > 1:
        common_dict[f'{key}_{index_of_max[key]}'] = value
    # If not, store the key and its maximum value in 'final_result'
    else:
        common_dict[key] = value

print(common_dict)
