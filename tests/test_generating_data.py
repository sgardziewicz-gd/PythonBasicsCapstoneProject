import random
import uuid
import time
import pytest
from data_generation import generate_data_line
from main import parse_str_schema


parameters_correct = [
    ({'empty_string': 'str'}, {'empty_string': ''}),
    ({'standalone_string': 'str:example'}, {'standalone_string': 'example'}),
    ({'random_string': 'str:rand'}, {'random_string': 'mocked_uuid'}),

    ({'empty_int': 'int'}, {'empty_int': None}),
    ({'standalone_int': 'int:42'}, {'standalone_int': 42}),
    ({'random_int': 'int:rand'}, {'random_int': 6825}),
    ({'random_int_range': 'int:rand(1, 100)'}, {'random_int_range': 54}),

    ({'choose_from_list_str': '["one", "two", "three"]'}, {'choose_from_list_str': 'two'}),
    ({'choose_from_list_int': '[1, 2, 3]'}, {'choose_from_list_int': 2}),

    ({'timestamp': 'timestamp'}, {'timestamp': 'mocked_time'}),
]


@pytest.mark.parametrize('test_input, expected', parameters_correct)
def test_generate_data_line(test_input, expected, monkeypatch):
    def mock_uuid():
        return 'mocked_uuid'

    def mock_timestamp():
        return 'mocked_time'

    monkeypatch.setattr(uuid, "uuid4", mock_uuid)
    monkeypatch.setattr(time, "time", mock_timestamp)

    random.seed(12345)
    actual = generate_data_line(test_input)
    assert actual == expected


def test_parse_str_schema():
    str_schema = "{\"date\": \"timestamp\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\"," \
                 "\"age\": \"int:rand(1, 90)\"}"
    expected = {'date': 'timestamp', 'name': 'str:rand', 'type': "['client', 'partner', 'government']",
                'age': 'int:rand(1, 90)'}
    actual = parse_str_schema(str_schema)
    assert actual == expected
