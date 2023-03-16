# Author: Shiritai (https://github.com/Shiritai)
import json
import os
import sys

paths = { # these are default setting
    "**/.git", "**/.svn",
    "**/.hg", "**/CVS",
    "**/.DS_Store", "**/Thumbs.db"
}

# working directory
work_dir = "./" if len(sys.argv) < 2 else sys.argv[1]
work_dir += '/' if work_dir[-1] != '/' else ''
# fetch more files to ignore from .gitignore
ignore_file = f"{work_dir}.gitignore"
# add ignore files to "paths" if .gitignore file exist
if os.path.isfile(ignore_file):
    with open(ignore_file, "r") as ignore:
        for l in ignore.readlines():
            l = l.strip()
            # if not a comment message
            if len(l) > 0 and not l.startswith("#"):
                # see https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options 
                if l.startswith("/"): # directory
                    paths.add("**" + l)
                elif l.startswith("!"): # don't want to ignore
                    pass
                elif ".vscode" not in l: # file or directory
                    # don't ignore .vscode directory since
                    # it is totally inconvenience not to see it...
                    paths.add("**/" + l)

json_str = json.dumps({"files.exclude": {
    key: True for key in sorted(paths)}}, indent=4)
os.makedirs(f"{work_dir}.vscode", exist_ok=True)
with open(f"{work_dir}.vscode/settings.json", "w") as settings:
    settings.write(json_str)