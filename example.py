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
    Hawk(os.getenv('HAWK_TOKEN'))
    helperFunction()


if __name__ == "__main__":
    main()
