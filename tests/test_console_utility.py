import json
import os
import random
import uuid

import pytest
from main import  save_file, get_data_schema_dict, delete_matching_jsonl_files_from_path, \
    multiprocess_save_files, print_to_console
from files_generation import generate_file_prefix


def test_save_file_from_json_file(tmp_path):
    test_schema = {'test_str': 'str:test', 'test_int': 'int:24'}
    with open(f'{tmp_path}/data_schema.json', 'w') as f:
        json.dump(test_schema, f)

    data_schema = get_data_schema_dict(f'{tmp_path}/data_schema.json')
    file_parameters = (tmp_path, data_schema, 1, 'test_data', 1, 'count', 1, 0)

    save_file(file_parameters)

    with open(f'{tmp_path}/test_data0.jsonl') as f:
        actual = json.load(f)

    expected = {'test_str': 'test', 'test_int': 24}
    assert actual == expected


def test_delete_matching_files_from_path(tmp_path):
    for i in range(3):
        with open(f'{tmp_path}/filename{i}.jsonl', 'w') as f:
            f.write('abc')

    delete_matching_jsonl_files_from_path(tmp_path, 'filename')

    actual = len(os.listdir(tmp_path))
    expected = 0
    assert actual == expected


def test_save_file_from_str_data_schema(tmp_path):
    str_schema = "{\"teststr\": \"str:test\"}"
    save_path = tmp_path
    data_schema = get_data_schema_dict(str_schema)
    data_lines = 5
    file_name = 'test_file'
    files_count = 5
    file_prefix = 'count'
    cpu_count = 1

    file_parameters = (save_path, data_schema, data_lines, file_name, files_count, file_prefix, cpu_count, 0)
    save_file(file_parameters)

    data = []
    for i in range(5):
        with open(f'{tmp_path}/test_file_{i}.jsonl', 'r') as f:
            data.append(f.readline())

    assert data == ['{"teststr": "test"}\n',
                    '{"teststr": "test"}\n',
                    '{"teststr": "test"}\n',
                    '{"teststr": "test"}\n',
                    '{"teststr": "test"}\n']


multiprocessing_parameters = [(1, 4, 1),
                              (3, 4, 3),
                              (8, 2, 8),
                              (17, 9, 17),
                              (12, 3, 12)]


@pytest.mark.parametrize('files_count, cpu_count, expected', multiprocessing_parameters)
def test_multiprocess_save_files(files_count, cpu_count, expected, tmp_path):
    str_schema = "{\"teststr\": \"str:test\"}"
    save_path = tmp_path
    data_schema = get_data_schema_dict(str_schema)
    data_lines = 5
    file_name = 'test_file'
    file_prefix = 'count'
    file_parameters = (save_path, data_schema, data_lines, file_name, files_count, file_prefix, cpu_count)
    multiprocess_save_files(file_parameters)

    assert len(os.listdir(tmp_path)) == expected


def test_print_to_console(capfd):
    data_schema = {'teststr': 'str:test'}
    data_lines = 3
    print_to_console(data_schema, data_lines)
    out, err = capfd.readouterr()
    assert out == ("{'teststr': 'test'}\n"
                   "{'teststr': 'test'}\n"
                   "{'teststr': 'test'}\n")


prefix_parameters = [(4, 'count', 1, 0, [0, 1, 2, 3]),
                     (2, 'uuid', 1, 0, ['mocked_uuid', 'mocked_uuid']),
                     (3, 'random', 1, 0, [6989721, 170610, 5010345])]


@pytest.mark.parametrize('files_count, file_prefix, cpu_count, modulo, expected', prefix_parameters)
def test_generate_file_prefix_count(files_count, file_prefix, cpu_count, modulo, expected, monkeypatch):
    def mock_uuid():
        return 'mocked_uuid'

    monkeypatch.setattr(uuid, "uuid4", mock_uuid)
    random.seed(12345)

    actual = generate_file_prefix(files_count, file_prefix, cpu_count, modulo)
    assert actual == expected
