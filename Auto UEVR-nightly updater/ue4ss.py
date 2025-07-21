from os import system, chdir, environ, scandir, remove, makedirs
from os.path import *
from sys import argv
import requests
from shutil import unpack_archive
from gamelocator import get_game_paths


def safe_copy(src, dest):
    data = open(src, "r+b").read()
    with open(dest, "wb") as f:
        f.write(data)
        f.seek(0)
        f.close()


url = f"https://api.github.com/repos/UE4SS-RE/RE-UE4SS/releases"
headers = {"Accept": "application/vnd.github.inertia-preview+json"}
r = requests.get(url, headers=headers)
dl = r.json()[0]["assets"][2]["browser_download_url"]
if not isdir(ue4sscache := join(environ["appdata"], "UE4SSCache")):
    makedirs(ue4sscache)
chdir(ue4sscache)

if not isfile(installs := join(ue4sscache, "Installs.txt")):
    with open(installs, "w") as f:
        f.write("")
        f.close()
with open("ue4ss.zip", "wb") as f:
    f.write(requests.get(rf"{str(dl)}").content)
    f.close()
system("DEL /F /A / Q dwmapi.dll | DEL /F /A /Q UE4SS | md ue4ss")
unpack_archive("ue4ss.zip", ue4sscache)
chdir(join(ue4sscache, "ue4ss"))
dll = abspath("UE4SS.dll")
files = [
    join(f.path, "Plugins", "ue4ss", "UE4SS.dll")
    for f in scandir(join(environ["appdata"], "UnrealVRMod"))
    if isdir(join(f.path, "Plugins", "ue4ss"))
]
for file in files:
    if isfile(file):
        print(f"Removing {file}")
        remove(file)
    safe_copy(dll, file)

for game_path in get_game_paths():
    if isdir(game_path):
        if isfile(old_dll := join(game_path, "ue4ss", "UE4SS.dll")):
            print(old_dll)
            remove(old_dll)
            safe_copy(dll, old_dll)
