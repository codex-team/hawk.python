# FastAPI integration

This extension adds support for the [FastAPI](https://fastapi.tiangolo.com/) web framework.

## Installation

```bash
pip install hawk-python-sdk[fastapi]
```

import Catcher module to your project.

```python
from hawk_python_sdk.modules.fastapi import HawkFastapi
from hawk_python_sdk.modules.fastapi import HawkFastapi
```

```python
app = FastAPI()

hawk = HawkFastapi({
    'app_instance': app,
    'token': '1234567-abcd-8901-efgh-123456789012'
})
```

Now all global fastapi errors would be sent to Hawk.

### Try-except

If you want to catch errors in try-except blocks see [this](../README.md#try-except)

## Manual sending

You can send any error to Hawk. See [this](../README.md#manual-sending)

### Event context

See [this](../README.md#event-context)

### Affected user

See [this](../README.md#affected-user)

### Addons

When some event handled by FastAPI Catcher, it adds some addons to the event data for Hawk.

| name      | type | description     |
| --------- | ---- | --------------- |
| `url`     | str  | Request URL     |
| `method`  | str  | Request method  |
| `headers` | dict | Request headers |
| `cookies` | dict | Request cookies |
| `params`  | dict | Request params  |

## Init params

To init Hawk Catcher just pass a project token and FastAPI app instance.

```python
app = FastAPI()

hawk = HawkFastapi({
    'app_instance': app,
    'token': '1234567-abcd-8901-efgh-123456789012'
})
```

### Additional params

If you need to use custom Hawk server then pass a dictionary with params.

```python
hawk = HawkFastapi({
    'app_instance': app,
    'token': '1234567-abcd-8901-efgh-123456789012',
    'collector_endpoint': 'https://<id>.k1.hawk.so',
})
```

Parameters:

| name                 | type                      | required     | description                                                                    |
| -------------------- | ------------------------- | ------------ | ------------------------------------------------------------------------------ |
| `app_instance`       | FastAPI                   | **required** | FastAPI app instance                                                           |
| `token`              | str                       | **required** | Your project's Integration Token                                               |
| `release`            | str                       | optional     | Release name for Suspected Commits feature                                     |
| `collector_endpoint` | string                    | optional     | Collector endpoint for sending event to                                        |
| `context`            | dict                      | optional     | Additional context to be send with every event                                 |
| `before_send`        | Callable[[dict], None]    | optional     | This Method allows you to filter any data you don't want sending to Hawk       |
| `set_user`           | Callable[[Request], User] | optional     | This Method allows you to set user for every request by fastapi request object |
| `with_addons`        | bool                      | optional     | Add framework addons to event data                                             |

## Requirements

See [this](../README.md#requirements)

And for fastapi you need:

- fastapi
