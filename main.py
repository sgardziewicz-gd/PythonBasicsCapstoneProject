import argparse
import json
import ast
import os.path
import sys
from os import path
import logging
import configparser
from multiprocessing import current_process
from data_generation import generate_data
from files_generation import multiprocess_save_files, save_file

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def exit_program(exit_info: str):
    logger.error(exit_info)
    logger.info(f'Exiting {current_process().name}')
    sys.exit(1)


def create_parser(default) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog='jsonlgenerator', description='Console utility that allows to generate test '
                                                                        'jsonl files, filled with data based on '
                                                                        'provided data schema')
    parser.add_argument("path_to_save_files", type=str,
                        help='Specifies path in which files would be generated in %(prog)s program')
    parser.add_argument("--data_lines", type=int, default=default['data_lines'],
                        help='Specifies the amount of data lines in each file in %(prog)s program. Default value is '
                             '10000')
    parser.add_argument("--data_schema", type=str, default=default['data_schema'],
                        help='Data schema specifies template on how should the result file look like in %(prog)s '
                             'program, can be provided as a path to json file or as a schema entered to command line. '
                             'Default data schema has date and name field.')
    parser.add_argument("--file_name", type=str, default=default['file_name'],
                        help='Specifies base name of generated file in %(prog)s program. Default is "default_name"')
    parser.add_argument("--files_count", type=int, default=default['files_count'],
                        help='Specifies amount of files to be generated in %(prog)s program. Default value is 5.')
    parser.add_argument("--file_prefix", type=str, default=default['file_prefix'],
                        help='Specifies what prefix to add to base name of the file in %(prog)s program, could be '
                             'count, random or uuid. Default prefix is "count"')  # 3 options
    parser.add_argument("--multiprocessing", type=int, default=default['multiprocessing'],
                        help='Specifies how many processes are going to be used in file generation in %(prog)s '
                             'program. Default value is 1')
    parser.add_argument("--clear_path", action='store_true',
                        help='clear_path flag specifies whether to clear all jsonl files from provided path before '
                             'file generation in %(prog)s program. On default it is disabled.')
    return parser


def parse_console_utility_args(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    save_path = args.path_to_save_files
    data_schema = args.data_schema
    data_lines = args.data_lines
    file_name = args.file_name
    files_count = args.files_count
    file_prefix = args.file_prefix
    clear_path = args.clear_path
    cpu_count = args.multiprocessing

    is_input_valid(save_path, cpu_count, data_lines, files_count)

    if clear_path:
        delete_matching_jsonl_files_from_path(save_path, file_name)

    data_schema = get_data_schema_dict(data_schema)
    file_parameters = (save_path, data_schema, data_lines, file_name, files_count, file_prefix, cpu_count, 0)

    if files_count == 0:
        print_to_console(data_schema, data_lines)
    else:
        if cpu_count > 1 and files_count > 1:
            multiprocess_save_files(file_parameters)
        else:
            save_file(file_parameters)


def is_input_valid(save_path, cpu_count, data_lines, files_count):
    is_path_correct(save_path)
    if cpu_count < 0:
        exit_program("Processes count cannot be less than 0")
    elif data_lines < 0:
        exit_program('Amount of data lines cannot be less than 0')
    elif files_count < 0:
        exit_program('Files count cannot be less than 0')
    else:
        return True


def is_path_correct(save_path: str) -> bool:
    if path.exists(save_path):
        if not path.isdir(save_path):
            exit_program("Provided path is not a directory")
        else:
            return True
    else:
        exit_program("Provided path does not exist")


def delete_matching_jsonl_files_from_path(save_path: str, file_name: str):
    count = 0
    for file in os.listdir(save_path):
        if file.startswith(file_name) and file.endswith('.jsonl'):
            os.remove(os.path.join(save_path, file))
            logger.info(f'Deleted {file}')
            count += 1
    logger.info(f'Deleted total {count} file/s')


def print_to_console(parsed_schema: dict, data_lines: int):
    logger.info('Started generating data for console output')
    data = generate_data(parsed_schema, data_lines)
    for line in data:
        print(line)
    logger.info('Finished generating data for console output')


def parse_str_schema(str_schema: str) -> dict:
    return ast.literal_eval(str_schema)


def get_data_schema_dict(data_schema: str) -> dict:
    try:
        if data_schema.endswith('.json'):
            with open(data_schema) as json_file:
                parsed_schema = json.load(json_file)
        else:
            parsed_schema = parse_str_schema(data_schema)
        return parsed_schema
    except json.decoder.JSONDecodeError:
        exit_program("Provided schema is not a valid JSON")


def get_default_values():
    config = configparser.ConfigParser()
    config.read('default.ini')
    return config['DEFAULT']


def main():
    default_values = get_default_values()
    parser = create_parser(default_values)
    parse_console_utility_args(parser)


if __name__ == '__main__':
    main()
