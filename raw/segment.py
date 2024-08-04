from lingpy import *
import collections

dct = collections.defaultdict(int)

csv = csv2list("suansu.tsv")
for row in csv:
    for s in row[4].split():
        dct[s] += 1

with open("profile.tsv", "w") as f:
    f.write("Grapheme\tIPA\tFrequency\n")
    for k, v in sorted(dct.items(), key=lambda x: x[1]):
        f.write("{0}\t{0}\t{1}\n".format(k, v))
