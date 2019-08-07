#!/usr/bin/env python3
# -*- coding: ISO-8859-1 -*-
import os
import argparse
from collections import OrderedDict
import codecs
from functools import reduce
from operator import concat
import re

from ynab import Transaction_DK

# Author: Stefan McKinnon Edwards
# Date: April 2018
# Converts a CSV file from Danske Bank for import to YNAB4.
#
# Reads a CSV file from Danske Bank and outputs
# either a QIF (or quiz? or, I forget) file
# or a CSV file for YNAB.
# Output CSV header:
# Date,Payee,Category,Memo,Outflow,Inflow
# Input CSV header:
# "Dato";"Tekst";"Beløb";"Saldo";"Status";"Afstemt"

    

def reader(line, filter=True, stats=('Udført',), cleared=('Udført',), notcleared=('Venter',), verbose=0, lineno=0):
    line = [s.strip('"') for s in line.rstrip().split(';')]
    if len(line) == 1:
        return None
    text = line[1]
    memo = ''
    if text.startswith('DK-NOTA'):
        memo = text[:13]
        text = text[13:]
    if text.startswith('MobilePay: '):
        memo = 'MobilePay'
        text = text[10:]
    startPos = text.find("))))") 
    if startPos != -1 :
        text = text[:startPos]
    t = Transaction_DK(line[0], text, amount_str=line[2], Memo=memo, Cleared=True)
    return t

    t = Transaction_DK(line[0], line[1], amount_str=line[2], Cleared=is_cleared)
    return t

'''

'''
def main(inp, outp, as_qif=False, verbose=0, qifopt=None):
       
    with codecs.open(inp,  encoding='latin1') as fin:
        l1 = fin.readline().rstrip()
        fields = [s.strip('"') for s in l1.split(';')]
        if fields != ['Dato', 'Tekst', 'Bel\xf8b', 'Saldo', 'Status', 'Afstemt']:
            print(fields)
            raise ValueError('Downloadet CSV fil har ikke den rigtige første linje')   
        with codecs.open(outp, 'w', encoding='utf-8') as fout:
            i = 0
            j = 0
            if not as_qif:
                fout.write('Date,Payee,Category,Memo,Outflow,Inflow\n')
                for line in fin:
                    j += 1
                    transaction = reader(line, verbose=verbose, lineno=j)
                    if transaction is not None:
                        print(transaction.csv(), file=fout)
                        i += 1
            else:
                if qifopt is None:
                    qifopt = {'header':'Bank'}
                    
                fout.write('!Type:{}\n'.format(qifopt['header']))
                for line in fin:
                    transaction = reader(line, filter=False, verbose=verbose, lineno=j)
                    if transaction is not None:
                        print(transaction.qif(), file=fout)
                        i += 1
                
    if verbose > 0:
        print('Converted',i,'lines.')
        print('Output written to',outp)

def make_output_name(input, qif=False, suffix='_ynab'):
    output, ext = os.path.splitext(input)
    if ext == '.csv' and qif == False or ext == '.qif' and qif == True:
        return output + suffix + ext
    ext = '.qif' if qif else '.csv'
    return output + ext
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts Danske Bank CSV files to YNAB formats.')
    parser.add_argument('input', help='Input filename, the CSV file from Danske Bank.')
    parser.add_argument('output', nargs='?', help='Output filename')
    parser.add_argument('-q','--qif', help='Output in QUICKEN format. Changes filtering', action='store_true')
    parser.add_argument('-qt', help='Modify "!Type" header in output file (Default: "Bank").', default="Bank", metavar='header type')
    parser.add_argument('--verbose', '-v', default=1, help='Verbose, adds logging output for your convenience.', action='count')
    parser.add_argument('--suffix', default='_ynab', help='Suffix to filename when input and output files are both CSV.')
    args = parser.parse_args()
    
    if args.output is None:
        args.output = make_output_name(args.input, qif=args.qif, suffix=args.suffix)
    
    if args.qif:
        qifopt = {'header':args.qt}
    else:
        qifopt = None
        
    main(args.input, args.output, as_qif=args.qif, verbose=args.verbose, qifopt=qifopt)
    


    
