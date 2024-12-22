# Hawk Python Catcher

Python errors Catcher module for [Hawk.so](https://hawk.so).

## Usage

Register an account and get a new project token.

If you want to connect specific frameworks see [Flask integration](./docs/flask.md), [FastAPI integration](./docs/fastapi.md).

### Install module

Install `hawk-python-sdk` from PyPI.

```shell
$ pip install hawk-python-sdk
```

Import Catcher module to your project.

```python
from hawk_python_sdk import Hawk
```

Then enable Hawk Catcher with your token and domain.

```python
hawk = Hawk(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0SWQiOiI1ZTZmNWM3NzAzOWI0MDAwMjNmZDViODAiLCJpYXQiOjE1ODQzNTY0NzF9.t-5Gelx3MgHVBrxTsoMyPQAdQ6ufVbPsts9zZLW3gM8")
```

Now all global errors would be sent to Hawk.

### Try-except

If you want to catch errors in try-except blocks then use `hawk.catch()` in except:

```python
try:
    ...
except:
    hawk.send()
```

### Manual sending

You can also pass event to the `hawk.send()` call, for example:

```python
try:
    ...
except:
    hawk.send(ValueError("error description"))
```

### Event context

It is possible to pass additional event context for debugging purposes:

```python
try:
    ...
except:
    hawk.send(ValueError("error description"), {"params": "value"})
```

### Affected user

You can also pass user, who affected with specific error:

```python
try:
    ...
except:
    hawk.send(ValueError("error description"), {"params": "value"}, {"id": 123})
```

## Init params

To init Hawk Catcher just pass a project token.

```python
hawk = Hawk('1234567-abcd-8901-efgh-123456789012')
```

### Additional params

If you need to use custom Hawk server then pass a dictionary with params.

```python
hawk = Hawk({
    'token': '1234567-abcd-8901-efgh-123456789012',
    'collector_endpoint': 'https://<id>.k1.hawk.so',
})
```

Parameters:

| name                 | type                   | required     | description                                                              |
| -------------------- | ---------------------- | ------------ | ------------------------------------------------------------------------ |
| `token`              | str                    | **required** | Your project's Integration Token                                         |
| `release`            | str                    | optional     | Release name for Suspected Commits feature                               |
| `collector_endpoint` | string                 | optional     | Collector endpoint for sending event to                                  |
| `context`            | dict                   | optional     | Additional context to be send with every event                           |
| `before_send`        | Callable[[dict], None] | optional     | This Method allows you to filter any data you don't want sending to Hawk |

## Requirements

- Python \>= 3.9
- requests

## Links

Repository: <https://github.com/codex-team/hawk.python>

Report a bug: <https://github.com/codex-team/hawk.python/issues>

PyPI Package: <https://pypi.python.org/pypi/hawk-python-sdk>

CodeX Team: <https://codex.so/>
