from hawkcatcher import Hawk

sample_token = "eyJpbnRlZ3JhdGlvbklkIjoiZGRjZmY4OTItODMzMy00YjVlLWIyYWQtZWM1MDQ5MDVjMjFlIiwic2VjcmV0IjoiZmJjYzIwMTEtMTY5My00NDIyLThiNDItZDRlMzdlYmI4NWIwIn0="
sample_token_host = "ddcff892-8333-4b5e-b2ad-ec504905c21e.k1.hawk.so"


def test_token_parsing():
    collector_host = Hawk.get_collector_host(sample_token)
    assert collector_host == sample_token_host


def test_settings_parsing():
    settings = Hawk.get_params(sample_token)

    right_settings = {
        'token': sample_token,
        'host': sample_token_host,
        'secure': True,
    }

    assert settings == right_settings

