#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Run the anasyn parser'''

##-Import
from src.parser_ui import AnasynParserUi

if __name__ == '__main__':
    app = AnasynParserUi()
    app.parse()
