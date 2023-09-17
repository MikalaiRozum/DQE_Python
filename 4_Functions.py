import re
import random
import string

# Module 2 Task

original_text = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


def normalize_text(text):
    # Convert the text to lowercase
    text_lower = text.lower()
    # Replace "iz" with "is" only when it's a standalone word
    text_fixed = text_lower.replace(" iz ", " is ")
    # Separate "iz" from fix“iZ”
    text_fixed = re.sub(r'([^ ])“', r'\1 “', text_fixed)
    return text_fixed


def capitalize_sentences(text):
    # Split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Capitalize the first letter of each sentence
    normalized_sentences = [sentence.capitalize() for sentence in sentences]
    return normalized_sentences


def extract_last_words(sentences):
    # Extract the last words from each sentence with punctuation removed
    last_words = [re.sub(r'[^\w\s]', '', sentence.split()[-1]) for sentence in sentences]
    return last_words


def create_new_sentence(last_words):
    # Create a new sentence from last words
    new_sentence = (" ".join(last_words) + ".").capitalize()
    return new_sentence


def count_whitespace(text):
    # Calculate the number of whitespace (spaces, tabs, and newlines).
    whitespace_count = text.count(" ") + text.count("\t") + text.count("\n")
    return whitespace_count


normalized_text = normalize_text(original_text)
normalized_sentences = capitalize_sentences(normalized_text)
last_words = extract_last_words(normalized_sentences)
new_sentence = create_new_sentence(last_words)
final_text = ' '.join(normalized_sentences) + ' ' + new_sentence
whitespace_count = count_whitespace(final_text)

print(final_text)
print(whitespace_count)


# Module 3 Task

def generate_random_dict(num_keys):
    return {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(num_keys)}


def generate_list_of_dicts(num_dicts):
    return [generate_random_dict(random.randint(2, 10)) for _ in range(num_dicts)]


def create_common_dict(dicts_list):
    common_dict = {}
    value_max = {}  # Dictionary to store the maximum values for each key
    index_of_max = {}  # Dictionary to store the index where the maximum value was found for each key
    count_of_max = {}  # Dictionary to store the count of times each key had a maximum value

    def update_max_values(key, value, i):
        if key in value_max:
            if value > value_max[key]:
                # If the current 'value' is greater than the stored maximum value
                # Update 'value_max' with the new maximum value
                # Update 'index_of_max' with the current index 'i'
                # Increment the count of maximum values for this key
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

    for i, dictionary in enumerate(dicts_list, start=1):
        for key, value in dictionary.items():
            update_max_values(key, value, i)

    for key, value in value_max.items():
        if count_of_max[key] > 1:
            common_dict[f'{key}_{index_of_max[key]}'] = value
        else:
            common_dict[key] = value

    return common_dict


def main():
    num_dicts = random.randint(2, 10)
    dicts_list = generate_list_of_dicts(num_dicts)
    common_dict = create_common_dict(dicts_list)

    print(dicts_list)
    print(common_dict)


if __name__ == "__main__":
    main()