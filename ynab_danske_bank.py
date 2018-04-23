#!/usr/bin/env python3
# -*- coding: ISO-8859-1 -*-
import os
import argparse
from collections import OrderedDict
import codecs
from functools import reduce
from operator import concat

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

class Transaction_DK(object):
    def __init__(self, Date, Payee, Category='', Memo='', amount_str=0.0):
        self.Date = Date.replace('.','/')
        self.Payee = Payee
        self.Category = Category
        self.Memo = Memo
        num = float(amount_str.replace('.','', 1).replace(',','.', 1))
        if (num < 0.0):
            self.Outflow = abs(num)
            self.Inflow = 0.0
        else:
            self.Outflow = 0.0
            self.Inflow = num

    def csv(self):
        o = '{}'.format(self.Outflow) if self.Outflow > 0.0 else ''
        i = '{}'.format(self.Inflow) if self.Inflow > 0.0 else ''
        s = '{!s},{!s},{!s},{!s},{},{}'.format(self.Date, self.Payee, self.Category, self.Memo, o, i)
        return s
    

def reader(line, stats=('Udført',)):
    line = [s.strip('"') for s in line.rstrip().split(';')]
    if not line[4] in stats:
        return None
    t = Transaction_DK(line[0], line[1], amount_str=line[2])
    return t

'''

'''
def main(inp, outp, as_qif=False):
    # check output file name
    
    with codecs.open(inp,  encoding='latin1') as fin:
        l1 = fin.readline().rstrip()
        fields = [s.strip('"') for s in l1.split(';')]
        if fields != ['Dato', 'Tekst', 'Bel\xf8b', 'Saldo', 'Status', 'Afstemt']:
            print(fields)
            raise ValueError('Downloadet CSV fil har ikke den rigtige første linje')   
        with codecs.open(outp, 'w', encoding='latin1') as fout:
            if not as_qif:
                fout.write('Date,Payee,Category,Memo,Outflow,Inflow\n')
                for line in fin:
                    transaction = reader(line)
                    if transaction is not None:
                        print(transaction.csv())
                

    
main('test/danskebank/test1.csv', 'bla')

    