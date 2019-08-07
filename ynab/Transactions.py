#mport os
#import argparse
#from collections import OrderedDict
#import codecs
#from functools import reduce
#from operator import concat
import re

# Author: Stefan McKinnon Edwards
# Date: April 2018
#
# Output CSV header:
# Date,Payee,Category,Memo,Outflow,Inflow

class Transaction_DK(object):
    def __init__(self, Date, Payee, Category='', Memo='', amount_str=0.0, Cleared=True):
        self.Date = Date.replace('.','/')
        self.Payee = re.sub('[ ]+[)]+','', Payee)
        self.Payee_raw = Payee
        self.Category = Category
        self.Memo = Memo
        self.Cleared = Cleared
        self.flow = float(amount_str.replace('.','', 1).replace(',','.', 1))
        if (self.flow < 0.0):
            self.Outflow = abs(self.flow)
            self.Inflow = 0.0
        else:
            self.Outflow = 0.0
            self.Inflow = self.flow

    def csv(self):
        o = '{}'.format(self.Outflow) if self.Outflow > 0.0 else ''
        i = '{}'.format(self.Inflow) if self.Inflow > 0.0 else ''
        s = '{!s},{!s},{!s},{!s},{},{}'.format(self.Date, self.Payee.replace(',',''), self.Category, self.Memo, o, i)
        return s

    def qif(self):
        c = '*' if self.Cleared else ' '
        s = 'D{}\nT{:+.2f}\nP{}\nC{}\n^\n'.format(self.Date, self.flow, self.Payee, c)
        return s


