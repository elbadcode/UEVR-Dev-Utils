import collections
from pprint import pprint
from glob import glob
from os import chdir, getcwd, scandir, rename, walk, environ
from os.path import (
    join,
    isfile,
    isdir,
    dirname,
    basename,
    splitext,
    exists,
    abspath,
    relpath,
)
from pathlib import Path
from re import findall
from collections.abc import Iterable
from pathlib import Path
from sys import argv
import typing


# unfinished and doesnt really have a clear goal yet
# so probably won't be finished but if you like python I've laid the groundwork for some stuff

if not str(getcwd()).endswith("sdkdump"):
    game = ""
    if len(argv) > 1:
        game = argv[1]
    else:
        game = input("Enter name of game (e.g. Client-Win64-Shipping)")
    game = basename(game).split(".")[0]
    chdir(join(environ["APPDATA"], "UnrealVRMod"))
    if not isdir(prof := join(getcwd(), game)):
        raise NameError("No matching profile found")
    if not isdir(sdk := join(prof, "sdkdump")):
        raise OSError("You need to dump an SDK first ")
    chdir(sdk)


filelist = [
    line.split("sdkdump")[1].split()[0]
    for line in open(".\\file_list.txt", "r").readlines()
]
sdk = getcwd()


class namespace:
    name: str
    members: list = []
    path = ""

    def __init__(name):
        path = join(sdk, name)
        members = [uobject(f.path) for f in scandir(path) if f.name.endswith(".hpp")]


class uobject:
    path: str
    uname: str = ""
    utype: str = ""
    shortname: str = ""
    imports: list = []
    functions: dict = {}
    namespaces: list
    properties: list = []

    def __init__(self, path):
        funcs = []
        if isfile(path):
            path = splitext(path)[
                0
            ]  # just store the path minus ext since we want to get to both hpp and cpp
        self.path = path
        namespaces = [namespace(dirname(path))]
        lines = open(Path(path + ".cpp"), "r").readlines()
        result_ln = lines[-3]
        if not result_ln.startswith("static auto result"):
            for line in lines:
                if line.startswith("static auto result"):
                    result_ln = line
                    break
        result = result_ln.rsplit('L"')[1]
        utype, uname = result.split()
        uname = uname.split('"')[0]
        shortname = uname.split(".")[1]
        funcstart = 0
        funcend = 0
        for line in (headlines := (open(Path(path + ".hpp"), "r").readlines())):
            if line.startswith("struct"):
                _name, par = line.split(":")
                if _name != shortname:
                    continue
                parent = par.split(" public ")[1].split(" {")[0]
                funcstart = headlines.index(line) + 1
            elif line.startswith("};") and funcstart != 0:
                funcend = headlines.index(line)
            elif line.startswith("namespace"):
                namespaces.append(
                    namespace(line.split("namespace ")[1].split(r" {")[0])
                )
        if funcstart != 0 and funcend != 0:
            funcs.extend(headlines[funcstart + 1 : funcend - 1])
        for func in funcs:
            self.functions[func.split("(")[0]] = func.split("("[1])

    def print(self, opt=["functions"]):
        if "name" in opt:
            pprint(self.uname)
            print("\n")
        if "type" in opt:
            pprint(self.utype)
            print("\n")
        if "full" in opt:
            pprint(self.path)
            print("\n")
        else:
            pprint(self.shortname)
            print("\n")
        if "imports" in opt:
            for i in self.imports:
                pprint(i)
            print("\n")
        if "functions" in opt:
            for f in self.functions:
                pprint(f)
            print("\n")
        if "namespaces" in opt:
            for n in self.namespaces:
                pprint(n)
            print("\n")
        if "properties" in opt:
            for p in self.properties:
                pprint(p)
            print("\n")

    def get_imports():
        lines = (
            open(Path(path + ".cpp"), "r")
            .readlines()
            .extend(open(Path(path + ".hpp"), "r").readlines())
        )
        _imports = []
        for line in lines:
            if line.startswith("#include"):
                imp = line.split()[1]
                if imp not in _imports:
                    _imports.append(imp)
        imports = _imports

    def lua_initializer():
        lua_text = f'local {shortname} = api:find_uobject("{utype} {uname}")'
        print(lua_text)


class ufunction:
    owner: uobject
    methods: list = []


# uclasses = [uobject()]

files = Path(getcwd()).rglob("*")
headers = [relpath(f) for f in files if relpath(f).endswith(".hpp")]
classes = [abspath(f) for f in files if f.endswith(".cpp")]
args = []
namespace_search = []
search_types = []
if len(argv) == 1:
    namespace_search = input("Enter namespaces\n").split(",")
    args = input("Enter search terms\n").split(",")
    search_types = input("Enter types\n")
else:
    args = argv[1:]

all_namespaces = [str(f.name).replace("_", "/") for f in scandir(getcwd()) if isdir(f)]
namespaces = (
    all_namespaces
    if namespace_search[0] == "*"
    else [
        n
        for n in all_namespaces
        if n in namespace_search or n.rsplit("/")[-1] in namespace_search
    ]
)
pprint(namespaces)
headers = [
    n.join("\\" + f.name)
    for n in namespaces
    for f in scandir(n.replace("/", "_"))
    if f.name.endswith(".hpp")
]

classnames = set([str(f).replace(".hpp", ".cpp") for f in headers])

for _class in classnames:
    if any(arg in _class for arg in args):
        print(_class)
        try:
            uclass = uobject(_class)
            if uclass.utype in search_types:
                uclass.print()
        except Exception as e:
            pass
