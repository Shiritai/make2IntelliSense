# Author: Shiritai (https://github.com/Shiritai)
import json
import os
import sys

method = "COPY_GIT_IGNORE"
methods = {
    "copy": "COPY_GIT_IGNORE",
    "follow": 'USE_GIT_IGNORE'
}

if len(sys.argv) >= 4:
    if sys.argv[3] in methods:
        method = sys.argv[3]
    else:  # currently not support option
        print(f'Option: {sys.argv[3]} is currently not supported, abort')
        exit(1)

# working directory
work_dir = "./" if len(sys.argv) < 2 else sys.argv[1]
work_dir += '/' if work_dir[-1] != '/' else ''
tar_dir = f'{work_dir}.vscode'
tar_file = f'{tar_dir}/settings.json'

os.makedirs(tar_dir, exist_ok=True)

json_dict: dict = {}
if os.path.isfile(tar_file):
    with open(tar_file, 'r') as f:
        json_dict = json.load(f)

if method == methods["copy"]:
    exclude = { # these are default setting
        "**/.git", "**/.svn",
        "**/.hg", "**/CVS",
        "**/.DS_Store", "**/Thumbs.db",
    }

    # You may like to use "replace" list to replace
    #   what you don't like into other things
    # e.g. ".*" is a horrible ignorant 
    #   since it ignores too many files, you may
    #   want to use things like ".[!v]*" to make
    #   .vscode directory always visible 
    #   meanwhile ignoring other files start with
    #   a dot and non-v character
    replace = {
        ".*": ".[!v]*"
    }

    # Use a bypass list not to exclude them.
    # Notice that they still have chance disappear
    #   since you may have ".*" ignored.
    bypass = {
        '.vscode'
    }

    # fetch more files to ignore from .gitignore
    ignore_file = f"{work_dir}.gitignore"
    # add ignore files to "exclude" if .gitignore file exist
    if os.path.isfile(ignore_file):
        with open(ignore_file, "r") as ignore:
            for l in ignore.readlines():
                l = l.strip()
                # if not a comment message
                if len(l) > 0 and not l.startswith("#"):
                    # see https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options 
                    if l.startswith("/"): # directory
                        exclude.add(l)
                    elif l.startswith("!"): # don't want to ignore
                        pass
                    elif replace.get(l) is not None:
                        # in replace list
                        exclude.add(replace[l])
                    elif all(b not in l for b in bypass):
                        # file or directory
                        exclude.add("**/" + l)
                        
    json_dict.update({"files.exclude": {
        key: True for key in sorted(exclude)}})
elif method == methods["follow"]:
    json_dict.update({"explorer.excludeGitIgnore": True})
else:
    pass # currently not supported option

with open(tar_file, "w") as settings:
    settings.write(json.dumps(json_dict, indent=4))