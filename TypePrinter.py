from os import scandir, makedirs
from pathlib import Path
from os.path import *
from sys import argv
from pprint import pprint


# requires a dump with our dumper7uevr in the same folder


def ascii_letters(string):
    # these numbers simply correspond to lowercase a-z and thus we have an easy oneliner to get only letters
    return "".join(x for x in string if (97 <= ord(x) <= 122))


def is_num(str):
    for c in str:
        try:
            i = int(c)
        except Exception as e:
            return False
        return True


def is_ascii(char):
    # these numbers simply correspond to lowercase a-z and thus we have an easy oneliner to get only letters
    return 97 <= ord(char.lower()) <= 122


def is_instance(obj):
    if is_num(obj.rsplit(".")[0].rsplit("_")[1]):
        return True


dumps = sorted(
    [f.name for f in scandir(".") if f.name.startswith("object_dump")], key=getctime
)
objects = [
    f.split()[1:] for f in open(dumps[-1], "r+", encoding="utf-8").readlines()[6:]
]

typedict = {t: [] for t in set(o[0] for o in objects)}
for o in objects:
    typedict[o[0]].append(o[1] + "\n")


if not isdir("Types"):
    makedirs("Types")


# Print functions
# pprint(typedict.get("Function", []))
for t in typedict:
    with open(join("types", t), "w", encoding="utf-8") as f:
        f.write(f"Count: {len(typedict[t])}\n")
        f.writelines(typedict[t])
        f.close()
