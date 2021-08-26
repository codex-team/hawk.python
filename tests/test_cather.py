import pytest

from hawkcatcher import Hawk
from hawkcatcher.errors import InvalidHawkToken

sample_token = "eyJpbnRlZ3JhdGlvbklkIjoiZGRjZmY4OTItODMzMy00YjVlLWIyYWQtZWM1MDQ5MDVjMjFlIiwic2VjcmV0IjoiZmJjYzIwMTEtMTY5My00NDIyLThiNDItZDRlMzdlYmI4NWIwIn0="
sample_token_host = "ddcff892-8333-4b5e-b2ad-ec504905c21e.k1.hawk.so"


def test_token_parsing():
    collector_host = Hawk.get_collector_host(sample_token)
    assert collector_host == sample_token_host


def test_token_parsing_with_wrong_token_format():
    wrong_token = "eyJpbnRlZ3joiZGRjZmY4OtZWM1MDQ5MDVjMjFlIEtMTY5My00NDIyLThiNDItZDRlMzdlYmI4NWIwIn0="
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_host(wrong_token)


def test_token_parsing_with_wrong_token_data():
    wrong_token = "eyJzZWNyZXQiOiJmYmNjMjAxMS0xNjkzLTQ0MjItOGI0Mi1kNGUzN2ViYjg1YjAifQ=="
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_host(wrong_token)


def test_token_parsing_no_token():
    wrong_token = ""
    with pytest.raises(InvalidHawkToken):
        Hawk.get_collector_host(wrong_token)


def test_settings_parsing():
    settings = Hawk.get_params(sample_token)

    right_settings = {
        'token': sample_token,
        'host': sample_token_host,
        'secure': True,
    }

    assert settings == right_settings
