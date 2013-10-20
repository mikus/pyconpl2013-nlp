# coding=utf-8
import argparse
import csv
import sys
import re
from pylev import levenshtein

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


# Wczytywanie stoplisty z pliku jako zbioru python
# np. domyślna stoplista produkuje następujący zbiór:
# set([u'fv', u'faktura'])

stoplist = set(map(lambda w: w.decode('utf-8').strip(), open('gsm.stop').read().split('\n')))


def prepare_for_levenshtein(text):
    """Ma zwrócić napis dla metryki LEVENSHTEINA"""
    r = ' '.join(sorted([item for item in tokenize_line(text) if not (item in stoplist)]))
    #print r
    return r


def prepare_for_dice(text):
    """Ma zwrócić zbiór wyrazów dla metryki DICEA"""
    s = set()
    n = 2
    t = ' '.join([item for item in tokenize_line(text) if not (item in stoplist)])
    for i in range(0, len(t)-n, n):
        s.add(t[i:i+n])
    return s


def prepare_for_lcs(text):
    """Ma zwrócić przetworzony napis dla metryki LCS"""
    return ' '.join(sorted([item for item in tokenize_line(text) if not (item in stoplist)]))


def lcs(S1, S2):
    M = [[0] * (1 + len(S2)) for i in range(1 + len(S1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(S1)):
        for y in range(1, 1 + len(S2)):
            if S1[x - 1] == S2[y - 1]:
                M[x][y] = M[x - 1][y - 1] + 1
                if M[x][y] > longest:
                    longest = M[x][y]
                    x_longest = x
            else:
                M[x][y] = 0
    return S1[x_longest - longest: x_longest]


preprare_methods = {
    'edit': prepare_for_levenshtein,
    'dice': prepare_for_dice,
    'lcs': prepare_for_lcs
}

parser = argparse.ArgumentParser(
    description='Wyszukuje podobne napisy.')

parser.add_argument('-m', '--method', required=True, choices=['edit', 'dice', 'lcs'])
parser.add_argument('-t', '--threshold', required=True, type=float)
parser.add_argument('-n', '--name', required=True)
parser.add_argument('-v', '--verbose', action='store_true', default=False)
args = parser.parse_args()

if args.method == 'dice' and (args.threshold < 0 or args.threshold > 1.0):
    parser.error(u'Próg (-t) dla metody dice\'a powinien być ustawiony pomiędzy 0.0 a 1.0.')

if args.method == 'lcs' and (args.threshold < 0 or args.threshold > 1.0):
    parser.error(u'Próg (-t) dla metody LCS powinien być ustawiony pomiędzy 0.0 a 1.0.')

name_prepared = preprare_methods[args.method](args.name.decode('utf-8'))

csvreader = csv.DictReader(sys.stdin)

count = 0
total_price = 0.0
try:

    for row in csvreader:
        row_text = row['name'].decode('utf-8')
        row_text_prepared = preprare_methods[args.method](row_text)
        match = False
        if args.method == 'edit':
            score = levenshtein(name_prepared, row_text_prepared)
            if args.verbose:
                print >> sys.stderr, row, ' levenshtein score=', score
            if score <= args.threshold:
                match = True

        elif args.method == 'dice':
            score = 1 - (
            2.0 * (len(name_prepared.intersection(row_text_prepared))) / (len(name_prepared) + len(row_text_prepared)))
            if args.verbose:
                print >> sys.stderr, row_text_prepared, ' dice score=', score
            if score <= args.threshold:
                match = True


        elif args.method == 'lcs':
            score = 1.0 * len(lcs(name_prepared, row_text_prepared)) / max(len(name_prepared), len(row_text_prepared))
            if args.verbose:
                print >> sys.stderr, row_text_prepared, ' lcs score=', score
            if score >= args.threshold:
                match = True

        if match:
            print u"[%.2f] %s" % (score, row_text)
            total_price += float(row['price'])
            count += 1
except KeyboardInterrupt:
    pass
if count:
    print u"Średnia cena: %.2f" % (total_price / count)
else:
    print u"Nie znaleziono żadnego pasującego przedmiotu."