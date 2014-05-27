#This file is part galatea_cms module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .cms import *

def register():
    Pool.register(
        Menu,
        Article,
        Block,
        module='galatea_cms', type_='model')
