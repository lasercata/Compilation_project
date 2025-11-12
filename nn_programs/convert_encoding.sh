#!/bin/bash

iconv -f iso-8859-1 -t UTF-8 "$1" > tmp
rm "$1"
mv tmp "$1"
