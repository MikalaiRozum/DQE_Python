import re

original_text = """homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# Convert the original text to lowercase
original_text_lower = original_text.lower()
# Replace "iz" with "is" only when it's a standalone word
original_text_fixed = original_text_lower.replace(" iz ", " is ")
# Separate "iz" from fix“iZ”
original_text_fixed = re.sub(r'([^ ])“', r'\1 “', original_text_fixed)
# Split the text into sentences
sentences = re.split(r'(?<=[.!?])\s+', original_text_fixed)
# Capitalize the first letter of each sentence
normalized_sentences = [sentence.capitalize() for sentence in sentences]
# Join the normalized sentences
normalized_text = ' '.join(normalized_sentences)
# Extract the last words from each sentence with punctuation removing
last_words = [re.sub(r'[^\w\s]', '', sentence.split()[-1]) for sentence in sentences]
# Create a new sentence from last words
new_sentence = (" ".join(last_words) + ".").capitalize()
# Combine the normalized text with the new sentence
final_text = normalized_text + ' ' + new_sentence
print(final_text)

# Calculate the number of whitespace (spaces, tabs, and newlines).
whitespace_count = final_text.count(" ") + final_text.count("\t") + final_text.count("\n")
print(whitespace_count)