#!/usr/bin/env python
# coding=utf-8

from collections import Counter
from itertools import chain, imap
import sys
import re

from pydic import PyDic


sjp = PyDic('data/sjp.pydic')


def tokenize_line(line):
    """
    Ta funkcja przyjmuje linię tekstu "Ala ma kota, a kot ma Ale!". 
    Powinna zwrócic generator, generujący kolejne wyrazy: ["Ala", "ma", "kota", "a", "kot", "ma", "Ale"
    
    Dzięki użyciu generatora, 
    """

    for word in re.findall(u'\w+', line.lower(), re.U):
        bases = [item for item in sjp.word_base(word) if item.islower()]
        if bases:
            yield min(bases, key=len)
        else:
            yield word

# Automatically load solution if available
tokenizer = tokenize_line
try:
    import z02_frequence_solution
    tokenizer = z02_frequence_solution.tokenize_line
except ImportError:
    pass


# Do frequency counting in 2 lines - batteries included :)
for word in Counter(chain.from_iterable(
        imap(lambda line: list(tokenizer(line.decode('utf-8'))), sys.stdin))).most_common():
    print word[1], word[0].encode('utf-8')
