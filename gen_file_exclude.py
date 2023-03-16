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

json_str: str = ''

if method == methods["copy"]:
    exclude = { # these are default setting
        "**/.git", "**/.svn",
        "**/.hg", "**/CVS",
        "**/.DS_Store", "**/Thumbs.db"
    }

    bypass = {
        '.vscode', '.vscode/**'
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
                        exclude.add("**" + l)
                    elif l.startswith("!"): # don't want to ignore
                        pass
                    elif all(b not in l for b in bypass): # file or directory
                        # use a bypass list not to exclude them
                        # Notice that they still have chance disappear
                        # since you may have ".*" ignored
                        exclude.add("**/" + l)
    json_str = json.dumps({"files.exclude": {
        key: True for key in sorted(exclude)}}, indent=4)
elif method == methods["follow"]:
    json_str = json.dumps({"explorer.excludeGitIgnore": True}, indent=4)
else:
    pass # currently not supported option

os.makedirs(f"{work_dir}.vscode", exist_ok=True)
with open(f"{work_dir}.vscode/settings.json", "w") as settings:
    settings.write(json_str)