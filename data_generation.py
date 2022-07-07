import ast
import logging
import uuid
import time
import random
from logging_helper import exit_program 
logger = logging.getLogger()


def generate_data_line(data_schema: dict) -> dict:
    data_schema_keys = data_schema.keys()
    data_schema_values = data_schema.values()
    data_values = []

    # data_schema_keys: value
    # value part
    for value in data_schema_values:
        data_type = value.split(':')[0]
        data_value = value.split(':')[1:]

        # nothing after ':' in value part
        if value.startswith('timestamp'):
            data_values.append(str(time.time()))
        elif value == 'int':
            data_values.append(None)
        elif value == 'str':
            data_values.append('')
        elif data_type.startswith('['):
            values_list = ast.literal_eval(data_type)
            data_values.append(random.choices(values_list)[0])

        # data_schema_keys : data_type:data_value[0]
        if data_value:
            if data_type == 'int':
                if data_value[0].startswith('rand('):
                    try:
                        random_range = data_value[0][5:-1].split(',')
                        data_values.append(random.randint(int(random_range[0]), int(random_range[1])))
                    except ValueError:
                        exit_program('Provided range of rand() could not be converted to int')
                elif data_value[0].startswith('rand'):
                    data_values.append(random.randint(0, 10000))
                else:
                    try:
                        data_values.append(int(data_value[0]))
                    except ValueError:
                        exit_program('Value provided for int could not be converted to int')


            elif data_type == 'str':
                if data_value[0].startswith('rand('):
                    exit_program('rand() is not viable for str type')
                elif data_value[0].startswith('rand'):
                    data_values.append(str(uuid.uuid4()))
                else:
                    data_values.append(data_value[0])

            elif data_type == 'timestamp':
                if data_value[0].startswith('rand('):
                    exit_program('rand() is not viable for timestamp type')
                else:
                    logger.warning('Timestamp type does not use additional parameters - they are ignored')

            else:
                exit_program('Provided type in schema is not valid')

    data_dict = dict(zip(list(data_schema_keys), data_values))
    return data_dict


def generate_data(data_schema: dict, data_lines: int) -> list:
    total_data = []
    for _ in range(data_lines):
        total_data.append(generate_data_line(data_schema))
    return total_data
