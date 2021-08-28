import hawkcatcher
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class InvalidToken(Exception):
    pass


class Module:
    @staticmethod
    def divide_by_zero():
        return 1 / 0

    def test_method(self):
        self.divide_by_zero()

    def mannual_sending(self):
        hawkcatcher.send(ValueError("lol"), {"ping": "pong", "number": 1})

    def send_custom_error(self):
        raise InvalidToken()

    def send_with_user(self):
        hawkcatcher.send(
            ValueError("USER"),
            None,
            {'id': 1, 'name': 'Alice'}
        )


def main():
    token = os.getenv('HAWK_TOKEN')

    if token is None or token == "":
        print('hawkcatcher token not provided. Please provide HAWK_TOKEN variable in .env file')
        return
    hawkcatcher.init(token)
    test = Module()
    test.mannual_sending()
    test.send_with_user()
    test.send_custom_error()


if __name__ == "__main__":
    main()
