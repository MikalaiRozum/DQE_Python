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

# Iteration through each dictionary in dicts_list (enumerate - to keep track of the dictionary number (from 1))
for i, dictionary in enumerate(dicts_list, start=1):
    for key, value in dictionary.items():
        # Checking if the key is already in the result_dict
        if key in common_dict:
            # If it is, compare the values and update if the current value is greater
            if value > common_dict[key]:
                common_dict[key] = value
                # Rename the key based on the dictionary number
                common_dict[f'{key}_{i}'] = common_dict.pop(key)
        else:
            # If the key is not in common_dict
            common_dict[key] = value

print(common_dict)