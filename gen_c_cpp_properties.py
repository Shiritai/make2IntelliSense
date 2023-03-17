# Author: Shiritai (https://github.com/Shiritai)
# ref: https://iotexpert.com/stupid-python-tricks-vscode-c_cpp_properties-json-for-linux-kernel-development/
# This program runs "make --dry-run" then processes the output to create a visual studio code
# c_cpp_properties.json file
import json
import os
import re
from run_cmd import cmd_stream
import sys

# list existing compiler include path, take first one
cc_include = cmd_stream("cc -xc /dev/null -E -Wp,-v 2>&1 | sed -n 's,^ ,,p'")[0]

includePath = {
    r"${workspaceFolder}/**",
    cc_include
}

defines = {
    "declare": set(),      # e.g. MODULE
    "kv_pair": {},         # e.g. A=B
    "black_kv_pair": set() # discard list
}

# gcc: FIRST_INSTANCE_PATH SECOND_INSTANCE_PATH ...
cc_path = cmd_stream("whereis gcc")[0].split()[1]

# language standard
std = {
    "c": set(),
    "c++": set()
}

# ------------------------
# compilation of regex
std_match = re.compile(r"-std=([\w|+]{1,3}\d{2})")
cc_match = re.compile(r'\s+CC\s+')
cpp_match = re.compile(r'\s+CC\s+')
# ------------------------

# figure out which version of the kernel we are using
kernel_ver = cmd_stream('uname -r')[0].strip()

# Take a line from the make output
# split the line into a list by using whitespace
# search the list for tokens of
# -I (gcc include)
# -D (gcc #define)
def process_command(line: str):
    for i in line.split():
        if len(i) <= 2:
            continue
        # the leading two character determine what the content is
        hint, content = i[:2], i[2:]
        if hint == "-I":
            p = f'/usr/src/linux-headers-{kernel_ver}/{content.replace("./", "")}'
            if os.path.exists(p):
                includePath.add(p)
        elif hint == "-D":
            if "=" in content: # has define value
                k, v = content.split("=")
                peek = defines["kv_pair"].get(k)
                if peek and peek != v:
                    # if duplicate key definition with different value exist
                    # then throw it to the discard list
                    defines["black_kv_pair"].add(k)
                defines["kv_pair"][k] = v
            else:
                defines["declare"].add(content)
        elif i.startswith("-std="):
            # found c/c++ compile standard
            lang_std, = std_match.search(i).groups()
            std["c" if "++" not in lang_std else "cpp"].add(lang_std)

# working directory
work_dir = "./" if len(sys.argv) < 2 else sys.argv[1]
work_dir += '/' if work_dir[-1] != '/' else ''
tar_dir = f'{work_dir}.vscode'
tar_file = f'{tar_dir}/c_cpp_properties.json'

os.makedirs(tar_dir, exist_ok=True)

json_dict: dict = {}
if os.path.isfile(tar_file):
    with open(tar_file, 'r') as f:
        json_dict = json.load(f)

make_arg = "" if len(sys.argv) < 3 else sys.argv[2]
# run make to find #defines and -I includes
lines = cmd_stream(f'cd {work_dir} && make {make_arg}')
for i in lines:
    # look for a line with " CC "... this is a super ghetto method
    val = cc_match.search(i)
    if val:
        process_command(i)

# -------------------
# handle exception
for k, v in std.items():
    if len(std["c"]) > 1:
        print(f"detect multiple {k} standards: {', '.join(v)}")
# -------------------

# Create the JSON
configs = {
    "name": "Linux",
    "includePath": sorted(list(includePath)),
    "defines": sorted((*defines["declare"], # key (only)
        *(f'{k}={v}' for k, v in defines["kv_pair"].items() # key=value
            if k not in defines["black_kv_pair"]))),
    "intelliSenseMode": "gcc-x64",
    "compilerPath": cc_path,
    "cStandard": (std["c"].pop() if len(std["c"]) > 0 else 'c99'),
    "cppStandard": (std["c++"].pop() if len(std["c++"]) > 0 else 'c++11'),
}

json_dict.update({
    "configurations": [configs, ],
    "version": 4
})

# Convert the Dictionary to a string of JSON
json_str = json.dumps(json_dict, indent=4)
# Save the JSON to the files
with open(tar_file, "w") as properties:
    properties.write(json_str)