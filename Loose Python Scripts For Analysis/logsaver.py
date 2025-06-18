from os import scandir, rename, makedirs, getcwd, system, environ
from os.path import join, isdir, isfile, dirname
from sys import argv


def copy_file(src, dst):
    open(dst, "wb").write(open(src, "rb").read())


verbose = [
    "Game Module Addr: ",
    "Game Module Size: ",
    "UGameEngine::get_tick_address",
    "Found function start ",
    "Reference point for",
    "Not ",
    "Call",
    "Found",
    "Skipping write to memory instruction at",
    "Found GEngine at",
    "Checking if ",
    "FName::get_to_string",
    "Running exhaustive_decode on ",
    "FName::get_constructor_from_candidate",
    "FUObjectArray",
    "Skipping potential",
    "max_chunks",
    "Calling FName::to_string",
    "Emulate",
    "vtable",
    "Examining",
]

targets = [
    "GUObjectArray",
    "FUObjectArray",
    "FUObjectItem",
    "GEngine",
    "GMalloc",
    "FText",
    "FName",
    "FMemory",
    "FConsole",
    "FCheat",
    "FScene",
    "EngineVersion",
    "IConsole",
    "FMalloc",
    "UObject",
    "UField",
    "UClass",
    "UStruct",
    "Realloc",
    "ProcessEvent",
    "UFunction",
    "Flags",
]


# cleanup()
verboselog = True


def haslog(prof):
    if not isdir(prof):
        return False
    if not isfile(log := join(prof, "log.txt")):
        return False
    copy_file(log, f"{log}.bak")
    return True


if len(argv) > 1:
    if argv[1].endswith(("v", "verbose")):
        verboselog = True
uevr = join(environ["APPDATA"], "UnrealVRMod")
games = [f.path for f in scandir(uevr) if haslog(f.path)]
print(games)
print("Scanning uevr directory")
for game in games:
    print(f"Scanning {game}")
    newname = ""
    with open(join(game, "log.txt"), "r+", encoding="utf-8") as logfile:
        try:
            newtext = ""
            text = logfile.read()
            for char in text:
                if ord(char) > 255:
                    print("Found non-ascii letters, substituting placeholder...")
                    char = "?"
                else:
                    newtext += char
            logfile.seek(0)
            logfile.write(newtext)
            logfile.seek(0)
        except Exception as e:
            print("Could not parse non-ascii characters")
            pass
    with open(join(uevr, game, "log.txt"), "r+", encoding="utf-8") as logfile:
        try:
            _lines = logfile.readlines()
            newname = "log_" + (_lines[0].split("]")[0])[1:].replace(" ", "_") + ".txt"
            keep = []
            lines = [li.rsplit("] ")[1] for li in _lines]
            for li in lines:
                if any([t in li for t in targets]):
                    print(li)
                    keep.append(li)
                if verboselog:
                    if any([v in li for v in verbose]):
                        keep.append(li)
            logfile.seek(0)
            if len(keep) > 0:
                with open(join(uevr, game, newname), "w", encoding="utf-8") as newfile:
                    newfile.writelines(keep)
                    newfile.seek(0)
                    newfile.close()
            logfile.close()
        except Exception as e:
            print(e)
            print(game)
