#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##-Imports
#---General
from os import listdir

import pytest

#---Project
from src.anasyn import main_anasyn


##-Init
nna_path = 'nn_programs/nna/'
nnp_path = 'nn_programs/nnp/'

files_nna = sorted([f for f in listdir(nna_path) if 'correct' in f])
files_nnp = sorted([f for f in listdir(nnp_path) if 'correct' in f])

nna_tuples = [('nna', nna_path + src, nna_path + 'expected/' + src + '.expected') for src in files_nna]
nnp_tuples = [('nnp', nnp_path + src, nnp_path + 'expected/' + src + '.expected') for src in files_nnp]

error_programs = sorted([nna_path + f for f in listdir(nna_path) if 'error' in f])


##-Tests
class TestAnasyn:
    '''Tests `main_anasyn`'''

    @pytest.mark.parametrize('nn_type, src_fn, expected_compiled_fn', nna_tuples + nnp_tuples)
    def test_correct(self, nn_type: str, src_fn: str, expected_compiled_fn: str):
        '''Tests to compile the correct programs'''

        with open(src_fn) as src_file:
            with open(expected_compiled_fn) as compiled_file:
                src = src_file.read()
                compiled = compiled_file.read().strip()

                assert main_anasyn(src).strip() == compiled, f'Failed for file {nn_type}/"{src_fn}"'

    @pytest.mark.parametrize('src_fn', error_programs)
    def test_error(self, src_fn: str):
        '''Tests to compile the programs with errors'''

        with open(src_fn) as src_file:
            src = src_file.read()

            with pytest.raises(SyntaxError):
                main_anasyn(src).strip()
