#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''File defining the user interface using argparse.'''

##-Imports
#---General
import argparse
import logging

#---Project
try:
    from anasyn import main_anasyn

except ModuleNotFoundError:
    from src.anasyn import main_anasyn


##-Init
version = '1.0.0'

##-Ui parser
class AnasynParserUi:
    '''Defines an argument parser'''

    def __init__(self):
        '''Initiate Parser'''

        #------Main parser
        #---Init
        # examples = 'Examples :'
        # examples += '\n\t./main.py [hash]'
        # examples += '\n\t./main.py -a az09 [hash]'
        # examples += '\n\t./main.py -a 0123456789abcdef -A sha256 [hash]'
        # examples += '\n\t./main.py -t 12 [hash]'
        # examples += '\n\t./main.py -m 4 -l 6 [hash]'

        self.parser = argparse.ArgumentParser(
            # prog='anasyn',
            description='Do the syntactical analysis of a NNP program.',
            # epilog=examples,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        #---Add arguments
        self.parser.add_argument(
            'inputfile',
            type=str,
            nargs=1,
            help='name of the input source file'
        )

        self.parser.add_argument(
            '-o', '--outputfile',
            dest='outputfile',
            action='store',
            default='',
            help='name of the output file (default: stdout)'
        )
        self.parser.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s 1.0'
        )
        self.parser.add_argument(
            '-d', '--debug',
            action='store_const',
            const=logging.DEBUG,
            default=logging.INFO,
            help='show debugging info on output'
        )
        self.parser.add_argument(
            '-p', '--pseudo-code',
            action='store_const',
            const=True,
            default=False,
            help='enables output of pseudo-code instead of assembly code'
        )
        self.parser.add_argument(
            '--show-ident-table',
            action='store_true',
            help='shows the final identifiers table'
        )

    def parse(self):
        '''Parse the arguments'''

        #---Get arguments
        args = self.parser.parse_args()

        with open(args.inputfile[0], 'r') as f:
            main_anasyn(f.read(), args.outputfile, args.show_ident_table, args.debug)
