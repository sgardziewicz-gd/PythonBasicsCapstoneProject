import concurrent.futures
import json
import os
import random
import uuid
import logging
from data_generation import generate_data
logger = logging.getLogger()


def generate_file_prefix(files_count: int, file_prefix: str, cpu_count: int, modulo: int) -> list:
    if file_prefix == 'count':
        prefix = [x for x in range(files_count * (cpu_count - 1), (files_count * cpu_count) + modulo)]
    elif file_prefix == 'random':
        prefix = [random.randint(0, 10000000) for _ in range(files_count)]  # possible two same file names
    elif file_prefix == 'uuid':
        prefix = [uuid.uuid4() for _ in range(files_count)]
    else:
        prefix = ['' for _ in range(files_count)]
    return prefix


def save_file(file_parameters: tuple):
    save_path, data_schema, data_lines, file_name, files_count, file_prefix, cpu_count, modulo = file_parameters

    prefix = generate_file_prefix(files_count, file_prefix, cpu_count, modulo)
    spacer = '_' if files_count > 1 else ''

    for i in range(files_count + modulo):
        full_name = ''.join([file_name, spacer, str(prefix[i]), '.jsonl'])
        logger.info(f'Started generating data for {full_name}')
        data = generate_data(data_schema, data_lines)
        with open(f'{save_path}/{full_name}', 'w') as f:
            for line in data:
                json.dump(line, f)
                f.write('\n')
        logger.info(f'Finished and saved file {full_name} to {save_path}')


def multiprocess_save_files(file_parameters: tuple):
    save_path, data_schema, data_lines, file_name, files_count, file_prefix, cpu_count = file_parameters
    if cpu_count > os.cpu_count():
        cpu_count = os.cpu_count()
    modulo = files_count % cpu_count
    files_count = files_count // cpu_count
    multiprocessing_parameters = []
    # to generate proper prefix if 'count', and modulo to carry proper number, if files count not divisible by cpu count
    for i in range(cpu_count):
        multiprocessing_parameters.append((save_path, data_schema, data_lines, file_name, files_count,
                                           file_prefix, i + 1, modulo))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(save_file, multiprocessing_parameters)
