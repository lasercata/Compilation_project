#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##-Imports
#---General
from subprocess import run

import pytest

#---Project
# from src.anasyn import main_anasyn


##-Init
test_expected_values = [
    #nn_type, nb, input, expected_output
    ('nna', 1, (), '1\n2\n3\n4\n'*4),

    ('nna', 2, (), 1),

    ('nna', 3, (0,), -34),
    ('nna', 3, (2,), -34),
    ('nna', 3, (20,), 20*3),
    ('nna', 3, (18,), ''),

    ('nna', 4, (0,), 0),
    ('nna', 4, (1, 0,), 0),
    ('nna', 4, (1, 1, 1, 1, 0,), 0),
    ('nna', 4, (2, 0,), 1),
    ('nna', 4, (2, 2, 0,), 2),
    ('nna', 4, (2, 2, 2, 0,), 3),
    ('nna', 4, (1, 2, 0,), 1),
    ('nna', 4, (2, 1, 0,), 1),
    ('nna', 4, (2, 1, 8, 0,), 2),
    ('nna', 4, (2, 4, 6, 8, 10, 12, 14, 16, 0,), 8),

    ('nnp', 1, (0,), '1\n2\n3\n4\n'*4 + '>1'), # there is '>' because it is the user prompt
    ('nnp', 1, (1,), '1\n2\n3\n4\n'*4 + '>2'),
    ('nnp', 1, (-1,), '1\n2\n3\n4\n'*4 + '>0'),

    ('nnp', 2, (0,), '3\n4\n' + '>1'), # there is '>' because it is the user prompt
    ('nnp', 2, (1,), '3\n4\n' + '>2'),
    ('nnp', 2, (-1,), '3\n4\n' + '>0'),

    ('nnp', 3, (), 14),

    ('nnp', 4, (), 6),

    ('nnp', 5, (), ''),
]


##-Utils
def make_run_command(nn_type: str, nb: int) -> list[str]:
    '''
    Crafts the command to run the given compiled file.

    In:
        - nn_type: either 'nna' or 'nnp'
        - nb: the number of the program (e.g 1 for correct1)
    Out:
        the command to run the given compiled file
    '''

    return f'python main.py r nn_programs/{nn_type}/expected/correct{nb}.nno.expected'.split(' ')

def make_input_command(*inputs) -> list[str]:
    '''
    Crafts the command to send the inputs to the main program

    In:
        - *inputs: the inputs
    Out:
        The echo command to send the inputs
    '''

    inputs_str = '\n'.join(str(i) for i in inputs)

    return ['echo', '-e', f'"{inputs_str}"']


##-Tests
@pytest.mark.parametrize('nn_type, nb, inputs, expected_output', test_expected_values)
def test_run(nn_type: str, nb: int, inputs: tuple, expected_output: str | int):
    '''
    Run the test for file `nn_type`/correct`nb`.nno.expected.

    In:
        - nn_type: either 'nna' or 'nnp'
        - nb: the number of the program (e.g 1 for correct1)
        - inputs: the input tuple for this run. If no input, set it to `()`.
        - expected_output: the expected output for this run
    Out:
        None, or AssertionError
    '''

    if inputs == ():
        command = make_run_command(nn_type, nb)
    else:
        command = make_input_command(*inputs) + ['|'] + make_run_command(nn_type, nb)
        command = ['bash', '-c', ' '.join(command)]

    result = run(command, capture_output=True, text=True)
    output = result.stdout.strip().strip('>')

    assert output == str(expected_output).strip(), 'Failed for file "{nn_type}/correct{nb}.nno.expected"'
