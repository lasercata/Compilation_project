#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''File defining the user interface using argparse.'''

##-Imports
#---General
import argparse
import logging

#---Project
from src.analex import main_analex
from src.anasyn import main_anasyn, compile_src
from src.interpretor import VM


##-Init
version = '1.0.0'


##-Utils
def get_file_content(fn: str, parser=None) -> str:
    '''
    Try to read the file `fn`.
    If not found and `parser` != None, raise an error with `parser.error`. If `parser` is None, raise an `ArgumentTypeError`.
    '''

    try:
        with open(fn, 'r') as f:
            content = f.read()

    except FileNotFoundError:
        if parser != None:
            parser.error(f'The file {fn} has not been found')
        else:
            raise argparse.ArgumentTypeError(f'The file {fn} has not been found')

    return content


##-Ui parser
class ParserUi:
    '''Defines an argument parser'''

    def __init__(self):
        '''Initiate Parser'''

        #------Main parser
        #---Init
        examples = 'Examples :'
        examples += '\n\t./main.py c -h'
        examples += '\n\t./main.py c tests/nna/correct1.nno -o correct1.obj'
        examples += '\n\t./main.py r correct1.obj'
        examples += '\n\t./main.py r tests/nna/correct1.nno -c'

        self.parser = argparse.ArgumentParser(
            # prog='anasyn',
            description='Analyse, compile, and run NNP programs',
            epilog=examples,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        #---Add arguments
        self.parser.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s ' + version
        )

        #---Sub parsers
        self.subparsers = self.parser.add_subparsers(required=True, dest='subparser')

        self.create_analyse()
        self.create_compile()
        self.create_run()

    def create_analyse(self):
        '''Creates the run subparser and add its arguments.'''
    
        #---Init
        self.parser_a = self.subparsers.add_parser('analyse', aliases=['a'], help='runs the lexical analysis of the NNP program')

        #---Add arguments
        self.parser_a.add_argument(
            'inputfile',
            type=str,
            nargs=1,
            help='name of the input source file'
        )

        self.parser_a.add_argument(
            '-o', '--outputfile',
            dest='outputfile',
            action='store',
            default='',
            help='name of the output file (default: stdout)'
        )

    def create_compile(self):
        '''Creates the compile subparser and add its arguments.'''
    
        #---Init
        self.parser_c = self.subparsers.add_parser('compile', aliases=['c'], help='compile a NNP program to NNP object code')

        #---Add arguments
        self.parser_c.add_argument(
            'inputfile',
            type=str,
            nargs=1,
            help='name of the input source file'
        )

        self.parser_c.add_argument(
            '-o', '--outputfile',
            dest='outputfile',
            action='store',
            default='',
            help='name of the output file (default: stdout)'
        )
        self.parser_c.add_argument(
            '--show-ident-table',
            action='store_true',
            help='shows the final identifiers table'
        )
        self.parser_c.add_argument(
            '-d', '--debug',
            action='store_const',
            const=logging.DEBUG,
            default=logging.INFO,
            help='show debugging info on output'
        )
        # self.parser_c.add_argument(
        #     '-p', '--pseudo-code',
        #     action='store_const',
        #     const=True,
        #     default=False,
        #     help='enables output of pseudo-code instead of assembly code'
        # )
        pass

    def create_run(self):
        '''Creates the run subparser and add its arguments.'''
    
        #---Init
        self.parser_r = self.subparsers.add_parser('run', aliases=['r'], help='runs a NNP object code')

        #---Add arguments
        self.parser_r.add_argument(
            'inputfile',
            type=str,
            nargs=1,
            help='name of the input source file'
        )

        self.parser_r.add_argument(
            '-d', '--debug',
            action='store_const',
            const=logging.DEBUG,
            default=logging.INFO,
            help='show debugging info on output'
        )
        self.parser_r.add_argument(
            '-c', '--compile',
            action='store_true',
            help='compile the file before running (the file is a source code and not object code)'
        )


    def parse(self):
        '''Parse the arguments of the main parser, to redirect to the right parser.'''

        #---Get arguments
        args = self.parser.parse_args()

        #---Redirect towards the right method
        if args.subparser in ('a', 'analyse'):
            self.parse_analyse(args)
        elif args.subparser in ('c', 'compile'):
            self.parse_compile(args)
        elif args.subparser in ('r', 'run'):
            self.parse_run(args)

    def parse_analyse(self, args):
        '''Parse the arguments for the `analyse` mode'''

        file_content = get_file_content(args.inputfile[0], self.parser_a)

        main_analex(file_content, args.outputfile)

    def parse_compile(self, args):
        '''Parse the arguments for the `compile` mode'''

        src_code = get_file_content(args.inputfile[0], self.parser_c)

        main_anasyn(src_code, args.outputfile, args.show_ident_table, args.debug)

    def parse_run(self, args):
        '''Parse the arguments for the `compile` mode'''

        if args.compile:
            src_code = get_file_content(args.inputfile[0], self.parser_c)

            try:
                instructions = compile_src(src_code, args.debug)
            except SyntaxError as err:
                # self.parser_r.error('syntax error: ' + str(err))
                print('Syntax error: ' + str(err))
                return

        else:
            instructions = get_file_content(args.inputfile[0], self.parser_c)

        vm = VM(instructions, args.debug)
        vm.run()

