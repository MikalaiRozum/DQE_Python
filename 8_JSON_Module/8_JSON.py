import os
import csv
import datetime
from Functions import normalize_text, capitalize_sentences
import re
import json

script_directory = os.path.dirname(os.path.abspath(__file__))
NEWSFEED_PATH = os.path.join(script_directory, 'newsfeed.txt')
CSV_FILE_PATH = os.path.join(script_directory, 'word_count.csv')
LETTER_COUNT_CSV_FILE_PATH = os.path.join(script_directory, 'letter_count.csv')


class JSONPublisher:
    def __init__(self, newsfeed_path, json_file_path=None):
        self.newsfeed_path = newsfeed_path
        self.json_file_path = json_file_path

    def publish_from_json(self):
        try:
            if self.json_file_path is None:
                # If json_file_path is not provided, look for a JSON file in the script's directory
                json_files = [file for file in os.listdir(script_directory) if file.endswith('.json')]
                if not json_files:
                    print('ERROR: No JSON files found in the script directory. Please provide a valid JSON file path.')
                    return False
                elif len(json_files) == 1:
                    self.json_file_path = os.path.join(script_directory, json_files[0])
                else:
                    print('Multiple JSON files found in the script directory. Please provide the specific JSON file path.')
                    return False

            with open(self.json_file_path, 'r') as json_file:
                data = json.load(json_file)

            for key, publication_info in data.items():
                publication_type = publication_info.get('publication_type', '').strip().capitalize()
                text = publication_info.get('text', '').strip()

                if publication_type and text:
                    content_publisher = ContentPublisher(publication_type, text)

                    if publication_type == 'News':
                        current_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
                        city = publication_info.get('city', '').strip()
                        if city:
                            content_publisher.body = f'News -------------------------\n{text}\n{city}, {current_time}'
                        else:
                            print('ERROR: City information missing for News. Skipping publication.')

                    elif publication_type == 'Personal blog':
                        author = publication_info.get('Author', '').strip()
                        if author:
                            content_publisher.body = f'Personal blog ----------------\n{text}\nAuthor: {author}'
                        else:
                            print('ERROR: Author information missing for Personal blog. Skipping publication.')

                    elif publication_type == 'Private ad':
                        expiration_date_str = publication_info.get('expiration_date', '').strip()
                        expiration_date = datetime.datetime.strptime(expiration_date_str, "%d/%m/%Y")
                        current_date = datetime.datetime.now()
                        days_left = (expiration_date - current_date).days
                        content_publisher.body = f'Private ad -------------------\n{text}\nActual until: {expiration_date.strftime("%d/%m/%Y")}, {days_left} days left'

                    else:
                        print(f'ERROR: Unknown publication type "{publication_type}". Skipping publication.')

                    content_publisher.write_to_file()

            # Remove file if it was successfully processed
            os.remove(self.json_file_path)
            print(f'INFO. Successful. Publications added from JSON. JSON file: {self.json_file_path} removed')
            return True

        except Exception as e:
            print(f'INFO. Failed to publish from JSON. Error: {e}')
            return False

class WordCounter:
    def __init__(self, newsfeed_path, csv_file_path):
        self.newsfeed_path = newsfeed_path
        self.csv_file_path = csv_file_path

    def update_word_count_csv(self):
        try:
            with open(self.newsfeed_path, 'r') as file:
                newsfeed_text = file.read().lower()

            # Use regular expression to remove non-alphabetic characters
            newsfeed_text = re.sub(r"(?<![a-zA-Z])'|'(?![a-zA-Z])|[^a-zA-Z\s']", '', newsfeed_text)
            word_count_dict = {word: newsfeed_text.split().count(word) for word in set(newsfeed_text.split())}

            with open(self.csv_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['word', 'count']
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(fieldnames)

                for word, count in word_count_dict.items():
                    writer.writerow([word, count])

        except Exception as e:
            print(f'INFO. Failed to update word count CSV. Error: {e}')


class LetterCounter:
    def __init__(self, newsfeed_path, letter_count_csv_file_path):
        self.newsfeed_path = newsfeed_path
        self.letter_count_csv_file_path = letter_count_csv_file_path

    def update_letter_count_csv(self):
        try:
            with open(self.newsfeed_path, 'r') as file:
                newsfeed_text = file.read()

            # Count the number of each letters
            letter_count_dict = {letter: newsfeed_text.lower().count(letter) for letter in set(newsfeed_text.lower()) if
                                 letter.isalpha()}
            uppercase_count_dict = {letter.lower(): newsfeed_text.count(letter) for letter in set(newsfeed_text) if
                                    letter.isupper()}

            with open(self.letter_count_csv_file_path, mode='w', newline='') as csv_file:
                fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(fieldnames)

                for letter, count_all in letter_count_dict.items():
                    count_uppercase = uppercase_count_dict.get(letter, 0)
                    percentage = round((count_uppercase / count_all) * 100, 2) if count_all > 0 else 0

                    writer.writerow([letter, count_all, count_uppercase, f"{percentage}%"])

        except Exception as e:
            print(f'INFO. Failed to update letter count CSV. Error: {e}')

class ContentPublisher:
    def __init__(self, content_type, text, body=''):
        self.type = content_type
        self.text = text
        self.body = body

    def write_to_file(self):
        try:
            with open(NEWSFEED_PATH, 'a') as f:
                f.write(self.body + '\n\n')
            print('INFO. Successful. New publication added.')
            return True
        except Exception as e:
            print(f'INFO. Fail. New publication was not added. Error: {e}')
            return False

    def publish(self):
        try:
            body_creator = {
                "NEWS": self.create_news_body,
                "PRIVATE AD": self.create_private_ad_body,
                "PERSONAL BLOG": self.create_personal_blog_body
            }
            self.body = body_creator.get(self.type.upper(), self.default_body)()
        except Exception as e:
            print(f'{e}')
            return False

        return self.write_to_file() if self.body else False

    @staticmethod
    def default_body():
        return ''

    def create_news_body(self):
        current_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M")
        max_retries = 3
        for _ in range(max_retries):
            city = input('City: ').strip().capitalize()
            if city.isalpha():
                break
            else:
                print("ERROR: City name should contain only alphabetic characters. Please try again.")
        else:
            print("Reached maximum number of retries. Exiting.")
            return None

        return f'News -------------------------\n{self.text}\n{city}, {current_time}'

    def create_private_ad_body(self):
        days_left, expiration_date = self.calculate_time_until_expiration()
        return f'Private ad -------------------\n{self.text}\nActual until: {expiration_date.strftime("%d/%m/%Y")}, {days_left} days left'

    @staticmethod
    def calculate_time_until_expiration():
        try:
            expiration_date_input = input('Please input "Actual until" date in format d/m/Y: ')
            expiration_date = datetime.datetime.strptime(expiration_date_input, "%d/%m/%Y")
            current_date = datetime.datetime.now()

            if expiration_date < current_date:
                raise ValueError("Expiration date cannot be in the past.")

            days_left = (expiration_date - current_date).days
            return str(days_left), expiration_date
        except Exception as e:
            print(f'ERROR: Enter a valid future date in the following format: d/m/Y. Error: {e}')
            return '', None

    def create_personal_blog_body(self):
        author = input('Author: ').strip().capitalize()
        return f'Personal blog ----------------\n{self.text}\nAuthor: {author}'


class InputHandler:
    @staticmethod
    def get_text_input():
        choice = input('Choose an option (Create text / Load text): ').strip().lower()

        if choice == 'create text':
            text = input('Enter the text: ')
        elif choice == 'load text':
            text = InputHandler.load_text_from_file()
        else:
            print('Invalid option. Please choose either "Create text" or "Load text".')
            return None

        return text

    @staticmethod
    def load_text_from_file():
        load_option = input('Choose an option (Select from default folder / Input file path): ').strip().lower()

        if load_option == 'select from default folder':
            file_path = os.path.join(script_directory, 'text.txt')
        elif load_option == 'input file path':
            file_path = input('Enter the file path: ').strip()
        else:
            print('Invalid option. Please choose either "Select from default folder" or "Input file path".')
            return None

        try:
            with open(file_path, 'r') as file:
                text = file.read()

            remove_file = input('Do you want to remove the processed file? (yes/no): ').strip().lower()
            if remove_file == 'yes':
                os.remove(file_path)
                print(f'File {file_path} removed successfully.')
            elif remove_file != 'no':
                print('Invalid option. Please choose either "yes" or "no".')

            return text
        except FileNotFoundError:
            print(f'ERROR: File not found at {file_path}')
        except PermissionError:
            print(f'ERROR: Permission denied. Make sure you have the necessary permissions to read the file at {file_path}')
        except Exception as e:
            print(f'Error loading text from file: {e}')

        return None


if __name__ == "__main__":
    allowed_content_types = ["News", "Private ad", "Personal blog"]

    user_choice = input('Choose an option (Create text / Load text / Load from JSON): ').strip().lower()

    if user_choice == 'load from json':
        json_option = input('Choose an option (Provide JSON path / Load from script directory): ').strip().lower()

        if json_option == 'provide json path':
            json_file_path = input('Enter the JSON file path: ').strip()
            json_publisher = JSONPublisher(NEWSFEED_PATH, json_file_path)
            json_publisher.publish_from_json()
        elif json_option == 'load from script directory':
            json_publisher = JSONPublisher(NEWSFEED_PATH)
            json_publisher.publish_from_json()
        else:
            print('Invalid option. Please choose either "Provide JSON path" or "Load from script directory".')

    else:
        content_type = input('Choose what you want to publish (News, Private ad, Personal blog): ').strip().capitalize()

        if content_type not in allowed_content_types:
            print('ERROR: Incorrect publishing type. Available types: News, Private ad, Personal blog')
        else:
            text = InputHandler.get_text_input()

            if text is not None:
                normalized_text = normalize_text(text)
                normalized_sentences = capitalize_sentences(normalized_text)
                final_text = ' '.join(normalized_sentences)
                new_publication_object = ContentPublisher(content_type, final_text)
                new_publication_object.publish()

                word_counter = WordCounter(NEWSFEED_PATH, CSV_FILE_PATH)
                letter_counter = LetterCounter(NEWSFEED_PATH, LETTER_COUNT_CSV_FILE_PATH)
                word_counter.update_word_count_csv()
                letter_counter.update_letter_count_csv()
