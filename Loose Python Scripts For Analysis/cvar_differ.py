import json
from collections import defaultdict
from os import scandir, getcwd, environ
from os.path import join, isdir, dirname, basename

def isvalid(f):
    try:
        with open(f, "r", encoding="utf-8") as file:
            text = file.read()
        return len(text) > 0 and not f.endswith(("common_data.json", "unique_keys.json"))
    except Exception as e:
        with open("ErrorFiles.txt", "a", encoding="utf-8") as j:
            j.write(f + "\n")
        return False

def load_files(files):
    data_dict = {}
    for f in files:
        if isvalid(f):
            with open(f, "r", encoding="utf-8") as file:
                data_dict[f] = json.load(file)
    return data_dict

def aggregate_data(data_dict):
    aggregated_data = defaultdict(lambda: {"description": "", "value": set()})
    common_key_dict = defaultdict(list)

    for file, data in data_dict.items():
        for key, value in data.items():
            common_key_dict[key].append(file)
            aggregated_data[key]["description"] += value.get("description", "") + " "
            aggregated_data[key]["value"].add(value.get("value", None))

    common_keys = [f"{key} {len(files)}" for key, files in common_key_dict.items() if len(files) > 1]
    unique_keys = [f'"{key}": "{basename(dirname(files[0]))}"' for key, files in common_key_dict.items() if len(files) == 1]
    return unique_keys, common_keys, aggregated_data

def main(files):
    data_dict = load_files(files)

    # Get sorted keys and aggregated data
    unique_keys, common_keys, aggregated_data = aggregate_data(data_dict)

    # Write unique keys to json
    with open("unique_keys.json", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_keys))

    # All cvars with more than 1 occurrence + the number of occurrences
    with open("common_keys.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(common_keys))

    # Merged dictionary of all cvars with descriptions and a list of all unique values
    with open("aggregate_data.json", "w", encoding="utf-8") as f:
        json.dump(aggregated_data, f, indent=4, default = tuple)


    for file in files:
        if not isvalid(file):
            pass
        unique_file_keys = set()
        with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key, value in data.items():
                    if key in [f.split(" ")[0] for f in common_keys]:
                        continue
                    else:
                        unique_file_keys.add(key)
        with open(f"{file}.unique.txt", "w", encoding = "utf-8") as f:
            f.write("\n".join(sorted(list(unique_file_keys))))


# uncomment for generalized usage
# files = [f.path for f in scandir(getcwd()) if f.name.endswith(".json")]
files = []
dirs = [f.path for f in scandir(join(environ["APPDATA"],"UnrealVRMod")) if isdir(f)]
for _dir in dirs:
    files.extend([f.path for f in scandir(_dir) if f.name.endswith("cvardump.json")])

main(files)
