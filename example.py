import os
from hawkcatcher import Hawk
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def helperFunction():
    return 1 / 0


class TestModule:

    def __init__(self):
        self.testMethod()

    def testMethod(self):
        helperFunction()


def main():
    token = os.getenv('HAWK_TOKEN')

    if token is None or token == "":
        print('Hawk token not provided. Please provide HAWK_TOKEN variable in .env file')
        return
    Hawk(token)
    helperFunction()


if __name__ == "__main__":
    main()
