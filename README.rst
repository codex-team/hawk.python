hawk.python
===========

Python errors Catcher module for `Hawk.so <https://hawk.so>`__.

Usage
-----

First of all, you should register an account on
`hawk.so <https://hawk.so/join>`__.

Then `register your project <https://hawk.so/websites/create>`__.

You'll get token for the project on email or you can just copy it on
`settings page <https://hawk.so/garage/settings>`__.

Install module
~~~~~~~~~~~~~~

Install ``hawkcatcher`` from PyPI.

.. code:: bash

    $ pip3 install hawkcatcher

Import Catcher module to your project.

.. code:: python

    from hawkcatcher import Hawk

Then enable Hawk Catcher with your token.

.. code:: python

    hawk = Hawk('1234567-abcd-8901-efgh-123456789012')

Now all global errors would be sent to Hawk.

Try-except
~~~~~~~~~~

If you want to catch errors in try-except blocks then use ``hawk.catch()`` in
except:

.. code:: python

    try:
        ...
    except:
        hawk.catch()

Init params
-----------

There are two way to init Hawk module.

Token
~~~~~

Just enter a project token.

.. code:: python

    hawk = Hawk('1234567-abcd-8901-efgh-123456789012')

Params dictionary
~~~~~~~~~~~~~~~~~

If you need to use custom Hawk server.

.. code:: python

    hawk = Hawk({
        'token': '1234567-abcd-8901-efgh-123456789012',
        'domain': 'myproject.codex',
        'host': 'hawk.so',
        'path': 'catcher/python',
        'secure': True,
    })

Links
-----

Repository: https://github.com/codex-team/hawk.python

Report a bug: https://github.com/codex-team/hawk.python/issues

PyPI Package: https://pypi.python.org/pypi/hawkcatcher

CodeX Team: https://ifmo.su
