from hawkcatcher import Hawk

hawk = Hawk({
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0SWQiOiI1ZTZmNWM3NzAzOWI0MDAwMjNmZDViODAiLCJpYXQiOjE1ODQzNTY0NzF9.t-5Gelx3MgHVBrxTsoMyPQAdQ6ufVbPsts9zZLW3gM8',
    'host': 'localhost:3000',
    'path': '/',
    'secure': False,
})


def helperFunction():
    return 1 / 0


class TestModule:

    def __init__(self):
        self.testMethod()

    def testMethod(self):
        helperFunction()

if __name__ == "__main__":
    try:
        TestModule()
    except Exception as e:
        hawk.catch()
