import os
import datetime

# Determine the path to the newsfeed.txt file relative to the current script's location
script_directory = os.path.dirname(os.path.abspath(__file__))
NEWSFEED_PATH = os.path.join(script_directory, 'newsfeed.txt')

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
                print("ERROR. City name should contain only alphabetic characters. Please try again.")
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
            return str(days_left), expiration_date  # Return both days left and the expiration date
        except Exception as e:
            print(f'ERROR. Enter a valid future date in the following format: d/m/Y. Error: {e}')
            return '', None

    def create_personal_blog_body(self):
        author = input('Author: ').strip().capitalize()
        return f'Personal blog ----------------\n{self.text}\nAuthor: {author}'


if __name__ == "__main__":
    allowed_content_types = ["News", "Private ad", "Personal blog"]
    content_type = input('Choose what you want to publish: News, Private ad, Personal blog): ')

    if content_type.strip().capitalize() not in allowed_content_types:
        print('ERROR. Incorrect publishing type. Available types: News, Private ad, Personal blog')
    else:
        text = input('Text: ')
        new_publication_object = ContentPublisher(content_type, text)
        new_publication_object.publish()