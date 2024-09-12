import random
import os
import hawkcatcher

def divide_by_zero():
    a = random.randint(1, 100)
    return a / 0

def trigger_manual_exception():
    messages = ["Invalid input", "Out of range", "Manual trigger"]
    raise ValueError(random.choice(messages))

def invalid_operation():
    operations = [None + 1, 'abc' - 2, {} + []]
    return random.choice(operations)

def index_out_of_range():
    lst = random.sample(range(10), 5)
    return lst[10] 

def key_error():
    d = {'name': 'Alice', 'age': 30}
    keys = ['address', 'phone', 'city']
    return d[random.choice(keys)]

def assertion_failure():
    values = [(10, 20), (5, 10), (2, 8)]
    a, b = random.choice(values)
    assert a > b, "Assertion failed: a is not greater than b" 

def value_error():
    invalid_strings = ['abc', 'NaN', 'invalid']
    return int(random.choice(invalid_strings)) 

exceptions = [
    divide_by_zero, trigger_manual_exception, 
    invalid_operation, index_out_of_range, key_error, 
    assertion_failure, value_error
]

token = os.getenv('HAWK_TOKEN')
hawkcatcher.init(token)

for _ in range(10):
    try:
        func = random.choice(exceptions)
        func()
    except Exception as e:
        random_ip = f'{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}'
        hawkcatcher.send(e, {'ip': random_ip, 'value': random.randint(1, 100)})