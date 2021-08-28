Hawk Python Catcher
===========

Python errors Catcher module for [Hawk.so](https://hawk.so).

Usage
-----

Register an account and get a new project token.

### Install module

Install `hawkcatcher` from PyPI.

``` {.sourceCode .bash}
$ pip install hawkcatcher
```

Import Catcher module to your project.

``` {.sourceCode .python}
from hawkcatcher import Hawk
```

Then enable Hawk Catcher with your token and domain.

``` {.sourceCode .python}
hawk = Hawk({
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0SWQiOiI1ZTZmNWM3NzAzOWI0MDAwMjNmZDViODAiLCJpYXQiOjE1ODQzNTY0NzF9.t-5Gelx3MgHVBrxTsoMyPQAdQ6ufVbPsts9zZLW3gM8',
    'host': 'localhost:3000',
    'path': '/',
    'secure': False,
})
```

Now all global errors would be sent to Hawk.

### Try-except

If you want to catch errors in try-except blocks then use `hawk.catch()` in except:

``` {.sourceCode .python}
try:
    ...
except:
    hawk.catch()
```

Init params
-----------

To init Hawk Catcher just pass a project token.

``` {.sourceCode .python}
hawk = Hawk('1234567-abcd-8901-efgh-123456789012')
```

### Additional params

If you need to use custom Hawk server then pass a dictionary with params.

``` {.sourceCode .python}
hawk = Hawk({
    'token': '1234567-abcd-8901-efgh-123456789012',
    'host': 'hawk.so',
    'secure': True,
})
```

Requirements
------------

-   Python \>= 3.5
-   requests

Links
-----

Repository: <https://github.com/codex-team/hawk.python>

Report a bug: <https://github.com/codex-team/hawk.python/issues>

PyPI Package: <https://pypi.python.org/pypi/hawkcatcher>

CodeX Team: <https://ifmo.su>
