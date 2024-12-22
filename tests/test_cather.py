from unittest.mock import Mock

import pytest

from hawk_python_sdk import __version__
from hawk_python_sdk import Hawk
from hawk_python_sdk.errors import InvalidHawkToken

sample_token = "eyJpbnRlZ3JhdGlvbklkIjoiZGRjZmY4OTItODMzMy00YjVlLWIyYWQtZWM1MDQ5MDVjMjFlIiwic2VjcmV0IjoiZmJjYzIwMTEtMTY5My00NDIyLThiNDItZDRlMzdlYmI4NWIwIn0="
sample_token_collector_endpoint = "https://ddcff892-8333-4b5e-b2ad-ec504905c21e.k1.hawk.so"


def test_token_parsing():
    collector_host = Hawk.get_collector_endpoint(sample_token)
    assert collector_host == sample_token_collector_endpoint


def test_token_parsing_with_wrong_token_format():
    wrong_token = "eyJpbnRlZ3joiZGRjZmY4OtZWM1MDQ5MDVjMjFlIEtMTY5My00NDIyLThiNDItZDRlMzdlYmI4NWIwIn0="
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_endpoint(wrong_token)


def test_token_parsing_with_wrong_token_data():
    wrong_token = "eyJzZWNyZXQiOiJmYmNjMjAxMS0xNjkzLTQ0MjItOGI0Mi1kNGUzN2ViYjg1YjAifQ=="
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_endpoint(wrong_token)


def test_token_parsing_no_token():
    wrong_token = ""
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_endpoint(wrong_token)


def test_settings_parsing():
    settings = Hawk.get_params(sample_token)

    right_settings = {
        'token': sample_token,
        'collector_endpoint': sample_token_collector_endpoint,
        'release': None,
        'before_send': None,
        'context': None
    }

    assert settings == right_settings


def test_manual_sending(mocker):
    hawk = Hawk(sample_token)
    mock = Mock()

    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(ValueError("sample error title"))
    mock.assert_called()


def test_manual_sending_with_context(mocker):
    hawk = Hawk(sample_token)
    mock = Mock()
    context = {"ping": "pong"}

    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(ValueError("sample error title"), context)
    event = mock.call_args.args[0]
    assert event['payload']['context'] == context


def test_release_sending(mocker):
    hawk = Hawk({
        'token': sample_token,
        'release': "first_version"
    })
    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(ValueError("sample error title"))
    event = mock.call_args.args[0]
    assert event['payload']['release'] == "first_version"


def test_before_send_hook(mocker):
    def before_send(event: dict) -> None:
        del event['payload']['context']['very_sensitive_info']

    hawk = Hawk({
        'token': sample_token,
        'before_send': before_send
    })

    mock = Mock()
    context = {"ping": "pong", "very_sensitive_info": "123"}

    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(ValueError("sample error title"), context)
    event = mock.call_args.args[0]

    context_to_send = {"ping": "pong"}
    assert event['payload']['context'] == context_to_send


def test_catcher_version_sending(mocker):
    hawk = Hawk(sample_token)
    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(ValueError("sample error title"))
    event = mock.call_args.args[0]
    assert event['payload']['catcherVersion'] == __version__


def test_event_type_sending(mocker):
    hawk = Hawk(sample_token)
    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    hawk.send(InvalidHawkToken())
    event = mock.call_args.args[0]
    assert event['payload']['type'] == 'InvalidHawkToken'


def test_user_sending(mocker):
    hawk = Hawk(sample_token)
    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    user = {
        'id': 1,
        'name': 'Bob',
    }

    hawk.send(InvalidHawkToken(), None, user)
    event = mock.call_args.args[0]
    assert event['payload']['user'] == user


def test_catch_traceback_on_manual_sending(mocker):
    hawk = Hawk(sample_token)

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send(ValueError("val err"))

    event = mock.call_args.args[0]
    assert event['payload']['backtrace'] is not None


def test_catch_exception_if_empty_send_call(mocker):
    hawk = Hawk(sample_token)

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send()

    event = mock.call_args.args[0]
    assert event['payload']['type'] == "ZeroDivisionError"


def test_wrap_context_if_not_object(mocker):
    hawk = Hawk(sample_token)

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send(ValueError("error description"), "data", {"id": 123})

    event = mock.call_args.args[0]
    assert type(event['payload']['context']) is dict


def test_do_not_send_error_if_no_settings(mocker):
    hawk = Hawk()

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send()

    mock.assert_not_called()


def test_do_not_send_error_if_token_is_empty(mocker):
    hawk = Hawk("")

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send()

    mock.assert_not_called()


def test_do_not_send_error_if_token_in_settings_is_empty(mocker):
    hawk = Hawk({"token": ""})

    mock = Mock()
    mocker.patch.object(Hawk, 'send_to_collector', new=mock)

    try:
        val = 1 / 0
    except Exception:
        hawk.send()

    mock.assert_not_called()
