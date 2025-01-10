import os
from hawk_python_sdk import Hawk
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class InvalidToken(Exception):
    pass


class TestModule:
    def __init__(self, hawk):
        self.hawk = hawk

    @staticmethod
    def divide_by_zero():
        return 1 / 0

    def test_method(self):
        self.divide_by_zero()

    def mannual_sending(self):
        self.hawk.send(ValueError("lol"), {"ping": "pong", "number": 1})

    def send_custom_error(self):
        raise InvalidToken()

    def send_with_user(self):
        self.hawk.send(
            ValueError("USER"),
            None,
            {'id': 1, 'name': 'Alice'}
        )


def main():
    token = os.getenv('HAWK_TOKEN')

    if token is None or token == "":
        print('Hawk token not provided. Please provide HAWK_TOKEN variable in .env file')
        return
    hawk = Hawk(token)
    test = TestModule(hawk)
    test.mannual_sending()
    test.send_with_user()
    test.send_custom_error()


if __name__ == "__main__":
    main()
