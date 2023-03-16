# Author: Shiritai (https://github.com/Shiritai)
# ref: https://iotexpert.com/stupid-python-tricks-vscode-c_cpp_properties-json-for-linux-kernel-development/
# This program runs "make --dry-run" then processes the output to create a visual studio code
# c_cpp_properties.json file
import json
import os
import re
import sys

includePath = set()
defines = {
    "declare": set(),      # e.g. MODULE
    "kv_pair": {},         # e.g. A=B
    "black_kv_pair": set() # discard list
}

# figure out which version of the kernel we are using
stream = os.popen('uname -r')
# get rid of the \n from the uname command
kernel_ver = stream.read().strip()

# Take a line from the make output
# split the line into a list by using whitespace
# search the list for tokens of
# -I (gcc include)
# -D (gcc #define)
def process_command(line: str):
    for i in line.split():
        if i[:2] == "-I":
            p = f'/usr/src/linux-headers-{kernel_ver}/{i[2:].replace("./", "")}'
            if os.path.exists(p):
                includePath.add(p)
        elif i[:2] == "-D":
            if "=" in i[2:]: # has define value
                k, v = i[2:].split("=")
                peek = defines["kv_pair"].get(k)
                if peek and peek != v:
                    defines["black_kv_pair"].add(k)
                defines["kv_pair"][k] = v
            else:
                defines["declare"].add(i[2:])

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

# run make to find #defines and -I includes
stream = os.popen(f'cd {work_dir} && make {"" if len(sys.argv) < 3 else sys.argv[2]}')
# stream = os.popen('make --dry-run')
dry_run = stream.read()
lines = dry_run.split('\n')
for i in lines:
    # look for a line with " CC "... this is a super ghetto method
    val = re.compile(r'\s+CC\s+').search(i)
    if val:
        process_command(i)

# Create the JSON 
configs = {
    "name": "Linux",
    "includePath": sorted(list(includePath)),
    "defines": sorted((*defines["declare"], # key (only)
        *(f'{k}={v}' for k, v in defines["kv_pair"].items() # key=value
            if k not in defines["black_kv_pair"]))),
    "intelliSenseMode": "gcc-x64",
    "compilerPath": "/usr/bin/gcc",
    "cStandard": "c99",
    "cppStandard": "c++17",
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